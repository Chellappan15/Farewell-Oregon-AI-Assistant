import logging
from typing import Any

import chromadb

from core.config import settings
from core.games import DEFAULT_GAME, get_game
from rag.embedding_model import get_embedding_model

logger = logging.getLogger(__name__)

_client = chromadb.PersistentClient(path=settings.chroma_db_path)
_collections: dict[str, Any] = {}

_HEADER_KEYS = ("title", "section", "subsection", "topic")


def _source_label(metadata: dict[str, Any]) -> str:
    parts = [str(metadata[key]) for key in _HEADER_KEYS if metadata.get(key)]
    return " > ".join(parts) if parts else "Game guide"


def retrieve_context(
    query: str,
    limit: int | None = None,
    is_hybrid: bool = False,
    game: str = DEFAULT_GAME,
) -> list[dict[str, Any]]:
    """Return the most relevant chunks with their source and distance.

    Chunks further away than RETRIEVAL_MAX_DISTANCE are dropped, so weak
    matches are not passed to the LLM.
    """
    embedded_question = get_embedding_model().encode(query)
    results = get_collection(game).query(
        query_embeddings=[embedded_question.tolist()],
        n_results=limit or settings.retrieval_top_k,
        include=["documents", "metadatas", "distances"],
    )

    if is_hybrid:
        ids = (results.get("ids") or [[]])[0]
    documents = (results.get("documents") or [[]])[0]
    metadatas = (results.get("metadatas") or [[]])[0]
    distances = (results.get("distances") or [[]])[0]

    chunks = []
    if is_hybrid:
        for text, metadata, distance, id in zip(documents, metadatas, distances, ids):
            if distance > settings.retrieval_max_distance:
                continue
            metadata = metadata or {}
            chunks.append(
                {
                    "text": text,
                    "id": id,
                    "source": _source_label(metadata),
                    "metadata": metadata,
                    "distance": round(float(distance), 4),
                }
            )
    else:
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
        "Retrieved %d of %d %s chunks within distance %.2f",
        len(chunks),
        len(documents),
        game,
        settings.retrieval_max_distance,
    )
    return chunks


def get_collection(game: str = DEFAULT_GAME):
    name = get_game(game).chroma_collection
    if name not in _collections:
        _collections[name] = _client.get_or_create_collection(name=name)
    return _collections[name]
