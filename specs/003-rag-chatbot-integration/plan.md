# Implementation Plan: RAG Chatbot Integration with Backend (Docsourous-style Floating Widget)

**Feature Branch**: `003-rag-chatbot-integration`
**Created**: 2025-12-09
**Status**: Draft
**Spec**: `specs/003-rag-chatbot-integration/spec.md`

## Summary

Integrate the existing RAG backend (Qdrant retriever + OpenAI/Google Gemini agents) with a Docsourous-style floating chatbot widget placed bottom-right on the book site. The widget must support (1) general questions handled directly by a **triage agent**, (2) context-heavy questions handed off to a **RAG agent** (prioritizing highlighted text and current page), and (3) summarization of user-selected text via a **summarizer agent**. Frontend calls the backend endpoints (`/agents/run`, `/rag/query`) with payloads containing `query`, `agent_type`, `current_page`, and `highlighted_text`. Deliver a secure, responsive, and testable integration.

## Technical Context

**Language/Version**: Frontend TypeScript (Docusaurus), Backend Python 3.12 (FastAPI)
**Primary Dependencies**: FastAPI, OpenAI Agents SDK (or equivalent), Qdrant-client, httpx/requests, langchain_text_splitters, React
**Storage**: Qdrant Cloud (vector store); ephemeral session state (in-memory/session storage in frontend)
**Testing**: pytest (backend), Jest + React Testing Library (frontend), manual acceptance tests for handoff flows
**Target Platform**: Web (Docsourous/Docusaurus pages hosted on Vercel), Backend on Railway (Docker)
**Project Type**: Full-stack web feature (frontend widget + backend agent endpoints)
**Performance Goals**: < 5s median response time for common queries; widget initial render < 250ms
**Constraints**: API keys must remain server-side; RAG retrieval prioritizes page/highlighted context; mobile-friendly UI
**Scale/Scope**: Single-book deployment initially; supports multiple concurrent users (50+)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

* **I. Accuracy & Truthfulness** — Agents must cite sources from the book when answers reference content.
* **II. Consistency & Clarity** — Single conversational tone and consistent citation format.
* **III. Safety & Ethics** — Avoid unsafe robotics instructions; summarize with safety checks.
* **IV. Reusability & Modularity** — Widget and backend agents are modular and reusable across books.
* **V. User-Centric Design** — Prioritize UX: quick answers, clear handoff messaging, and graceful errors.

## Project Structure

### Documentation (this feature)

```text
specs/003-rag-chatbot-integration/
├── plan.md              # This file
├── research.md          # Phase 0 research
├── data-model.md        # Session, message, agent payload models
├── quickstart.md        # How to run and test locally
├── contracts/
│   ├── agent_run_request.json
│   └── agent_run_response.json
└── tasks.md             # Generated tasks for sprints
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── triage_agent.py
│   │   ├── rag_agent.py
│   │   └── summarizer_agent.py
│   ├── config/
│   │   └── llm.py
│   │   └── __Init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── api_routes.py
│   │   └── context.py
│   ├── services/
│   │   ├── qdrant_service.py
│   │   ├── retriever.py
│   │   └── embedding_service.py
│   │   └── chunker_service.py
│   │   └── mdx_parser.py
│   │   └── verify_metadata.py
│   │   └── ingestion_pipeline.py
│   │   └── __init__.py
│   ├── routers/
│   │   ├── agent_router.py
│   │   └── __init__.py
│   └── main.py
└── tests/

frontend/
└── src/
    ├── components/
    │   └── ChatWidget/
    │       ├── index.tsx
    │       ├── styles.module.css
    │       ├── ChatWindow/
    │       │   ├── index.tsx
    │       │   └── styles.module.css
    │       ├── MessageBubble/
    │       │   ├── index.tsx
    │       │   └── styles.module.css
    │       └── TypingIndicator/
    │           ├── index.tsx
    │           └── styles.module.css
    ├── services/
    │   └── agentClient.ts
```

**Structure Decision**: Use existing Docusaurus frontend; add `src/components/ChatWidget` and `src/services/agentClient.ts`. Backend reuses current agents and retriever; add router `agent_router.py`.

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
| --------- | ---------- | ------------------------------------ |
| N/A       | N/A        | N/A                                  |

---

## Phase 0: Research & Contracts

**Objective**: Finalize API contracts and UI behavior before implementation.

**Tasks**:

* Create `contracts/agent_run_request.json` and `agent_run_response.json` describing payloads:

  ```json
  {
    "agent_type": "triage" |"summarizer"| "rag",
    "query": "string",
    "highlighted_text": "optional string",
    "current_page": "optional string",
    "session_id": "optional string"
  }
  ```

  Response:

  ```json
  {
    "message": "string",
    "sources": [{"slug":"", "chapter_number":"", "page_number":0, "snippet":"","slug":""}],
    "agent_used": "triage"|"rag"|"summarizer"
  }
  ```
* Define session model (`ConversationSession`, `ChatMessage`) in `data-model.md`.
* Confirm CORS, rate limits, and security considerations.

**Deliverable**: `specs/003-rag-chatbot-integration/contracts/*`


## Phase 1: Frontend Widget (UI) — MVP

**Objective**: Implement a lightweight, accessible floating chatbot component.

**Tasks**:

1. `ChatWidget/index.tsx` with `styles.module.css` — renders FAB, toggles ChatWindow.
2. `ChatWindow/index.tsx` with `styles.module.css` — message list, input box, send button, typing indicator.
3. `MessageBubble/index.tsx`  with `styles.module.css` — user/agent messages and source citations UI.
4. `agentClient.ts`  with `styles.module.css` — wrapper calling backend endpoints (`/agents/run`). Handles:

   * `POST /agents/run` for triage & summarizer
   * JSON payload with `current_page` and `highlighted_text`
   * session id header

