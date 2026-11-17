import logging
import threading

from mysql.connector import errors, pooling

from core.config import settings

logger = logging.getLogger(__name__)

_pool: pooling.MySQLConnectionPool | None = None
_pool_lock = threading.Lock()


class DatabaseUnavailableError(Exception):
    """Raised when MySQL cannot be reached."""


def _get_pool() -> pooling.MySQLConnectionPool:
    """Create the pool on first use, so the app can start without MySQL."""
    global _pool
    if _pool is None:
        with _pool_lock:
            if _pool is None:
                _pool = pooling.MySQLConnectionPool(
                    pool_name="llm_pool",
                    pool_size=settings.db_pool_size,
                    host=settings.db_host,
                    port=settings.db_port,
                    user=settings.db_user,
                    password=settings.db_password,
                    database=settings.db_name,
                    ssl_disabled=settings.db_ssl_disabled,
                )
    return _pool


def get_db_connection():
    try:
        return _get_pool().get_connection()
    except (errors.InterfaceError, errors.OperationalError) as exc:
        logger.error("Database connection failed: %s", exc)
        raise DatabaseUnavailableError() from exc
