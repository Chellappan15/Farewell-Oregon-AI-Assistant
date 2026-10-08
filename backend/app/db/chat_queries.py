import json

from db.connect import cursor, conn

import json

def get_chat_history(chat_id: int):
    query = """
        SELECT chat_history
        FROM chat
        WHERE chat_id = %s
    """

    cursor.execute(query, (chat_id,))

    history = cursor.fetchone()

    if not history:
        return []

    return json.loads(history.get('chat_history'))

def chatProgress(id: int, chat_id: int, chat_title: str, data):
    json_data = json.dumps(data)

    query = """
        INSERT INTO chat (id, chat_id, chat_title, chat_history)
        VALUES (%s, %s, %s, JSON_ARRAY(JSON_EXTRACT(%s, '$')))

        ON DUPLICATE KEY UPDATE
            chat_history = JSON_ARRAY_APPEND(
                chat_history,
                '$',
                JSON_EXTRACT(%s, '$')
            )
    """

    cursor.execute(
        query,
        (id, chat_id, chat_title, json_data, json_data)
    )

    conn.commit()

def get_chats_query(user_id: int):
    query = """
            SELECT chat_title
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
            INSERT INTO chat(id) 
            VALUES (%s)
            """
    cursor.execute(
        query,
        (id,)
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