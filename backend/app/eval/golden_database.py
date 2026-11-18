import json
import logging
import random
import time

from datasets import Dataset
from core.config import settings
from eval.llm_answers import generate_answer
from LLM.token_estimator import chunk_selection
from rag.retriever import retrieve_context

logger = logging.getLogger(__name__)

_SAMPLE_SEED = 42

def load_golden_data() -> list[dict]:
    """Read the golden JSONL file into a list of rows."""
    try:
        data = []
        with open(settings.golden_data, "r", encoding="utf-8") as file:
            for line_number, line in enumerate(file, start=1):
                if not line.strip():
                    continue
                try:
                    data.append(json.loads(line))
                except json.JSONDecodeError as exc:
                    raise ValueError(
                        f"Invalid JSON on line {line_number} of {settings.golden_data}: {exc.msg}"
                    ) from exc
        return data

    except FileNotFoundError as exc:
        logger.error("Golden dataset not found: %s", settings.golden_data)
        raise RuntimeError(f"Golden dataset not found: {settings.golden_data}") from exc
    except ValueError:
        logger.exception("Golden dataset contains invalid JSON")
        raise


def select_rows(rows: list[dict], count: int) -> list[dict]:
    """Pick a fixed, reproducible sample. count <= 0 means use every row."""
    if count <= 0 or count >= len(rows):
        return rows
    return random.Random(_SAMPLE_SEED).sample(rows, count)


def create_dataset() -> Dataset:
    """Run retrieval + generation for each golden question.

    Returns a Dataset in the RAGAS format:
    user_input, retrieved_contexts, response, reference.
    """
    try:
        golden_rows = select_rows(load_golden_data(), int(settings.eval_count))
        rows = []
        failed = 0

        for item in golden_rows:
            try:
                chunks = chunk_selection(retrieve_context(item["question"]))
                contexts = [chunk["text"] for chunk in chunks]
                answer = generate_answer(item["question"], contexts)
                time.sleep(4.5)
            except Exception:
                # One bad question should not stop the whole eval run
                failed += 1
                logger.exception("Eval failed for %s", item.get("id"))
                continue

            rows.append(
                {
                    "user_input": item["question"],
                    "retrieved_contexts": contexts,
                    "response": answer,
                    "reference": item["gold_answer"],
                }
            )

        logger.info(
            "Created eval dataset: %d rows, %d failed, %d selected",
            len(rows), failed, len(golden_rows),
        )
        if not rows:
            raise RuntimeError("No eval rows were created; check the logs above.")

        return Dataset.from_list(rows)

    except Exception:
        logger.exception("Failed to create the evaluation dataset")
        raise