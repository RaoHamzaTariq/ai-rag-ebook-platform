# **Research: BetterAuth Integration with FastAPI Backend and Neon PostgreSQL**

## **Decision: JWT Token Validation Approach**

**Rationale:**
We chose to use **JWT tokens with JWKS validation** for stateless authentication. This approach allows the FastAPI backend to verify tokens issued by BetterAuth without maintaining server‑side sessions or storing session state. After initial JWKS retrieval, public keys can be cached for performance, reducing overhead. This matches BetterAuth’s recommended pattern for external API authentication. ([Better Auth][1])

**Alternatives considered:**

* **Session‑based authentication** (frontend cookies) — easier but not reliable for backend API verification without custom logic.
* **OAuth2 with database token storage** — more complex, higher database load, unnecessary for this use case.

## **Decision: Database Schema Design**

**Rationale:**
Use **UUID primary keys** with explicit foreign key relationships between users, conversations, and messages to ensure data integrity and scalability. **JSONB fields** are used for RAG source metadata to allow flexible storage of embeddings and references.

**Alternatives considered:**

* **Auto‑increment integers** — easier but less secure and predictable.
* **Single flat table** — violates normalization, hampers efficient querying and scaling.

## **Decision: Authentication Middleware Pattern**

**Rationale:**
FastAPI middleware using a JWT bearer scheme cleanly separates authentication from your business logic. It allows protecting specific endpoints without modifying existing RAG agent flows. Middleware also simplifies applying token verification uniformly across routes.

**Alternatives considered:**

* **Decorator‑based authentication** — requires modifying many endpoints.
* **Manual token checks in each route** — repetitive and error‑prone.

## **Decision: BetterAuth Configuration for JWT**

**Rationale:**
BetterAuth supports a **JWT plugin** that provides both token issuance and a JWKS endpoint for public key discovery. This enables external API services (like your FastAPI backend) to verify tokens issued by BetterAuth without maintaining state. ([Better Auth][1])

**Alternatives considered:**

* **Custom JWT implementation** — more complex and risky.
* **Third‑party auth providers** — would require different integration patterns and more dependencies.


## **Decision: Async Database Operations**

**Rationale:**
Keeping database operations asynchronous using **asyncpg + SQLModel** preserves the non‑blocking performance of your existing RAG system. This is crucial for maintaining responsiveness when handling many concurrent chat requests.

**Alternatives considered:**

* **Synchronous DB operations** — blocks FastAPI’s event loop and harms performance.
* **Opening a new connection per request** — causes resource exhaustion.

## **Decision: Conversation History Architecture**

**Rationale:**
Storing conversations and messages in **separate but related tables** allows efficient querying, pagination, and filtering while preserving chat context. Each conversation is linked to a user, and messages reference their parent conversation.

**Alternatives considered:**

* **Single array field for messages** — difficult to query or paginate.
* **No conversation grouping** — loses context across sessions.

## **Security Considerations Researched**

* Token expiration and refresh behavior designed according to BetterAuth recommendations. ([Better Auth][1])
* SQL injection prevention through **parameterized queries** with SQLModel/asyncpg.
* CORS configuration for secure production environments.
* Considered secure cookie settings for session handling if using additional BetterAuth plugins.

## **Performance Optimizations Researched**

* **Connection pooling** for Neon PostgreSQL to handle many concurrent users.
* **JWKS caching** to reduce validation overhead — fetch once and reuse keys until rotation. ([Better Auth][1])
* Proper **indexing** on user_id and conversation_id for efficient message retrieval.
* **Pagination** strategies to efficiently handle large conversation histories.

---

## **Summary of Research Findings**

| Area                      | Decision                  | Key Reason                                  |
| ------------------------- | ------------------------- | ------------------------------------------- |
| Auth Strategy             | JWT via BetterAuth + JWKS | Stateless, backend verifiable tokens        |
| Schema Design             | UUID keys + relations     | Secure, scalable, query‑efficient           |
| Auth Middleware           | FastAPI middleware        | Clean integration, centralized verification |
| DB Operations             | Async                     | Non‑blocking, high concurrency              |
| Conversation Architecture | Separate tables           | Maintain context & efficient querying       |
