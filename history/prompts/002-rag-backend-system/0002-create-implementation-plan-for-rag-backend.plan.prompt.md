---
id: 0002
title: Create Implementation Plan for RAG Backend
stage: plan
date: 2025-12-06
surface: agent
model: claude-sonnet-4-5-20250929
feature: 002-rag-backend-system
branch: 002-rag-backend-system
user: unknown
command: /sp.plan
labels: ["plan", "rag", "backend", "fastapi", "qdrant"]
links:
  spec: "E:/AI Native Books/ai-rag-ebook-platform/specs/002-rag-backend-system/spec.md"
  ticket: null
  adr: null
  pr: null
files:
  - E:/AI Native Books/ai-rag-ebook-platform/specs/002-rag-backend-system/plan.md
tests:
  - none
---

## Prompt

Build a proper plan

# RAG Backend System — Plan Prompt

We are building a **RAG backend** for an AI-native textbook using **FastAPI, Qdrant, and OpenAI Agents SDK**. Follow the steps in order.

## 1. FastAPI Setup
- Create modular app with routers: `/chunks`, `/rag`, `/agents`
- Configure environment variables for Gemini/OpenAI & Qdrant

## 2. Qdrant Setup
- Create collection: `textbook_chunks`
- Metadata: `slug`, `chapter_number`, `chapter_title`, `lesson_id`, `section_heading`, `source_file_path`
- Functions: `upsert_chunks()`, `clear_collection()`

## 3. MDX Loader & Metadata Extraction
- Recursively scan `frontend/docs/**/*.mdx`
- Extract frontmatter, headings, content, slug, chapter_number, chapter_title, lesson_id
- Return structured objects per file

## 4. Chunking & Embedding
- Split text into 500–1000 token chunks
- Preserve code blocks and context
- Embed using Gemini/OpenAI embeddings

## 5. Ingestion Pipeline
- Load → Extract → Chunk → Embed → Store in Qdrant
- Route: `POST /chunks/rebuild` → returns number of indexed chunks

## 6. Retriever
- Retrieval priority:
  1. Highlighted text
  2. Current page chunks
  3. Global top 3 relevant chunks
- Function: `retrieve_context(query, highlighted_text=None, slug=None)`

## 7. AI Agents
- **Summarizer**: summarize input text
- **RAG Agent**: generate answers using retriever tool, cite sources
- **Reviewer**: check new content vs existing MDX

## 8. Routes
- `/rag/query` → query + optional highlighted text + slug → returns answer + sources
- `/agents/summarize` → returns summary
- `/agents/run` → run selected agent with payload

**Implementation Phases**:
1️⃣ FastAPI Setup → 2️⃣ Qdrant → 3️⃣ MDX Loader → 4️⃣ Chunking → 5️⃣ Embedding → 6️⃣ Ingestion → 7️⃣ Retriever → 8️⃣ Agents → 9️⃣ Routes

---

## Response snapshot

I have created the initial implementation plan for the RAG backend system, outlining the technical context, project structure, and constitution alignment. The next steps are to conduct research, define the data model, and create API contracts.

---

## Outcome

- ✅ Impact: A structured implementation plan was created, providing a clear roadmap for developing the RAG backend.
- 🧪 Tests: none
- 📁 Files: `plan.md` was created and populated.
- 🔁 Next prompts: `/sp.tasks` to generate the implementation tasks from the plan.
- 🧠 Reflection: The initial attempt to write the file failed because I used `Write` instead of `Edit` on a template file. The process must be to read the template first, then edit it.

---

## Evaluation notes (flywheel)

- Failure modes observed: The `Write` tool failed with a 'File has not been read yet' error, which was incorrect. The actual error was that I should have used the `Edit` tool to modify the existing template file rather than overwriting it completely. The subsequent `Edit` call also failed due to an unexpected modification, forcing a re-read.
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Ensure the workflow for handling template files is explicitly defined: always read then edit, never write.
