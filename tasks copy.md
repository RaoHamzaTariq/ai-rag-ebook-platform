# RAG Backend System Development Tasks

## 1. Setup FastAPI Project and Environment
*   **Task Name**: Setup FastAPI Project
*   **Priority**: P1
*   **Description / Instructions**: Initialize a new FastAPI project, set up a virtual environment, install necessary dependencies (FastAPI, Uvicorn, Qdrant-client, OpenAI, Pydantic), and configure basic project structure (`routers`, `services`, `models`, `utils`).
*   **Dependencies**: None
*   **Expected Output / Deliverable**: A running FastAPI application with a basic `main.py` and structured directories.
*   **Endpoint / Route**: `/` (root endpoint for basic health check)
*   **Testing Criteria**: Run `uvicorn main:app --reload` and access `http://localhost:8000`. Verify basic FastAPI boilerplate response.

## 2. Setup Qdrant Client and Collections
*   **Task Name**: Configure Qdrant Client and Collection
*   **Priority**: P1
*   **Description / Instructions**: Initialize Qdrant client, create a new collection named `textbook_chunks` with appropriate vector size (e.g., 1536 for OpenAI embeddings) and schema for metadata fields (`slug`, `chapter_number`, `chapter_title`, `lesson_id`, `section_headings`, `highlighted_text`, `page_number`).
*   **Dependencies**: Task 1 (FastAPI Setup)
*   **Expected Output / Deliverable**: Qdrant client initialized and `textbook_chunks` collection created.
*   **Endpoint / Route**: None (internal service)
*   **Testing Criteria**: Verify collection creation via Qdrant's admin interface or a simple Qdrant client script to list collections.

## 3. Scan MDX files, extract content and metadata
*   **Task Name**: MDX Content and Metadata Extraction
*   **Priority**: P1
*   **Description / Instructions**: Develop a service to scan MDX files from a specified directory, parse their content, and extract structured metadata: `slug`, `chapter_number`, `chapter_title`, `lesson_id`, `section_headings`. Implement error handling for file parsing.
*   **Dependencies**: Task 1 (FastAPI Setup)
*   **Expected Output / Deliverable**: A Python function/service that takes an MDX file path and returns content and a dictionary of extracted metadata.
*   **Endpoint / Route**: None (internal service for ingestion pipeline)
*   **Testing Criteria**: Create a unit test for the extraction service using a mock MDX file to ensure correct content and metadata are extracted.

## 4. Chunk the content while preserving code blocks
*   **Task Name**: Content Chunking with Code Preservation
*   **Priority**: P1
*   **Description / Instructions**: Implement a chunking mechanism that breaks down the extracted content into chunks of 500-1000 tokens. Crucially, ensure that code blocks are identified and kept intact within single chunks, or at least handled gracefully to prevent splitting within a code block.
*   **Dependencies**: Task 3 (Content and Metadata Extraction)
*   **Expected Output / Deliverable**: A Python function that takes raw content and returns a list of text chunks.
*   **Endpoint / Route**: None (internal service for ingestion pipeline)
*   **Testing Criteria**: Unit tests with sample content including code blocks to verify chunk sizes and code block integrity.

## 5. Generate embeddings for each chunk using Gemini/OpenAI API
*   **Task Name**: Generate Embeddings
*   **Priority**: P1
*   **Description / Instructions**: Integrate with the Gemini/OpenAI API to generate vector embeddings for each text chunk. Handle API key management securely (e.g., environment variables) and implement retry mechanisms for API calls.
*   **Dependencies**: Task 4 (Content Chunking)
*   **Expected Output / Deliverable**: A Python function that takes a list of text chunks and returns a list of corresponding embedding vectors.
*   **Endpoint / Route**: None (internal service for ingestion pipeline)
*   **Testing Criteria**: Call the function with sample chunks and verify that it returns vectors of the expected dimension.

## 6. Store chunks with embeddings and metadata into Qdrant
*   **Task Name**: Store Chunks in Qdrant
*   **Priority**: P1
*   **Description / Instructions**: Develop a service to store the generated chunks, their embeddings, and associated metadata (from Task 3) into the `textbook_chunks` Qdrant collection. Ensure metadata fields are correctly indexed for efficient filtering during retrieval.
*   **Dependencies**: Task 2 (Qdrant Setup), Task 5 (Generate Embeddings)
*   **Expected Output / Deliverable**: A Python function/service to ingest a chunk with its embedding and metadata into Qdrant.
*   **Endpoint / Route**: None (internal service for ingestion pipeline)
*   **Testing Criteria**: Ingest a few sample chunks and then query Qdrant to verify that the chunks, embeddings, and metadata are correctly stored and retrievable.

