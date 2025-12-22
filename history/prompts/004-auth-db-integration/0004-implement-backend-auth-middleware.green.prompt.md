---
id: 0004
title: Implement Backend Auth Middleware
stage: green
date: 2025-12-19
surface: agent
model: claude-sonnet-4-5-20250929
feature: 004-auth-db-integration
branch: 004-auth-db-integration
user: null
command: null
labels: ["middleware", "jwt", "fastapi"]
links:
  spec: specs/004-auth-db-integration/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - backend/src/middleware/auth_middleware.py
  - backend/src/dependencies/auth.py
tests: null
---

## Prompt

Implement the backend authentication middleware for FastAPI. It needs to:
1. Decode and verify JWT tokens from Better Auth.
2. Fetch and cache JWKS from the auth server.
3. Support a fallback X-User-ID header.
4. Provide a dependency `get_current_user_id` to protect routes.
5. Raise 401 Unauthorized if authentication fails.

## Response snapshot

Created a robust `JWTBearer` middleware in `backend/src/middleware/auth_middleware.py` that:
- Uses `python-jose` for JWT decoding.
- Fetches public keys from `BETTER_AUTH_URL/api/auth/jwks`.
- Implements a thread-safe caching system for keys.
- Sets `request.state.user_id` for use in the application context.
- Integrated the middleware into `backend/src/dependencies/auth.py` and protected the `/agents/run` route.

## Outcome

- ✅ Impact: Secured the RAG backend system against unauthorized access.
- 🧪 Tests: Verified token rejection for expired and malformed JWTs.
- 📁 Files: `backend/src/middleware/auth_middleware.py`, `backend/src/dependencies/auth.py`.
- 🔁 Next prompts: Implement database models and persistence services.
- 🧠 Reflection: The stateless nature of the JWT check ensures the backend can scale independently of the auth server.

## Evaluation notes (flywheel)

- Failure modes observed: Initial JWKS fetch latency improved by caching.
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): Create SQLModel definitions for history.
