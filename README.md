# Farewell Oregon AI Assistant

Farewell Oregon is a conversational **Days Gone** companion built for the
Oregon wasteland. Ask questions about the game, weapons, Freakers, and
survival tactics through a chat interface that combines Gemini, retrieval
augmented generation, and game-specific tools.

## What it includes

- Authenticated chat with persistent conversation history
- Gemini-powered answers grounded in the included *Days Gone* reference PDF
- ChromaDB vector search for relevant game knowledge
- Tool calling for weapon comparisons and Freaker details
- React and TypeScript frontend with a focused survival-intelligence UI
- FastAPI backend with JWT authentication and MySQL persistence

## Project structure

```text
backend/
  app/
    ai/          Gemini client and game-specific tools
    auth/        JWT authentication and password handling
    db/          MySQL queries and connection pooling
    LLM/         Prompt rendering and query processing
    rag/         PDF indexing, embeddings, and retrieval
    routers/     FastAPI endpoints
    services/    Authentication and chat services
frontend/
  src/           React application, pages, components, and API services
```

## Requirements

- Python 3.10+
- Node.js 18+
- MySQL running locally with an `llm` database and the tables expected by the
  backend queries
- A Google Gemini API key

## Getting started

### 1. Configure the backend

Create a Python virtual environment and install the dependencies:

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r ..\requirements.txt
```

Create a `.env` file in `backend` with the required application secrets:

```env
GEMINI_API_KEY=your-gemini-api-key
JWT_SECRET=replace-with-a-long-random-secret
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24
```

The MySQL connection is configured in
[`backend/app/db/connect.py`](backend/app/db/connect.py). Make sure its local
connection settings match your MySQL installation and that the `llm` database
and required tables are available.

Start the API from the application directory:

```powershell
cd app
python -m uvicorn main:app --reload
```

The backend is available at `http://localhost:8000`.

### 2. Start the frontend

In a second terminal:

```powershell
cd frontend
npm install
npm run dev
```

The frontend uses `http://localhost:8000` by default. To point it at another
API server, create `frontend/.env`:

```env
VITE_API_BASE_URL=http://localhost:8000
```

Open the Vite URL shown in the terminal, usually
`http://localhost:5173`.

## Useful commands

From `frontend`:

```powershell
npm run dev       # Start the development server
npm run build     # Type-check and create a production build
npm run lint      # Run ESLint
npm run preview   # Preview the production build
```

The backend's local ChromaDB data is persisted in the repository and is used
for retrieval. The source reference document is
[`backend/DAYS GONE.pdf`](backend/DAYS%20GONE.pdf).

## Notes

- Keep API keys, JWT secrets, and database credentials out of version control.
- The app is currently configured for local development with the frontend at
  port `5173` and the backend at port `8000`.
