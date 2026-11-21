from core.games import DEFAULT_GAME
from rag.chunking import chunking_function
from rag.embedding_model import get_embedding_model


def embedder(game: str = DEFAULT_GAME):
    chunks = chunking_function(game)
    embeddings = get_embedding_model().encode([chunk.page_content for chunk in chunks])
    return {
        "embeddings": embeddings,
        "chunks": chunks,
    }
