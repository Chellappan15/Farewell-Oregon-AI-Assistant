from db.connect import cursor, conn

def addUser(name, email):
    query = """
        INSERT INTO users (name, email)
        VALUES (%s, %s)
    """

    cursor.execute(query, (name, email))

    conn.commit()

    return cursor.lastrowid