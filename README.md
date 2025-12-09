# ai-rag-ebook-platform
AI-powered RAG eBook platform where users read content, and chat with an intelligent assistant built using FastAPI, Docusaurus, Qdrant, Neon DB, and OpenAI Agents.



Project Purpose & Vision:

Create an AI-powered eBook platform that allows users to interact with books via a chatbot.
Users can search, query, and get context-aware answers from uploaded eBooks using RAG (Retrieval-Augmented Generation).
The goal is to enhance learning by providing instant, accurate, and referenced AI-driven responses.

Target Users:

Students, learners, and self-study enthusiasts.
Users who prefer interactive learning through AI-assisted reading.

Core Features:

User authentication and profile management (Better Auth).
Multi-language eBook reading interface (English, Urdu).
Chatbot with contextual responses citing chapter/page and source link.
Text selection → “Ask with Chatbot” functionality.
Persistent chat history per user.
Backend powered by FastAPI, frontend by Docusaurus.
RAG system using Qdrant vector database and OpenAI Agents SDK.

Guiding Principles:

Security: Handle user data safely; encrypt sensitive info.
Scalability: Support multiple books, users, and languages.
Maintainability: Clean, modular code with clear separation of concerns (frontend/backend/AI).
UX: Intuitive book interface and chatbot interaction.
AI Ethics: Provide correct citations, avoid hallucinations, respect user privacy.

Technology Stack Context:

Frontend: Docusaurus (TypeScript) with i18n.
Backend: FastAPI (Python) with AI integration.
Database: Neon DB for structured data; Qdrant for embeddings.
AI System: OpenAI Agents SDK for RAG.
Deployment: GitHub Pages (frontend), Railway with Docker (backend).

Constraints & Considerations:

Only handle eBooks in supported languages initially.
Chatbot must provide references for all answers.
Keep conversation history persistent and tied to user profiles.
Follow best practices for API design, frontend routing, and modularization.

Goals & Expected Outcomes:

Fully functional AI-powered eBook platform.
Accurate, context-aware chatbot responses.
Seamless, multilingual user experience.
Secure and scalable system architecture.


Create the specification for the AI-native textbook titled “Physical AI & Humanoid Robotics”. This specification defines how the book content should be structured, authored, and prepared for integration with a RAG system.

Requirements:

Scope:
Cover all modules of the Physical AI & Humanoid Robotics course:
Foundations of Physical AI & Embodied Intelligence
ROS 2 Fundamentals
Gazebo Simulation & Digital Twin
Unity for Robot Visualization
NVIDIA Isaac Sim & Isaac ROS
Vision, Perception, and Navigation (VSLAM, Sensors)
Humanoid Kinematics, Bipedal Locomotion & Balance
Manipulation & Grasping
Conversational Robotics (GPT integration)
Capstone: Autonomous Humanoid Project

Content Structure:

Chapters must have:
Chapter ID, Title, and Metadata
Learning Objectives
Sections with headings and subheadings
Explanations, examples, and diagrams.
Code snippets in Python or ROS 2 where applicable
Page numbers or markers for RAG retrieval

Standards:

Clear, structured, and educational content
Consistent terminology and tone
Avoid jargon where possible
Ensure factual accuracy aligned with robotics and AI principles

Output Format:

MDX-compatible files for Docusaurus
Each chapter as a separate MDX file
Include metadata required for RAG ingestion (chapter_id, page_number, slug, url)

Acceptance Criteria:

Full set of chapters covering all modules
Properly formatted for Docusaurus
Ready for ingestion into the RAG system



Create a detailed development plan for the AI-native textbook “Physical AI & Humanoid Robotics”, based on the specification provided. The plan should break the work into clear, actionable steps with priorities, dependencies, and outcomes.

Requirements:

Tasks Breakdown:

Divide the book into chapters and sections based on course modules.
Define tasks for writing, reviewing, and formatting each chapter.
Include tasks for adding code snippets, diagrams, and examples.

Dependencies:

Identify dependencies between chapters, technical examples, and RAG metadata.
Specify which chapters can be developed in parallel.

Timeline & Milestones:

Suggest a sequence for completing chapters, review, and final formatting.
Include checkpoints for RAG metadata validation and MDX readiness.

Outputs & Deliverables:

Fully formatted MDX files per chapter.
Complete metadata (chapter_id, page_number, slug, URL) for RAG.
Ready-for-ingestion book repository for frontend integration.

