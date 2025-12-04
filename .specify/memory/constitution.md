<!-- Sync Impact Report:
Version change: 0.1.0 → 0.2.0
Modified principles:
  - Data Security & Privacy (integrated into Safety & Ethics)
  - Scalability & Performance (no direct equivalent, implicit in other principles)
  - Code Maintainability & Modularity (renamed to Reusability & Modularity)
  - User Experience (UX) (renamed to User-Centric Design)
  - AI Ethics & Citation (renamed to Accuracy & Truthfulness, Safety & Ethics)
Added sections:
  - Accuracy & Truthfulness
  - Consistency & Clarity
  - Reusability & Modularity
  - User-Centric Design
Removed sections: None (principles were refactored/merged)
Templates requiring updates:
  - .specify/templates/plan-template.md: ⚠ pending
  - .specify/templates/spec-template.md: ⚠ pending
  - .specify/templates/tasks-template.md: ⚠ pending
  - .specify/templates/commands/*.md: ⚠ pending
Follow-up TODOs: None
-->
# AI-Native eBook: Physical AI & Humanoid Robotics Constitution

## Core Principles

### I. Accuracy & Truthfulness
All content, answers, and code generated or used within the project MUST be factually correct, verifiable, and strictly aligned with the book content. There shall be absolutely no hallucinations, fabricated information, or misleading statements. Chatbot responses MUST include explicit citations (e.g., chapter/section, page number, source link) to ensure verifiability and respect intellectual property.

### II. Consistency & Clarity
Terminology, style, tone, and formatting MUST be uniform across all project artifacts, including eBook chapters, chatbot responses, AI agent prompts, and user interface elements. Explanations and content MUST be concise, unambiguous, and learner-friendly, catering to students and self-learners of robotics, ROS 2, Gazebo, Isaac, and VLA concepts.

### III. Safety & Ethics
No content or guidance provided by the platform, especially concerning robotics, MUST be unsafe or potentially harmful. All AI behavior and generated content MUST adhere to responsible AI principles, proactively protecting user privacy, actively avoiding bias, and ensuring inclusivity. Data handling, particularly sensitive user information, MUST be secure, encrypted, and compliant with privacy regulations.

### IV. Reusability & Modularity
All AI agents, subagents, and skills developed for this project MUST be designed to be modular, single-purpose, and reusable across multiple features, chapters, or learning contexts. Code, prompts, and configurations MUST be well-scoped, independently testable, and maintainable, promoting efficient development and consistent behavior.

### V. User-Centric Design
All AI behavior, platform features, and design choices MUST prioritize optimal learning outcomes, usability, and accessibility for the end-user. This includes personalized learning experiences adapted to user background and learning level, as well as accurate localization for supported languages (e.g., Urdu), ensuring a seamless and engaging user journey.

## Technology Stack Context

**Frontend**: Docusaurus (TypeScript) with i18n for multi-language support.
**Backend**: FastAPI (Python) for robust AI integration and API services.
**Database**: Neon DB for structured data, Qdrant for vector embeddings.
**AI System**: OpenAI Agents SDK for Retrieval-Augmented Generation (RAG).
**Deployment**: GitHub Pages for frontend, Railway with Docker for backend.

## Constraints & Considerations

- **Language Support**: Initially, only handle eBooks in supported languages (English, Urdu).
- **Chatbot References**: The chatbot MUST provide references for all answers.
- **Persistent History**: Conversation history MUST be persistent and tied to user profiles.
- **Best Practices**: Adhere to best practices for API design, frontend routing, and modularization.

## Goals & Expected Outcomes

- **Functional Platform**: A fully functional AI-powered eBook platform.
- **Accurate AI**: Accurate, context-aware chatbot responses.
- **Seamless UX**: A seamless, multilingual user experience.
- **Secure & Scalable**: A secure and scalable system architecture.

## Governance

This Constitution supersedes all other practices. Amendments require thorough documentation, approval, and a clear migration plan. All Pull Requests and code reviews MUST verify compliance with these principles. Complexity MUST always be justified. These rules are mandatory for all AI agents, subagents, skills, and human contributors, overriding any conflicting prompts, instructions, or specifications in the project.

**Version**: 0.2.0 | **Ratified**: 2025-12-04 | **Last Amended**: 2025-12-04
