import json
import logging
import math
import subprocess
from datetime import datetime, timezone
from pathlib import Path

from langchain_core.embeddings import Embeddings
from ragas.cache import DiskCacheBackend
from ragas.metrics import (
    AnswerRelevancy,
    answer_correctness,
    faithfulness,
    context_precision,
    context_recall,
)
from eval.golden_database import create_dataset
from rag.embedding_model import get_embedding_model
from ragas import evaluate, RunConfig
from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper
from langchain_google_genai import ChatGoogleGenerativeAI
from core.config import settings

logger = logging.getLogger(__name__)

JUDGE_MODEL = "gemini-3.5-flash-lite"
RELEVANCY_STRICTNESS = 1
answer_relevancy = AnswerRelevancy(strictness=RELEVANCY_STRICTNESS)
METRICS = [
    answer_correctness,
    answer_relevancy,
    faithfulness,
    context_precision,
    context_recall,
]
METRIC_NAMES = [m.name for m in METRICS]
RESULTS_DIR = Path(__file__).resolve().parents[2] / "eval_results"

class LocalEmbeddings(Embeddings):
    """Judge embeddings on the shared local MiniLM model: no API calls."""

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return get_embedding_model().encode(texts).tolist()

    def embed_query(self, text: str) -> list[float]:
        return get_embedding_model().encode(text).tolist()


_judge_cache = (
    DiskCacheBackend(cache_dir=str(Path(settings.eval_cache_dir) / f"judge_{JUDGE_MODEL}"))
    if settings.eval_cache
    else None
)
judge_llm = LangchainLLMWrapper(
    ChatGoogleGenerativeAI(model=JUDGE_MODEL, google_api_key=settings.gemini_api_key),
    cache=_judge_cache,
)
judge_embeddings = LangchainEmbeddingsWrapper(LocalEmbeddings())


def _git_commit() -> str:
    try:
        commit = subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"], cwd=RESULTS_DIR.parent, text=True
        ).strip()
        dirty = subprocess.check_output(
            ["git", "status", "--porcelain"], cwd=RESULTS_DIR.parent, text=True
        ).strip()
        return f"{commit}-dirty" if dirty else commit
    except Exception:
        return "unknown"


def _clean(value):
    """NaN is not valid JSON; store it as null."""
    if isinstance(value, float) and math.isnan(value):
        return None
    return round(value, 4) if isinstance(value, float) else value


def evaluator():
    try:
        evaluation_dataset, meta = create_dataset()
        scores = evaluate(
            evaluation_dataset,
            metrics=METRICS,
            llm=judge_llm,
            embeddings=judge_embeddings,
            run_config=RunConfig(
                timeout=180, max_workers=settings.eval_workers, max_retries=10, max_wait=60
            ),
        )

        df = scores.to_pandas()
        df.insert(0, "id", [m["id"] for m in meta])
        df.insert(1, "evaluation_type", [m["evaluation_type"] for m in meta])

        metrics = [name for name in METRIC_NAMES if name in df.columns]
        by_type = df.groupby("evaluation_type")[metrics].mean()
        by_type.insert(0, "count", df.groupby("evaluation_type").size())

        commit = _git_commit()
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        RESULTS_DIR.mkdir(exist_ok=True)
        base = RESULTS_DIR / f"{stamp}_{settings.eval_game}_{settings.eval_mode}_{settings.eval_retrieval_mode}_{commit}"

        df.to_csv(f"{base}_rows.csv", index=False)

        summary = {
            "timestamp_utc": stamp,
            "git_commit": commit,
            "eval_mode": settings.eval_mode,
            "game": settings.eval_game,
            "retrieval_mode": settings.eval_retrieval_mode,
            "retrieval_top_k": settings.retrieval_top_k,
            "rows": len(df),
            "answer_model": settings.gemini_model,
            "judge_model": JUDGE_MODEL,
            "judge_embeddings": settings.embedding_model,
            "relevancy_strictness": RELEVANCY_STRICTNESS,
            "overall": {name: _clean(float(df[name].mean())) for name in metrics},
            "nan_counts": {name: int(df[name].isna().sum()) for name in metrics},
            "by_evaluation_type": {
                etype: {k: _clean(float(v)) if k != "count" else int(v) for k, v in row.items()}
                for etype, row in by_type.iterrows()
            },
        }
        with open(f"{base}_summary.json", "w", encoding="utf-8") as file:
            json.dump(summary, file, indent=2)

        print(scores)
        print(by_type.round(4).to_string())
        logger.info("Eval results saved to %s_*.{csv,json}", base)

        return summary
    except Exception as e:
        logger.exception("Evaluation failed: %s", e)
        raise
