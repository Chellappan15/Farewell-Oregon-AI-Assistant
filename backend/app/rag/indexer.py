import logging

from rag.embeddings import embedder
from rag.retriever import get_collection

logger = logging.getLogger(__name__)

def index_documents() -> int:
    result = embedder()
    chunks = result["chunks"]
    get_collection().upsert(
        embeddings=result["embeddings"].tolist(),
        documents=chunks,
        ids=[f"chunk_{index}" for index in range(len(chunks))],
    )
    logger.info("Indexed %d document chunks", len(chunks))
    return len(chunks)


if __name__ == "__main__":
    index_documents()
