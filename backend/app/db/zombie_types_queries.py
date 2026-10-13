from db.connect import get_db_connection

def get_zombie_details(zombie_name: str):
    conn = get_db_connection()
    cursor = None

    try:
        cursor = conn.cursor(dictionary=True)

        query = """
                SELECT *
                FROM zombie_details
                WHERE name = (%s)
                """

        cursor.execute(query, (zombie_name,))

        result = cursor.fetchall()

        return result

    finally:
        if cursor is not None:
            cursor.close()
        conn.close()