Quality & Standards:

Ensure content clarity, consistency, and factual accuracy.
Confirm code snippets and examples are correct and executable where applicable.


Create a detailed task list for developing the AI-native textbook “Physical AI & Humanoid Robotics”, based on the specification and plan. Each task should be actionable, assigned a priority, and include expected output.

Requirements:

Chapter-Wise Tasks:

Break the book into chapters corresponding to the course modules:

Foundations of Physical AI & Embodied Intelligence
ROS 2 Fundamentals
Gazebo Simulation & Digital Twin
Unity for Robot Visualization
NVIDIA Isaac Sim & Isaac ROS
Vision, Perception, and Navigation
Humanoid Kinematics, Bipedal Locomotion & Balance
Manipulation & Grasping
Conversational Robotics (GPT integration)
Capstone: Autonomous Humanoid Project

Section-Wise Subtasks:

For each chapter, create subtasks for:
Writing content and explanations
Adding examples and analogies
Inserting code snippets (Python/ROS 2)
Creating diagrams or illustrations
Assigning metadata for RAG (chapter_id, page_number, slug, URL)

Task Attributes:

Include priority (High/Medium/Low)
Include expected output (e.g., MDX file, metadata JSON, diagram image)
Include dependencies (e.g., code snippets depend on ROS 2 explanation being written first)

Final Tasks:

Review and edit each chapter for clarity and accuracy
Validate MDX formatting for Docusaurus
Ensure metadata is ready for RAG ingestion



Generate a detailed task list for creating the AI-native textbook “Physical AI & Humanoid Robotics.”
The tasks should be broken down into clear, actionable steps that an AI agent or human contributor can execute directly.
Do not include RAG, chatbot, backend, or frontend tasks.
Focus only on book writing, chapter creation, content structure, and MDX formatting.

Task Requirements:
1. Chapter Planning & Structure
Create tasks for planning each chapter based on course modules.
Define tasks for outlining chapter objectives, section breakdown, and required explanations.
Include tasks for deciding where examples, diagrams, or code snippets are needed.

2. Writing Tasks

Break writing into small, manageable tasks such as:
Write introduction for Chapter X
Write section on concept Y
Explain topic Z with diagrams or analogies
Write step-by-step explanation of ROS 2 configuration
Write python code example for Robotics concept
Draft summary and learning outcomes
Each chapter should have multiple writing tasks.

3. Technical Content Tasks

Tasks to create or refine code snippets (Python, ROS 2, URDF, etc.)
Tasks to generate diagrams: architecture diagrams, robotics pipeline diagrams, simulation flow, sensor layouts, etc.
Tasks to draft pseudo-code or step-by-step explanations for robotics processes.

4. MDX Formatting Tasks

Convert each chapter into properly structured MDX format.
Add headings, subheadings, lists, tables, and code blocks.
Insert images and diagrams using proper Docusaurus MDX syntax.
Validate formatting for consistency and readability.

5. Review & Refinement

Tasks for technical accuracy review.
Tasks for rewriting unclear or ambiguous content.
Tasks for ensuring consistent terminology acros chapters.
Tasks for grammar, clarity, and tone refinement.
Tasks for internal cross-referencing between chapters.

6. Metadata Preparation

Even though this is not RAG-specific, include basic metadata tasks such as:
Assign chapter IDs, titles, and slugs
Add frontmatter to each MDX file
Ensure all chapters follow a consistent metadata structure
(Do not include embeddings or RAG ingestion tasks.)

7. Final Assembly Tasks

Compile all chapters into the Docusaurus /docs folder.
Verify sidebar structure aligns with book flow.
Ensure navigation is consistent and all links work.
Perform a final content sweep to ensure chapter cohesion.

Output Format

The task list should be:
Highly detailed
Structured hierarchically
Broken into granular, actionable items
Organized by chapter and by type of task (writing, diagrams, formatting, metadata, review)


Perfect! I understand — you want the **detailed, phase-by-phase task breakdown**, like your original `Tasks.md`, but **updated for the new chapter folder structure** (main + subtopic files) and **focused only on book creation**. Here’s the full detailed rewrite:

---

# **Tasks for AI-Native Textbook: Physical AI & Humanoid Robotics**

*(Updated for main + subtopic structure)*

## **Implementation Strategy**

This task list is designed for incremental delivery, focusing on completing each section before moving to the next. The goal is to generate an immediately executable plan for an AI agent or human contributor.

