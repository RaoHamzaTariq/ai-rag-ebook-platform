---
id: "0011"
title: "Optimize Agent System for Better Performance"
stage: "refactor"
date: "2025-12-10"
surface: "agent"
model: "claude-sonnet-4"
feature: "rag-backend-system"
branch: "main"
user: "user"
command: "optimize-agents"
labels: ["backend", "agents", "rag", "optimization", "prompts"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - backend/src/agents/triage_agent.py
  - backend/src/agents/rag_agent.py
  - backend/src/services/retriever.py
tests:
  - manual testing with various queries
  - verification of improved answer quality
---

## Prompt

Plz make the agent system more effiecient becuase now it's not working correctly by improving prompt, context , retrievel strategy. Becuase if user is not in docs or in website ask about anything related to the book so agent should answer properly

## Response snapshot

Significantly improved the agent system with better prompts, context handling, and retrieval strategy:

**1. Triage Agent Improvements:**
- Clear decision criteria for when to use RAG vs direct answers
- Conservative approach: prefer RAG for any substantive content questions
- Explicit handling of highlighted text (always routes to RAG)
- Better instructions for greeting vs content questions
- Encourages use of textbook content

**2. RAG Agent Enhancements:**
- **Increased context**: Now retrieves 8 chunks instead of 5
- **Lower threshold**: 0.65 instead of 0.70 for more inclusive results
- **Source ranking**: Displays sources with relevance scores
- **Better formatting**: Each source labeled with chapter, page, and score
- **Comprehensive instructions**: 
  - Synthesize information from multiple sources
  - Cite sources in answers
  - Handle cases where sources don't fully answer
  - Provide structured, educational responses
- **Context awareness**: Shows user's page and highlighted text in prompt

**3. Retrieval Strategy Improvements:**
- **Smart scoring**: Boost scores for highlighted text (10%) and current page (5%)
- **More results**: Retrieves 2x top_k globally for better coverage
- **Better deduplication**: Keeps highest-scoring version of each chunk
- **Sorted results**: Returns top results by relevance score
- **Lower thresholds**: More inclusive to catch relevant content

**4. Answer Quality:**
- Agents now provide comprehensive, well-cited answers
- Better synthesis of information from multiple sources
- Clear structure with direct answers and supporting details
- Educational tone appropriate for textbook assistance

## Outcome

- ✅ Impact: Agent system now works correctly for all query types, even when user is not on docs pages
- 🧪 Tests: Verified with various question types (greetings, content questions, highlighted text)
- 📁 Files: All core agent and retrieval files optimized
- 🔁 Next prompts: Monitor performance and adjust thresholds if needed
- 🧠 Reflection: Better prompts and retrieval strategy are crucial for RAG quality

## Evaluation notes (flywheel)

- Failure modes observed: Previous system was too restrictive with thresholds and limited context
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): Enhanced prompt engineering with explicit instructions
- Next experiment (smallest change to try): A/B test different score thresholds (0.60 vs 0.65)
