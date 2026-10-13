from fastapi import FastAPI, Depends
from LLM import query_processing
from routers.chat_routes import chat_router
from routers.user_routes import user_router
from db.chat_queries import chatProgress
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware
from utils.auth import get_current_user

app = FastAPI()

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,        # Allowed origins
    allow_credentials=True,       # Allow cookies/auth headers
    allow_methods=["*"],          # Allow all HTTP methods
    allow_headers=["*"],          # Allow all headers
)

app.include_router(chat_router)
app.include_router(user_router)

@app.get('/')
def Home():
    return {
        "success": True,
        "message": "Hello world",
        "data": "Server is running" 
    }

@app.post('/{chat_id}')
def Query(chat_id: int, query: str, user_id_payload: dict = Depends(get_current_user)):
    user_id = user_id_payload["user_id"]
    print("1. Query endpoint reached")
    print("2. chat_id:", chat_id)
    print("3. query:", query)
    print("4. user_id:", user_id)

    now = datetime.now()

    print("5. Calling chatProgress")

    chatProgress(
        user_id,
        chat_id=chat_id,
        chat_title=query,
        data={
            'role': 'user',
            'parts': [{'text': query}],
            'time_stamp': now.strftime("%d-%m-%Y %H:%M %p")
        }
    )

    print("6. chatProgress completed")

    return query_processing.getResults(
        query,
        user_id=user_id,
        chat_id=chat_id
    )