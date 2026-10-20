from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers.chat_routes import chat_router
from routers.user_routes import user_router


app = FastAPI()

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router)
app.include_router(user_router)


@app.get("/")
def home():
    return {
        "success": True,
        "message": "Hello world",
        "data": "Server is running",
    }