## **Dependencies**

Chapters can be planned and written largely in parallel once the overall structure is established. Review and refinement tasks for each chapter depend on the writing and technical content tasks for that chapter. Final assembly depends on all chapters being complete and formatted.

---

## **Phase 1: Setup**

* [ ] **T001** Review and validate the generated task list for the AI-Native Textbook project `tasks.md`

---

## **Phase 2: Foundational**

* [ ] **T002** Establish common guidelines for chapter folder structure, naming conventions, and MDX formatting:
  `frontend/docs/chapter-template/main.mdx`
  `frontend/docs/chapter-template/subtopic-template.mdx`

---

## **Phase 3: Chapter Planning & Structure**

### **User Story: Plan Chapter 1 — Foundations of Physical AI & Embodied Intelligence**

* [ ] **T003 [US1]** Define folder structure for Chapter 1:

  ```
  frontend/docs/chapter-1/
      main.mdx
      subtopic-1.mdx
      subtopic-2.mdx
      subtopic-3.mdx
      subtopic-4.mdx
  ```
* [ ] **T004 [US1]** Outline main.mdx content for Chapter 1 (introduction + core concepts)
* [ ] **T005 [US1]** Identify and name subtopics (subtopic-1 to subtopic-4)
* [ ] **T006 [US1]** Define content goal for each subtopic file (theoretical concepts only)

### **User Story: Plan Chapter 2 — ROS Fundamentals**

* [ ] **T007 [US2]** Define folder structure for Chapter 2:

  ```
  frontend/docs/chapter-2/
      main.mdx
      subtopic-1.mdx
      subtopic-2.mdx
      subtopic-3.mdx
      subtopic-4.mdx
  ```
* [ ] **T008 [US2]** Outline main.mdx content for Chapter 2 (ROS architecture + core concepts)
* [ ] **T009 [US2]** Identify and name subtopics (subtopic-1 to subtopic-4)
* [ ] **T010 [US2]** Define content goal for each subtopic file

---

## **Phase 4: Writing Tasks**

### **User Story: Draft Chapter 1 Content**

* [ ] **T011 [US1]** Write main.mdx content for Chapter 1
* [ ] **T012 [US1]** Write subtopic-1.mdx content (e.g., Embodiment in Physical AI)
* [ ] **T013 [US1]** Write subtopic-2.mdx content (e.g., Sensors & Perception)
* [ ] **T014 [US1]** Write subtopic-3.mdx content (e.g., Motor Control & Actuators)
* [ ] **T015 [US1]** Write subtopic-4.mdx content (optional, e.g., Interaction Loops)

### **User Story: Draft Chapter 2 Content**

* [ ] **T016 [US2]** Write main.mdx content for Chapter 2
* [ ] **T017 [US2]** Write subtopic-1.mdx content (e.g., ROS 2 Nodes)
* [ ] **T018 [US2]** Write subtopic-2.mdx content (e.g., Topics & Services)
* [ ] **T019 [US2]** Write subtopic-3.mdx content (e.g., Packages & Launch Files)
* [ ] **T020 [US2]** Write subtopic-4.mdx content (optional, e.g., Parameter Management)

---

## **Phase 5: Review & Refinement**

### **User Story: Review Chapter 1**

* [ ] **T021 [US1]** Review main.mdx for technical accuracy and clarity
* [ ] **T022 [US1]** Review subtopic-1.mdx for clarity and conceptual correctness
* [ ] **T023 [US1]** Review subtopic-2.mdx for clarity and conceptual correctness
* [ ] **T024 [US1]** Review subtopic-3.mdx for clarity and conceptual correctness
* [ ] **T025 [US1]** Review subtopic-4.mdx (optional)
* [ ] **T026 [US1]** Ensure consistent terminology across main and subtopic files

### **User Story: Review Chapter 2**

* [ ] **T027 [US2]** Review main.mdx for technical accuracy and clarity
* [ ] **T028 [US2]** Review subtopic-1.mdx
* [ ] **T029 [US2]** Review subtopic-2.mdx
* [ ] **T030 [US2]** Review subtopic-3.mdx
* [ ] **T031 [US2]** Review subtopic-4.mdx (optional)
* [ ] **T032 [US2]** Ensure terminology consistency across main and subtopic files

---

## **Phase 6: Final Assembly Tasks**

