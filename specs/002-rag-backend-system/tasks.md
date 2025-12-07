---
description: "Task list for RAG Backend System"
---

# RAG Backend System Development Tasks

**Input**: Design documents from `/specs/002-rag-backend-system/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

## Phase 1: Setup FastAPI Project and Environment

**Purpose**: Project initialization and basic structure

- [ ] T001 P1 Setup FastAPI Project: Initialize a new FastAPI project, set up a virtual environment, install necessary dependencies (FastAPI, Uvicorn, Qdrant-client, OpenAI, Pydantic), and configure basic project structure (`routers`, `services`, `models`, `utils`). (backend/src/main.py, backend/src/requirements.txt)
  *   **Dependencies**: None
  *   **Expected Output / Deliverable**: A running FastAPI application with a basic `main.py` and structured directories.
  *   **Endpoint / Route**: `/` (root endpoint for basic health check)
  *   **Testing Criteria**: Run `uvicorn main:app --reload` and access `http://localhost:8000`. Verify basic FastAPI boilerplate response.

## Phase 2: Setup Qdrant Client and Collections

**Purpose**: Core vector database setup

- [ ] T002 P1 Configure Qdrant Client and Collection: Initialize Qdrant client, create a new collection named `textbook_chunks` with appropriate vector size (e.g., 1536 for Gemini embeddings) and schema for metadata fields (`slug`, `chapter_number`, `chapter_title`, `lesson_id`, `page_number`). (backend/src/services/qdrant_service.py)
  *   **Dependencies**: T001
  *   **Expected Output / Deliverable**: Qdrant client initialized and `textbook_chunks` collection created.
  *   **Endpoint / Route**: None (internal service)
  *   **Testing Criteria**: Verify collection creation via Qdrant's admin interface or a simple Qdrant client script to list collections.

## Phase 3: Scan MDX files, extract content and metadata

**Purpose**: Data ingestion - content extraction

- [ ] T003 P1 MDX Content and Metadata Extraction: Develop a service to scan MDX files from a specified directory, parse their content, and extract structured metadata: `slug`, `chapter_number`, `chapter_title`, `lesson_id`, `page_number`. Implement error handling for file parsing. (backend/services/mdx_parser.py)
  *   **Dependencies**: T001
  *   **Expected Output / Deliverable**: A Python function/service that takes an MDX file path and returns content and a dictionary of extracted metadata.
  *   **Endpoint / Route**: None (internal service for ingestion pipeline)
  *   **Testing Criteria**: Create a unit test for the extraction service using a mock MDX file to ensure correct content and metadata are extracted.

## Phase 4: Chunk the content while preserving code blocks

**Purpose**: Data ingestion - content preparation

- [ ] T004 P1 Content Chunking with Code Preservation: Implement a chunking mechanism that breaks down the extracted content into chunks of 500-1000 tokens. Crucially, ensure that code blocks are identified and kept intact within single chunks, or at least handled gracefully to prevent splitting within a code block. (backend/services/chunker.py)
  *   **Dependencies**: T003
  *   **Expected Output / Deliverable**: A Python function that takes raw content and returns a list of text chunks.
  *   **Endpoint / Route**: None (internal service for ingestion pipeline)
  *   **Testing Criteria**: Unit tests with sample content including code blocks to verify chunk sizes and code block integrity.

## Phase 5: Generate embeddings for each chunk using Gemini/OpenAI API

**Purpose**: Data ingestion - vector representation

- [ ] T005 P1 Generate Embeddings: Integrate with the Gemini/OpenAI API to generate vector embeddings for each text chunk. Handle API key management securely (e.g., environment variables) and implement retry mechanisms for API calls. (backend/src/services/embedding_generator.py)
  *   **Dependencies**: T004
  *   **Expected Output / Deliverable**: A Python function that takes a list of text chunks and returns a list of corresponding embedding vectors.
  *   **Endpoint / Route**: None (internal service for ingestion pipeline)
  *   **Testing Criteria**: Call the function with sample chunks and verify that it returns vectors of the expected dimension.

## Phase 6: Store chunks with embeddings and metadata into Qdrant

**Purpose**: Data ingestion - persistence

- [ ] T006 P1 Store Chunks in Qdrant: Develop a service to store the generated chunks, their embeddings, and associated metadata (from Task T003) into the `textbook_chunks` Qdrant collection. Ensure metadata fields are correctly indexed for efficient filtering during retrieval. (backend/src/services/qdrant_ingestor.py)
  *   **Dependencies**: T002, T005
  *   **Expected Output / Deliverable**: A Python function/service to ingest a chunk with its embedding and metadata into Qdrant.
  *   **Endpoint / Route**: None (internal service for ingestion pipeline)
  *   **Testing Criteria**: Ingest a few sample chunks and then query Qdrant to verify that the chunks, embeddings, and metadata are correctly stored and retrievable.

