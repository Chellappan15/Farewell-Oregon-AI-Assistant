"""Retrieval-only eval: no LLM calls, runs fully local.

For each answerable golden question, a retrieved chunk counts as relevant when it
contains a line of the question's evidence quote (after normalising markdown,
punctuation and whitespace). Abstention questions have no evidence and are skipped.

Metrics per retrieval mode:
  hit_rate         - share of questions with at least one relevant chunk in the context
  mrr              - mean of 1 / rank of the first relevant chunk (0 if none)
  evidence_recall  - share of evidence lines found anywhere in the context
                     (matters for multi_field questions with several lines)
  avg_latency_ms   - retrieval time per question

Run from backend/app:
  python -m eval.retrieval_eval
  python -m eval.retrieval_eval --modes dense hybrid --limit 30
  python -m eval.retrieval_eval --golden "../Days Gone Paraphrase Eval.jsonl"
  python -m eval.retrieval_eval --game gta6
"""
import argparse
import csv
import json
import logging
import re
import subprocess
import time
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

from core.config import settings
from eval.golden_database import load_golden_data
from LLM.token_estimator import chunk_selection
from rag.context_builder import RETRIEVAL_MODES, build_context, ensure_bm25_index
from core.games import GAME_KEYS, get_game

logger = logging.getLogger(__name__)

RESULTS_DIR = Path(__file__).resolve().parents[2] / "eval_results"
METRICS = ("hit", "reciprocal_rank", "evidence_recall", "latency_ms")


def _normalise(text: str) -> str:
    text = text.lower().replace("**", "").replace("`", "")
    text = re.sub(r"^\s*[-*•]\s+", "", text, flags=re.MULTILINE)
    text = re.sub(r"[^\w\s]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def _evidence_lines(row: dict) -> list[str]:
    evidence = row.get("evidence") or {}
    lines = [_normalise(line) for line in (evidence.get("quote") or "").split("\n")]
    return [line for line in lines if line]


def score_row(question: str, evidence: list[str], mode: str, game: str) -> dict:
    """Retrieve exactly as the chat does (incl. token budget) and score the result."""
    start = time.perf_counter()
    chunks = chunk_selection(build_context(question, mode, game))
    latency_ms = (time.perf_counter() - start) * 1000

    texts = [_normalise(chunk["text"]) for chunk in chunks]
    first_rank = next(
        (rank for rank, text in enumerate(texts, start=1) if any(line in text for line in evidence)),
        None,
    )
    found = sum(1 for line in evidence if any(line in text for text in texts))

    return {
        "hit": 1.0 if first_rank else 0.0,
        "reciprocal_rank": 1.0 / first_rank if first_rank else 0.0,
        "evidence_recall": found / len(evidence),
        "latency_ms": latency_ms,
        "first_relevant_rank": first_rank or "",
        "chunks_returned": len(chunks),
    }


def _mean(values: list[float]) -> float:
    return round(sum(values) / len(values), 4) if values else 0.0


def _summarise(rows: list[dict]) -> dict:
    return {
        "questions": len(rows),
        "hit_rate": _mean([r["hit"] for r in rows]),
        "mrr": _mean([r["reciprocal_rank"] for r in rows]),
        "evidence_recall": _mean([r["evidence_recall"] for r in rows]),
        "avg_latency_ms": round(_mean([r["latency_ms"] for r in rows]), 1),
    }


def _git_commit() -> str:
    try:
        return subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            capture_output=True, text=True, check=True,
        ).stdout.strip()
    except Exception:
        return "unknown"


def _load_rows(golden_path: str | None, game: str) -> list[dict]:
    if not golden_path:
        return load_golden_data(game)
    with open(golden_path, "r", encoding="utf-8") as file:
        return [json.loads(line) for line in file if line.strip()]


def run_retrieval_eval(
    modes: list[str],
    limit: int = 0,
    golden_path: str | None = None,
    game: str | None = None,
) -> dict:
    game = get_game(game or settings.eval_game).key
    all_rows = _load_rows(golden_path, game)
    golden = [row for row in all_rows if _evidence_lines(row)]
    skipped = len(all_rows) - len(golden)
    if limit > 0:
        golden = golden[:limit]

    if any(mode in ("text", "hybrid") for mode in modes):
        ensure_bm25_index(game)

    results: list[dict] = []
    for mode in modes:
        logger.info("Evaluating %s retrieval mode=%s on %d questions", game, mode, len(golden))
        build_context(golden[0]["question"], mode, game)
        for row in golden:
            scores = score_row(row["question"], _evidence_lines(row), mode, game)
            results.append(
                {
                    "mode": mode,
                    "id": row.get("id"),
                    "evaluation_type": row.get("evaluation_type"),
                    "question": row["question"],
                    **scores,
                }
            )

    summary = {
        "timestamp_utc": datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ"),
        "git_commit": _git_commit(),
        "game": game,
        "golden_file": Path(golden_path or get_game(game).golden_data).name,
        "retrieval_top_k": settings.retrieval_top_k,
        "retrieval_max_distance": settings.retrieval_max_distance,
        "rrf_k": settings.rrf_k,
        "embedding_model": settings.embedding_model,
        "skipped_without_evidence": skipped,
        "overall": {},
        "by_evaluation_type": {},
    }
    for mode in modes:
        mode_rows = [r for r in results if r["mode"] == mode]
        summary["overall"][mode] = _summarise(mode_rows)
        by_type: dict[str, list[dict]] = defaultdict(list)
        for r in mode_rows:
            by_type[r["evaluation_type"]].append(r)
        summary["by_evaluation_type"][mode] = {
            etype: _summarise(type_rows) for etype, type_rows in sorted(by_type.items())
        }

    RESULTS_DIR.mkdir(exist_ok=True)
    tag = "paraphrase" if golden_path and "paraphrase" in Path(golden_path).name.lower() else "golden"
    base = RESULTS_DIR / f"{summary['timestamp_utc']}_retrieval_{game}_{tag}_{summary['git_commit']}"
    with open(f"{base}_rows.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=list(results[0].keys()))
        writer.writeheader()
        writer.writerows(results)
    with open(f"{base}_summary.json", "w", encoding="utf-8") as file:
        json.dump(summary, file, indent=2)

    _print_table(summary, modes)
    logger.info("Retrieval eval saved to %s_*.{csv,json}", base)
    return summary


def _print_table(summary: dict, modes: list[str]) -> None:
    header = f"{'mode':<8}{'n':>5}{'hit_rate':>10}{'mrr':>8}{'ev_recall':>11}{'ms':>8}"
    print("\n" + header + "\n" + "-" * len(header))
    for mode in modes:
        s = summary["overall"][mode]
        print(
            f"{mode:<8}{s['questions']:>5}{s['hit_rate']:>10.3f}{s['mrr']:>8.3f}"
            f"{s['evidence_recall']:>11.3f}{s['avg_latency_ms']:>8.1f}"
        )
    print()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser(description="Retrieval-only eval (no LLM calls)")
    parser.add_argument("--modes", nargs="+", choices=RETRIEVAL_MODES, default=list(RETRIEVAL_MODES))
    parser.add_argument("--limit", type=int, default=0, help="Only the first N questions (0 = all)")
    parser.add_argument("--golden", default=None, help="JSONL file to use instead of the game's golden set")
    parser.add_argument("--game", choices=GAME_KEYS, default=None, help="Game to evaluate (default: EVAL_GAME)")
    args = parser.parse_args()
    run_retrieval_eval(args.modes, args.limit, args.golden, args.game)