* [ ] **T033** Place all chapter folders correctly in `frontend/docs/`
* [ ] **T034** Update sidebar structure in `sidebars.js`
* [ ] **T035** Verify internal navigation and cross-linking between chapters
* [ ] **T036** Perform final content sweep to ensure chapter cohesion and flow

---

## **Output Summary**

* **Total Tasks:** 36

* **Structure Per Chapter:**

  * main.mdx
  * subtopic-1.mdx
  * subtopic-2.mdx
  * subtopic-3.mdx
  * subtopic-4.mdx (optional)

* **Parallelizable Tasks:** Writing of subtopic files across chapters can happen in parallel

* **MVP Scope:** Complete Chapter 1 fully (main + all subtopics)

---

If you want, I can **now rewrite this Tasks.md to cover all 13 chapters of the “Physical AI & Humanoid Robotics” course**, fully detailed, **with proper main + subtopic files**.

Do you want me to do that next?




Master Textbook Generation Blueprint: Physical AI & Humanoid RoboticsThis single blueprint provides the complete Table of Contents, the mandatory file structure, and the exact, reusable prompt template for generating all subsequent lessons. Use this structure to maintain perfect consistency, tone, and technical readiness (MDX/RAG) for your Docusaurus platform.1. Complete Table of Contents (TOC) and Mandatory File Structure (14 Lessons)This TOC defines the scope, structure, and the mandatory file path for every lesson. This structure aligns with Docusaurus documentation organization (docs/[chapter-slug]/[lesson-slug].mdx).Chapter IDChapter TitleLesson IDLesson TitleModule AlignmentFile Path (Docusaurus MDX)Status01Foundations & Sensing1.1Embodied Intelligence and Physical LawsWeek 1-2docs/01-foundations/1-1-embodied-intelligence.mdxDone1.2The Importance of Real-Time and LatencyWeek 1-2docs/01-foundations/1-2-real-time.mdxDone1.3Cameras, LIDAR, and Perception SystemsWeek 1-2docs/01-foundations/1-3-perception-systems.mdxDone1.4Tactile and Internal Sensors: IMUs, Force/Torque, and TemperatureWeek 1-2docs/01-foundations/1-4-internal-sensors.mdxNEXT02The Robotic Nervous System (ROS 2)2.1ROS 2 Architecture: Nodes, Topics, Services, and ActionsWeek 3-5docs/02-ros2/2-1-ros2-architecture.mdxTo Generate2.2Building ROS 2 Packages with Python (rclpy)Week 3-5docs/02-ros2/2-2-rclpy-packages.mdxTo Generate2.3Robot Description: URDF/SDF for Humanoid KinematicsWeek 3-5docs/02-ros2/2-3-urdf-kinematics.mdxTo Generate03The Digital Twin (Simulation)3.1Gazebo Simulation: Physics, Gravity, and Collision ModelingWeek 6-7docs/03-simulation/3-1-gazebo-physics.mdxTo Generate3.2High-Fidelity Visualization: Unity and Scene SetupWeek 6-7docs/03-simulation/3-2-unity-visualization.mdxTo Generate04Advanced AI & Control (NVIDIA Isaac)4.1Isaac Sim: Photorealistic Simulation and Synthetic DataWeek 8-10docs/04-isaac/4-1-isaac-sim-data.mdxTo Generate4.2Isaac ROS: Hardware-Accelerated VSLAM and Perception PipelinesWeek 8-10docs/04-isaac/4-2-vslam-pipelines.mdxTo Generate05Humanoid Action & VLA Integration5.1Bipedal Locomotion and Balance ControlWeek 11-12docs/05-humanoid/5-1-locomotion-balance.mdxTo Generate5.2Manipulation & Grasping with Humanoid HandsWeek 11-12docs/05-humanoid/5-2-manipulation-grasping.mdxTo Generate5.3Conversational Robotics (VLA): GPT to ROS 2 Action SequenceWeek 13docs/05-humanoid/5-3-vla-cognitive.mdxTo Generate2. Reusable MDX Lesson Generation Prompt TemplateINSTRUCTIONS: Copy and paste the prompt template below for the next lesson in the TOC. You must replace all bracketed placeholders ([LIKE_THIS]) with the specific content for the current lesson (e.g., Lesson 1.4). The entire output must be in a single markdown file block.Prompt Template to Copy and UseAI LESSON GENERATION PROMPT: [LESSON_ID] - [LESSON_TITLE]

