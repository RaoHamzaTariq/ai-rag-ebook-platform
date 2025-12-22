# AI-Native RAG eBook Platform

A modern, "AI-Native" textbook platform featuring an integrated RAG (Retrieval-Augmented Generation) chatbot. This system allows users to read content and interact with an AI agent that answers questions based on the book's content, persisting their conversations across sessions.

## 🏗 Architecture

The project consists of three main microservices:

1.  **Frontend (`/frontend`)**:
    *   **Framework**: Docusaurus (React/TypeScript).
    *   **Features**: Displays the ebook content, manages user UI, and embeds the Better Auth client.
    *   **Deployment**: Vercel.

2.  **Auth Server (`/auth-server`)**:
    *   **Framework**: Node.js + Express + Better Auth.
    *   **Features**: Handles all authentication logic (Sign Up, Sign In, Session Management), issues JWTs, and exposes a JWKS endpoint for token verification. Connects directly to the Database to manage users.
    *   **Deployment**: Railway.

3.  **Backend (`/backend`)**:
    *   **Framework**: FastAPI (Python).
    *   **Features**: 
        *   **RAG Agent**: Processes user queries using OpenAI and Qdrant vector store.
        *   **Persistence**: Stores chat history and messages in Neon PostgreSQL.
        *   **Authorization**: Verifies Better Auth JWTs by checking the Auth Server's JWKS.
    *   **Deployment**: Railway.

## 🚀 Getting Started

### Prerequisites

*   **Node.js** (v20+)
*   **Python** (v3.11+)
*   **PostgreSQL** (Neon DB recommended)
*   **OpenAI API Key**
*   **Qdrant** (Vector Database)

### 1. Database Setup (Neon PostgreSQL)

You need a PostgreSQL database. Get your connection string (e.g., from Neon Console).
It should look like: `postgres://user:pass@host:port/dbname?sslmode=require`

### 2. Auth Server Setup

Handles user creation and login.

```bash
cd auth-server
# Copy env example
cp .env.example .env
npm install
npm run dev
# Runs on Port 3001
```

**Required `.env` Variables**:
*   `DATABASE_URL`: Your Postgres connection string.
*   `BETTER_AUTH_SECRET`: Random string for encryption.
*   `FRONTEND_URL`: `http://localhost:3000` (for CORS).

### 3. Backend Setup (FastAPI)

Handles the AI logic and chat storage.

```bash
cd backend
# Create Virtual Env
python -m venv .venv
# Activate: .venv\Scripts\activate (Windows) or source .venv/bin/activate (Mac/Linux)
pip install -r requirements.txt
uv run src/main.py
# Runs on Port 8000
```

**Required `.env` Variables**:
*   `DATABASE_URL`: Same Postgres connection string.
*   `BETTER_AUTH_URL`: `http://localhost:3001` (to fetch JWKS).
*   `OPENAI_API_KEY`: Your key.
*   `QDRANT_URL` / `QDRANT_API_KEY`: Your vector store credentials.

### 4. Frontend Setup (Docusaurus)

The user interface.

```bash
cd frontend
# Copy env example if available, or just set env vars
npm install
npm start
# Runs on Port 3000
```

**Required Environment Variables**:
*   `NEXT_PUBLIC_BETTER_AUTH_URL`: `http://localhost:3001` (Must be public/accessible by browser).
*   `REACT_APP_BACKEND_URL`: `http://localhost:8000`.

## 🌐 Deployment Logic

Since we use multiple services, deployment requires correct linking:

1.  **Auth Server (Railway)**: Deployed first.
2.  **Backend (Railway)**: Needs `BETTER_AUTH_URL` pointing to the deployed Auth Server.
3.  **Frontend (Vercel)**: Needs `NEXT_PUBLIC_BETTER_AUTH_URL` pointing to the deployed Auth Server.

See [DEPLOYMENT.md](./DEPLOYMENT.md) for a detailed step-by-step guide.

## 🛠 Usage Flow

1.  User visits Frontend.
2.  User clicks "Sign In" -> Request goes to **Auth Server** (Port 3001).
3.  On success, User gets a **JWT**.
4.  User sends a chat message on Frontend.
5.  Frontend sends request to **Backend** (Port 8000) with `Authorization: Bearer <JWT>`.
6.  **Backend** checks `BETTER_AUTH_URL/api/auth/jwks` to verify signature.
7.  **Backend** allows request, calls AI Agent, and saves chat to **Neon DB**.
