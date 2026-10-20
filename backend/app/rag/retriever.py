import os
from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer

_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
_model = SentenceTransformer(_MODEL_NAME)
_database_path = os.getenv(
    "CHROMA_DB_PATH",
    str(Path(__file__).resolve().parents[2] / "chroma_db"),
)
_client = chromadb.PersistentClient(path=_database_path)
_collection = _client.get_or_create_collection(name="days_gone")

def retrieve_context(query: str, limit: int = 5):
    embedded_question = _model.encode(query)
    results = _collection.query(
        query_embeddings=[embedded_question.tolist()],
        n_results=limit,
    )
    return results["documents"]

def get_collection():
    return _collection