## 7. Build retriever with prioritization logic
*   **Task Name**: Implement Prioritized Retriever
*   **Priority**: P1
*   **Description / Instructions**: Design and implement a retriever service that queries the `textbook_chunks` Qdrant collection. The retrieval logic must prioritize results based on:
    1.  Highlighted text matches (if available in query).
    2.  Chunks from the current page/context.
    3.  Top 3 global chunks (most relevant from the entire collection).
    This implies modifying Qdrant queries to include filtering by metadata fields like `page_number` and `highlighted_text` presence, and then combining results.
*   **Dependencies**: Task 6 (Store Chunks in Qdrant)
*   **Expected Output / Deliverable**: A Python function that takes a query, optional current page context, and optional highlighted text, and returns a prioritized list of relevant chunks.
*   **Endpoint / Route**: None (internal service for RAG agent)
*   **Testing Criteria**: Unit tests with various query scenarios (with/without highlighted text, with/without current page context) to ensure correct prioritization and retrieval.

## 8. Implement RAG AI agent using the retriever
*   **Task Name**: Develop RAG AI Agent
*   **Priority**: P1
*   **Description / Instructions**: Implement a RAG (Retrieval Augmented Generation) AI agent using the OpenAI Agents SDK and the retriever built in Task 7. The agent should take a user query, retrieve relevant chunks, and then use a Gemini model (via OpenAI API key) to generate a coherent and contextually relevant response based on the retrieved information.
*   **Dependencies**: Task 7 (Prioritized Retriever)
*   **Expected Output / Deliverable**: A Python class/function for the RAG agent that takes a query and returns a generated response.
*   **Endpoint / Route**: None (internal service for `/agents/run`)
*   **Testing Criteria**: Integration tests where the RAG agent is queried with sample questions, and the generated responses are evaluated for relevance and accuracy based on the retrieved chunks.

## 9. Implement Summarizer agent
*   **Task Name**: Develop Summarizer Agent
*   **Priority**: P2
*   **Description / Instructions**: Implement a separate AI agent using the OpenAI Agents SDK and Gemini API key for summarization. This agent should be capable of summarizing longer text passages or a set of retrieved chunks.
*   **Dependencies**: OpenAI Agents SDK setup (from Task 8 implicitly)
*   **Expected Output / Deliverable**: A Python class/function for the Summarizer agent that takes text and returns a summary.
*   **Endpoint / Route**: None (internal service for `/agents/run`)
*   **Testing Criteria**: Unit tests with various text inputs to verify summary quality and conciseness.

## 10. Implement Reviewer/Enhance agent
*   **Task Name**: Develop Reviewer/Enhance Agent
*   **Priority**: P2
*   **Description / Instructions**: Implement a separate AI agent using the OpenAI Agents SDK and Gemini API key for reviewing or enhancing text. This agent could, for example, rephrase text, check for grammar, or expand on ideas.
*   **Dependencies**: OpenAI Agents SDK setup (from Task 8 implicitly)
*   **Expected Output / Deliverable**: A Python class/function for the Reviewer/Enhance agent that takes text and returns an enhanced version.
*   **Endpoint / Route**: None (internal service for `/agents/run`)
*   **Testing Criteria**: Unit tests with sample text inputs to evaluate the agent's ability to review or enhance content effectively.

## 11. Create API Endpoints
*   **Task Name**: Implement API Endpoints
*   **Priority**: P1
*   **Description / Instructions**: Create the following FastAPI endpoints:
    *   `POST /chunks/rebuild`: Triggers the full ingestion pipeline (scanning, chunking, embedding, storing).
    *   `POST /rag/query`: Accepts a user query, potentially current page context and highlighted text, and returns the RAG agent's response.
    *   `POST /agents/run`: A generic endpoint to run different AI agents (RAG, Summarizer, Reviewer/Enhance) based on a payload, specifying which agent to run and its inputs.
*   **Dependencies**: Task 6 (Store Chunks), Task 8 (RAG Agent), Task 9 (Summarizer Agent), Task 10 (Reviewer/Enhance Agent)
*   **Expected Output / Deliverable**: Functional FastAPI endpoints as described.
*   **Endpoint / Route**: `/chunks/rebuild`, `/rag/query`, `/agents/run`
*   **Testing Criteria**:
    *   `POST /chunks/rebuild`: Send a POST request and verify logs for ingestion pipeline execution.
    *   `POST /rag/query`: Send a POST request with a query and verify a relevant response from the RAG agent.
    *   `POST /agents/run`: Send POST requests to trigger Summarizer and Reviewer/Enhance agents with appropriate payloads and verify their outputs.
