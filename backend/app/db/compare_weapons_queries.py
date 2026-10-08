from db.connect import conn, cursor

def get_weapon_statistics(weapon_1: str, weapon_2: str):
    query = """
            SELECT *
            FROM weapon_info
            WHERE name IN (%s, %s)
            """
    cursor.execute(
        query,
        (weapon_1, weapon_2,)
    )

    result = cursor.fetchall()

    return result