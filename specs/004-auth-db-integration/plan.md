# **Implementation Plan: BetterAuth Integration with FastAPI Backend and Neon PostgreSQL**

**Branch:** 004-auth-db-integration
**Date:** 2025-12-17
**Spec:** [@/specs/004-auth-db-integration/spec.md]
**Input:** Feature spec for integrating BetterAuth authentication with FastAPI backend and Neon PostgreSQL for user accounts and chat history storage.

## **Summary**

Integrate BetterAuth authentication with the existing RAG chatbot system to provide **user accounts** and **persistent chat history**.

* Secures all chat interactions with JWT/Bearer token authentication.
* Stores conversation history in **Neon PostgreSQL**.
* Maintains **existing RAG agent functionality** and Qdrant search.
* Implements **user-specific data isolation**.

## **Technical Context**

* **Languages/Versions:** Python 3.11, TypeScript/JavaScript (frontend)
* **Primary Dependencies:** FastAPI, BetterAuth (frontend JWT/Bearer plugin), asyncpg, SQLAlchemy/SQLModel, Neon PostgreSQL
* **Storage:** Neon PostgreSQL database
* **Testing:** pytest (backend), Jest (frontend)
* **Target Platform:** Web app (Linux backend, browser frontend)
* **Performance Goals:** <200ms p95 for authenticated requests, support 1000 concurrent users
* **Constraints:** JWT/Bearer token validation <50ms, secure session management, GDPR compliant
* **Scale/Scope:** 10k users, 1M chat messages, multi-tenant isolation

## **Constitution Check**

* **GATE:** Must pass before Phase 0 research; recheck after Phase 1 design.
* **Security:** JWT/Bearer validation + DB security implemented per standards
* **Performance:** All DB and auth operations async
* **Data Privacy:** User data isolated per GDPR
* **Architecture:** Clear separation of concerns maintained


## **Project Structure**

### **Documentation**

```
specs/004-auth-db-integration/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
└── tasks.md             # Phase 2 output
```

### **Source Code**

```
backend/
├── src/
│   ├── models/
│   │   ├── user.py
│   │   ├── conversation.py
│   │   └── message.py
│   ├── services/
│   │   ├── auth.py
│   │   ├── user_service.py
│   │   ├── conversation_service.py
│   │   └── message_service.py
│   ├── middleware/
│   │   └── auth_middleware.py
│   ├── api/
│   │   ├── auth.py
│   │   └── conversations.py
│   └── config/
│       └── database.py
└── tests/

frontend/
├── src/
│   ├── components/
│   │   ├── auth/
│   │   ├── chat/
│   │   └── history/
│   ├── services/
│   │   ├── authClient.ts
│   │   └── conversationClient.ts
│   └── contexts/
│       └── AuthContext.tsx
└── tests/
```

**Decision:** Maintain separation between frontend and backend while enabling proper auth flow via JWT/Bearer tokens.

## **Complexity Tracking**

| Violation                   | Why Needed                                      | Alternative Rejected                       |
| --------------------------- | ----------------------------------------------- | ------------------------------------------ |
| JWT Validation Middleware   | Required to securely validate BetterAuth tokens | Direct session passing is insecure         |
| Database Connection Pooling | Required for high concurrency                   | Single connections would exhaust resources |


## **Implementation Strategy**

### **High-Level Flow**

1. **Frontend**: BetterAuth login/signup → receives JWT/Bearer token.
2. **API Requests**: Token sent in Authorization header.
3. **FastAPI Backend**: Validates token against JWKS (JWT) or Bearer introspection.
4. **RAG Agent**: Uses Qdrant to fetch embeddings & generate answers.
5. **NeonDB**: Stores user messages, agent responses, and conversation sessions.


### **Phase Breakdown**

1. **Phase 1: Setup / Foundational**

   * Project structure, env vars, logging, middleware scaffold
   * Install BetterAuth client & backend dependencies

2. **Phase 2: Database (Neon)**

   * User, Conversation, Message models
   * Async DB pool
   * Migrations, indexes, testing

3. **Phase 3: Backend Auth Middleware**

   * JWT/Bearer verification middleware
   * JWKS fetching & caching
   * Authenticated user dependency
   * Protect AI endpoints

4. **Phase 4: Backend Chat Persistence**

   * Save user messages and AI responses
   * Services: UserService, ConversationService, MessageService
   * Conversation history endpoints

5. **Phase 5: Frontend Auth Integration**

   * Integrate BetterAuth client (JWT/Bearer)
   * Login/signup UI & protected routes
   * Include token in API calls

6. **Phase 6: Frontend Conversation History UI**

   * Conversation list & viewer
   * Chat window & message bubble updates
   * Pagination, search/filter

7. **Phase 7: UX & Flow**

   * Full chat + auth flows
   * Session persistence
   * Conversation switching
   * Loading states & error handling

8. **Phase 8: Testing**

   * Backend: unit & integration tests for auth, protected endpoints, services
   * Frontend: UI tests for login, chat widget, history

9. **Phase 9: Deployment & Monitoring**

   * Prod env vars & DB migrations
   * Monitoring auth + chat endpoints
   * Logging & performance verification

### **Dependencies**

* Phase 2 → Phase 3 → Phase 4 → Phase 5 → Phase 6 → Phase 7 → Phase 8 → Phase 9
* `[P]` tasks can run in parallel

