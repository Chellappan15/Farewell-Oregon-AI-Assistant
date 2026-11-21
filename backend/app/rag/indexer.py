import argparse
import hashlib
import json
import logging

from core.games import DEFAULT_GAME, GAME_KEYS

from rag.embeddings import embedder
from rag.retriever import get_collection

logger = logging.getLogger(__name__)


def _chunk_id(content: str, metadata: dict) -> str:
    """Stable ID: the same chunk always gets the same ID across re-indexes."""
    payload = json.dumps(metadata, sort_keys=True) + "\n" + content
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:32]


def index_documents(game: str = DEFAULT_GAME) -> int:
    result = embedder(game)
    chunks = result["chunks"]
    embeddings = result["embeddings"].tolist()

    records: dict[str, tuple[str, dict, list[float]]] = {}
    for chunk, embedding in zip(chunks, embeddings):
        chunk_id = _chunk_id(chunk.page_content, chunk.metadata)
        records.setdefault(chunk_id, (chunk.page_content, chunk.metadata, embedding))

    collection = get_collection(game)

    existing_ids = set(collection.get(include=[])["ids"])
    stale_ids = list(existing_ids - records.keys())
    if stale_ids:
        collection.delete(ids=stale_ids)

    ids = list(records.keys())
    collection.upsert(
        ids=ids,
        documents=[records[i][0] for i in ids],
        metadatas=[records[i][1] for i in ids],
        embeddings=[records[i][2] for i in ids],
    )
    logger.info("Indexed %d %s chunks, removed %d stale chunks", len(ids), game, len(stale_ids))

    from hybrid_search.bm25_indexer import build_bm25_index
    build_bm25_index(game)

    return len(ids)


def ensure_vector_index(game: str = DEFAULT_GAME) -> None:
    """Index a game's knowledge base if its Chroma collection is empty (e.g. a fresh container)."""
    if get_collection(game).count() > 0:
        return
    logger.warning("Chroma collection for %s is empty; indexing the knowledge base now", game)
    index_documents(game)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser(description="Index a game's knowledge base (Chroma + BM25)")
    parser.add_argument("--game", choices=GAME_KEYS, help="Game to index (default: all games)")
    args = parser.parse_args()
    for key in [args.game] if args.game else GAME_KEYS:
        index_documents(key)
