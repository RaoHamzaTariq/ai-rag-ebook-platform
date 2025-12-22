# Feature Specification: Better Auth + FastAPI + PostgreSQL Integration

**Feature Branch**: `004-auth-db-integration`
**Created**: 2025-12-11
**Status**: Implemented
**Updated**: 2025-12-22

## Feature Overview & Goals

The purpose of this feature is to restrict chatbot access to authenticated users, persist conversation history linked to user accounts, and provide secure access to RAG (Retrieval-Augmented Generation) chatbot features. Better Auth is used for identity management across three integrated services:
1. **Auth Server**: A Node.js environment managing the core authentication logic and database interaction with the Better Auth library.
2. **FastAPI Backend**: Verifies the identity of incoming requests using shared JWT verification keys (JWKS) and manages the RAG pipeline and history persistence.
3. **Frontend**: A Docusaurus React application providing the user interface for chatting and account management.

The system emphasizes high-quality responses, data isolation by user ID, and a premium interactive experience with rich text rendering.

## User Scenarios & Testing

### User Story 1 - User Authentication and Session Management (Priority: P1)

User needs to sign up, sign in, and maintain a persistent session across application usage. The user should be able to securely authenticate and have their session managed automatically via one of the project's dedicated auth flows.

**Why this priority**: Foundational requirement - without authentication, users cannot access protected chatbot features or have their conversations persisted.

**Acceptance Scenarios**:
1. **Given** user is not authenticated, **When** user signs up with valid credentials on the signup page, **Then** user account is created and session is established immediately.
2. **Given** user has an account, **When** user signs in via the login form, **Then** a JWT/session is established and the user is redirected to the dashboard/chatbot.
3. **Given** user has an active session, **When** user returns to application, **Then** `authClient.getSession()` reveals the user remains authenticated without requiring a re-login.

---

### User Story 2 - Authenticated Chat Access (Priority: P1)

User needs to access the RAG chatbot functionality only after successful authentication. The system must verify user identity (via JWT or X-User-ID) before allowing any calls to the AI agents.

**Why this priority**: Primary business value - ensuring only authenticated users can access the LLM-powered features.

**Acceptance Scenarios**:
1. **Given** user is not authenticated, **When** user sees the chat widget, **Then** an "Authentication Required" prompt and login link are displayed instead of the chat input.
2. **Given** user is authenticated, **When** user sends a query, **Then** the `agentClient` automatically injects the Bearer token into headers and the request succeeds.
3. **Given** an invalid or missing token, **When** a request hits `/agents/run`, **Then** the backend raises an `HTTP 401 Unauthorized` exception.

---

### User Story 3 - PostgreSQL Persistence for Conversations (Priority: P1)

User conversations and messages must be securely stored in the PostgreSQL database, linked to user IDs to ensure that data is not lost between sessions.

**Why this priority**: Provides continuity and enables the AI to recall context in future updates, while allowing users to review their history.

**Acceptance Scenarios**:
1. **Given** user is authenticated, **When** user sends a message, **Then** the message is saved to the `Message` table with the correct `conversation_id` and `user_id`.
2. **Given** the agent responds, **When** the response is generated, **Then** it is saved as an `assistant` role message with all retrieved RAG sources stored in JSON.
3. **Given** a user ID, **When** querying conversations, **Then** only that user's specific history is returned (data isolation).

---

### User Story 4 - High-Relevance RAG and Rich Formatting (Priority: P2)

Authenticated users should receive precise, highly relevant answers formatted for readability, including tables and bold text.

**Why this priority**: Differentiates the product by providing cleaner, more focused educational content from the Physical AI textbook.

**Acceptance Scenarios**:
1. **Given** a factual query about the textbook, **When** RAG processes the request, **Then** exactly the top 3 most relevant sources are retrieved.
2. **Given** the agent provides a structured response, **When** the message is displayed, **Then** markdown elements (tables, bold, italic) are rendered correctly using `react-markdown`.
3. **Given** a source reference, **When** clicked in the UI, **Then** the user is directed to the correct documentation slug and chapter.

---

### User Story 5 - Privacy and Data Isolation (Priority: P2)

Users must have confidence that their data is isolated and handled securely, with no possibility of seeing other users' chat logs.

**Why this priority**: Crucial for security compliance and user trust.

**Acceptance Scenarios**:
1. **Given** User A and User B, **When** User A queries their history, **Then** no messages from User B are visible.
2. **Given** a request with an `X-User-ID` header, **When** validated by the middleware, **Then** the ID must exist in the database and belong to the active session if providing a JWT.
3. **Given** no authentication is found, **When** trying to create a conversation, **Then** the `ConversationService` rejects the operation.

---

### Edge Cases

- **Missing JWT**: The system falls back to a verified `X-User-ID` provided by the auth state but raises 401 if both are missing.
- **JWKS Failure**: The middleware caches public keys for 5 minutes; if the auth server is down, the current session remains valid until the cache expires.
- **Malformed IDs**: Using String IDs instead of UUIDs prevents common conversion errors with Better Auth's base62 ID format.
- **No Relevance**: If no chunks pass the high similarity threshold (0.70), the agent provides a helpful answer but notes the lack of specific textbook context.

## Requirements

### Functional Requirements

- **FR-001**: System MUST support user registration with email/password via Better Auth and a dedicated signup form.
- **FR-002**: System MUST support persistent sessions using `better-auth/react` and `jwtClient`.
- **FR-003**: System MUST provide a protected `/agents/run` endpoint requiring valid authentication.
- **FR-004**: System MUST verify tokens in FastAPI middleware using a JWKS lookup from the auth server.
- **FR-005**: System MUST store user records in a local `User` table for metadata and sync.
- **FR-006**: System MUST persist conversation threads and individual messages with timestamps.
- **FR-007**: System MUST store RAG sources, including slugs and snippets, within a JSONB-compatible field.
- **FR-008**: System MUST provide an API to retrieve all messages for a specific conversation ID.
- **FR-009**: System MUST render markdown responses on the frontend to support tables and rich text.
- **FR-010**: System MUST enforce CORS to restricted origins in production environments.
- **FR-011**: System MUST limit RAG retrieval to exactly the top 3 sources to maintain response focus.

### Key Entities

- **User**: (id: string, email: string, name: string) - Linked directly to Better Auth user entity.
- **Conversation**: (id: string, user_id: string, title: string) - Represents a specific chat thread.
- **Message**: (id: string, conversation_id: string, role: string, content: string, sources: JSON) - Individual interactions.
- **RAGSource**: Metadata including chapter number, page number, and snippet.

## Success Criteria

### Measurable Outcomes

- **SC-001**: 100% of user queries from authenticated sessions are correctly attributed to the user in the database.
- **SC-002**: JWT validation time remains below 50ms after the initial JWKS fetch.
- **SC-003**: Chat history loads in the UI in under 500ms following an authenticated request.
- **SC-004**: Unauthenticated users are consistently blocked from API access with 401 responses.
- **SC-005**: RAG responses citing at least 1 source have 100% correct links to the Docusaurus documentation platform.
- **SC-006**: Table formatting in agent responses renders with zero visual artifacts on both mobile and desktop.
