# Data Model: Better Auth Integration with Neon PostgreSQL

## Entity: User
**Description**: Represents authenticated users in the system (integrated with Better Auth)

**Fields**:
- `id`: UUID (Primary Key, from Better Auth), not null
- `email`: VARCHAR(255), unique, not null (from Better Auth)
- `name`: VARCHAR(255), nullable (from Better Auth)
- `created_at`: TIMESTAMP, default: now()
- `updated_at`: TIMESTAMP, default: now()
- `is_active`: BOOLEAN, default: true

**Relationships**:
- One-to-many with Conversation (user has many conversations)
- One-to-many with Message (user has many messages)

## Entity: Conversation
**Description**: Groups related messages into logical conversations

**Fields**:
- `id`: UUID (Primary Key, default: gen_random_uuid())
- `user_id`: UUID (Foreign Key to users.id), not null
- `title`: VARCHAR(255), not null
- `created_at`: TIMESTAMP, default: now()
- `updated_at`: TIMESTAMP, default: now()
- `is_active`: BOOLEAN, default: true

**Relationships**:
- Many-to-one with User (belongs to one user)
- One-to-many with Message (conversation has many messages)

## Entity: Message
**Description**: Stores individual messages in conversations

**Fields**:
- `id`: UUID (Primary Key, default: gen_random_uuid())
- `conversation_id`: UUID (Foreign Key to conversations.id), not null
- `user_id`: UUID (Foreign Key to users.id), not null
- `role`: VARCHAR(20) ('user' or 'assistant'), not null
- `content`: TEXT, not null
- `sources`: JSONB, nullable (for RAG sources)
- `timestamp`: TIMESTAMP, default: now()
- `agent_type`: VARCHAR(50), nullable (for tracking which agent was used)

**Relationships**:
- Many-to-one with Conversation (belongs to one conversation)
- Many-to-one with User (belongs to one user)

## Database Indexes
**users table**:
- `idx_users_email`: Index on email column for fast user lookup

**conversations table**:
- `idx_conversations_user_id`: Index on user_id for efficient user conversation queries

**messages table**:
- `idx_messages_conversation_timestamp`: Composite index on conversation_id and timestamp for chronological message retrieval
- `idx_messages_user_id_timestamp`: Index on user_id and timestamp for user message queries

## Validation Rules
- Email format validation for User.email
- Role must be either 'user' or 'assistant' for Message.role
- Required fields validation for all non-nullable fields
- Foreign key constraints to maintain referential integrity

## State Transitions
- User can be activated/deactivated via is_active field
- Conversations can be marked as inactive but preserved for history
- Messages are immutable once created (no updates/deletions)

## Integration Notes
- User data is primarily managed by Better Auth
- Only user_id, email, and name are stored in our database (synchronized from Better Auth)
- Session management is handled by Better Auth cookies
- JWT tokens can be obtained via Better Auth JWT plugin if needed for external services