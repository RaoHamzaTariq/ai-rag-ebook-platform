---
description: "Task list for RAG Backend System"
---

# RAG Backend System Development Tasks

**Input**: Design documents from `/specs/002-rag-backend-system/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

## Phase 1: Setup FastAPI Project and Environment

**Purpose**: Project initialization and basic structure

- [x] T001 P1 Setup FastAPI Project: Initialize a new FastAPI project, set up a virtual environment, install necessary dependencies (FastAPI, Uvicorn, Qdrant-client, OpenAI, Pydantic), and configure basic project structure (`routers`, `services`, `models`, `utils`). (backend/src/main.py, backend/src/requirements.txt)
  *   **Dependencies**: None
  *   **Expected Output / Deliverable**: A running FastAPI application with a basic `main.py` and structured directories.
  *   **Endpoint / Route**: `/` (root endpoint for basic health check)
  *   **Testing Criteria**: Run `uvicorn main:app --reload` and access `http://localhost:8000`. Verify basic FastAPI boilerplate response.

## Phase 2: Setup Qdrant Client and Collections

**Purpose**: Core vector database setup

- [x] T002 P1 Configure Qdrant Client and Collection: Initialize Qdrant client, create a new collection named `physical_ai_chunks` with appropriate vector size (e.g., 1536 for Gemini embeddings) and schema for metadata fields (`slug`, `chapter_number`, `chapter_title`, `lesson_id`, `page_number`). (backend/src/services/qdrant_service.py)
  *   **Dependencies**: T001
  *   **Expected Output / Deliverable**: Qdrant client initialized and `physical_ai_chunks` collection created.
  *   **Endpoint / Route**: None (internal service)
  *   **Testing Criteria**: Verify collection creation via Qdrant's admin interface or a simple Qdrant client script to list collections.

## Phase 3: Scan MDX files, extract content and metadata

**Purpose**: Data ingestion - content extraction

- [x] T003 P1 MDX Content and Metadata Extraction: Develop a service to scan MDX files from a specified directory, parse their content, and extract structured metadata: `slug`, `chapter_number`, `chapter_title`, `lesson_id`, `page_number`. Implement error handling for file parsing. (backend/services/mdx_parser.py)
  *   **Dependencies**: T001
  *   **Expected Output / Deliverable**: A Python function/service that takes an MDX file path and returns content and a dictionary of extracted metadata.
  *   **Endpoint / Route**: None (internal service for ingestion pipeline)
  *   **Testing Criteria**: Create a unit test for the extraction service using a mock MDX file to ensure correct content and metadata are extracted.

## Phase 4: Chunk the content while preserving code blocks

**Purpose**: Data ingestion - content preparation

- [x] T004 P1 Content Chunking with Code Preservation: Implement a chunking mechanism that breaks down the extracted content into chunks of 500-1000 tokens. Crucially, ensure that code blocks are identified and kept intact within single chunks, or at least handled gracefully to prevent splitting within a code block. (backend/services/chunker.py)
  *   **Dependencies**: T003
  *   **Expected Output / Deliverable**: A Python function that takes raw content and returns a list of text chunks.
  *   **Endpoint / Route**: None (internal service for ingestion pipeline)
  *   **Testing Criteria**: Unit tests with sample content including code blocks to verify chunk sizes and code block integrity.

## Phase 5: Generate embeddings for each chunk using Gemini API

**Purpose**: Data ingestion - vector representation

- [x] T005 P1 Generate Embeddings: Integrate with the Gemini API to generate vector embeddings for each text chunk. Handle API key management securely (e.g., environment variables) and implement retry mechanisms for API calls. (backend/src/services/embedding_generator.py)
  *   **Dependencies**: T004
  *   **Expected Output / Deliverable**: A Python function that takes a list of text chunks and returns a list of corresponding embedding vectors.
  *   **Endpoint / Route**: None (internal service for ingestion pipeline)
  *   **Testing Criteria**: Call the function with sample chunks and verify that it returns vectors of the expected dimension.

## Phase 6: Store chunks with embeddings and metadata into Qdrant

**Purpose**: Data ingestion - persistence

- [x] T006 P1 Store Chunks in Qdrant: Develop a service to store the generated chunks, their embeddings, and associated metadata (from Task T003) into the `physical_ai_chunks` Qdrant collection. Ensure metadata fields are correctly indexed for efficient filtering during retrieval. (backend/src/services/qdrant_ingestor.py)
  *   **Dependencies**: T002, T005
  *   **Expected Output / Deliverable**: A Python function/service to ingest a chunk with its embedding and metadata into Qdrant.
  *   **Endpoint / Route**: None (internal service for ingestion pipeline)
  *   **Testing Criteria**: Ingest a few sample chunks and then query Qdrant to verify that the chunks, embeddings, and metadata are correctly stored and retrievable.

## Phase 7: Build retriever with prioritization logic

**Purpose**: Information retrieval

- [ ] T007 P1 Implement Prioritized Retriever: Design and implement a retriever service that queries the `physical_ai_chunks` Qdrant collection. The retrieval logic must prioritize results based on:
    1. Highlighted text matches (if available in query). 
    2. Chunks from the current page/context. 
    3. Top 3 global chunks (most relevant from the entire collection). This implies modifying Qdrant queries to include filtering by metadata fields like `page_number` and `highlighted_text` presence, and then combining results. (backend/src/services/retriever.py)
  *   **Dependencies**: T006
  *   **Expected Output / Deliverable**: A Python function that takes a query, optional current page context, and optional highlighted text, and returns a prioritized list of relevant chunks.
  *   **Endpoint / Route**: None (internal service for RAG agent)
  *   **Testing Criteria**: Unit tests with various query scenarios (with/without highlighted text, with/without current page context) to ensure correct prioritization and retrieval.

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


## Dependencies & Execution Order

### Phase Dependencies

-   **Setup (Phase 1)**: No dependencies - can start immediately
-   **Qdrant Setup (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
-   **Content Extraction (Phase 3)**: Depends on Setup completion
-   **Content Chunking (Phase 4)**: Depends on Content Extraction completion
-   **Embedding Generation (Phase 5)**: Depends on Content Chunking completion
-   **Qdrant Storage (Phase 6)**: Depends on Qdrant Setup and Embedding Generation completion
-   **Retriever (Phase 7)**: Depends on Qdrant Storage completion
-   **RAG Agent (Phase 8)**: Depends on Retriever completion
-   **Summarizer Agent (Phase 9)**: Depends on Setup (for OpenAI SDK)
-   **Reviewer/Enhance Agent (Phase 10)**: Depends on Setup (for OpenAI SDK)
-   **API Endpoints (Phase 11)**: Depends on Qdrant Storage, RAG Agent, Summarizer Agent, Reviewer/Enhance Agent completion

### Parallel Opportunities

-   Summarizer Agent and Reviewer/Enhance Agent (T009, T010) can be developed in parallel with RAG agent development (T008) after the initial setup.

## Implementation Strategy

### Incremental Delivery

1.  Complete Phase 1: Setup
2.  Complete Phase 2: Qdrant Setup
3.  Complete Phase 3: MDX Content and Metadata Extraction
4.  Complete Phase 4: Content Chunking with Code Preservation
5.  Complete Phase 5: Generate Embeddings
6.  Complete Phase 6: Store Chunks in Qdrant
7.  Complete Phase 7: Implement Prioritized Retriever
8.  Complete Phase 8: Develop RAG AI Agent
9.  Complete Phase 9: Develop Summarizer Agent
10. Complete Phase 10: Develop Reviewer/Enhance Agent
11. Complete Phase 11: Implement API Endpoints
