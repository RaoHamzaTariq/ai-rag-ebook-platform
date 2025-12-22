# **Tasks: BetterAuth Integration with PostgreSQL for Chat History**

**Feature:** Authenticated RAG Chatbot with History persistence
**Release Date:** 2025-12-23
**Spec:** /specs/004-auth-db-integration/spec.md
**Plan:** /specs/004-auth-db-integration/plan.md

---

## **Phase 1: Setup / Foundational (Completed)**

**Goal:**
Establish the multi-service architecture and core configuration for authentication and logging.

**Independent Test Criteria:**
✔ Auth-server, Backend, and Frontend are communicating
✔ Environment variables for database and auth URLs are set correctly
✔ Logging system is active for auth and database events

**Tasks:**
* [X] T001 Create project structure (auth-server, backend, frontend subdirectories)
* [X] T002 Configure environment variables (NEXT_PUBLIC_BETTER_AUTH_URL, DATABASE_URL)
* [X] T003 Initialize basic FastAPI app with logging configuration
* [X] T004 Setup separate log files for general application and security errors

## **Phase 2: Database Schema & Connectivity (Completed)**

**Goal:**
Build a persistent storage layer compatible with the Better Auth ID system.

**Independent Test Criteria:**
✔ PostgreSQL tables created for Users, Conversations, and Messages
✔ String-based IDs used to match Better Auth's random strings
✔ Successful connection from FastAPI to the SQL database

**Tasks:**
* [X] T005 Define the `User` model using SQLModel (matching Better Auth fields)
* [X] T006 Define the `Conversation` and `Message` models with foreign key constraints
* [X] T007 Implement the `init_db` logic to auto-create tables on startup
* [X] T008 Add performance indexes for `user_id` and `timestamp` fields
* [X] T009 Verify database migrations and connection pooling settings

## **Phase 3: Backend Authentication Middleware (Completed)**

**Goal:**
Enable secure, stateless token verification for all protected API routes.

**Independent Test Criteria:**
✔ Backend correctly fetches and caches JWKS from the auth server
✔ Bearer tokens in headers are decoded and validated
✔ Requests without valid identification return 401 Unauthorized

**Tasks:**
* [X] T010 Implement `JWTBearer` middleware in `auth_middleware.py`
* [X] T011 Add JWKS caching logic (5-minute refresh interval)
* [X] T012 Support `X-User-ID` as a verified fallback for robust sessions
* [X] T013 Create the `get_current_user_id` dependency for route protection
* [X] T014 Remove all anonymous/dummy user fallbacks from the security layer

## **Phase 4: Data Services & Persistence (Completed)**

**Goal:**
Handle the business logic for storing and retrieving user interactons.

**Independent Test Criteria:**
✔ User messages and AI responses are saved to the database
✔ Conversations are correctly grouped and listed per user
✔ Retrieval of chat history works without data leakage between users

**Tasks:**
* [X] T015 Implement `UserService` for syncing Better Auth data to local DB
* [X] T016 Implement `ConversationService` for creating and listing chat threads
* [X] T017 Implement `MessageService` with JSON support for RAG source storage
* [X] T018 Integrate history persistence into the `/agents/run` endpoint
* [X] T019 Ensure agents can successfully save multi-source citations in JSONB format

## **Phase 5: Frontend Authentication UI (Completed)**

**Goal:**
Integrate the Better Auth client and provide a user-friendly registration flow.

**Independent Test Criteria:**
✔ Users can successfully sign up and log in via the web interface
✔ Authentication state is maintained across browser refreshes
✔ Unauthenticated users see proper prompts in the chat widget

**Tasks:**
* [X] T020 Install and configure `better-auth/react` client
* [X] T021 Implement the `AuthContext` provider for global state management
* [X] T022 Build the Signup form with real-time validation
* [X] T023 Update the `ChatWindow` component to conditionally render input fields
* [X] T024 Ensure `agentClient.ts` fetches and sends the JWT Bearer token

## **Phase 6: Rich UI & RAG Refinement (Completed)**

**Goal:**
Polish the chatbot experience with high-quality responses and clear formatting.

**Independent Test Criteria:**
✔ Chatbot responses support Bold, Italics, and Tables
✔ Only the top 3 most relevant textbook resources are retrieved
✔ Source links correctly route to the internal documentation slugs

**Tasks:**
* [X] T025 Install `react-markdown` and `remark-gfm` in the frontend
* [X] T026 Update `MessageBubble` to render Markdown content instead of plain text
* [X] T027 Refine the `Retriever` service to limit results to `top_k=3`
* [X] T028 Enhance `rag_agent.py` prompts for better citation accuracy
* [X] T029 Implement table wrappers for responsive UI on mobile devices

## **Phase 7: Production Readiness (Completed)**

**Goal:**
Harden the system for real-world deployment.

**Independent Test Criteria:**
✔ CORS is restricted to production domains
✔ Debug information (like full JWTs) is not leaked to console
✔ System handles missing environment variables gracefully

**Tasks:**
* [X] T030 Implement production-safe CORS middleware settings
* [X] T031 Clean up all debug `print` statements from the auth layer
* [X] T032 Configure Uvicorn to run with stable settings (no reload in prod)
* [X] T033 Verify robust error logging for 401 and 500 status codes
* [X] T034 Perform end-to-end audit of data isolation between user accounts

---

## **Dependencies & Ordering**

*   **Setup** -> **Database** -> **Auth Middleware** -> **Services** -> **Frontend Integration** -> **UI Polish** -> **Prod Hardening**
*   This project strictly follows the stateless JWT pattern for scalability.
