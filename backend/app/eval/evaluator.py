import logging
from ragas.metrics import (
    answer_correctness,
    answer_relevancy,
    faithfulness,
    context_precision,
    context_recall,
)
from eval.golden_database import create_dataset
from ragas import evaluate, RunConfig
from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from core.config import settings

judge_llm = LangchainLLMWrapper(
    ChatGoogleGenerativeAI(model="gemini-3.5-flash-lite", google_api_key=settings.gemini_api_key)
)
judge_embeddings = LangchainEmbeddingsWrapper(
    GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001", google_api_key=settings.gemini_api_key)
)

def evaluator():
    try:
        evaluation_dataset = create_dataset()
        scores = evaluate(
            evaluation_dataset,
            metrics=[
                answer_correctness,
                answer_relevancy,
                faithfulness,
                context_precision,
                context_recall,
            ],
            llm=judge_llm,
            embeddings=judge_embeddings,
            run_config=RunConfig(max_workers=1, max_retries=10, max_wait=60)
        )

        print("Dataset: ", evaluation_dataset)
        print(scores)

        return scores
    except Exception as e: 
        logging.exception("Evaluation failed: %s", e)