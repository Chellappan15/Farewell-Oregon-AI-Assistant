import os
from dataclasses import dataclass, field
from pathlib import Path

from dotenv import load_dotenv

_BACKEND_DIR = Path(__file__).resolve().parents[2]
load_dotenv(_BACKEND_DIR / ".env")


_missing_required: list[str] = []


def _env(name: str, default: str | None = None, *, required: bool = False) -> str | None:
    value = os.getenv(name, default)
    if required and not value:
        _missing_required.append(name)
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
    db_host: str = field(default_factory=lambda: _env("DB_HOST", "localhost"))
    db_port: int = field(default_factory=lambda: int(_env("DB_PORT", "3306")))
    db_user: str = field(default_factory=lambda: _env("DB_USER", required=True))
    db_password: str = field(default_factory=lambda: _env("DATABASE_PASSWORD", required=True))
    db_name: str = field(default_factory=lambda: _env("DB_NAME", "llm"))
    db_pool_size: int = field(default_factory=lambda: int(_env("DB_POOL_SIZE", "5")))
    db_ssl_disabled: bool = field(default_factory=lambda: _env_bool("DB_SSL_DISABLED", False))

    jwt_secret: str = field(default_factory=lambda: _env("JWT_SECRET", required=True))
    jwt_algorithm: str = field(default_factory=lambda: _env("JWT_ALGORITHM", "HS256"))
    jwt_expiration_hours: int = field(default_factory=lambda: int(_env("JWT_EXPIRATION_HOURS", "24")))

    gemini_api_key: str = field(default_factory=lambda: _env("GEMINI_API_KEY", required=True))
    gemini_model: str = field(default_factory=lambda: _env("GEMINI_MODEL", "gemini-3.1-flash-lite"))

    embedding_model: str = field(
        default_factory=lambda: _env("EMBEDDING_MODEL", "sentence-transformers/all-MiniLM-L6-v2")
    )
    chroma_db_path: str = field(
        default_factory=lambda: _env("CHROMA_DB_PATH", str(_BACKEND_DIR / "chroma_db"))
    )
    chroma_collection: str = field(default_factory=lambda: _env("CHROMA_COLLECTION", "days_gone"))
    retrieval_top_k: int = field(default_factory=lambda: int(_env("RETRIEVAL_TOP_K", "5")))
    retrieval_max_distance: float = field(
        default_factory=lambda: float(_env("RETRIEVAL_MAX_DISTANCE", "1.2"))
    )
    knowledge_base_path: str = field(
        default_factory=lambda: _env("KNOWLEDGE_BASE_PATH", str(_BACKEND_DIR / "Days Gone Data.md"))
    )

    golden_data: str = field(
        default_factory=lambda: _env("GOLDEN_DATA", str(_BACKEND_DIR / "Days Gone Golden Eval.jsonl"))
    )

    eval_count: int = field(
        default_factory=lambda: int(_env("EVAL_COUNT", "50"))
    )
    eval_mode: str = field(default_factory=lambda: _env("EVAL_MODE", "full").strip().lower())
    eval_quick_count: int = field(default_factory=lambda: int(_env("EVAL_QUICK_COUNT", "20")))
    eval_retrieval_mode: str = field(
        default_factory=lambda: _env("EVAL_RETRIEVAL_MODE", "hybrid").strip().lower()
    )
    eval_game: str = field(default_factory=lambda: _env("EVAL_GAME", "days_gone").strip().lower())
    eval_workers: int = field(default_factory=lambda: int(_env("EVAL_WORKERS", "1")))
    eval_sleep: float = field(default_factory=lambda: float(_env("EVAL_SLEEP", "4.5")))
    eval_cache: bool = field(default_factory=lambda: _env_bool("EVAL_CACHE", True))
    eval_cache_dir: str = field(
        default_factory=lambda: _env("EVAL_CACHE_DIR", str(_BACKEND_DIR / "eval_results" / ".cache"))
    )

    log_level: str = field(default_factory=lambda: _env("LOG_LEVEL", "INFO").strip().upper())

    cors_origins: list[str] = field(
        default_factory=lambda: _env_list("CORS_ORIGINS", "*")
    )

    tokens: int = field(
        default=3000
    )

    chat_history: int = field(
        default=3000
    )

    rrf_k: int = 60


settings = Settings()

if _missing_required:
    raise RuntimeError(
        "Missing required environment variables: "
        + ", ".join(_missing_required)
        + ". Add them to backend/.env (see backend/.env.example)."
    )
