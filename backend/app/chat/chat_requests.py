from db.chat_queries import newChat, delete_chat_query, get_chats_query
import json

def newChatCreation(user_id):
    chat_id = newChat(id = user_id)

    return {
        "message": "Chat created successfully",
        "success": True,
        "data": {
            "chatId": chat_id
        }
    }

def delete_chat_request(user_id, chat_id):
    data = delete_chat_query(user_id, chat_id)

    return ({
        "success": True,
        "message": "Chat deleted successfully"
    })

def get_chats_request(user_id: int):
    data = get_chats_query(user_id)
    return ({
        "success": True,
        "message": "Chat list loaded successfully",
        "data": data
    })