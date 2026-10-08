from sentence_transformers import SentenceTransformer
from .chunking import chunking_function

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def embedder():
    result = chunking_function()
    embeddings = model.encode(result)
    print("Shape", embeddings.shape)

    return {
        "embeddings": embeddings,
        "chunks": result
    }