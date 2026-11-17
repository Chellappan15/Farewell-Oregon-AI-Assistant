from mysql.connector import pooling

from core.config import settings

connection_pool = pooling.MySQLConnectionPool(
    pool_name="llm_pool",
    pool_size=settings.db_pool_size,
    host=settings.db_host,
    port=settings.db_port,
    user=settings.db_user,
    password=settings.db_password,
    database=settings.db_name,
    ssl_disabled=settings.db_ssl_disabled,
)


def get_db_connection():
    return connection_pool.get_connection()
