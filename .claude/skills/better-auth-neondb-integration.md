# BetterAuth + NeonDB Integration Guide (Docsourous + FastAPI)

This document provides a **comprehensive, implementation-ready reference** for integrating **BetterAuth (frontend, JWT-based)** with a **FastAPI backend** that stores user accounts and chat history in **Neon PostgreSQL**, along with RAG chat support using Qdrant and OpenAI Agents SDK.

---

## Table of Contents

1. [Architecture Overview](#1-architecture-overview)
2. [Prerequisites](#2-prerequisites)
3. [Frontend BetterAuth Setup (JWT)](#3-frontend-betterauth-setup-jwt)
4. [Backend FastAPI JWT Validation](#4-backend-fastapi-jwt-validation)
5. [Neon PostgreSQL Database Schema](#5-neon-postgresql-database-schema)
6. [Backend API Services & Routes](#6-backend-api-services--routes)
7. [Docsourous Frontend API Integration](#7-docsourous-frontend-api-integration)
8. [Security Considerations](#8-security-considerations)
9. [Testing & Monitoring](#9-testing--monitoring)
10. [Deployment Guidelines](#10-deployment-guidelines)
11. [Appendix: Code Examples](#11-appendix-code-examples)

---

## 1. Architecture Overview

```
+-----------------+      JWT Token       +----------------------+
|                 |  <----------------->  |                      |
|   Frontend      |                      |    FastAPI Backend    |
| (Docsourous)    |                      |   (Python + Uvicorn) |
| + BetterAuth    |                      |  + JWT Middleware    |
|   JWT Plugin    |                      |  + Neon PostgreSQL   |
|                 |                      |  + Qdrant + RAG      |
+-----------------+                      +----------------------+
          |                                         |
          |    Fetch protected data / chat UI       |
          +---------------------------------------->|
                                                   |
                                     +-------------v-----------+
                                     |   Neon PostgreSQL        |
                                     |   Users, Conv, Messages  |
                                     +--------------------------+
```

---

## 2. Prerequisites

### Local Tools

* Node.js 18+
* Python 3.11+
* Neon PostgreSQL instance
* BetterAuth configured frontend
* Qdrant instance for embeddings
* OpenAI API key for RAG generation

### Environment Variables Needed

**Frontend (.env.local):**

```
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3000
NEXT_PUBLIC_BACKEND_URL=http://localhost:8000
```

**Backend (.env):**

```
BETTER_AUTH_URL=http://localhost:3000
BETTER_AUTH_AUDIENCE=http://localhost:3000
DATABASE_URL=postgresql://username:password@host:port/dbname
QDRANT_URL=http://localhost:6333
OPENAI_API_KEY=your-openai-key
```

Ensure environment variables are loaded before running services.

---

## 3. Frontend BetterAuth Setup (JWT)

Docsourous doesn’t have an internal API server — so the frontend must:

1. Use BetterAuth’s **JWT plugin**
2. Retrieve a JWT token after login
3. Store the token
4. Send the token with requests to the FastAPI backend

---

### 3.1 Install BetterAuth Client and JWT Plugin

```bash
cd frontend
npm install better-auth better-auth/plugins
```

---

### 3.2 Create `authClient`

`frontend/src/lib/authClient.ts`

```ts
import { createAuthClient } from "better-auth/client";
import { jwtClient } from "better-auth/client/plugins";

export const authClient = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_BETTER_AUTH_URL,
  plugins: [jwtClient()]
});
```

---

### 3.3 Getting JWT Token

When user logs in (or on page load):

```ts
async function getJwtToken() {
  const { data, error } = await authClient.token();
  if (error) {
    console.error("Token fetch error:", error);
    return null;
  }
  return data?.token ?? null;
}
```

Store locally:

```ts
const token = await getJwtToken();
localStorage.setItem("authToken", token);
```

---

### 3.4 Logout

```ts
await authClient.signOut();
localStorage.removeItem("authToken");
```

---

## 4. Backend FastAPI JWT Validation

### 4.1 Install Dependencies

```bash
cd backend
pip install fastapi uvicorn python-jose httpx python-dotenv sqlmodel asyncpg
```

---

### 4.2 Load Environment Variables

Create `backend/.env` then:

```python
from dotenv import load_dotenv
load_dotenv()
```

---

### 4.3 JWT Middleware (auth_middleware.py)

```python
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
import httpx
import os

class JWTBearer(HTTPBearer):
    def __init__(self, auto_error=True):
        super().__init__(auto_error=auto_error)
        self.jwks = None

    async def _fetch_jwks(self):
        jwks_url = f"{os.getenv('BETTER_AUTH_URL')}/api/auth/jwks"
        async with httpx.AsyncClient() as client:
            resp = await client.get(jwks_url)
            self.jwks = resp.json()
        return self.jwks

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        if not credentials or credentials.scheme.lower() != "bearer":
            raise HTTPException(401, "Unauthorized")

        token = credentials.credentials
        try:
            if not self.jwks:
                await self._fetch_jwks()

            payload = jwt.decode(
                token,
                self.jwks,
                algorithms=["RS256"],
                audience=os.getenv("BETTER_AUTH_AUDIENCE"),
                issuer=os.getenv("BETTER_AUTH_URL")
            )
            request.state.user = payload
            return payload

        except JWTError:
            raise HTTPException(401, "Invalid token or expired")
```

---

### 4.4 Backend Dependencies

Use JWTBearer in routes:

```python
from fastapi import Depends, APIRouter, Request
from middleware.auth_middleware import JWTBearer

router = APIRouter()

@router.post("/agents/run", dependencies=[Depends(JWTBearer())])
async def run_agent(request: Request, body: dict):
    user = request.state.user
    ...
```

---

## 5. Neon PostgreSQL Database Schema

### 5.1 Users Table

```sql
CREATE TABLE users (
  id UUID PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  name VARCHAR(255),
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  is_active BOOLEAN DEFAULT TRUE
);
```

---

### 5.2 Conversations Table

```sql
CREATE TABLE conversations (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES users(id),
  title VARCHAR(255),
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  is_active BOOLEAN DEFAULT TRUE
);
```

---

### 5.3 Messages Table

```sql
CREATE TABLE messages (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  conversation_id UUID REFERENCES conversations(id),
  user_id UUID REFERENCES users(id),
  role VARCHAR(20),
  content TEXT,
  sources JSONB,
  timestamp TIMESTAMPTZ DEFAULT NOW(),
  agent_type VARCHAR(50)
);
```

---

## 6. Backend API Services & Routes

### 6.1 User Service (Python)

```python
from sqlmodel import Session, select
from models.user import User

class UserService:
    @staticmethod
    def get_or_create(session: Session, user_id: str, email: str, name: str):
        q = select(User).where(User.id == user_id)
        user = session.exec(q).first()
        if user:
            return user
        user = User(id=user_id, email=email, name=name)
        session.add(user)
        session.commit()
        session.refresh(user)
        return user
```

---

### 6.2 Conversation Service

```python
class ConversationService:
    @staticmethod
    def create(session: Session, user_id: str, title: str):
        conv = Conversation(user_id=user_id, title=title)
        session.add(conv)
        session.commit()
        session.refresh(conv)
        return conv
```

---

## 7. Docsourous Frontend API Integration

### 7.1 Generic Fetch Wrapper

```js
async function apiFetch(path, method="GET", body=null) {
  const token = localStorage.getItem("authToken");
  const url = `${process.env.NEXT_PUBLIC_BACKEND_URL}${path}`;

  const headers = {
    "Content-Type": "application/json",
    "Authorization": `Bearer ${token}`,
  };

  return fetch(url, {
    method,
    headers,
    body: body ? JSON.stringify(body) : null
  });
}
```

---

### 7.2 Chat Widget Request

```js
const response = await apiFetch("/agents/run", "POST", { question });
const data = await response.json();
```

---

## 8. Security Considerations

* Always validate JWT tokens via JWKS
* Never store BetterAuth secrets on backend
* Use HTTPS in production
* Use CORS middleware to allow frontend origin

---

## 9. Testing & Monitoring

### 9.1 Testing

* Verify protected endpoints return 401 without token
* Check correct user from JWT
* Validate conversation persistence

---

## 10. Deployment Guidelines

* Set environment variables securely
* Ensure QDRANT and PostgreSQL connections are configured
* Use CORS configuration matching your frontend origin
* Monitor token failures

---

## 11. Appendix: Code Examples

### JWT Example

```json
{
  "sub": "uuid-user-id",
  "email": "user@example.com",
  "name": "User Name",
  "iat": 1700000000,
  "exp": 1700003600
}
```