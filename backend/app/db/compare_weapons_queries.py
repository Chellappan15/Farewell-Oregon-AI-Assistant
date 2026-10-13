from db.connect import get_db_connection

def get_weapon_statistics(weapon_1: str, weapon_2: str):
    conn = get_db_connection()
    cursor = None

    try:
        cursor = conn.cursor(dictionary=True)

        query = """
                SELECT *
                FROM weapon_info
                WHERE name IN (%s, %s)
                """

        cursor.execute(query, (weapon_1, weapon_2))

        result = cursor.fetchall()

        return result

    finally:
        if cursor is not None:
            cursor.close()
        conn.close()