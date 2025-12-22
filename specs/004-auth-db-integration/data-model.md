# Data Model Specification: Auth & Chat History

This document outlines the database schema and data relationships for the AI RAG Ebook Platform's authentication and conversation history system.

## **Database Schema Overview**

The system uses a PostgreSQL database with a shared schema between the **Better Auth Server** and the **FastAPI Backend**. This allows the backend to perform high-performance joins and filtered queries on user-specific chat history.

## **Entity Relationship Diagram (Conceptual)**

- **User** (1:N) -> **Conversation**
- **Conversation** (1:N) -> **Message**

## **Table Definitions**

### **1. User Table (`user`)**
Managed primarily by Better Auth but synced/indexed by the FastAPI Backend.

| Column | Type | Primary Key | Description |
| :--- | :--- | :---: | :--- |
| `id` | `VARCHAR` | YES | Unique User ID (Base62 string from Better Auth) |
| `email` | `VARCHAR` | NO | User's email address (Unique) |
| `name` | `VARCHAR` | NO | User's display name |
| `emailVerified` | `BOOLEAN` | NO | Verification status |
| `image` | `VARCHAR` | NO | Profile picture URL |
| `createdAt` | `TIMESTAMP` | NO | UTC creation time |
| `updatedAt` | `TIMESTAMP` | NO | UTC last update time |
| `role` | `VARCHAR` | NO | RBAC role (default: "user") |

**Indexes:**
- `idx_users_email`: For fast login and lookup.

---

### **2. Conversation Table (`conversation`)**
Groups individual chat interactions into logical threads.

| Column | Type | Primary Key | Description |
| :--- | :--- | :---: | :--- |
| `id` | `VARCHAR` | YES | UUID string uniquely identifying the conversation |
| `user_id` | `VARCHAR` | NO | Foreign Key to `user.id` |
| `title` | `VARCHAR` | NO | Auto-generated title from the first query |
| `created_at` | `TIMESTAMP` | NO | UTC creation time |
| `updated_at` | `TIMESTAMP` | NO | Last interaction time |
| `is_active` | `BOOLEAN` | NO | Soft-delete flag (default: true) |

**Indexes:**
- `idx_conversations_user_id`: For listing history for a specific user.

---

### **3. Message Table (`message`)**
Stores individual turns in a dialogue, including RAG metadata.

| Column | Type | Primary Key | Description |
| :--- | :--- | :---: | :--- |
| `id` | `VARCHAR` | YES | UUID string uniquely identifying the message |
| `conversation_id` | `VARCHAR` | NO | Foreign Key to `conversation.id` |
| `user_id` | `VARCHAR` | NO | Foreign Key to `user.id` (for direct user lookup) |
| `role` | `VARCHAR` | NO | Either "user" or "assistant" |
| `content` | `TEXT` | NO | The message body (supports Markdown) |
| `sources` | `JSON` | NO | Array of source objects (slug, chapter, snippet) |
| `timestamp` | `TIMESTAMP` | NO | UTC time of message |
| `agent_type` | `VARCHAR` | NO | Which agent generated the response (e.g., "rag") |

**Indexes:**
- `idx_messages_conversation_timestamp`: For retrieving chat history in chronologial order.
- `idx_messages_user_id_timestamp`: For user-wide message auditing.

## **Data Integrity Decisions**

1. **String-based Identifiers**: We use `VARCHAR` (String) for all primary and foreign keys. This ensures 100% compatibility with Better Auth's internal Base62 ID generation and avoids "bad hex string" errors in SQLModel.
2. **JSON Source Storage**: RAG sources are stored as a JSON array within the `Message` table. This allows for flexible metadata (like relevancy scores or snippets) without requiring a heavy many-to-many relationship for document fragments.
3. **UTC Everywhere**: All timestamps are stored and retrieved in UTC to ensure consistency across different user timezones.
4. **Foreign Key Enforcement**: Conversations and messages are strictly linked to valid user IDs to prevent orphaned data and ensure data privacy.