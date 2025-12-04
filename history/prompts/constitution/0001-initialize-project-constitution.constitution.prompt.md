---
id: 0001
title: Initialize Project Constitution
stage: constitution
date: 2025-12-04
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: main
user: human
command: /sp.constitution
labels: ["constitution", "initialization"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  null
---

## Prompt

```text
Create the constitution using the below context

Project Constitution — AI-Native eBook: Physical AI & Humanoid Robotics

This Constitution defines the non-negotiable rules for the entire project:
the eBook, RAG system, backend, frontend, reusable intelligence, and all generated artifacts.

1. Purpose

Create an AI-native, interactive textbook titled Physical AI & Humanoid Robotics, supported by a high-quality RAG system that helps learners understand
robotics, ROS 2, Gazebo, Isaac, and VLA concepts through accurate AI-assisted answers.

2. Content Standards

Writing must be clear, structured, accurate, and educational.
Maintain consistent terminology across robotics and AI topics.
Provide explanations suited for students and self-learners.
No unnecessary complexity; prioritize clarity and correctness.

3. RAG & AI Response Rules

All chatbot answers must be grounded strictly in retrieved book content.
Every answer must include chapter/section citations.
Absolutely no hallucinated or fabricated content.

4. Technical Standards

Frontend: Docusaurus (TypeScript) + BetterAuth
Backend: FastAPI + NeonDB + Qdrant + OpenAI Agents SDK.
Code must be modular, typed, and maintainable across the project.
All workflows must support deterministic RAG ingestion.

5. Reusable Intelligence Standards

Subagents and skills must be single-purpose, reusable, and well-scoped.
Prompts must be consistent, concise, and follow naming conventions.

6. Personalization & Localization

Personalization must respect user background, learning level, and preferences.
Urdu translations must preserve meaning and technical accuracy.

7. Safety & Ethics

No unsafe robotics instructions.
All generated content must follow responsible AI and robotics practices.

8. Enforcement

This Constitution applies to every chapter, feature, API, subagent, and skill, and overrides all conflicting instructions.
```

## Response snapshot

Initialized the project constitution with all specified principles and governance details.

## Outcome

- ✅ Impact: Project constitution file created and updated successfully.
- 🧪 Tests: No tests were run for this operation.
- 📁 Files: One file was modified: .specify/memory/constitution.md
- 🔁 Next prompts: Continue with project development based on the constitution.
- 🧠 Reflection: The constitution was successfully created based on user input.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
