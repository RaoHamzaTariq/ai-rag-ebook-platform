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