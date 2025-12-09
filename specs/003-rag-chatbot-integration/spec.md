# Feature Specification: RAG Chatbot Integration with Backend

**Feature Branch**: `003-rag-chatbot-integration`  
**Created**: 2025-12-09  
**Status**: Draft  
**Input**: Objective: Generate a specification for integrating the RAG backend with a frontend chatbot that appears as a floating widget in the bottom-right corner of a web page, similar to Docsourous. The chatbot should support: Asking general queries handled by a triage agent. Complex queries that require document context handled by a RAG agent (handoff from triage agent). Summarizing selected text using a summarizer agent. Requirements: Chatbot UI: Collapsible floating widget, input box, conversation history, typing indicator. Integration: Frontend calls backend endpoints (/agents/run, /rag/query) with appropriate payload including optional highlighted_text and current_page. Agents Behavior: Triage agent handles simple queries and decides if RAG agent handoff is needed. RAG agent retrieves relevant chunks using the retriever and generates answers. Summarizer agent works independently for selected text. Response Handling: Display AI responses in the widget, handle errors gracefully. Non-functional: Responsive, secure (API keys hidden), fast response time (~2–5s). Deliverables: Detailed UI behavior, frontend-backend integration, API payload/response structure, session handling, and error scenarios. Output: A clear, developer-ready specification for implementing the chatbot integration, suitable for frontend and backend developers.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Ask General Query (Priority: P1)

A user opens the chatbot widget and asks a general question (e.g., "What is a neural network?").  

**Why this priority**: General queries are the most common interaction and provide immediate value without requiring document context.  
**Independent Test**: Open chatbot widget, enter a general question, verify the response comes directly from the triage agent.  

**Acceptance Scenarios**:

1. **Given** the widget is collapsed, **When** user clicks to expand and types a general question, **Then** the triage agent responds in the conversation area.  
2. **Given** the widget is open, **When** user sends multiple general questions, **Then** conversation history displays all queries and responses in order.


### User Story 2 - Ask Contextual Query (Priority: P1)

A user selects text or references a specific page and asks a complex question requiring context from the textbook (e.g., "Explain QoS in chapter 2").  

**Why this priority**: Enables RAG functionality and ensures knowledge from documents is accessible, critical for advanced users.  

**Independent Test**: Select text/current page, enter query, and confirm triage agent delegates to RAG agent and returns a relevant answer.  

**Acceptance Scenarios**:

1. **Given** highlighted text or page context, **When** user submits query, **Then** triage agent hands off to RAG agent.  
2. **Given** RAG agent retrieves relevant chunks, **When** answer is generated, **Then** response is displayed in the conversation history with appropriate formatting.


### User Story 3 - Summarize Selected Text (Priority: P2)

A user highlights a portion of text on the webpage and requests a summary.  

**Why this priority**: Provides efficient content digestion; less frequent than general queries but adds high value.  

**Independent Test**: Highlight text, trigger summarization, and verify response comes from summarizer agent with concise summary.  

**Acceptance Scenarios**:

1. **Given** highlighted text, **When** user clicks "Summarize," **Then** summarizer agent returns a summary in the widget.  
2. **Given** multiple consecutive summarization requests, **When** user submits them, **Then** conversation history shows all summaries sequentially.


### User Story 4 - Conversation UI (Priority: P1)

The widget must support input, conversation history, typing indicator, and collapsible behavior.  

**Why this priority**: Fundamental UX requirement; ensures smooth interaction.  

**Independent Test**: Verify widget toggling, text input, typing indicator, and conversation persistence during a session.  

**Acceptance Scenarios**:

1. **Given** collapsed widget, **When** user clicks the widget icon, **Then** it expands smoothly.  
2. **Given** conversation ongoing, **When** a response is being generated, **Then** typing indicator appears.  
3. **Given** multiple queries, **When** user scrolls, **Then** conversation history scrolls properly and remains visible.

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

  {
    "agent_type": "triage"|"summarizer",
    "query": "string",
    "highlighted_text": "optional string",
    "current_page": "optional string"
  }

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

