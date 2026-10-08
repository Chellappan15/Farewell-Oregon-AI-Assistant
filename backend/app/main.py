from fastapi import FastAPI
from LLM import query_processing
from routers.chat_routes import chat_router
from db.chat_queries import chatProgress
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware

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

@app.get('/')
def Home():
    return {
        "message": "Hello world" 
    }

@app.post('/{chat_id}')
def Query(query: str, chat_id: int):
    now = datetime.now()
    print(query)
    chatProgress(1, chat_id = chat_id, chat_title = query, data = {
        'role': 'user',
        'parts': [
            {
                "text": query
            }
        ],
        "time_stamp": now.strftime("%d-%m-%Y %H:%M %p")
    })
    return query_processing.getResults(query, user_id = 1, chat_id = chat_id)