# Quickstart: Auth & History Integration

This guide provides the necessary steps to set up and run the integrated Authentication and Chat History system locally for development.

## **Prerequisites**

- **Node.js 20+** (for Auth Server and Frontend)
- **Python 3.12+** (for Backend)
- **PostgreSQL Database** (Local or Neon)
- **Qdrant Vector DB** (for RAG features)

## **Service 1: Auth Server (Modern Identity)**

The Auth Server manages user registration and JWT issuance.

1. **Navigate to the directory**: `cd auth-server`
2. **Install dependencies**: `npm install`
3. **Configure Environment**: Create a `.env` file:
   ```env
   DATABASE_URL=your_postgresql_url
   FRONTEND_URL=http://localhost:3000
   PORT=3001
   ```
4. **Run development server**: `npm run dev`
   - Access JWKS at: `http://localhost:3001/api/auth/jwks`

## **Service 2: Backend (FastAPI & AI)**

The Backend verifies identities and manages the AI RAG pipeline.

1. **Navigate to the directory**: `cd backend`
2. **Setup Environment**:
   ```env
   DATABASE_URL=your_postgresql_url
   BETTER_AUTH_URL=http://localhost:3001
   ALLOWED_ORIGINS=http://localhost:3000
   QDRANT_URL=your_qdrant_url
   OPENAI_API_KEY=your_key
   ```
3. **Run the API**: `uv run uvicorn src.main:app --reload --port 8000`
   - API Docs: `http://localhost:8000/docs`

## **Service 3: Frontend (Docusaurus UI)**

The Frontend provides the interactive user experience.

1. **Navigate to the directory**: `cd frontend`
2. **Install dependencies**: `npm install`
3. **Configure Environment**:
   ```env
   NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3001
   REACT_APP_BACKEND_URL=http://localhost:8000
   ```
4. **Run the site**: `npm start`
   - Access at: `http://localhost:3000`

## **Key Authentication Flows**

### **Sign Up**
1. Visit `http://localhost:3000/signup`.
2. Fill the form; the user is created in the `user` table.
3. Upon success, you are redirected to the login page.

### **Chat Interaction**
1. Log in via `http://localhost:3000/login`.
2. Open the chat widget in the documentation.
3. Send a message.
4. The system validates your JWT, saves the message, retrieves 3 RAG sources, and returns a Markdown response.

## **Troubleshooting**

- **401 Unauthorized**: Ensure the Auth Server is running and the `Authorization` header is being sent by the `agentClient.ts`.
- **DB Connection Failures**: Verify `DATABASE_URL` is consistent across both `auth-server` and `backend`.
- **CORS Errors**: Check that `ALLOWED_ORIGINS` in the backend matches your frontend URL.
