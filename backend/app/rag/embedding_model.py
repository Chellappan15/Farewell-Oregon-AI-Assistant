from functools import lru_cache

from sentence_transformers import SentenceTransformer

from core.config import settings


@lru_cache(maxsize=1)
def get_embedding_model() -> SentenceTransformer:
    """Load the embedding model once per process and share it."""
    return SentenceTransformer(settings.embedding_model)
