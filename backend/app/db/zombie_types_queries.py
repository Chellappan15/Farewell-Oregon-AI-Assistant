from db.connect import cursor

def get_zombie_details(zombie_name: str):
    query = """
            SELECT *
            FROM zombie_details
            WHERE name = (%s)
            """

    cursor.execute(
        query,
        (zombie_name, )
    )

    result = cursor.fetchall()

    return result