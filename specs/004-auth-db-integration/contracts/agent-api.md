# API Contract: AI Agent Runner

**Endpoint**: `POST /agents/run`
**Authentication**: Required (JWT Bearer Token or X-User-ID)

## **Request Body (JSON)**

```json
{
  "agent_type": "rag",
  "query": "What are the core concepts of Physical AI?",
  "current_page": "5",
  "highlighted_text": "embodied intelligence",
  "session_id": "optional-uuid-for-conversation"
}
```

- `agent_type`: "triage", "summarizer", or "rag".
- `query`: The user's input string.
- `current_page`: (Optional) Current chapter/page context.
- `highlighted_text`: (Optional) Specifically selected text from the UI.
- `session_id`: (Optional) Existing conversation ID. If omitted, a new one is created.

## **Response Body (JSON)**

```json
{
  "message": "**Physical AI** focuses on... [Markdown Content]",
  "sources": [
    {
      "slug": "chapter-1-foundations",
      "chapter_number": "1",
      "page_number": 12,
      "snippet": "Physical AI involves the integration of..."
    }
  ],
  "agent_used": "rag",
  "timestamp": "2025-12-22T15:00:00Z"
}
```

- `message`: The AI-generated response in GFM Markdown format.
- `sources`: Array of citation objects used for the response.
- `agent_used`: Identification of which agent handled the request.

## **Error Responses**

- `401 Unauthorized`: Authentication missing or invalid.
- `500 Internal Server Error`: AI pipeline or database failure.
