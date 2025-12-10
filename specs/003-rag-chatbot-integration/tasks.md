---
description: "Task list for RAG Chatbot integration (Docsourous-style floating widget)"
---

# Tasks: RAG Chatbot Integration

**Input**: `/specs/003-rag-chatbot-integration/plan.md`  
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/  

**Tests**: Include backend/frontend verification tasks for agent logic, session handling, and widget UX  

**Organization**: Tasks grouped by user story for independent implementation  

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel  
- **[Story]**: Maps to specific user story (e.g., US1: Frontend Widget, US2: Backend Endpoints, US3: Agent Logic)  

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Initialize project structure and basic dependencies  

- [x] T001 Check project structure per implementation plan (backend/src/, frontend/src/, tests/)  
- [x] T002 Initialize frontend project with React/TypeScript and Docusaurus dependencies  
- [x] T003 Initialize backend project with FastAPI, Python 3.12, and dependency management  
- [x] T004 Configure linting, formatting, and pre-commit hooks for backend and frontend  

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before any user story implementation  

- [x] T005 Define session and chat message models (`ConversationSession`, `ChatMessage`) in backend/src/models/session.py  
- [x] T006 Configure CORS, environment variables, and API key management  
- [x] T007 Setup basic logging framework for backend and frontend  

**Checkpoint**: Foundation ready - all user stories can now start  


## Phase 3: User Story 1 - Frontend Widget (Priority: P1) 🎯 MVP

**Goal**: Implement Docsourous-style floating chatbot with collapsible chat window

**Independent Test**: Open/close widget, send test messages, observe typing indicator

### Implementation

- [x] T010 [US1] Create ChatWidget component in frontend/src/components/ChatWidget/index.tsx
- [x] T011 [US1] Add FAB button and toggle functionality for ChatWindow
- [x] T012 [US1] Implement ChatWindow with message list, input box, send button, typing indicator in frontend/src/components/ChatWidget/ChatWindow/index.tsx
- [x] T013 [US1] Implement MessageBubble component for user/agent messages and citations in frontend/src/components/ChatWidget/MessageBubble/index.tsx
- [x] T014 [US1] Create TypingIndicator component in frontend/src/components/ChatWidget/TypingIndicator/index.tsx
- [x] T015 [US1] Implement agentClient service to call `/agents/run` with session_id, current_page, highlighted_text in frontend/src/services/agentClient.ts
- [x] T016 [US1] Integrate ChatWidget into Docusaurus layout (footer/global theme) using Root theme component

**Testing**

- [ ] T017 [US1] Verify widget renders and toggles open/close
- [ ] T018 [US1] Verify typing indicator appears on send
- [ ] T019 [US1] Test sending sample messages and rendering responses  

## Phase 4: User Story 2 - Backend Endpoints (Priority: P1)

**Goal**: Implement `/agents/run` endpoint, handle requests for triage, summarizer, and RAG agents  

**Independent Test**: POST `/agents/run` returns proper JSON with agent_used and sources  

### Implementation

- [x] T020 [US2] Create AgentRequest and AgentResponse models in backend/src/models/api_routes.py  
- [x] T021 [US2] Implement `POST /agents/run` in backend/src/routers/agent_router.py  
- [x] T022 [US2] Add input validation, error handling, and session_id handling  
- [x] T023 [US2] Configure logging of agent decisions without storing PII  
- [x] T024 [US2] Ensure CORS allows frontend origin only  

**Testing**

- [x] T025 [US2] Test endpoint with triage agent requests  
- [x] T026 [US2] Test endpoint with summarizer requests and highlighted_text  
- [x] T027 [US2] Test endpoint with RAG requests including current_page context  


## Phase 5: User Story 3 - Agent Behavior & Handoff Logic (Priority: P1)

**Goal**: Implement triage → RAG handoff and summarizer logic  

**Independent Test**: Triage labels correctly, RAG retrieves prioritized chunks, summarizer returns concise summaries  

### Implementation

