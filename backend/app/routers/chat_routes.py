from fastapi import APIRouter, Depends

from auth.dependencies import get_current_user
from services.chat_service import (
    create_chat,
    delete_chat,
    get_chat_messages,
    list_chats,
    process_chat_query,
)

chat_router = APIRouter(prefix="/chat")

@chat_router.get("/new-chat")
def chat_creation(current_user: dict = Depends(get_current_user)):
    return create_chat(int(current_user["user_id"]))

@chat_router.delete("/delete-chat")
def delete_chat_route(
    chat_id: int,
    current_user: dict = Depends(get_current_user),
):
    return delete_chat(int(current_user["user_id"]), chat_id)

@chat_router.get("/")
def get_chats_routes(current_user: dict = Depends(get_current_user)):
    return list_chats(int(current_user["user_id"]))

@chat_router.get("/retrieve-messages")
def retrieve_messages(
    chat_id: int,
    current_user: dict = Depends(get_current_user),
):
    return get_chat_messages(int(current_user["user_id"]), chat_id)

@chat_router.post("/{chat_id}")
def query_chat(
    chat_id: int,
    query: str,
    current_user: dict = Depends(get_current_user),
):
    return process_chat_query(
        user_id=int(current_user["user_id"]),
        chat_id=chat_id,
        query=query,
    )
