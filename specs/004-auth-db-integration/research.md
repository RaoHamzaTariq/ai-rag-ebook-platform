# **Research: BetterAuth Integration with FastAPI and PostgreSQL**

## **Decision: Authentication Strategy (Stateless JWT)**

**Rationale:**
We selected a **Stateless JWT with JWKS validation** strategy. This allows the FastAPI backend to verify identities without maintaining its own user sessions or making a database call for every request. By fetching the Public Keys from the `auth-server`'s `/api/auth/jwks` endpoint, the backend can cryptographically prove the token was issued by our identity provider.

**Alternatives Considered:**
*   **Session Cookies**: Rejected because it requires shared memory/sessions between Node.js and Python or a common Redis store, which adds infrastructure complexity.
*   **Opaque Tokens**: Rejected because it requires the backend to call the auth server on every request ("introspection"), which would hurt latency.

---

## **Decision: ID Management (String-based identifiers)**

**Rationale:**
Better Auth v1 generates random string identifiers (e.g., `N1pk9L...`) rather than standard version 4 UUIDs. To ensure binary compatibility and prevent "badly formed hexadecimal UUID string" errors, we explicitly defined all ID fields in our `Message`, `Conversation`, and `User` tables as `String`.

**Impact:**
This ensures that the `user_id` provided in the JWT sub-claim maps perfectly to the foreign key in our chat history tables without requiring manual casting or conversion logic.

---

## **Decision: Authentication Middleware Pattern**

**Rationale:**
We implemented a custom `JWTBearer` class that inherits from FastAPI's security utilities. This allows for a clean, dependency-injection-based protection system. Using a middleware/dependency pattern ensures that we can protect the `/agents/run` endpoint with a single line of code without cluttering the business logic of our RAG agents.

**Security Feature:**
The middleware includes a robust 5-minute caching mechanism for the JWKS, ensuring that if the auth server is temporarily under load, the backend can still verify current users using the cached public keys.

---

## **Decision: RAG Retrieval Constraints (top_k=3)**

**Rationale:**
Research into user response quality showed that providing too many sources (previously 8) led to diluted answers and cluttered UI. By restricting retrieval to the **top 3 most relevant resources**, we force the AI to synthesize the most important textbook data, leading to "higher density" educational responses.

**Relevance Tuning:**
We raised the `score_threshold` to `0.70` to ensure that only high-quality chunks are used in generating answers, eliminating filler text.

---

## **Decision: Rich Text Display Format**

**Rationale:**
Educational content often involves structured data that plain text cannot convey effectively. We decided to use **Markdown** as the communication standard between the AI and the frontend. By integrating `react-markdown` and `remark-gfm`, we enabled support for tables, bold emphasis, and lists.

---

## **Performance Optimizations**

*   **JWKS Caching**: Prevents network overhead for token validation.
*   **Database Indexing**: Explicitly added indexes on `(user_id, timestamp)` to ensure that history retrieval remains fast even as users accumulate thousands of messages.
*   **Connection Pooling**: Configured SQLAlchemy/SQLModel `QueuePool` to handle the bursty nature of AI chat traffic efficiently.

---

## **Research Summary Findings**

| Feature | Decision | Key Reason |
| :--- | :--- | :--- |
| **Identity Provider** | Better Auth v1 | Framework-agnostic and simplifies Node./Python interop. |
| **Token Format** | JWT (RS256) | Standardized, secure, and supports stateless validation. |
| **History Storage** | PostgreSQL | SQLModel provided the best balance of speed and schema safety. |
| **ID Type** | String (Varchar) | Compatibility with existing Better Auth string IDs. |
| **Response Format** | GFM Markdown | Allows high-quality table and rich-text rendering. |
