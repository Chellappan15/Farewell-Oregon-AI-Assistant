import mysql.connector
from mysql.connector import pooling

connection_pool = pooling.MySQLConnectionPool(
    pool_name="llm_pool",
    pool_size=5,
    host="localhost",
    port=3306,
    user="root",
    password="welcome@123",
    database="llm",
    ssl_disabled=True
)


def get_db_connection():
    return connection_pool.get_connection()