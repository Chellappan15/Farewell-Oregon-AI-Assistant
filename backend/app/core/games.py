"""Supported games and where each game's data lives.

Every per-game piece (knowledge base, Chroma collection, BM25 index, golden set,
Gemini tools) is looked up here by the game key sent with each chat request.
"""
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from core.config import settings

_BACKEND_DIR = Path(__file__).resolve().parents[2]

GameKey = Literal["days_gone", "gta6"]
DEFAULT_GAME: GameKey = "days_gone"


@dataclass(frozen=True)
class GameConfig:
    key: str
    name: str                  # shown to the LLM and in logs
    knowledge_base_path: Path
    chroma_collection: str
    bm25_index_path: Path
    golden_data: Path


GAMES: dict[str, GameConfig] = {
    "days_gone": GameConfig(
        key="days_gone",
        name="Days Gone",
        knowledge_base_path=Path(settings.knowledge_base_path),
        chroma_collection=settings.chroma_collection,
        bm25_index_path=_BACKEND_DIR / "bm25_index.pkl",
        golden_data=Path(settings.golden_data),
    ),
    "gta6": GameConfig(
        key="gta6",
        name="GTA 6",
        knowledge_base_path=_BACKEND_DIR / "GTA 6 Data.md",
        chroma_collection="gta6",
        bm25_index_path=_BACKEND_DIR / "bm25_index_gta6.pkl",
        golden_data=_BACKEND_DIR / "GTA 6 Golden Eval.jsonl",
    ),
}
GAME_KEYS: tuple[str, ...] = tuple(GAMES)


def get_game(key: str) -> GameConfig:
    try:
        return GAMES[key]
    except KeyError:
        raise ValueError(f"Unknown game {key!r}; expected one of {GAME_KEYS}") from None
