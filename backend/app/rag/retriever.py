import logging
from typing import Any

import chromadb

from core.config import settings
from rag.embedding_model import get_embedding_model

logger = logging.getLogger(__name__)

_client = chromadb.PersistentClient(path=settings.chroma_db_path)
_collection = _client.get_or_create_collection(name=settings.chroma_collection)

_HEADER_KEYS = ("title", "section", "subsection", "topic")


def _source_label(metadata: dict[str, Any]) -> str:
    parts = [str(metadata[key]) for key in _HEADER_KEYS if metadata.get(key)]
    return " > ".join(parts) if parts else "Days Gone guide"


def retrieve_context(query: str, limit: int | None = None) -> list[dict[str, Any]]:
    """Return the most relevant chunks with their source and distance.

    Chunks further away than RETRIEVAL_MAX_DISTANCE are dropped, so weak
    matches are not passed to the LLM.
    """
    embedded_question = get_embedding_model().encode(query)
    results = _collection.query(
        query_embeddings=[embedded_question.tolist()],
        n_results=limit or settings.retrieval_top_k,
        include=["documents", "metadatas", "distances"],
    )

    documents = (results.get("documents") or [[]])[0]
    metadatas = (results.get("metadatas") or [[]])[0]
    distances = (results.get("distances") or [[]])[0]

    chunks = []
    for text, metadata, distance in zip(documents, metadatas, distances):
        if distance > settings.retrieval_max_distance:
            continue
        metadata = metadata or {}
        chunks.append(
            {
                "text": text,
                "source": _source_label(metadata),
                "metadata": metadata,
                "distance": round(float(distance), 4),
            }
        )

    logger.info(
        "Retrieved %d of %d chunks within distance %.2f",
        len(chunks),
        len(documents),
        settings.retrieval_max_distance,
    )
    return chunks


def get_collection():
    return _collection
