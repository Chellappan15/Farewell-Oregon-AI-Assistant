import logging
from core.config import settings
from rag.retriever import retrieve_context
from hybrid_search.bm25_indexer import search_bm25
from hybrid_search.rerank import rerank_documents

logger = logging.getLogger(__name__)

def reciprocal_rank_function(query: str, chunk_size: int = settings.retrieval_top_k):
    k = settings.rrf_k
    try:
        # Retrieve vector chunks
        vector_chunks = retrieve_context(query=query, is_hybrid=True)

        # Retrieve best matching chunks
        bm_chunks = search_bm25(query=query)

        fused = {}
        # RRF calculation
        for results in (vector_chunks, bm_chunks):
            for rank, document in enumerate(results, start=1):

                doc_id = document["id"]

                if doc_id not in fused:
                    fused[doc_id] = {
                        "id": doc_id,
                        "text": document["text"],
                        "metadata": document["metadata"],
                        "rrf_score": 0.0
                    }

                fused[doc_id]["rrf_score"] += 1 / (k + rank)

        return sorted(fused.values(),
                      key = lambda doc: doc["rrf_score"],
                      reverse=True) 
    except Exception:
        logger.exception("Error occurred during reciprocal rank fusion")
        raise

if __name__ == "__main__":
    data = reciprocal_rank_function("Who is deacon's wife?")
    print(rerank_documents(query="Who is deacon's wife?", documents=data))