## Phase 7: Build retriever with prioritization logic

**Purpose**: Information retrieval

- [ ] T007 P1 Implement Prioritized Retriever: Design and implement a retriever service that queries the `textbook_chunks` Qdrant collection. The retrieval logic must prioritize results based on:
    1. Highlighted text matches (if available in query). 
    2. Chunks from the current page/context. 
    3. Top 3 global chunks (most relevant from the entire collection). This implies modifying Qdrant queries to include filtering by metadata fields like `page_number` and `highlighted_text` presence, and then combining results. (backend/src/services/retriever.py)
  *   **Dependencies**: T006
  *   **Expected Output / Deliverable**: A Python function that takes a query, optional current page context, and optional highlighted text, and returns a prioritized list of relevant chunks.
  *   **Endpoint / Route**: None (internal service for RAG agent)
  *   **Testing Criteria**: Unit tests with various query scenarios (with/without highlighted text, with/without current page context) to ensure correct prioritization and retrieval.

## Phase 8: Implement RAG AI agent using the retriever

**Purpose**: AI agent for question answering

- [ ] T008 P1 Develop RAG AI Agent: Implement a RAG (Retrieval Augmented Generation) AI agent using the OpenAI Agents SDK and the retriever built in Task T007. The agent should take a user query, retrieve relevant chunks, and then use a Gemini model (via OpenAI API key) to generate a coherent and contextually relevant response based on the retrieved information. (backend/src/agents/rag_agent.py)
  *   **Dependencies**: T007
  *   **Expected Output / Deliverable**: A Python class/function for the RAG agent that takes a query and returns a generated response.
  *   **Endpoint / Route**: None (internal service for `/agents/run`)
  *   **Testing Criteria**: Integration tests where the RAG agent is queried with sample questions, and the generated responses are evaluated for relevance and accuracy based on the retrieved chunks.

## Phase 9: Implement Summarizer agent

**Purpose**: AI agent for content summarization

- [ ] T009 P2 Develop Summarizer Agent: Implement a separate AI agent using the OpenAI Agents SDK and Gemini API key for summarization. This agent should be capable of summarizing longer text passages or a set of retrieved chunks. (backend/agents/summarizer_agent.py)
  *   **Dependencies**: T001 (OpenAI Agents SDK setup implicitly)
  *   **Expected Output / Deliverable**: A Python class/function for the Summarizer agent that takes text and returns a summary.
  *   **Endpoint / Route**: None (internal service for `/agents/run`)
  *   **Testing Criteria**: Unit tests with various text inputs to verify summary quality and conciseness.

## Phase 10: Implement Reviewer/Enhance agent

**Purpose**: AI agent for text review and enhancement

- [ ] T010 P2 Develop Reviewer/Enhance Agent: Implement a separate AI agent using the OpenAI Agents SDK and Gemini API key for reviewing or enhancing text. This agent could, for example, rephrase text, check for grammar, or expand on ideas. (backend/agents/reviewer_agent.py)
  *   **Dependencies**: T001 (OpenAI Agents SDK setup implicitly)
  *   **Expected Output / Deliverable**: A Python class/function for the Reviewer/Enhance agent that takes text and returns an enhanced version.
  *   **Endpoint / Route**: None (internal service for `/agents/run`)
  *   **Testing Criteria**: Unit tests with sample text inputs to evaluate the agent's ability to review or enhance content effectively.

## Phase 11: Create API Endpoints

**Purpose**: External interface for the backend system

- [ ] T011 P1 Implement API Endpoints: Create the following FastAPI endpoints:
    *   `POST /chunks/rebuild`: Triggers the full ingestion pipeline (scanning, chunking, embedding, storing).
    *   `POST /rag/query`: Accepts a user query, potentially current page context and highlighted text, and returns the RAG agent's response.
    *   `POST /agents/run`: A generic endpoint to run different AI agents (RAG, Summarizer, Reviewer/Enhance) based on a payload, specifying which agent to run and its inputs. (backend/routers/ingestion_router.py, backend/routers/rag_router.py, backend/routers/agent_router.py)
  *   **Dependencies**: T006, T008, T009, T010
  *   **Expected Output / Deliverable**: Functional FastAPI endpoints as described.
  *   **Endpoint / Route**: `/chunks/rebuild`, `/rag/query`, `/agents/run`
  *   **Testing Criteria**:
    *   `POST /chunks/rebuild`: Send a POST request and verify logs for ingestion pipeline execution.
    *   `POST /rag/query`: Send a POST request with a query and verify a relevant response from the RAG agent.
    *   `POST /agents/run`: Send POST requests to trigger Summarizer and Reviewer/Enhance agents with appropriate payloads and verify their outputs.

---

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
