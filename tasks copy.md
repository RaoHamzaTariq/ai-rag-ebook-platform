## Phase 8: Build Agents Layer

* [ ] **T008‑A**: Create `llm.py` config — configure Gemini + Agents SDK client + shared model instance.

  * **Dependencies**: environment variables (`GEMINI_API_KEY`, etc.), installation of `openai-agents`.
  * **Deliverable**: `backend/src/config/llm.py` that exports a shared model object usable by all agents.

* [ ] **T008‑B**: Implement `triage_agent.py`. This agent should:

  * Inspect user query.
  * If the query is simple / generic (e.g. “Define X”, “What is Y?”) answer directly (no retrieval needed).
  * If query likely requires content from textbook / context (e.g. “In chapter 2, what is QoS?”, or “Explain ROS 2 topics based on book”) → **handoff to RAG agent**.

  - **Dependencies**: `llm.py`, `rag_agent.py` (to be defined), Agents SDK configuration.
  - **Deliverable**: `backend/src/agents/triage_agent.py`.

* [ ] **T008‑C**: Implement `rag_agent.py`. This agent should:

  1. Take user query (or context/handoff from triage).
  2. Use retriever service (from Phase 7) to fetch relevant chunks.
  3. Construct prompt/context combining user query + retrieved chunks.
  4. Call Gemini (via Agents SDK) to generate answer based on context.

  * **Dependencies**: retriever service, `llm.py`.
  * **Deliverable**: `backend/src/agents/rag_agent.py`.

* [ ] **T008‑D**: Implement `summarizer_agent.py`. This agent handles summarization requests (e.g. user supplies a block of text — maybe highlighted text — and asks “summarize this”). It does **not** use retriever or handoffs.

  * **Dependencies**: `llm.py`.
  * **Deliverable**: `backend/src/agents/summarizer_agent.py`.

## Phase 9: Integrate Agents with API (FastAPI)

* [ ] **T009‑A**: Define a unified API route for agent runs: `POST /agents/run`. Payload includes: `agent_type` (e.g. `"triage"` or `"summarizer"`), and necessary inputs (query, optional highlighted_text, optional current_page, optional text_for_summarization).

  * If `agent_type = "triage"` → run triage agent (which may handoff to rag internally).
  * If `agent_type = "summarizer"` → run summarizer agent.
  * **Dependencies**: Agents implemented in Phase 8, FastAPI server setup.
  * **Deliverable**: `backend/src/routers/agent_router.py` (or similar).

* [ ] **T009‑B**: (Optional) Provide backward‑compatibility / convenience route for RAG-only queries, e.g. `POST /rag/query` as before, which under the hood uses triage → rag (for clarity).

## Phase 10: Testing & QA for Agents

* [ ] **T010‑A**: Unit tests for triage agent: ensure it correctly distinguishes simple vs context‑heavy queries, and delegates correctly.
* [ ] **T010‑B**: Integration tests for RAG agent: given sample queries, verify retrieving from Qdrant + response generation with correct context.
* [ ] **T010‑C**: Unit tests for summarizer agent: pass sample text plus edge-cases (short text, very long text) — check summary quality / length.
* [ ] **T010‑D**: System tests: call `/agents/run` with various payloads (simple question, context question, summarization) and inspect outputs.

## Phase 11: Documentation & Deployment Prep

* [ ] **T011‑A**: Document agent usage patterns in README (how triage works, which agent to call when).
* [ ] **T011‑B**: Define config examples (`.env.example`) — showing required environment variables (Gemini key, Qdrant URL/key, etc.)
* [ ] **T011‑C**: Prepare production deployment checklist — LLM rate‑limits, Qdrant connection, error handling for agent failures.