**Deliverable**: Embedded widget component that sends queries and displays responses.

**Testing Criteria**:

* Open/close widget works.
* Typing indicator appears while awaiting response.
* 1–2 sample messages render correctly.


## Phase 2: Backend Endpoints & Integration

**Objective**: Expose stable endpoints to run agents and accept contextual payloads.

**Tasks**:

1. `agent_router.py` — `POST /agents/run` (triage/summarizer)

   * Accepts `AgentRequest` (see contracts) and returns normalized `AgentResponse`.
3. Implement input validation and session ID handling.
4. Ensure CORS is configured to allow Docusaurus origin(s).
5. Add structured logging for triage decisions and RAG handoffs.

**Deliverable**: Backend API accessible by widget, with documented request/response schemas.

**Testing Criteria**:

* `POST /agents/run` with `agent_type=triage` returns agent response.
* `POST /agents/run` with `agent_type=summarizer` returns summary for sample highlighted text.


## Phase 3: Agent Behavior & Handoff Logic

**Objective**: Implement triage → rag handoff flow and ensure retriever usage.

**Tasks**:

1. **Triage Agent**:

   * Fast, low-cost LLM call to classify query: `simple` vs `requires_context`.
   * If `simple`, generate answer directly (no retriever).
   * If `requires_context`, return a handoff status and trigger RAG agent.
2. **RAG Agent**:

   * Accept `query`, `current_page`, `highlighted_text`.
   * Call `RetrieverService.retrieve(query, current_page, highlighted_text)` which returns prioritized chunks (highlighted → current page → top global 3).
   * Build system prompt with retrieved chunks and call Gemini via agent SDK to produce answer with citations.
3. **Summarizer Agent**:

   * Accepts highlighted text (or set of chunks) and returns concise summary.
   * Not part of triage; invoked directly from `agent_router`.

**Deliverable**: Working agents with clear handoff semantics.

**Testing Criteria**:

* Triage labels queries correctly on test set.
* Handoff triggers RAG agent and response includes sources.
* Summarizer summarizes selected text accurately.

## Phase 4: Conversation Sessions & History

**Objective**: Keep per-session conversation view during a user's visit.

**Tasks**:

* Frontend keeps in-memory session (or sessionStorage) with `session_id`.
* Each message includes `session_id` sent to backend for logging (not persisted long-term).
* Backend returns `agent_used` and `sources` to display citations.
* Optional: persist conversations to Neon DB if required later (out of MVP scope).

**Deliverable**: Session-backed conversation that persists during a browser session.

**Testing Criteria**:

* Conversation state survives page scrolls and widget close/open within a session.
* Session id passed and logged by backend.


## Phase 5: UX Enhancements & Edge Cases

**Objective**: Improve usability and handle errors gracefully.

**Tasks**:

* Add validations: block empty/whitespace queries.
* Rate-limit button (debounce) and queue requests.
* Retry strategy for transient backend errors.
* Show user-friendly error message when agent/backend fails.
* Provide “View sources” link for RAG responses (open chapter page or highlight).

**Deliverable**: Robust widget UX with graceful degradation.

**Testing Criteria**:

* Simulate backend failure; widget shows error and allows retry.
* Highlighted-text summarization works end-to-end.


## Phase 6: QA, Performance & Security

**Objective**: Validate correctness, performance, and secure deployment.

**Tasks**:

* Backend unit & integration tests for:

  * Triage decision logic
  * Retriever ordering and filtering
  * RAG prompt construction and output parsing
* Frontend tests for component rendering and agent integration (mocked backend).
* Performance test: average latency < 5s for median queries.
* Security checks:

  * Ensure no API keys in frontend bundle
  * CORS restricted to allowed origins
  * Logging does not record PII

**Deliverable**: Test reports and security checklist.

**Testing Criteria**:

* Pass test suite and manual acceptance tests.
* Latency and load tests within targets.

## Phase 7: Deployment & Rollout

**Objective**: Deploy backend and integrate widget into the live book site.

**Tasks**:

* Backend: build Docker image, deploy to Railway with env vars (GOOGLE_API_KEY, QDRANT_ENDPOINT, QDRANT_API_KEY).
* Frontend: add widget script to Docusaurus layout (footer or global theme).
* Smoke test in staging: triage, RAG handoff, summarize flows.
* Go-live: monitor logs and metrics for errors or slow responses.

**Deliverable**: Production-ready chatbot on book pages.

**Testing Criteria**:

* End-to-end tests pass in staging and production smoke tests.


## Outputs & Deliverables

* `specs/003-rag-chatbot-integration/` (contracts, plan, quickstart)
* Frontend ChatWidget components and `agentClient.ts`
* Backend endpoints `/agents/run` with triage/RAG/summarizer agents
* Session handling and basic logging for handoffs
* Test suite and deployment configs (Dockerfile, Railway setup notes)

## Quality & Standards

* Answers referencing book content MUST include source citations (slug, chapter, snippet).
* UI must be responsive and accessible (keyboard focus, aria labels).
* LLM prompts and handoff logic must be logged (but not full user text long-term) for debugging.

## Risks & Mitigations

* **Latency** (RAG retrieval + LLM response): Mitigate with small retrieval windows, caching, and prioritizing local page context.
* **Incorrect handoff**: Continuously tune triage classifier prompts; include fallback to RAG after user request.
* **API cost/safety**: Use short prompts, batching where possible; guard against unsafe robotics instructions.