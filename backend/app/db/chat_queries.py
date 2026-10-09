import json
from db.connect import cursor, conn

def get_chat_history(chat_id: int):
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


def chatProgress(id: int, chat_id: int, chat_title: str, data):
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
# Front-end requests
def get_chats_query(user_id: int):
    query = """
            SELECT chat_title, id, chat_id
            FROM chat
            WHERE id = (%s)
            """

    cursor.execute(
        query,
        (user_id, )
    )

    return cursor.fetchall()

def newChat(id):
    query = """
            INSERT INTO chat(id, chat_title) 
            VALUES (%s, %s)
            """
    cursor.execute(
        query,
        (id, "New Chat", )
    )

    conn.commit()

    return cursor.lastrowid

def delete_chat_query(user_id: int, chat_id: int):
    query =  """
            DELETE 
            FROM chat
            WHERE chat_id = (%s) AND id = (%s)
            """

    cursor.execute(
        query,
        (chat_id, user_id, )
    )

    conn.commit()
    
    return cursor.fetchall()

def retrieve_messages(user_id: int, chat_id: int):
    query = """
            SELECT chat_history
            FROM chat
            WHERE chat_id = (%s) AND id = (%s)
            """

    cursor.execute(
        query, 
        (chat_id, user_id, )
    )

    history = cursor.fetchone()

    if not history.get("chat_history"):
        return []

    return json.loads(history.get('chat_history'))