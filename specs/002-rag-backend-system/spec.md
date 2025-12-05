# Feature Specification: RAG Backend System for AI-Native Textbook

**Feature Branch**: `1-rag-backend-system`
**Created**: 2025-12-05
**Status**: Draft

---

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Content Ingestion and Processing (Priority: P1)

As a content manager, I want the system to automatically process all MDX files from the textbook content, so that they are chunked, embedded, and stored in a searchable vector database.

**Why this priority**: This is the foundational step for the entire RAG system. Without processed content, no queries can be answered.

**Independent Test**: Run the ingestion pipeline and verify that vectors and metadata exist in the Qdrant `textbook_chunks` collection for given MDX files.

**Acceptance Scenarios**:

1. **Given** a new MDX file is added to `frontend/docs/`, **When** the ingestion process runs, **Then** the content is chunked, embedded, and stored with correct metadata (`slug`, `chapter_number`, `chapter_title`, `lesson_id`, `section_headings`, `source_file_path`).
2. **Given** an existing MDX file is updated, **When** ingestion runs, **Then** the corresponding Qdrant entries are updated.
3. **Given** an MDX file with frontmatter, headings, paragraphs, and code blocks, **When** processed, **Then** text is chunked by sections preserving code blocks, with correct metadata extraction.

---

### User Story 2 - Student Query via RAG (Priority: P1)

As a student, I want to ask a question related to the textbook content, so that I can receive an accurate, context-aware answer with citations.

**Why this priority**: This is the primary user-facing feature and the core value proposition.

**Independent Test**: Send a query to `/rag/query` and verify the response includes relevant answers with source citations from the vector database.

**Acceptance Scenarios**:

1. **Given** the vector database is populated, **When** a user submits a query, **Then** the system retrieves relevant chunks, generates a coherent answer, and returns it with sources.
2. **Given** a user’s query and `current_page_slug`, **When** processed, **Then** retrieval prioritizes chunks from the current page before fetching other relevant chunks.
3. **Given** a user highlights text when querying, **When** processed, **Then** highlighted text is used as primary context for retrieval.

---

### User Story 3 - AI Agent Content Interaction (Priority: P2)

As a content author or student, I want to use specialized AI agents to review, enhance, or query content, so that I can validate content accuracy and improve the material.

**Why this priority**: Extends RAG functionality to advanced proactive use cases beyond simple Q&A.

**Independent Test**: Send a request to `/agents/run` with agent type and query, and verify responses match the agent’s role.

**Acceptance Scenarios**:

1. **Given** a user query and the `student_query` agent, **When** run, **Then** it returns a RAG-powered answer similar to the main query endpoint.
2. **Given** a new content draft and `review` agent, **When** run, **Then** it validates content against MDX material and flags contradictions/repetitions.
3. **Given** a topic and `enhance` agent, **When** run, **Then** it suggests improvements, examples, or clarifications based on existing content.

---

### Edge Cases

* MDX file without frontmatter → log a warning and skip.
* Empty user query → return a helpful prompt.
* Embedding service unavailable → fail safely with retry option.
* Non-MDX files → ignore.

---

## Requirements *(mandatory)*

### Functional Requirements

* **FR-001**: Recursively scan `frontend/docs/**/*.mdx`.
* **FR-002**: Parse MDX frontmatter to extract `slug`, `chapter_number`, `chapter_title`, `lesson_id`.
* **FR-003**: Extract section headings.
* **FR-004**: Chunk MDX content into 500–1000 token segments, keeping related blocks together.
* **FR-005**: Generate vector embeddings per chunk.
* **FR-006**: Store embeddings + metadata in Qdrant collection `textbook_chunks`.
* **FR-007**: Provide FastAPI backend.
* **FR-008**: `POST /rag/query` accepts query, optional `current_page_slug`, optional `highlighted_text`.
* **FR-009**: Retrieval prioritizes highlighted text + current page before global search.
* **FR-010**: RAG response includes generated answer + list of sources with metadata.
* **FR-011**: `POST /chunks/rebuild` triggers full content re-ingestion.
* **FR-012**: `POST /agents/run` executes specialized AI agents (`student_query`, `review`, `enhance`).

### Key Entities

* **Textbook Chunk**: Segment of MDX text with attributes:

  * Raw text
  * Vector embedding
  * Metadata: `slug`, `chapter_number`, `chapter_title`, `lesson_id`, `section_heading`, `source_file_path`

---

## Success Criteria *(mandatory)*

### Measurable Outcomes

* **SC-001**: 95% of queries return relevant answers with correct citations in ≤5s.
* **SC-002**: Ingestion of 1,000 MDX files (~1,500 words each) completes in <30 minutes.
* **SC-003**: For 100 benchmark questions, 90% receive satisfactory answers per human evaluation.
* **SC-004**: Handle 50 concurrent queries without >20% response time degradation.
