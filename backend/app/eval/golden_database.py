import hashlib
import json
import logging
import random
import time
from collections import defaultdict
from pathlib import Path

from datasets import Dataset
from diskcache import Cache
from core.config import settings
from eval.llm_answers import generate_answer
from LLM.token_estimator import chunk_selection
from rag.context_builder import RETRIEVAL_MODES, build_context, ensure_bm25_index
from core.games import DEFAULT_GAME, get_game

logger = logging.getLogger(__name__)

_SAMPLE_SEED = 42
_MIN_PER_TYPE = 3
_ANSWER_PROMPT_VERSION = "v3"

def load_golden_data(game: str = DEFAULT_GAME) -> list[dict]:
    """Read a game's golden JSONL file into a list of rows."""
    golden_path = get_game(game).golden_data
    try:
        data = []
        with open(golden_path, "r", encoding="utf-8") as file:
            for line_number, line in enumerate(file, start=1):
                if not line.strip():
                    continue
                try:
                    data.append(json.loads(line))
                except json.JSONDecodeError as exc:
                    raise ValueError(
                        f"Invalid JSON on line {line_number} of {golden_path}: {exc.msg}"
                    ) from exc
        return data

    except FileNotFoundError as exc:
        logger.error("Golden dataset not found: %s", golden_path)
        raise RuntimeError(f"Golden dataset not found: {golden_path}") from exc
    except ValueError:
        logger.exception("Golden dataset contains invalid JSON")
        raise


def eval_size() -> int:
    """Number of questions for the current EVAL_MODE."""
    return settings.eval_quick_count if settings.eval_mode == "quick" else settings.eval_count


def select_rows(rows: list[dict], count: int) -> list[dict]:
    """Pick a fixed, reproducible sample, stratified by evaluation_type.

    Each type gets a share proportional to its size, with at least
    _MIN_PER_TYPE rows, so small types (abstention, multi_field) are always
    represented. count <= 0 means use every row.
    """
    if count <= 0 or count >= len(rows):
        return rows

    groups: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        groups[row.get("evaluation_type", "unknown")].append(row)

    alloc = {
        etype: min(len(group), max(_MIN_PER_TYPE, round(count * len(group) / len(rows))))
        for etype, group in groups.items()
    }
    largest = max(groups, key=lambda etype: len(groups[etype]))
    alloc[largest] = max(0, min(len(groups[largest]), alloc[largest] + count - sum(alloc.values())))

    rng = random.Random(_SAMPLE_SEED)
    selected = []
    for etype in sorted(groups):
        selected.extend(rng.sample(groups[etype], alloc[etype]))
    return selected


def _answer_cache() -> Cache | None:
    if not settings.eval_cache:
        return None
    return Cache(str(Path(settings.eval_cache_dir) / "answers"))


def _answer_key(question: str, contexts: list[str], game: str) -> str:
    payload = json.dumps(
        [settings.gemini_model, _ANSWER_PROMPT_VERSION, game, question, contexts], ensure_ascii=False
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def create_dataset() -> tuple[Dataset, list[dict]]:
    """Run retrieval + generation for each golden question.

    Returns a Dataset in the RAGAS format
    (user_input, retrieved_contexts, response, reference) and a parallel
    list of per-row metadata (id, evaluation_type) in the same order.
    """
    mode = settings.eval_retrieval_mode
    game = get_game(settings.eval_game).key
    if mode not in RETRIEVAL_MODES:
        raise ValueError(f"EVAL_RETRIEVAL_MODE must be one of {RETRIEVAL_MODES}, got {mode!r}")
    if mode in ("text", "hybrid"):
        ensure_bm25_index(game)

    try:
        golden_rows = select_rows(load_golden_data(game), eval_size())
        cache = _answer_cache()
        rows = []
        meta = []
        failed = 0
        cache_hits = 0

        for item in golden_rows:
            try:
                chunks = chunk_selection(build_context(item["question"], mode, game))
                contexts = [chunk["text"] for chunk in chunks]
                key = _answer_key(item["question"], contexts, game)
                answer = cache.get(key) if cache is not None else None
                if answer is None:
                    answer = generate_answer(item["question"], chunks, get_game(game).name)
                    if cache is not None and answer:
                        cache.set(key, answer)
                    if settings.eval_sleep > 0:
                        time.sleep(settings.eval_sleep)
                else:
                    cache_hits += 1
            except Exception:
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
            meta.append(
                {
                    "id": item.get("id"),
                    "evaluation_type": item.get("evaluation_type"),
                }
            )

        if cache is not None:
            cache.close()
        logger.info(
            "Created eval dataset (game=%s, retrieval=%s): %d rows, %d failed, %d selected, %d answers from cache",
            game, mode, len(rows), failed, len(golden_rows), cache_hits,
        )
        if not rows:
            raise RuntimeError("No eval rows were created; check the logs above.")

        return Dataset.from_list(rows), meta

    except Exception:
        logger.exception("Failed to create the evaluation dataset")
        raise