import logging
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
from rag.indexer import ensure_vector_index
from core.games import GAME_KEYS
from db.connect import get_db_connection
from hybrid_search.bm25_indexer import index_path
from rag.retriever import get_collection

# Without this, every logger.info in the app is dropped (Python's default level is WARNING)
logging.basicConfig(
    level=settings.log_level,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    for game in GAME_KEYS:
        ensure_vector_index(game)
        ensure_bm25_index(game)
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


@app.get("/health")
def health():
    """Liveness: the process is up and answering. Checks nothing else."""
    return {"status": "ok"}


@app.get("/ready")
def ready():
    """Readiness: MySQL answers and every game's indexes exist. 503 if anything is missing."""
    checks: dict[str, bool] = {}

    try:
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            cursor.fetchall()
            cursor.close()
            checks["mysql"] = True
        finally:
            conn.close()
    except Exception:
        logger.exception("Readiness check: MySQL unavailable")
        checks["mysql"] = False

    for game in GAME_KEYS:
        try:
            checks[f"{game}_vector_index"] = get_collection(game).count() > 0
        except Exception:
            logger.exception("Readiness check: Chroma unavailable for %s", game)
            checks[f"{game}_vector_index"] = False
        checks[f"{game}_bm25_index"] = index_path(game).exists()

    is_ready = all(checks.values())
    return JSONResponse(
        status_code=status.HTTP_200_OK if is_ready else status.HTTP_503_SERVICE_UNAVAILABLE,
        content={"status": "ready" if is_ready else "not_ready", "checks": checks},
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
    # Imported here so the app runs without the eval packages (requirements-eval.txt)
    try:
        from eval.evaluator import evaluator
    except ImportError:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "success": False,
                "message": "Eval packages are not installed. Run: pip install -r requirements-eval.txt",
            },
        )
    return evaluator()