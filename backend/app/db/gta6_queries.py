from db.connect import get_db_connection

_TABLES = {"gta6_characters", "gta6_regions", "gta6_editions"}


def _fetch(query: str, params: tuple = ()) -> list[dict]:
    conn = get_db_connection()
    cursor = None
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, params)
        return cursor.fetchall()
    finally:
        if cursor is not None:
            cursor.close()
        conn.close()


def get_all_rows(table: str) -> list[dict]:
    """All rows of a small lookup table (names are matched in Python)."""
    if table not in _TABLES:
        raise ValueError(f"Unsupported table: {table}")
    return _fetch(f"SELECT * FROM {table} ORDER BY id")


def get_facts(topic: str) -> list[dict]:
    return _fetch(
        "SELECT fact_key, fact_value FROM gta6_facts WHERE topic = %s ORDER BY id",
        (topic,),
    )
