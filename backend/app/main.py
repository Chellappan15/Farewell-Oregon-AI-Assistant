from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from core.config import settings
from db.connect import DatabaseUnavailableError
from routers.chat_routes import chat_router
from routers.user_routes import user_router
from services.exceptions import ChatNotFoundError
from rag.context_builder import ensure_bm25_index

# Eval
from eval.evaluator import evaluator


@asynccontextmanager
async def lifespan(app: FastAPI):
    ensure_bm25_index()
    yield


app = FastAPI(lifespan=lifespan)

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


@app.exception_handler(DatabaseUnavailableError)
async def database_unavailable_handler(request: Request, exc: DatabaseUnavailableError):
    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content={
            "success": False,
            "message": "The service is temporarily unavailable. Please try again shortly.",
        },
    )


@app.exception_handler(RequestValidationError)
async def validation_error_handler(request: Request, exc: RequestValidationError):
    # Return a single readable message (the frontend shows `detail` as text).
    first = exc.errors()[0] if exc.errors() else {}
    message = str(first.get("msg", "Invalid request.")).removeprefix("Value error, ")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"success": False, "message": message, "detail": message},
    )


@app.get("/")
def home():
    return {
        "success": True,
        "message": "Hello world",
        "data": "Server is running",
    }

@app.get("/evaluate")
def evaluate():
    return evaluator()