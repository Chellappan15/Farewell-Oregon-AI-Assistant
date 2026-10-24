from datetime import datetime

from db.chat_queries import (
    chatProgress,
    delete_chat_query,
    get_chats_query,
    newChat,
    retrieve_messages,
)
from LLM.query_processing import getResults, getResultsStream

def create_chat(user_id: int):
    chat_id = newChat(id=user_id)
    return {
        "message": "Chat created successfully",
        "success": True,
        "data": {"chatId": chat_id},
    }

def delete_chat(user_id: int, chat_id: int):
    delete_chat_query(user_id, chat_id)
    return {"success": True, "message": "Chat deleted successfully"}

def list_chats(user_id: int):
    return {
        "success": True,
        "message": "Chat list loaded successfully",
        "data": get_chats_query(user_id),
    }

def get_chat_messages(user_id: int, chat_id: int):
    data = retrieve_messages(user_id, chat_id)
    if data == "Chat_id not available":
        return {"success": False, "message": "Chat is not available"}
    return {
        "success": True,
        "message": f"Chat history for chat_id: {chat_id}",
        "data": data,
    }

def process_chat_query(user_id: int, chat_id: int, query: str):
    now = datetime.now()
    chatProgress(
        user_id,
        chat_id=chat_id,
        chat_title=query,
        data={
            "role": "user",
            "parts": [{"text": query}],
            "time_stamp": now.strftime("%d-%m-%Y %H:%M %p"),
        },
    )
    return getResults(query, user_id=user_id, chat_id=chat_id)

def process_chat_query_stream(user_id: int, chat_id: int, query: str):
    now = datetime.now()
    chatProgress(
        user_id,
        chat_id=chat_id,
        chat_title=query,
        data={
            "role": "user",
            "parts": [{"text": query}],
            "time_stamp": now.strftime("%d-%m-%Y %H:%M %p"),
        },
    )
    return getResultsStream(query, user_id=user_id, chat_id=chat_id)