- [x] T028 [US3] Implement triage agent in backend/src/agents/triage_agent.py  
- [x] T029 [US3] Implement RAG agent in backend/src/agents/rag_agent.py  
- [x] T030 [US3] Implement Summarizer agent in backend/src/agents/summarizer_agent.py  
- [x] T031 [US3] Integrate retriever service in backend/src/services/retriever.py  
- [x] T032 [US3] Add handoff logic from triage → RAG based on query type  

**Testing**

- [x] T033 [US3] Validate triage classification on test queries  
- [x] T034 [US3] Validate RAG retrieval prioritizes highlighted → current page → top 3 global chunks  
- [x] T035 [US3] Validate summarizer agent outputs concise summaries  


## Phase 6: User Story 4 - Sessions & Conversation History (Priority: P2)

**Goal**: Track per-session conversation with session_id, display sources in UI  

**Independent Test**: Conversation persists within a browser session  

- [x] T036 [US4] Implement in-memory or sessionStorage session tracking in frontend  
- [x] T037 [US4] Ensure session_id is sent with every agent request  
- [x] T038 [US4] Return agent_used and sources to frontend for citation display  
- [x] T039 [US4] Optional: prepare Neon DB persistence for future  

**Testing**

- [x] T040 [US4] Verify session survives widget close/open and page scroll  
- [x] T041 [US4] Verify sources display correctly for RAG responses  


## Phase 7: User Story 5 - UX & Edge Cases (Priority: P2)

**Goal**: Improve widget usability, validate inputs, handle errors gracefully  

**Independent Test**: Widget handles empty queries, backend errors, and retry correctly  

- [x] T042 [US5] Block empty/whitespace queries in frontend  
- [x] T043 [US5] Debounce send button and queue requests  
- [x] T044 [US5] Retry transient backend errors automatically  
- [x] T045 [US5] Display friendly error messages when agent/backend fails  
- [x] T046 [US5] Add “View sources” link to open chapter/highlighted text  

**Testing**

- [x] T047 [US5] Simulate backend failure and verify error handling  
- [x] T048 [US5] Verify highlighted-text summarization works end-to-end  


## Phase 8: QA, Performance & Security (Priority: P1)

**Goal**: Test correctness, performance (<5s median), and secure deployment  

- [x] T049 [US6] Backend unit tests for triage, RAG, summarizer, and retriever logic  
- [x] T050 [US6] Frontend tests for component rendering and integration with mocked backend  
- [x] T051 [US6] Performance tests for latency < 5s for median queries  
- [x] T052 [US6] Verify API keys not exposed in frontend bundle  
- [x] T053 [US6] Security checks: CORS, logging, input validation  


## Phase 9: Deployment & Rollout (Priority: P1)

**Goal**: Deploy backend and integrate widget into live book site  

- [x] T054 [US7] Build Docker image for backend  
- [x] T055 [US7] Deploy backend to Railway with env vars (GOOGLE_API_KEY, QDRANT_ENDPOINT, QDRANT_API_KEY)  
- [x] T056 [US7] Integrate widget script into Docusaurus global layout  
- [x] T057 [US7] Smoke test: triage, RAG handoff, summarize flows  
- [x] T058 [US7] Monitor logs and metrics for errors/latency  

---

## Phase 10: Polish & Cross-Cutting Concerns

- [x] T059 [P] Update documentation in specs/ and docs/  
- [x] T060 Refactor backend/frontend code for clarity and maintainability  
- [x] T061 [P] Add additional unit/integration tests as needed  
- [x] T062 Optimize performance across all user stories  
- [x] T063 Security hardening final review  
- [x] T064 Validate quickstart.md instructions for developers  


## Dependencies & Execution Order

- Setup → Foundational → User Stories (US1–US5) → QA/Polish → Deployment  
- User Stories can run in parallel once foundational tasks complete  
- Within each story: models → services → endpoints → frontend → integration → testing  
- Checkpoints after each story ensure independent testability  

