# Quickstart Guide: Better Auth Integration

## Prerequisites
- Node.js 18+ and npm
- Python 3.11+ with uv
- Neon PostgreSQL database instance
- Better Auth configured in frontend

## Frontend Setup

### 1. Install Better Auth
```bash
cd frontend
npm add better-auth better-auth/plugins
```

### 2. Configure Better Auth in frontend
Create `frontend/src/lib/auth.ts`:
```typescript
import { betterAuth } from "better-auth";
import { jwt } from "better-auth/plugins";

export const auth = betterAuth({
  baseURL: process.env.NEXT_PUBLIC_BETTER_AUTH_URL || "http://localhost:3000",
  database: {
    // Better Auth will handle its own database tables
  },
  plugins: [
    jwt() // Enable JWT tokens if needed for external services
  ]
});
```

### 3. Initialize Better Auth client
Create `frontend/src/lib/authClient.ts`:
```typescript
import { createAuthClient } from "better-auth/client";
import { jwtClient } from "better-auth/client/plugins";

export const authClient = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_BETTER_AUTH_URL || "http://localhost:3000",
  plugins: [
    jwtClient()
  ]
});
```

## Backend Setup

### 1. Install required dependencies
```bash
cd backend
uv add python-jose cryptography
```

### 2. Configure JWT verification middleware
Create `backend/src/middleware/auth_middleware.py`:
```python
from fastapi import HTTPException, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import httpx
from jose import jwt, JWTError
import os
from typing import Optional

class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)
        self.jwks_client = None

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)

        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            token = credentials.credentials
            user_id = await self.verify_jwt(token)
            if not user_id:
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            request.state.user_id = user_id
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    async def verify_jwt(self, token: str) -> Optional[str]:
        # Fetch JWKS from Better Auth
        jwks_url = f"{os.getenv('BETTER_AUTH_URL', 'http://localhost:3000')}/api/auth/jwks"
        if not self.jwks_client:
            async with httpx.AsyncClient() as client:
                jwks_response = await client.get(jwks_url)
                jwks = jwks_response.json()
                self.jwks_client = jwks

        try:
            # Decode and verify the token
            payload = jwt.decode(
                token,
                self.jwks_client,
                algorithms=["RS256"],
                audience=os.getenv('BETTER_AUTH_AUDIENCE', 'your-app-audience')
            )
            return payload.get('sub')  # User ID is in 'sub' claim
        except JWTError:
            return None
```

### 3. Create database models
Update `backend/src/models/user.py`:
```python
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
import uuid

class User(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    email: str = Field(unique=True, nullable=False)
    name: Optional[str] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = Field(default=True)
```

### 4. Create services for user management
Create `backend/src/services/user_service.py`:
```python
from sqlmodel import Session, select
from ..models.user import User
from typing import Optional
import uuid

class UserService:
    @staticmethod
    async def get_or_create_user(session: Session, user_id: str, email: str, name: Optional[str] = None) -> User:
        # Check if user already exists
        statement = select(User).where(User.id == user_id)
        result = session.exec(statement)
        user = result.first()

        if user:
            # Update user info if needed
            if name and user.name != name:
                user.name = name
                user.updated_at = datetime.utcnow()
                session.add(user)
                session.commit()
            return user
        else:
            # Create new user
            user = User(
                id=uuid.UUID(user_id),
                email=email,
                name=name
            )
            session.add(user)
            session.commit()
            session.refresh(user)
            return user
```

## Database Migration
Run database migrations to create the required tables:
```bash
cd backend
# Run your existing migration command or create new ones for the auth tables
```

## Environment Variables
Add these to your `.env` files:

Frontend (.env.local):
```
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3000
```

Backend (.env):
```
BETTER_AUTH_URL=http://localhost:3000
BETTER_AUTH_AUDIENCE=your-app-audience
```

## Testing the Integration
1. Start the Better Auth server
2. Start the FastAPI backend
3. Verify that protected endpoints require valid Better Auth tokens
4. Test user creation and authentication flow
5. Verify that chat history is properly associated with authenticated users
