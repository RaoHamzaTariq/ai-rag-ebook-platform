# API Contract: History & Conversations

**Base Path**: `/conversations`
**Authentication**: Required (JWT Bearer Token)

## **1. List Conversations**
**Endpoint**: `GET /`

**Response**:
```json
[
  {
    "id": "conv_uuid",
    "title": "Core Concepts of AI",
    "updated_at": "2025-12-22T10:00:00Z"
  }
]
```

## **2. Get Conversation History**
**Endpoint**: `GET /{conversation_id}/messages`

**Response**:
```json
[
  {
    "id": "msg_uuid",
    "role": "user",
    "content": "Tell me about robotics",
    "timestamp": "2025-12-22T09:55:00Z"
  },
  {
    "id": "msg_uuid_2",
    "role": "assistant",
    "content": "Robotics involves...",
    "sources": [...],
    "timestamp": "2025-12-22T09:55:05Z"
  }
]
```

## **3. Create Message**
**Endpoint**: `POST /{conversation_id}/messages`

**Request**:
```json
{
  "role": "user",
  "content": "Next question..."
}
```

## **Security Note**
All endpoints are scoped to the `user_id` extracted from the JWT. Attempting to access a `conversation_id` belonging to another user will return a `404 Not Found` or `401 Unauthorized` for privacy.
