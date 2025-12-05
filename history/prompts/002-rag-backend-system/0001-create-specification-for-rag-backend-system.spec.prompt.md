---
id: 0002
title: Create RAG Backend System Specification
stage: spec
date: 2025-12-05
surface: agent
model: claude-sonnet-4-5-20250929
feature: 002-rag-backend-system
branch: 002-rag-backend-system
user: null
command: /sp.specify
labels: ["RAG", "backend", "specification", "AI-textbook"]
links:
  spec: specs/002-rag-backend-system/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/002-rag-backend-system/spec.md
tests: null
---

## Prompt

# **Specification Prompt: RAG Backend System for AI-Native Textbook**

**Goal:**
Build a fully functional RAG backend for the AI-native textbook platform. The backend must process MDX content from the existing Docusaurus docs, extract structured metadata, create vector embeddings, store them in Qdrant, and provide a RAG-powered AI agent system using OpenAI Agents SDK with Gemini API key.

## **1. Input Source & Metadata Extraction**

* **Source:** `frontend/docs/**/*.mdx`

* **Required metadata to extract per MDX file:**

  * `slug` → URL-friendly identifier for chapter/page
  * `chapter_number` → numeric chapter identifier
  * `chapter_title` → the title of the chapter
  * `lesson_id` → unique ID for each lesson/page
  * `section_headings` → all main headings/subheadings

* **Process:**

  1. Read all MDX files recursively.
  2. Parse the frontmatter for metadata (chapter number, title, slug).
  3. Extract the textual content and sections.
  4. Preserve code blocks, diagrams references, and inline examples separately for embedding context.


## **2. Text Chunking & Preprocessing**

* **Chunking Rules:**

  * Split text by headings, paragraphs, or sections (keep code blocks together).
  * Maintain context length ~500–1000 tokens per chunk.
  * Annotate each chunk with metadata:

    * `chapter_number`
    * `chapter_title`
    * `slug`
    * `lesson_id`
    * `section_heading`
    * `source_file_path`

* **Preprocessing:**

  * Remove JSX, imports, and MDX components that are not useful for embeddings.
  * Normalize whitespace and markdown formatting.

## **3. Embedding Generation**

* **Embedder:** Use **OpenAI embeddings (text-embedding-3-large)** or another chosen model.
* **Output:** Each chunk → vector embedding with associated metadata.
* **Storage:** Temporarily store embeddings in memory or local cache before pushing to Qdrant.

## **4. Qdrant Vector Database Setup**

* **Collection:** `textbook_chunks`

* **Fields:**

  * `embedding` → vector of chunk content
  * `metadata` → dictionary with `slug`, `chapter_number`, `chapter_title`, `lesson_id`, `section_heading`, `source_file_path`

* **Functionality:**

  * Insert chunk embeddings with metadata
  * Update embeddings if MDX content changes
  * Support similarity search with filters (e.g., chapter_number or slug)

## **5. Retriever & RAG Logic**

* **Retrieval Strategy:**

  1. Prioritize current page selection (if user highlights text, include it in context).
  2. Retrieve top 3 chunks from Qdrant based on similarity.
  3. Include metadata in retrieved context for citations.
  4. Construct RAG prompt combining:

     * Selected user text
     * Current page chunks
     * Top 3 additional chunks

* **RAG Engine:**

  * Combine retrieved chunks + user query into structured prompt.
  * Send to LLM (Gemini API) with proper instructions to answer accurately and reference sources.

## **6. AI Agents Using OpenAI Agents SDK**

* **Agent Types:**

  1. **Student Query Agent** → answer user questions with RAG context.
  2. **Chapter Review Agent** → validate new content against existing MDX content.
  3. **Content Enhancement Agent** → suggest improvements, add examples, or clarify explanations.

* **Tool Integration:**

  * Each agent has access to:

    * RAG retriever API (Qdrant-based)
    * Current page selection context
    * Chunked embeddings for multi-chapter reference

* **Requirements:**

  * Agent responses must be grounded in MDX content.
  * Include citations (slug + section heading + lesson_id) in responses.


## **7. Backend API (FastAPI)**

* **Routes:**

```python
POST /rag/query
Body: {
    "query": "User question",
    "current_page_slug": "chapter1/introduction",
    "highlighted_text": "optional text user selected"
}
Response: {
    "answer": "LLM-generated response",
    "sources": [
        {"slug": "...", "chapter_number": 1, "section_heading": "...", "lesson_id": "..."}
    ]
}

POST /chunks/rebuild
Body: None
Response: {"status": "Chunks rebuilt and re-embedded"}

GET /chunks/{slug}
Response: List of chunks with metadata

POST /agents/run
Body: {
    "agent_type": "student_query | review | enhance",
    "query": "...",
    "current_page_slug": "...",
    "highlighted_text": "optional"
}
Response: {"agent_response": "..."}
```

* **Requirements:**

  * FastAPI backend
  * Async support for embedding generation and Qdrant queries
  * Proper error handling and logging

## **8. User Interaction & Highlight Integration**

* Users can select text on the page
* The backend incorporates **selected text as priority context** for retrieval
* System retrieves **current page chunks first**, then top 3 global chunks for additional context
* Ensures **answers are grounded in both local and global content**

## **9. Deployment & Configuration**

* Environment Variables:

  * `OPENAI_API_KEY` → Gemini API key
  * `QDRANT_URL` → Qdrant endpoint
  * `QDRANT_API_KEY` → if using cloud Qdrant
* Dockerized deployment optional
* CI/CD pipeline to rebuild chunks whenever MDX content changes

## **10. Deliverables**

1. Backend FastAPI project with:

   * Qdrant integration
   * Embedding and chunking pipeline
   * RAG retriever and prompt builder
   * OpenAI Agents SDK integration

2. Complete API documentation with example requests/responses.

3. Fully functioning system:

   * Highlight integration for user-selected text
   * Current page chunk prioritization
   * Top-N additional chunk retrieval


## Response snapshot

Created a feature branch `1-rag-backend-system`.  
Developed a comprehensive specification `specs/002-rag-backend-system/spec.md` that outlines:

- User stories for content ingestion, RAG query, and AI agent interaction
- Functional requirements (FR-001 to FR-012)
- Key entities (Textbook Chunk metadata structure)
- Edge cases handling (missing frontmatter, empty queries, service unavailability)
- Success criteria (SC-001 to SC-004)
- Testing and verification methods (pipeline validation, API endpoints, retrieval prioritization)

Specification is structured for implementation planning and integration with the AI textbook content.

## Outcome

- ✅ Impact: RAG backend system specification completed, providing clear guidance for ingestion, query, and AI agent functionality.
- 🧪 Tests: Independent test procedures defined for each user story, including MDX ingestion verification, query accuracy, and agent behavior.
- 📁 Files: Created `specs/002-rag-backend-system/spec.md`.
- 🔁 Next prompts: /sp.plan or /sp.implement to create feature implementation PHRs.
- 🧠 Reflection: Specification clearly maps content requirements to backend features, ensures measurable outcomes, and supports RAG integration for the textbook content.

## Evaluation notes (flywheel)

- Failure modes observed: None at the specification stage; potential ingestion errors noted for future implementation.
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): Begin phased implementation; first validate content ingestion pipeline with a subset of MDX files.
