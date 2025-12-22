# **Quickstart Guide: BetterAuth + FastAPI + Neon PostgreSQL + RAG Chatbot**

This guide helps you quickly set up authentication using **BetterAuth (JWT)** in the frontend and verify it in your **FastAPI backend** while storing user chats in **Neon PostgreSQL**.

## **Prerequisites**

* Node.js 18+ and npm
* Python 3.11+ with `uvicorn`
* Neon PostgreSQL database instance
* BetterAuth configured in the frontend
* Your RAG chatbot and Qdrant setup already running


## **1. Frontend Setup (BetterAuth + JWT)**

### **1.1 Install BetterAuth**

```bash
cd frontend
npm install better-auth better-auth/plugins
```

> We’ll use the **JWT plugin** so your frontend can fetch a JWT token for FastAPI backend validation. ([Better Auth][1])

### **1.2 Configure BetterAuth Server (Frontend Side)**

Create `frontend/src/lib/auth.ts`:

```typescript
import { betterAuth } from "better-auth";
import { jwt } from "better-auth/plugins";

export const auth = betterAuth({
  baseURL: process.env.NEXT_PUBLIC_BETTER_AUTH_URL || "http://localhost:3000",
  plugins: [ jwt() ] // Enable JWT plugin
});
```

### **1.3 Initialize BetterAuth Client**

Create `frontend/src/lib/authClient.ts`:

```typescript
import { createAuthClient } from "better-auth/client";
import { jwtClient } from "better-auth/client/plugins";

export const authClient = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_BETTER_AUTH_URL || "http://localhost:3000",
  plugins: [ jwtClient() ] // Pull JWT tokens
});
```

## **2. Frontend Usage (Get JWT Token)**

Where you make API calls (e.g., when user logs in or before sending a request to backend):

```ts
// Fetch JWT token from BetterAuth client
const { data, error } = await authClient.token();
if (error || !data?.token) {
  console.error("Failed to get JWT token:", error);
} else {
  const jwtToken = data.token;
  // Store token and use in fetch calls
  localStorage.setItem("authToken", jwtToken);
}
```

Then include this token in requests:

```ts
fetch("/api/agents/run", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    "Authorization": `Bearer ${jwtToken}`
  },
  body: JSON.stringify({ question })
});
```


## **3. Backend Setup (FastAPI)**

### **3.1 Install Python Dependencies**

```bash
cd backend
pip install python-jose httpx python-dotenv
```

We’ll use **python-jose** to verify JWT tokens your frontend sends using BetterAuth’s public keys (from JWKS). ([Better Auth][1])


### **3.2 JWT Middleware (Validate Token)**

Create `backend/src/middleware/auth_middleware.py`:

```python
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
import httpx
import os

class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)
        self.jwks_cache = None

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        if credentials and credentials.scheme == "Bearer":
            token = credentials.credentials
            user = await self.verify_jwt(token)
            if not user:
                raise HTTPException(status_code=401, detail="Invalid or expired token")
            request.state.user = user
            return user
        raise HTTPException(status_code=401, detail="Unauthorized")

    async def verify_jwt(self, token: str):
        jwks_url = f"{os.getenv('BETTER_AUTH_URL')}/api/auth/jwks"
        async with httpx.AsyncClient() as client:
            jwks_resp = await client.get(jwks_url)
            jwks = jwks_resp.json()

        try:
            payload = jwt.decode(
                token,
                jwks,
                algorithms=["EdDSA", "RS256"],
                audience=os.getenv("BETTER_AUTH_AUDIENCE"),
                issuer=os.getenv("BETTER_AUTH_URL")
            )
            return payload
        except JWTError:
            return None
```


### **3.3 Add to FastAPI Routes**

In your router:

```python
from fastapi import APIRouter, Depends, Request
from backend.src.middleware.auth_middleware import JWTBearer

router = APIRouter()

@router.post("/agents/run", dependencies=[Depends(JWTBearer())])
async def run_agent(request: Request, payload: dict):
    user = request.state.user  # from token
    # use user info for DB storage and chat logic
    return ...
```

## **4. Database Models & Storage**

### **4.1 User Model (SQLModel Example)**

File: `backend/src/models/user.py`:

```python
from sqlmodel import SQLModel, Field
from datetime import datetime
import uuid

class User(SQLModel, table=True):
    id: str = Field(primary_key=True)
    email: str
    name: str | None
    created_at: datetime = Field(default_factory=datetime.utcnow)
```

### **4.2 Conversation/Message Models**

Similar models should relate user to messages; store question/answer, timestamps.

## **5. Database Migration**

Run migrations or execute your schema creation code so tables exist in Neon PostgreSQL.

```bash
# Example
cd backend
alembic upgrade head
```

(or whatever migration tool you use)

## **6. Environment Variables**

**Frontend `.env.local`**

```
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3000
```

**Backend `.env`**

```
BETTER_AUTH_URL=http://localhost:3000
BETTER_AUTH_AUDIENCE=http://localhost:3000
DATABASE_URL=postgresql://...
```

> `BETTER_AUTH_AUDIENCE` must match the expected token audience. Default is your base URL. ([Better Auth][1])

---

## **7. Test It All**

1. Run your BetterAuth server (frontend auth).
2. Run your FastAPI backend.
3. Login/signup via the frontend.
4. Obtain a JWT token from BetterAuth.
5. Call a protected endpoint like `/agents/run`.
6. Validate responses and confirm that chat history is associated with the authenticated user.
