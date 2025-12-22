# **Data Model: BetterAuth Integration with Neon PostgreSQL**

## **Entity: User**

**Description:**
Represents authenticated users in the system — synchronized from BetterAuth (via JWT payload).

**Fields:**

* `id`: UUID (Primary Key, from BetterAuth JWT “sub” claim), not null
* `email`: VARCHAR(255), unique, not null (from BetterAuth JWT payload)
* `name`: VARCHAR(255), nullable (from BetterAuth JWT payload)
* `created_at`: TIMESTAMP, default: now()
* `updated_at`: TIMESTAMP, default: now()
* `is_active`: BOOLEAN, default: true

**Relationships:**

* One‑to‑many with `Conversation` (a user has many conversations)
* One‑to‑many with `Message` (a user authored many messages)


## **Entity: Conversation**

**Description:**
A logical grouping of messages (chat sessions) for a user.

**Fields:**

* `id`: UUID (Primary Key, default: gen_random_uuid()), not null
* `user_id`: UUID (Foreign Key to `users.id`), not null
* `title`: VARCHAR(255), not null (optional chat title or first message preview)
* `created_at`: TIMESTAMP, default: now()
* `updated_at`: TIMESTAMP, default: now()
* `is_active`: BOOLEAN, default: true

**Relationships:**

* Many‑to‑one with `User` (each conversation belongs to one user)
* One‑to‑many with `Message` (conversation has many messages)

## **Entity: Message**

**Description:**
Stores individual messages in a conversation — both user input and assistant output.

**Fields:**

* `id`: UUID (Primary Key, default: gen_random_uuid()), not null
* `conversation_id`: UUID (Foreign Key to `conversations.id`), not null
* `user_id`: UUID (Foreign Key to `users.id`), not null
* `role`: VARCHAR(20) (`'user'` or `'assistant'`), not null
* `content`: TEXT, not null
* `sources`: JSONB, nullable (for storing RAG source metadata — e.g., docs/pages referenced)
* `timestamp`: TIMESTAMP, default: now(), not null
* `agent_type`: VARCHAR(50), nullable (indicates which AI agent processed this message, if applicable)

**Relationships:**

* Many‑to‑one with `Conversation`
* Many‑to‑one with `User`


## **Database Indexes**

To support fast queries and scalable performance:

**`users` table:**

* `idx_users_email`: Index on `email` for fast lookup

**`conversations` table:**

* `idx_conversations_user_id`: Index on `user_id` for efficient user conversation retrieval

**`messages` table:**

* `idx_messages_conversation_timestamp`: Composite index on `conversation_id` and `timestamp` — supports ordered retrieval per conversation
* `idx_messages_user_id_timestamp`: Index on `user_id` and `timestamp` — supports user‑wide message queries


## **Validation Rules**

* **User.email** — must be a valid email format and unique
* **Message.role** — only accepts two values: `'user'` or `'assistant'`
* **Non‑nullable fields** must contain valid data
* **Foreign key constraints** ensure referential integrity

## **State Transitions**

* **User**: can be activated or deactivated through `is_active`; deactivated users cannot chat
* **Conversation**: can be marked inactive (e.g., archived) while preserving history
* **Messages**: are **immutable** once created — no updates or deletions to preserve audit and context


## **Integration Notes**

* **User data** (id, email, name) comes from BetterAuth JWT tokens verified by FastAPI via JWKS endpoint.
* Only essential fields (id, email, name) are stored locally — BetterAuth manages actual auth.
* **Session state** is not stored server‑side; backend verifies JWT tokens per request.
* JWT tokens can be obtained from BetterAuth using the JWT plugin and the `authClient.token()` method in frontend.
* Chat data and history linkage rely on the user id extracted from the JWT’s `sub` claim during backend validation.
* Flexible JSONB (`sources`) allows storing RAG metadata (text snippet references, URLs, doc IDs, etc) without rigid schema changes.