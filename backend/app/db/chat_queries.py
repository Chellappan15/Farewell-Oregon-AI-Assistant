import json
import logging

from db.connect import get_db_connection

logger = logging.getLogger(__name__)

def get_chat_history(chat_id: int, user_id: int):
    conn = get_db_connection()
    cursor = None

    try:
        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT chat_history
            FROM chat
            WHERE chat_id = %s and id = %s
        """

        cursor.execute(query, (chat_id, user_id, ))
        history = cursor.fetchone()

        if not history or not history.get("chat_history"):
            logger.info("No history found for chat_id=%s", chat_id)
            return []

        return json.loads(history.get("chat_history"))

    finally:
        if cursor is not None:
            cursor.close()
        conn.close()

def chatProgress(id: int, chat_id: int, chat_title: str, data) -> int:
    """Append a message to a chat owned by `id`.

    Only updates an existing row that belongs to the user, so it can never
    write into another user's chat or create a chat with an arbitrary ID.
    Returns the number of rows updated (0 = chat not found / not owned).
    """
    conn = get_db_connection()
    cursor = None

    try:
        cursor = conn.cursor(dictionary=True)
        json_data = json.dumps(data)

        query = """
            UPDATE chat
            SET
                chat_title = CASE
                    WHEN chat_title = 'New Chat' THEN %s
                    ELSE chat_title
                END,
                chat_history = JSON_ARRAY_APPEND(
                    COALESCE(chat_history, JSON_ARRAY()),
                    '$',
                    JSON_EXTRACT(%s, '$')
                )
            WHERE chat_id = %s AND id = %s
        """

        cursor.execute(query, (chat_title, json_data, chat_id, id))
        conn.commit()

        return cursor.rowcount

    finally:
        if cursor is not None:
            cursor.close()
        conn.close()

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

        return cursor.rowcount

    finally:
        if cursor is not None:
            cursor.close()
        conn.close()

def retrieve_messages(user_id: int, chat_id: int):
    conn = get_db_connection()
    cursor = None

    try:
        cursor = conn.cursor(dictionary=True)

        query = """
        SELECT chat_id
        FROM chat
        WHERE id = (%s) and chat_id = (%s)
        """

        cursor.execute(query, (user_id, chat_id, ))

        chat_id_in_db = cursor.fetchone()

        if chat_id_in_db is None:
            return None

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