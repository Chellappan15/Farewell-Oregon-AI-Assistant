import json
from db.connect import get_db_connection

def get_chat_history(chat_id: int):
    conn = get_db_connection()
    cursor = None

    try:
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT chat_history
            FROM chat
            WHERE chat_id = %s
        """

        cursor.execute(query, (chat_id,))
        history = cursor.fetchone()

        print("Requested chat_id:", chat_id)
        print("Database result:", history)

        if not history:
            return []

        print("Chat history value:", history.get("chat_history"))
        return json.loads(history.get("chat_history"))

    finally:
        if cursor is not None:
            cursor.close()
        conn.close()

def chatProgress(id: int, chat_id: int, chat_title: str, data):
    conn = get_db_connection()
    cursor = None

    try:
        cursor = conn.cursor(dictionary=True)
        json_data = json.dumps(data)

        query = """
            INSERT INTO chat (id, chat_id, chat_title, chat_history)
            VALUES (
                %s,
                %s,
                %s,
                JSON_ARRAY(JSON_EXTRACT(%s, '$'))
            )
            ON DUPLICATE KEY UPDATE
            chat_title = CASE
                WHEN chat_title = 'New chat' THEN %s
                ELSE chat_title
            END,
            chat_history = JSON_ARRAY_APPEND(
                COALESCE(chat_history, JSON_ARRAY()),
                '$',
                JSON_EXTRACT(%s, '$')
            )
        """

        cursor.execute(
            query,
            (id, chat_id, chat_title, json_data, chat_title, json_data)
        )

        conn.commit()

    finally:
        if cursor is not None:
            cursor.close()
        conn.close()

# Front-end requests
def get_chats_query(user_id: int):
    conn = get_db_connection()
    cursor = None

    try:
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT chat_title, id, chat_id
            FROM chat
            WHERE id = (%s)
        """

        cursor.execute(query, (user_id,))
        return cursor.fetchall()

    finally:
        if cursor is not None:
            cursor.close()
        conn.close()

def newChat(id):
    conn = get_db_connection()
    cursor = None

    try:
        cursor = conn.cursor(dictionary=True)

        query = """
            INSERT INTO chat(id, chat_title)
            VALUES (%s, %s)
        """

        cursor.execute(query, (id, "New Chat"))
        conn.commit()

        return cursor.lastrowid

    finally:
        if cursor is not None:
            cursor.close()
        conn.close()

def delete_chat_query(user_id: int, chat_id: int):
    conn = get_db_connection()
    cursor = None

    try:
        cursor = conn.cursor(dictionary=True)

        query = """
            DELETE
            FROM chat
            WHERE chat_id = (%s) AND id = (%s)
        """

        cursor.execute(query, (chat_id, user_id))
        conn.commit()

        return cursor.fetchall()

    finally:
        if cursor is not None:
            cursor.close()
        conn.close()


def retrieve_messages(user_id: int, chat_id: int):
    conn = get_db_connection()
    cursor = None

    try:
        cursor = conn.cursor(dictionary=True)

        # Check if chat id exists
        query = """
        SELECT chat_id
        FROM chat
        WHERE id = (%s) and chat_id = (%s)
        """

        cursor.execute(query, (user_id, chat_id, ))

        chat_id_in_db = cursor.fetchone()

        if chat_id_in_db is None:
            return "Chat_id not available"

        query = """
            SELECT chat_history
            FROM chat
            WHERE chat_id = (%s) AND id = (%s)
        """

        cursor.execute(query, (chat_id, user_id, ))
        history = cursor.fetchone()

        if history is None or not history.get("chat_history"):
            return []

        return json.loads(history.get("chat_history"))

    finally:
        if cursor is not None:
            cursor.close()
        conn.close()