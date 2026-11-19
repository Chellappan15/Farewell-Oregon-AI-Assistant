import logging
import pickle
import re
from functools import lru_cache
from pathlib import Path

from rank_bm25 import BM25Okapi

from rag.embeddings import embedder
from rag.indexer import _chunk_id

logger = logging.getLogger(__name__)

INDEX_PATH = Path(__file__).resolve().parents[2] / "bm25_index.pkl"


def tokenize(text: str) -> list[str]:
    return re.findall(r"\w+", text.lower())


def build_bm25_index() -> int:
    chunks = embedder()["chunks"]

    records: dict[str, dict] = {}
    for chunk in chunks:
        chunk_id = _chunk_id(chunk.page_content, chunk.metadata)
        records.setdefault(
            chunk_id,
            {"id": chunk_id, "text": chunk.page_content, "metadata": chunk.metadata},
        )

    documents = list(records.values())
    bm25 = BM25Okapi([tokenize(doc["text"]) for doc in documents])

    with open(INDEX_PATH, "wb") as file:
        pickle.dump({"bm25": bm25, "documents": documents}, file)

    logger.info("Saved BM25 index with %d chunks to %s", len(documents), INDEX_PATH)
    return len(documents)


@lru_cache(maxsize=1)
def load_bm25_index() -> dict:
    if not INDEX_PATH.exists():
        raise RuntimeError(
            f"BM25 index not found at {INDEX_PATH}. Run: python -m hybrid_search.bm25_indexer"
        )
    with open(INDEX_PATH, "rb") as file:
        return pickle.load(file)


def search_bm25(query: str, limit: int = 5) -> list[dict]:
    """Return the top chunks for the query, best match first."""
    index = load_bm25_index()
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
    build_bm25_index()