1. PERSONA AND AUDIENCE STANDARDS:
Persona: Act as a friendly, encouraging, and knowledgeable technology tutor.
Tone: Simple, approachable, and highly focused on clarity. Avoid jargon where a simple analogy can be used.
Target Audience: Absolute beginners (Middle School / Early High School level). Keep the language direct and avoid overly academic phrasing.
Length: Total content body MUST be within 700-800 words.

2. CORE CONTENT GOAL:
Generate a complete, self-contained lesson covering the fundamental concepts of "[ONE_SENTENCE_GOAL_DESCRIPTION]". The content must build logically on the previous chapters/lessons and align with the specified module focus.

3. REQUIRED OUTPUT STRUCTURE (MDX/MARKDOWN FILE):
The entire output MUST be generated as a single file block using the MDX Markdown format.

A. YAML Frontmatter (MANDATORY for RAG/Docusaurus):
The file MUST begin with the following YAML block, using the structure defined in the Master TOC.
---
id: lesson-[LESSON_ID_SLUG]
title: Lesson [LESSON_ID]: [LESSON_TITLE]
sidebar_label: [SHORTENED_LESSON_TITLE]
chapter_id: [CHAPTER_ID_NUMBER]
page_number: [SIMULATED_RAG_PAGE_MARKER]
slug: /[CHAPTER_SLUG]/[LESSON_ID_SLUG]
---

B. DOCUMENT BODY (MANDATORY SECTIONS & MDX INSTRUCTIONS):

