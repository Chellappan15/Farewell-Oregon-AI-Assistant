import logging
from typing import Any, Literal

from core.config import settings
from core.games import DEFAULT_GAME
from rag.retriever import _source_label, retrieve_context
from hybrid_search.bm25_indexer import build_bm25_index, index_path, search_bm25
from hybrid_search.rrf import reciprocal_rank_function
from hybrid_search.rerank import rerank_documents

logger = logging.getLogger(__name__)

RetrievalMode = Literal["dense", "text", "hybrid"]
RETRIEVAL_MODES: tuple[str, ...] = ("dense", "text", "hybrid")


def ensure_bm25_index(game: str = DEFAULT_GAME) -> None:
    """Build a game's BM25 index if it is missing, so text/hybrid retrieval never fails on it."""
    path = index_path(game)
    if path.exists():
        return
    logger.warning("BM25 index for %s not found at %s; building it now", game, path)
    build_bm25_index(game)


def _with_source(chunks: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """BM25 and reranked chunks have no 'source' key; the prompt template needs one."""
    return [
        {**chunk, "source": chunk.get("source") or _source_label(chunk.get("metadata") or {})}
        for chunk in chunks
    ]


def build_context(
    query: str,
    mode: RetrievalMode = "hybrid",
    game: str = DEFAULT_GAME,
) -> list[dict[str, Any]]:
    """Return the chunks passed to the LLM, best first, for the chosen retrieval mode.

    dense  -> vector search (Chroma) only
    text   -> BM25 keyword search only
    hybrid -> vector + BM25 fused with RRF, then reranked by the cross-encoder
    """
    top_k = settings.retrieval_top_k

    if mode == "dense":
        chunks = retrieve_context(query=query, limit=top_k, game=game)
    elif mode == "text":
        chunks = search_bm25(query=query, limit=top_k, game=game)
    elif mode == "hybrid":
        fused = reciprocal_rank_function(query, game=game)
        chunks = rerank_documents(query=query, documents=fused, top_k=top_k)
    else:
        raise ValueError(f"Unknown retrieval mode: {mode}")

    logger.info("Retrieval game=%s mode=%s returned %d chunks", game, mode, len(chunks))
    return _with_source(chunks)
