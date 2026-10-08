from fastapi import APIRouter
from chat.chat_requests import newChatCreation, delete_chat_request, get_chats_request

chat_router = APIRouter(
    prefix = '/chat'
)

@chat_router.get('/new-chat')
def functionCall():
    return newChatCreation(user_id = 1)

@chat_router.delete('/delete-chat')
def delete_chat_route(user_id: int, chat_id: int):
    return delete_chat_request(user_id, chat_id)

@chat_router.get('/')
def get_chats_routes(user_id: int):
    return get_chats_request(user_id)