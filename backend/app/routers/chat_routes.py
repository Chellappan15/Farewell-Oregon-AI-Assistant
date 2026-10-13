from fastapi import APIRouter, Depends
from chat.chat_requests import (
    newChatCreation,
    delete_chat_request,
    get_chats_request,
    retrieve_messages_request,
)
from utils.auth import get_current_user

chat_router = APIRouter(
    prefix = '/chat'
)

@chat_router.get('/new-chat')
def functionCall(current_user: dict = Depends(get_current_user)):
    user_id = int(current_user["user_id"])
    return newChatCreation(user_id = user_id)

@chat_router.delete('/delete-chat')
def delete_chat_route(chat_id: int, current_user: dict = Depends(get_current_user)):
    user_id = int(current_user["user_id"])
    return delete_chat_request(user_id = user_id, chat_id = chat_id)

@chat_router.get('/')
def get_chats_routes(current_user: dict = Depends(get_current_user)):
    user_id = int(current_user["user_id"])
    return get_chats_request(user_id = user_id)

@chat_router.get('/retrieve-messages')
def retrieve_messages(chat_id: int, current_user: dict = Depends(get_current_user)):
    user_id = int(current_user["user_id"])
    return retrieve_messages_request(user_id = user_id, chat_id = chat_id)