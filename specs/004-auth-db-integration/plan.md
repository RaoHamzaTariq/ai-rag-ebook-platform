# **Implementation Plan: BetterAuth Integration with FastAPI and PostgreSQL**

**Branch:** `004-auth-db-integration`
**Status:** Implemented
**Spec:** /specs/004-auth-db-integration/spec.md

## **Summary**

The goal was to integrate the Better Auth framework into the RAG eBook platform to provide secure user accounts and persistent chat history. The implementation ensures that every chat interaction is authenticated, private, and stored in a local PostgreSQL database while maintaining high performance for the AI agents.

## **Technical Context**

*   **Backend Stack**: Python 3.12, FastAPI, SQLModel (SQLAlchemy 2.0 based), Uvicorn.
*   **Auth Server Stack**: Node.js, Express, Better Auth v1, PostgreSQL.
*   **Frontend Stack**: React 19, Docusaurus 3.x, `better-auth/react`.
*   **Security Protocol**: Stateless JWT verification with RS256 using remote JWKS discovery.
*   **Data Layer**: PostgreSQL with connection pooling for concurrent RAG requests.

---

## **Project Architecture (Final)**

### **1. Source Code Organization**

```
ai-rag-ebook-platform/
├── auth-server/           # Central Identity Service
│   └── src/auth.ts        # Better Auth Config (JWT Plugin)
├── backend/               # AI & History Service
│   ├── src/
│   │   ├── middleware/    # Security layer (stateless JWT decoding)
│   │   ├── dependencies/  # FastAPI Route Guards
│   │   ├── services/      # Business Logic (User/Conv/Msg)
│   │   └── agents/        # RAG Agent (top_k=3 limitation)
│   └── logs/              # Production log files
└── frontend/              # Web Interface
    └── src/
        ├── components/    # ChatWidget, SignUpForm, Login
        ├── contexts/      # AuthContext (Identity state)
        └── services/      # agentClient.ts (Bearer injection)
```

---

## **Implementation strategy**

### **High-Level Flow**

1.  **Identity Creation**: Users register on the frontend, which communicates with the `auth-server`.
2.  **Token Issuance**: The auth server issues a cryptographically signed JWT.
3.  **Secure Request**: The frontend sends the JWT in the `Authorization: Bearer` header to the backend.
4.  **Verification**: The backend `JWTBearer` middleware verifies the token integrity using the auth server's JWKS.
5.  **Context Scoping**: The request is assigned a `user_id`, ensuring all subsequent database operations are scoped to that specific user.
6.  **AI Interaction**: The agent generates a response citing sources; both the message and sources are persisted to history.

---

## **Phase Overview**

### **Phase 1: Setup & Environment**
*   Configuration of triple-service communication.
*   Setup of production-ready logger for auth and database events.

### **Phase 2: Data Modeling**
*   Creation of `User`, `Conversation`, and `Message` models using SQLModel.
*   Mapping IDs as strings to perfectly align with Better Auth's random string identifiers.

### **Phase 3: The Security Layer**
*   Implementation of the `JWTBearer` middleware.
*   Discovery of public keys at `/api/auth/jwks` for stateless validation.
*   Strict enforcement of authentication (removal of all anonymous modes).

### **Phase 4: History persistence**
*   Async services for handling concurrent database writes.
*   Automatic syncing of user profiles from the JWT payload to the local `User` table.

### **Phase 5: User Interface Integration**
*   Integration of `better-auth/react` hooks into the frontend.
*   Building the Signup and Login components.
*   Implementing conditional UI states (e.g., hiding chat input for guest users).

### **Phase 6: Content Quality & Formatting**
*   Limiting RAG retrieval to the top 3 results for educational clarity.
*   Implementing Markdown support (bold, italics, tables) in the chat interface.

### **Phase 7: Production Hardening**
*   CORS origin restriction based on environment variables.
*   Hiding sensitive security data from logs.
*   Optimizing database pooling for high load.

---

## **Complexity Tracking**

| Challenge | Solution | Rationale |
| :--- | :--- | :--- |
| **ID Mismatches** | Standardized on `String` IDs | UUID conversion fails for Better Auth's base62 random strings. |
| **Stateless Validation** | JWKS Caching | Prevents calling the auth server on every single API request. |
| **Rich Text Rendering** | React Markdown + CSS | Ensures AI tables and code snippets look premium in chat. |
| **Response Quality** | Restricted top_k | Reducing from 8 to 3 sources significantly improves answer precision. |

---

## **Success Metrics**

*   **Latency**: JWT verification overhead < 5ms (post-cache).
*   **Security**: ZERO instances of data leakage between user conversation logs.
*   **Engagement**: Support for all standard Markdown formatting in AI responses.
