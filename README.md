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