import hashlib
import json
import logging

from rag.embeddings import embedder
from rag.retriever import get_collection

logger = logging.getLogger(__name__)


def _chunk_id(content: str, metadata: dict) -> str:
    """Stable ID: the same chunk always gets the same ID across re-indexes."""
    payload = json.dumps(metadata, sort_keys=True) + "\n" + content
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:32]


def index_documents() -> int:
    result = embedder()
    chunks = result["chunks"]
    embeddings = result["embeddings"].tolist()

    # Build the new index, skipping exact duplicate chunks.
    records: dict[str, tuple[str, dict, list[float]]] = {}
    for chunk, embedding in zip(chunks, embeddings):
        chunk_id = _chunk_id(chunk.page_content, chunk.metadata)
        records.setdefault(chunk_id, (chunk.page_content, chunk.metadata, embedding))

    collection = get_collection()

    # Remove chunks that no longer exist in the source document.
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
    logger.info("Indexed %d chunks, removed %d stale chunks", len(ids), len(stale_ids))

    # Keep the BM25 index in sync with Chroma (imported here to avoid a circular import).
    from hybrid_search.bm25_indexer import build_bm25_index
    build_bm25_index()

    return len(ids)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    index_documents()
