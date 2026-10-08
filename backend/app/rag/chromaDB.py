import chromadb
from .embeddings import embedder

from sentence_transformers import SentenceTransformer

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
client = chromadb.PersistentClient(path="./chroma_db")

collection = client.get_or_create_collection(
    name="days_gone"
)

def add_to_chroma():
    result = embedder()

    embeddings = result["embeddings"]
    chunks = result["chunks"]
    collection.add(
        embeddings=embeddings.tolist(),
        documents=chunks,
        ids=[f"chunk_{i}" for i in range(len(chunks))]
    )

add_to_chroma()

def retrieve_context(query: str):
    embedded_question = model.encode(query)

    results = collection.query(
        embedded_question,
        n_results = 5
    )
    
    return results['documents']