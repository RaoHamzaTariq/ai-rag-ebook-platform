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





