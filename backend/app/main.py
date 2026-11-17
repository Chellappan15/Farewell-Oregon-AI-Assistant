from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from core.config import settings
from routers.chat_routes import chat_router
from routers.user_routes import user_router
from services.exceptions import ChatNotFoundError


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router)
app.include_router(user_router)


@app.exception_handler(ChatNotFoundError)
async def chat_not_found_handler(request: Request, exc: ChatNotFoundError):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"success": False, "message": "Chat not found"},
    )


@app.get("/")
def home():
    return {
        "success": True,
        "message": "Hello world",
        "data": "Server is running",
    }
