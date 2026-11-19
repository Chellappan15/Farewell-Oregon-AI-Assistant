from sentence_transformers import CrossEncoder

# Load once at application startup
reranker = CrossEncoder(
    "cross-encoder/ms-marco-MiniLM-L-6-v2"
)


def rerank_documents(
    query: str,
    documents: list[dict],
    top_k: int = 5
) -> list[dict]:

    if not documents:
        return []

    # Create query-document pairs
    pairs = [
        (query, doc["text"])
        for doc in documents
    ]

    # Score each pair
    scores = reranker.predict(pairs)

    # Attach scores to documents
    reranked = [
        {
            **doc,
            "rerank_score": float(score)
        }
        for doc, score in zip(documents, scores)
    ]

    # Sort by relevance
    reranked.sort(
        key=lambda doc: doc["rerank_score"],
        reverse=True
    )

    return reranked[:top_k]
