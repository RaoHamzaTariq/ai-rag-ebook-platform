# **Tasks: BetterAuth Integration with Neon PostgreSQL for Chat History**

**Feature:** Add authentication using BetterAuth (frontend), protect AI chat endpoints, and store user accounts and conversation history in Neon PostgreSQL
**Date:** 2025‑12‑13
**Spec:** /specs/004‑auth‑db‑integration/spec.md
**Plan:** /specs/004‑auth‑db‑integration/plan.md

---

## **Phase 1: Setup / Foundational**

**Goal:**
Set up project structure, env vars, and core config for auth + database.

**Independent Test Criteria:**
✔ Project folder structure ready
✔ Env vars for BetterAuth JWT/Bearer and Neon are set
✔ Logging + middleware scaffold present

**Tasks:**

* [X] T001 Create project structure per implementation plan
* [X] T002 Set up BetterAuth environment variables in frontend and backend
* [X] T003 Configure Neon PostgreSQL connection in backend
* [X] T004 Initialize authentication middleware scaffolding in backend
* [X] T005 Set up logging config for auth events
* [X] T006 [P] Install BetterAuth client deps (frontend)
* [X] T007 [P] Install backend deps (asyncpg, SQLModel)
* [X] T008 Create config files for auth & DB


## **Phase 2: Database (Neon)**

**Goal:**
Build DB schema for users, conversations, messages.

**Independent Test Criteria:**
✔ Tables created with proper keys
✔ Relationships set
✔ Indexes for performance

**Tasks:**

* [X] T009 Create `User` model (id, email, etc.)
* [X] T010 Create `Conversation` model (id, user_id)
* [X] T011 Create `Message` model (id, content, sender, timestamp)
* [X] T012 [P] Set up async DB connection pool
* [X] T013 Create DB migration scripts
* [X] T014 Initialize DB on startup
* [X] T015 Add indexes on user_id, conversation_id
* [X] T016 Test DB connection & schema

## **Phase 3: Backend Auth Middleware**

**Goal:**
Enable FastAPI to *verify BetterAuth tokens* for protected routes.

**Independent Test Criteria:**
✔ Tokens from BetterAuth JWT/Bearer plugin are verified
✔ Invalid tokens rejected
✔ Authenticated user available to endpoints

> **Important:** BetterAuth provides either a *Bearer plugin* or a *JWT plugin + JWKS endpoint* that your backend can use to validate tokens. Session cookies alone won’t be usable unless you fetch a JWT via `/api/auth/token` or the Bearer plugin. ([Better Auth][1])

**Tasks:**

* [X] T017 Create JWT/Bearer verification middleware
* [X] T018 Implement JWKS fetching & caching (if using JWT plugin)
* [X] T019 Create authenticated user dependency (`get_current_user`)
* [X] T020 Protect `/agents/run` with auth middleware
* [X] T021 Add error handling for unauthorized access
* [X] T022 Add utility functions for token introspection
* [X] T023 Test token verification with sample tokens

## **Phase 4: Backend Chat Persistence**

**Goal:**
Store user messages and agent responses with history.

**Independent Test Criteria:**
✔ User messages saved before AI run
✔ AI responses + sources saved
✔ History endpoints return correct data

**Tasks:**

* [X] T024 Save user message at `/agents/run`
* [X] T025 Save AI response + RAG source links
* [X] T026 Create `UserService` for user logic
* [X] T027 Create `ConversationService`
* [X] T028 Create `MessageService`
* [X] T029 Implement GET `/users/me`
* [X] T030 GET `/conversations` (list)
* [X] T031 GET `/conversations/{conv_id}`
* [X] T032 POST `/conversations/{conv_id}/messages`
* [X] T033 Ensure assoc with authenticated user
* [X] T034 Test chat persistence

---

## **Phase 5: Frontend Auth Integration**

**Goal:**
Integrate BetterAuth in frontend, enable login & secure chat requests.

**Independent Test Criteria:**
✔ Users can login/logout
✔ Tokens included in API calls
✔ Chat widget protected

> Use BetterAuth **JWT or Bearer plugin** on frontend to get a token your backend can verify, then send it as `Authorization: Bearer <token>` in requests.

**Tasks:**

* [X] T035 Install BetterAuth client deps
* [X] T036 Config `authClient` to retrieve Bearer/JWT tokens
* [X] T037 Create Login page & styles
* [X] T038 Create Signup page & styles
* [X] T039 Create Forgot Password page & styles
* [X] T040 Implement `AuthContext` provider
* [X] T041 Create login form w/ validation
* [X] T042 Create signup form w/ validation
* [X] T043 Add social login buttons
* [X] T044 Create `ProtectedRoute` for secured routes
* [X] T045 Create `PublicRoute`
* [X] T046 Implement redirect logic after login/signup
* [X] T047 Update API client to include `Authorization` header
* [X] T048 Restrict chat widget based on auth
* [X] T049 Implement session/token storage & refresh
* [X] T050 Navigation guards based on auth state
* [ ] T051 Test frontend auth

---

## **Phase 6: Frontend Conversation History UI**

**Goal:**
Show conversation history.

**Independent Test Criteria:**
✔ Users see their history
✔ Messages display correctly
✔ Sources from RAG responses shown

**Tasks:**

* [X] T052 Conversation list component
* [X] T053 Conversation viewer component
* [X] T054 Update ChatWindow to integrate history
* [X] T055 Update MessageBubble for RAG sources
* [X] T056 Add pagination
* [X] T057 Add search/filter
* [ ] T058 Test UI

## **Phase 7: UX & Flow**

**Goal:**
End‑to‑end auth and chat UX.

**Independent Test Criteria:**
✔ Auth + chat flows work
✔ Conversations switch smoothly

**Tasks:**

* [X] T059 Full chat flow (login → protected API → response)
* [X] T060 Persist session across refresh
* [X] T061 Create new conversations from UI
* [X] T062 Conversation switching
* [X] T063 Loading states
* [ ] T064 Test full flow
* [X] T065 Error handling

## **Phase 8: Testing**

**Goal:**
Add tests for backend auth + chat + frontend UI.

**Independent Test Criteria:**
✔ Auth middleware coverage
✔ Protected endpoints reject unauthorized
✔ UI works with auth

**Tasks:**

* [X] T066 Unit tests for auth middleware
* [X] T067 Integration tests for protected endpoints
* [X] T068 Unit tests for UserService
* [X] T069 Integration tests for conversation endpoints
* [X] T070 UI tests for login
* [X] T071 UI tests for chat widget
* [X] T072 UI tests for history
* [X] T073 Test error scenarios

## **Phase 9: Deployment & Monitoring**

**Goal:**
Prepare deployment with proper configs.

**Independent Test Criteria:**
✔ Env vars ready
✔ Migrations run
✔ Monitoring auth + chat endpoints

**Tasks:**

* [X] T074 Update prod env vars
* [X] T075 Deployment scripts + migrations
* [X] T076 Monitoring auth/chat
* [X] T077 Document deployment
* [X] T078 Test staging deploy
* [X] T079 Logging in production
* [X] T080 Verify performance metrics

## **Dependencies & Ordering**

* Phase 2 → Phase 3 → Phase 4 → Phase 5 → Phase 6 → Phase 7 → Phase 8 → Phase 9
* Tasks marked `[P]` can run in parallel
