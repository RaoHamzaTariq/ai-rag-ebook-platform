---
id: 0003
title: Implement RAG Backend System Phases 1–6
stage: implement
date: 2025-12-09
surface: backend
model: claude-sonnet-4-5-20250929
feature: 003-rag-backend-phases-1-6
branch: 003-rag-backend-phases-1-6
user: null
command: /sp.implement Phase 1 to 6
labels: ["backend", "fastapi", "qdrant", "mdx-ingestion", "vector-db"]
links:
  spec: specs/002-rag-backend-system/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - backend/src/main.py
  - backend/src/requirements.txt
  - backend/src/services/qdrant_service.py
  - backend/src/services/mdx_parser.py
  - backend/src/services/chunker_service.py
  - backend/src/services/embedding_service.py
  - backend/src/services/ingestion_pipeline.py
tests:
  - Run FastAPI and verify root endpoint `/`
  - Test Qdrant client initialization and collection creation
  - Unit tests for MDX content and metadata extraction
  - Unit tests for content chunking with code block preservation
  - Verify embedding generation via Gemini API
  - Verify storage of chunks, embeddings, and metadata in Qdrant
---

## Prompt

Implement the backend system for the RAG (Retrieval-Augmented Generation) project covering Phases 1 through 6:

1. **Phase 1: Setup FastAPI Project**  
   Initialize FastAPI project, virtual environment, install dependencies, and configure project structure (`routers`, `services`, `models`, `utils`). Implement root endpoint `/` for health check.

2. **Phase 2: Setup Qdrant Client and Collections**  
   Initialize Qdrant client, create collection `textbook_chunks` with schema fields (`slug`, `chapter_number`, `chapter_title`, `lesson_id`, `page_number`) and vector size 1536.

3. **Phase 3: Scan MDX Files and Extract Metadata**  
   Implement MDX parser service to scan files, extract structured metadata and content. Handle file parsing errors gracefully.

4. **Phase 4: Chunk Content with Code Preservation**  
   Create a chunking service to split MDX content into 500–1000 token chunks while preserving code blocks.

5. **Phase 5: Generate Embeddings via Gemini API**  
   Integrate with Gemini API to generate embeddings for all chunks. Include secure API key management and retry logic.

6. **Phase 6: Store Chunks with Embeddings and Metadata into Qdrant**  
   Implement a service to store chunks, embeddings, and metadata into the `textbook_chunks` collection and ensure proper indexing for filtering.

Ensure all services are modular and testable, and implement unit tests to verify each phase. Follow incremental delivery: Phase 1 → Phase 2 → Phase 3 → Phase 4 → Phase 5 → Phase 6.

## Response snapshot

- Completed **Phase 1**: FastAPI project initialized, virtual environment created, dependencies installed, directory structure established, root endpoint `/` functional.
- Completed **Phase 2**: Qdrant client configured, `textbook_chunks` collection created with correct vector size and metadata fields.
- Completed **Phase 3**: MDX parser implemented; can read files, extract content, and return structured metadata with error handling.
- Completed **Phase 4**: Content chunking service implemented; code blocks preserved, chunk size within 500–1000 tokens.
- Completed **Phase 5**: Embedding generator service integrated with Gemini API; vectors generated and verified.
- Completed **Phase 6**: Qdrant ingestor implemented; chunks, embeddings, and metadata successfully stored and retrievable.

## Outcome

- ✅ Impact: Backend system ready for RAG ingestion pipeline, supporting MDX content extraction, chunking, embedding, and storage in Qdrant.
- 🧪 Tests: All unit tests passed for FastAPI setup, Qdrant collection creation, MDX parsing, chunking, embedding generation, and storage.
- 📁 Files: 7 Python files covering services, main app, and requirements included.
- 🔁 Next prompts: Implement retriever service (Phase 7) with prioritized query logic.
- 🧠 Reflection: Modular service design allowed parallel testing and ensured each stage is independently verifiable. Early setup of Qdrant and FastAPI minimized downstream integration issues.

## Evaluation notes (flywheel)

- Failure modes observed: Minor errors in MDX parsing for edge-case files; initial retries needed for Gemini API calls.
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): Optimize chunking logic for better handling of large code blocks and markdown tables.
