from db.chat_queries import newChat, delete_chat_query, get_chats_query, retrieve_messages
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

def retrieve_messages_request(user_id: int, chat_id: int):
    data = retrieve_messages(user_id, chat_id)

    if len(data) == 0:
        return ({
            "success": False,
            "message": "Chat is not available"
        })
    else:
        return ({
            "success": True,
            "message": f"Chat history for chat_id: {chat_id}",
            "data": data
        })