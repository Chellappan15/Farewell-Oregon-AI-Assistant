from fastapi import APIRouter, Depends, status
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

from auth.dependencies import get_current_user
from rag.context_builder import RetrievalMode
from services.chat_service import (
    create_chat,
    delete_chat,
    get_chat_messages,
    list_chats,
    process_chat_query,
    process_chat_query_stream,
)


class ChatRequest(BaseModel):
    query: str = Field(min_length=1, max_length=1000)
    retrieval_mode: RetrievalMode = "hybrid"


chat_router = APIRouter(prefix="/chat")


@chat_router.post("/new-chat", status_code=status.HTTP_201_CREATED)
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
    request: ChatRequest,
    current_user: dict = Depends(get_current_user),
):
    return process_chat_query(
        user_id=int(current_user["user_id"]),
        chat_id=chat_id,
        query=request.query,
        retrieval_mode=request.retrieval_mode,
    )


@chat_router.post("/{chat_id}/stream")
def query_chat_stream(
    chat_id: int,
    request: ChatRequest,
    current_user: dict = Depends(get_current_user),
):
    return StreamingResponse(
        process_chat_query_stream(
            user_id=int(current_user["user_id"]),
            chat_id=chat_id,
            query=request.query,
            retrieval_mode=request.retrieval_mode,
        ),
        media_type="text/plain; charset=utf-8",
    )
