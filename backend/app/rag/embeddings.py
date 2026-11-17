from rag.chunking import chunking_function
from rag.embedding_model import get_embedding_model


def embedder():
    chunks = chunking_function()
    embeddings = get_embedding_model().encode([chunk.page_content for chunk in chunks])
    return {
        "embeddings": embeddings,
        "chunks": chunks,
    }
