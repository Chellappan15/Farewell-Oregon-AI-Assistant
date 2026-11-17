"""Central application settings.

All configuration is read from environment variables (loaded from backend/.env
once, here). Import `settings` instead of calling os.getenv() in modules.
"""

import os
from dataclasses import dataclass, field
from pathlib import Path

from dotenv import load_dotenv

_BACKEND_DIR = Path(__file__).resolve().parents[2]
load_dotenv(_BACKEND_DIR / ".env")


def _env(name: str, default: str | None = None, *, required: bool = False) -> str | None:
    value = os.getenv(name, default)
    if required and not value:
        raise RuntimeError(f"{name} must be configured in the environment.")
    return value


def _env_bool(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _env_list(name: str, default: str) -> list[str]:
    return [item.strip() for item in os.getenv(name, default).split(",") if item.strip()]


@dataclass(frozen=True)
class Settings:
    # Database
    db_host: str = field(default_factory=lambda: _env("DB_HOST", "localhost"))
    db_port: int = field(default_factory=lambda: int(_env("DB_PORT", "3306")))
    db_user: str = field(default_factory=lambda: _env("DB_USER", required=True))
    db_password: str = field(default_factory=lambda: _env("DATABASE_PASSWORD", required=True))
    db_name: str = field(default_factory=lambda: _env("DB_NAME", "llm"))
    db_pool_size: int = field(default_factory=lambda: int(_env("DB_POOL_SIZE", "5")))
    # SSL is ON unless explicitly disabled (only do that for local development).
    db_ssl_disabled: bool = field(default_factory=lambda: _env_bool("DB_SSL_DISABLED", False))

    # LLM
    gemini_model: str = field(default_factory=lambda: _env("GEMINI_MODEL", "gemini-3.1-flash-lite"))

    # RAG
    embedding_model: str = field(
        default_factory=lambda: _env("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
    )
    chroma_db_path: str = field(
        default_factory=lambda: _env("CHROMA_DB_PATH", str(_BACKEND_DIR / "chroma_db"))
    )
    chroma_collection: str = field(default_factory=lambda: _env("CHROMA_COLLECTION", "days_gone"))
    retrieval_top_k: int = field(default_factory=lambda: int(_env("RETRIEVAL_TOP_K", "10")))
    # Chunks with a distance above this are dropped (lower = more similar).
    retrieval_max_distance: float = field(
        default_factory=lambda: float(_env("RETRIEVAL_MAX_DISTANCE", "1.2"))
    )
    knowledge_base_path: str = field(
        default_factory=lambda: _env("KNOWLEDGE_BASE_PATH", str(_BACKEND_DIR.parent / "DAYS GONE.md"))
    )

    # API
    cors_origins: list[str] = field(
        default_factory=lambda: _env_list("CORS_ORIGINS", "http://localhost:5173")
    )


settings = Settings()