1. H1 Title & Summary: Use H1 (#) for the title and a single, concise, one-sentence summary immediately below it.

2. Introduction & Hook (H2):
   - Use H2 (##).
   - Relate the topic back to the overall goal of Physical AI (bridging digital and physical).
   - Use a simple, relatable analogy as a hook.

3. Main Concept Explanation (H2):
   - Use H2 (##).
   - Detailed, clear explanation of the primary concept.
   - **Instruction:** Use proper LaTeX-style syntax for any scientific notation or formulas. Enclose inline formulas in `$` and display formulas in `$$`.

4. Secondary Concept Explanation (H2):
   - Use H2 (##).
   - Detailed explanation of a related, supporting concept.
   - **Instruction:** Use Markdown bulleted lists or sub-headings (H3) when differentiating between types or components.

5. Code/Diagram Requirement (H2):
   - Use H2 (##).
   - Include a section for a key diagram or a conceptual code snippet (Python/ROS 2).
   - **Instruction:** If a diagram is crucial for understanding, add the tag `[Image of X]` where X is a specific, technical query (e.g., ``). For code, add a simple Python code block showing the concept.

6. Brainstorming Challenge (H2):
   - Use H2 (##).
   - Title must be "Brainstorming Challenge: [Relevant Scenario]".
   - Challenge the reader to apply the lesson's concepts.

7. Key Takeaways Table (H2):
   - Use H2 (##).
   - Title must be "Quick Reference" or "Key Concepts in Action."
   - Create a clean, **two-column Markdown table** summarizing 3-4 key points (Concept, Function, Example).

8. Self-Test Q&A (H2):
   - Use H2 (##).
   - Generate a final section with **EXACTLY 5 Questions** and their corresponding **Answers** to test core comprehension. Use bold text for the Q/A indicators.

4. NEXT LESSON TO GENERATE: [LESSON_ID] [LESSON_TITLE]


















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

---

**Implementation Phases**:  
1️⃣ FastAPI Setup → 2️⃣ Qdrant → 3️⃣ MDX Loader → 4️⃣ Chunking → 5️⃣ Embedding → 6️⃣ Ingestion → 7️⃣ Retriever → 8️⃣ Agents → 9️⃣ Routes


You are required to generate **detailed step-by-step tasks** for building a RAG backend system for the AI-native textbook. Follow the instructions below carefully.

## Instructions for AI

1. **Focus**: Generate tasks for the **backend flow** only (FastAPI, Qdrant, OpenAI Agents SDK).  

3. **System Flow**: Tasks should follow this **logical order**:
   1. Setup FastAPI project and environment  
   2. Setup Qdrant client and collections  
   3. Scan MDX files, extract content and metadata (`slug`, `chapter_number`, `chapter_title`, `lesson_id`, `section_headings`)  
   4. Chunk the content (500–1000 tokens) while preserving code blocks  
   5. Generate embeddings for each chunk using Gemini/OpenAI API  
   6. Store chunks with embeddings and metadata into Qdrant  
   7. Build retriever with prioritization logic:
      - Highlighted text first
      - Current page chunks next
      - Top 3 global chunks after  
   8. Implement RAG AI agent using the retriever  
   9. Implement Summarizer agent  
   10. Implement Reviewer/Enhance agent  
   11. Create endpoints:
       - `POST /chunks/rebuild` → trigger full ingestion  
       - `POST /rag/query` → query content  
       - `POST /agents/run` → run AI agents  
4. **Dependencies**: Ensure tasks respect dependencies (e.g., embeddings require chunking; retriever requires stored embeddings).  
5. **Outputs**: Every task should clearly state the deliverable (e.g., function, module, endpoint, Qdrant collection).  
6. **Testing**: Specify how each task can be tested or verified.


## Additional Requirements

- Prioritize **current page chunks and highlighted text** in retrieval logic  
- Ensure **FastAPI project structure** is modular: `routers`, `services`, `models`, `utils`  
- Provide clear logging and error handling for all ingestion and agent pipelines  
- Use **OpenAI Agents SDK with Gemini API key** for all AI interactions  
- Store Qdrant collection as `textbook_chunks` with proper metadata fields  

Generate a **complete list of tasks** following this structure and logical order. Each task should be actionable and ready for implementation.









Here’s a **complete developer-ready specification** for the RAG backend + frontend chatbot integration, written in your template style:

````markdown
# Feature Specification: Floating Chatbot Integration with RAG Backend

**Feature Branch**: `006-floating-chatbot-rag`  
**Created**: 2025-12-09  
**Status**: Draft  
**Input**: User description: "Integrate a floating chatbot widget on the bottom-right corner of the web page that interacts with the RAG backend system. Supports simple queries (triage agent), context-aware queries (RAG agent), and summarization of selected text (summarizer agent)."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Ask General Query (Priority: P1)

A user opens the chatbot widget and asks a general question (e.g., "What is a neural network?").  

**Why this priority**: General queries are the most common interaction and provide immediate value without requiring document context.  

**Independent Test**: Open chatbot widget, enter a general question, verify the response comes directly from the triage agent.  

**Acceptance Scenarios**:

1. **Given** the widget is collapsed, **When** user clicks to expand and types a general question, **Then** the triage agent responds in the conversation area.  
2. **Given** the widget is open, **When** user sends multiple general questions, **Then** conversation history displays all queries and responses in order.

---

### User Story 2 - Ask Contextual Query (Priority: P1)

A user selects text or references a specific page and asks a complex question requiring context from the textbook (e.g., "Explain QoS in chapter 2").  

**Why this priority**: Enables RAG functionality and ensures knowledge from documents is accessible, critical for advanced users.  

**Independent Test**: Select text/current page, enter query, and confirm triage agent delegates to RAG agent and returns a relevant answer.  

**Acceptance Scenarios**:

1. **Given** highlighted text or page context, **When** user submits query, **Then** triage agent hands off to RAG agent.  
2. **Given** RAG agent retrieves relevant chunks, **When** answer is generated, **Then** response is displayed in the conversation history with appropriate formatting.

---

### User Story 3 - Summarize Selected Text (Priority: P2)

A user highlights a portion of text on the webpage and requests a summary.  

**Why this priority**: Provides efficient content digestion; less frequent than general queries but adds high value.  

**Independent Test**: Highlight text, trigger summarization, and verify response comes from summarizer agent with concise summary.  

**Acceptance Scenarios**:

1. **Given** highlighted text, **When** user clicks "Summarize," **Then** summarizer agent returns a summary in the widget.  
2. **Given** multiple consecutive summarization requests, **When** user submits them, **Then** conversation history shows all summaries sequentially.

---

### User Story 4 - Conversation UI (Priority: P1)

The widget must support input, conversation history, typing indicator, and collapsible behavior.  

**Why this priority**: Fundamental UX requirement; ensures smooth interaction.  

**Independent Test**: Verify widget toggling, text input, typing indicator, and conversation persistence during a session.  

**Acceptance Scenarios**:

1. **Given** collapsed widget, **When** user clicks the widget icon, **Then** it expands smoothly.  
2. **Given** conversation ongoing, **When** a response is being generated, **Then** typing indicator appears.  
3. **Given** multiple queries, **When** user scrolls, **Then** conversation history scrolls properly and remains visible.

---

### Edge Cases

- What happens when API call fails or network error occurs? → Display user-friendly error in widget.  
- What happens if the query is empty or only whitespace? → Prevent submission and show validation message.  
- How does the system handle multiple simultaneous queries? → Queue requests; responses appear in order.  
- How to handle unsupported file content or missing document chunks? → Notify user: "Context not available."

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST render a floating, collapsible chatbot widget in the bottom-right corner.  
- **FR-002**: System MUST allow text input and submit queries.  
- **FR-003**: System MUST maintain conversation history per session.  
- **FR-004**: System MUST show typing indicator while awaiting AI response.  
- **FR-005**: Frontend MUST call `/agents/run` or `/rag/query` with payload:  
  ```json
  {
    "agent_type": "triage"|"summarizer",
    "query": "string",
    "highlighted_text": "optional string",
    "current_page": "optional string"
  }
````

* **FR-006**: System MUST display AI responses in conversation area.
* **FR-007**: System MUST handle errors gracefully and show notifications to the user.
* **FR-008**: Triage agent MUST decide if RAG handoff is required for complex queries.
* **FR-009**: RAG agent MUST retrieve relevant chunks using backend retriever service.
* **FR-010**: Summarizer agent MUST summarize highlighted text independently.
* **FR-011**: System MUST be responsive across desktop, tablet, and mobile devices.
* **FR-012**: API keys and sensitive data MUST be hidden; no keys exposed in frontend code.

### Key Entities *(include if feature involves data)*

* **ConversationSession**: Tracks messages, timestamps, user ID, current page, and highlighted text.
* **ChatMessage**: Represents a single message in the conversation, includes role (`user` / `agent`) and content.
* **AgentPayload**: API payload structure including agent_type, query, highlighted_text, and current_page.
* **AgentResponse**: Response from backend, includes message content and optional metadata (source page/chunk IDs).

## Success Criteria *(mandatory)*

### Measurable Outcomes

* **SC-001**: Users can submit a query and receive a response in <5 seconds.
* **SC-002**: At least 95% of general queries are answered correctly by triage agent.
* **SC-003**: RAG agent provides relevant context-aware answers for >90% of complex queries.
* **SC-004**: Summarizer agent returns concise summaries for selected text with <20% loss of meaning.
* **SC-005**: Widget displays conversation history correctly for at least 20 messages per session.
* **SC-006**: Frontend remains responsive and functional across desktop and mobile screens.
* **SC-007**: API keys remain hidden; no frontend leaks sensitive data.

```

---

This specification includes:  

- User stories with **priority, independent testability, and acceptance scenarios**  
- **Edge cases** for errors, empty input, and multiple queries  
- **Functional requirements** for frontend-backend integration, agent behavior, and security  
- **Key entities** (ConversationSession, ChatMessage, AgentPayload, AgentResponse)  
- **Measurable success criteria**  

It is **ready for developers** to implement both frontend widget and backend integration.  

If you want, I can also create a **visual diagram and API payload sequence** for the frontend-backend flow to attach to this spec for clarity.  

Do you want me to do that next?
```





Objective: Generate a detailed implementation plan to integrate the RAG backend system with a frontend floating chatbot widget (like Docsourous) that appears in the bottom-right corner of a web page.

Scope:

The chatbot should allow users to:

Ask general questions handled by a triage agent.

Ask context-heavy questions handled by a RAG agent (handoff from triage agent).

Summarize selected text using the summarizer agent.

The frontend should communicate with backend endpoints (/agents/run, /rag/query) with context info such as highlighted_text and current_page.

The system should maintain conversation history, handle errors gracefully, and provide responsive, secure, and fast responses.

Requirements for the Plan:

Divide tasks into phases (e.g., frontend setup, backend integration, agent communication, UI implementation, testing).

Each phase should include:

Purpose

Dependencies

Expected deliverables

API/UX considerations

Testing criteria

Include integration details for connecting the chatbot UI to the backend, including session management and handling agent handoffs.

Mention non-functional requirements such as responsiveness, security, and error handling.

Provide the plan in a developer-friendly, actionable format, suitable for use in project management or sprint planning.

Output: A clear, phased implementation plan with tasks, dependencies, expected deliverables, and testing criteria for each phase, enabling frontend and backend developers to implement the chatbot integration efficiently