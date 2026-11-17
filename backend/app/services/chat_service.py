from db.chat_queries import (
    chatProgress,
    delete_chat_query,
    get_chats_query,
    newChat,
    retrieve_messages,
)
from LLM.query_processing import getResults, getResultsStream
from services.exceptions import ChatNotFoundError
from utils.time_utils import utc_now_iso
from LLM.token_estimator import estimator

def create_chat(user_id: int):
    chat_id = newChat(id=user_id)
    return {
        "message": "Chat created successfully",
        "success": True,
        "data": {"chatId": chat_id},
    }


def delete_chat(user_id: int, chat_id: int):
    deleted_rows = delete_chat_query(user_id, chat_id)
    if deleted_rows == 0:
        raise ChatNotFoundError(chat_id)
    return {"success": True, "message": "Chat deleted successfully"}


def list_chats(user_id: int):
    return {
        "success": True,
        "message": "Chat list loaded successfully",
        "data": get_chats_query(user_id),
    }


def get_chat_messages(user_id: int, chat_id: int):
    data = retrieve_messages(user_id, chat_id)
    if data is None:
        raise ChatNotFoundError(chat_id)
    return {
        "success": True,
        "message": f"Chat history for chat_id: {chat_id}",
        "data": data,
    }


def process_chat_query(user_id: int, chat_id: int, query: str):
    _save_user_message(user_id, chat_id, query)
    return getResults(query, user_id=user_id, chat_id=chat_id)


def process_chat_query_stream(user_id: int, chat_id: int, query: str):
    _save_user_message(user_id, chat_id, query)
    return getResultsStream(query, user_id=user_id, chat_id=chat_id)


def _save_user_message(user_id: int, chat_id: int, query: str) -> None:
    """Save the user's message, rejecting chats the user does not own."""
    updated_rows = chatProgress(
        user_id,
        chat_id=chat_id,
        chat_title=query,
        data={
            "role": "user",
            "parts": [{"text": query}],
            "time_stamp": utc_now_iso(),
            "token": estimator(query)
        },
    )
    if updated_rows == 0:
        raise ChatNotFoundError(chat_id)
