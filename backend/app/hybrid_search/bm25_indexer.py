import argparse
import logging
import pickle
import re
from functools import lru_cache
from pathlib import Path

from rank_bm25 import BM25Okapi

from core.games import DEFAULT_GAME, GAME_KEYS, get_game
from rag.embeddings import embedder
from rag.indexer import _chunk_id

logger = logging.getLogger(__name__)

def index_path(game: str = DEFAULT_GAME) -> Path:
    """Each game has its own index file (Days Gone keeps bm25_index.pkl)."""
    return get_game(game).bm25_index_path


def tokenize(text: str) -> list[str]:
    return re.findall(r"\w+", text.lower())


def build_bm25_index(game: str = DEFAULT_GAME) -> int:
    chunks = embedder(game)["chunks"]

    records: dict[str, dict] = {}
    for chunk in chunks:
        chunk_id = _chunk_id(chunk.page_content, chunk.metadata)
        records.setdefault(
            chunk_id,
            {"id": chunk_id, "text": chunk.page_content, "metadata": chunk.metadata},
        )

    documents = list(records.values())
    bm25 = BM25Okapi([tokenize(doc["text"]) for doc in documents])

    path = index_path(game)
    with open(path, "wb") as file:
        pickle.dump({"bm25": bm25, "documents": documents}, file)

    # A rebuilt file must replace any copy already loaded in this process
    load_bm25_index.cache_clear()
    logger.info("Saved %s BM25 index with %d chunks to %s", game, len(documents), path)
    return len(documents)


@lru_cache(maxsize=None)
def load_bm25_index(game: str = DEFAULT_GAME) -> dict:
    path = index_path(game)
    if not path.exists():
        raise RuntimeError(
            f"BM25 index not found at {path}. Run: python -m hybrid_search.bm25_indexer --game {game}"
        )
    with open(path, "rb") as file:
        return pickle.load(file)


def search_bm25(query: str, limit: int = 5, game: str = DEFAULT_GAME) -> list[dict]:
    """Return the top chunks for the query, best match first."""
    index = load_bm25_index(game)
    scores = index["bm25"].get_scores(tokenize(query))

    ranked = sorted(zip(index["documents"], scores), key=lambda pair: pair[1], reverse=True)

    results = []
    for doc, score in ranked[:limit]:
        if score <= 0:  
            break
        results.append({**doc, "score": float(score)})
    return results


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser(description="Build a game's BM25 index")
    parser.add_argument("--game", choices=GAME_KEYS, help="Game to build (default: all games)")
    args = parser.parse_args()
    for key in [args.game] if args.game else GAME_KEYS:
        build_bm25_index(key)
