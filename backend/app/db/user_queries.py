from db.connect import get_db_connection

def get_user_by_email(email: str):
    """Retrieves a user record by email address (includes password hash for auth verification)."""

    conn = get_db_connection()
    cursor = None

    try:
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT id, name, email, password
            FROM users
            WHERE email = %s
        """

        cursor.execute(query, (email,))

        return cursor.fetchone()

    finally:
        if cursor is not None:
            cursor.close()
        conn.close()

def get_user_by_id(user_id: int):
    """Retrieves safe user public profile by ID (excludes password hash)."""

    conn = get_db_connection()
    cursor = None

    try:
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT id, name, email
            FROM users
            WHERE id = %s
        """

        cursor.execute(query, (user_id,))

        return cursor.fetchone()

    finally:
        if cursor is not None:
            cursor.close()
        conn.close()

def create_user(email: str, password_hash: str, name: str = None):
    """Inserts a new user record with securely hashed password."""

    conn = get_db_connection()
    cursor = None

    try:
        cursor = conn.cursor(dictionary=True)

        query = """
            INSERT INTO users (name, email, password)
            VALUES (%s, %s, %s)
        """

        user_name = name.strip() if name and name.strip() else email.split("@")[0]

        cursor.execute(
            query,
            (user_name, email.strip().lower(), password_hash)
        )

        conn.commit()

        return cursor.lastrowid

    finally:
        if cursor is not None:
            cursor.close()
        conn.close()