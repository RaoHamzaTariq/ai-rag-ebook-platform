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