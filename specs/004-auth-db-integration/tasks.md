# Tasks: Better Auth Integration with Neon PostgreSQL for Chat History

**Feature**: Add authentication using Better Auth (frontend), protect AI chat endpoints, store user accounts and conversation history in Neon DB
**Date**: 2025-12-13
**Spec**: `/specs/004-auth-db-integration/spec.md`
**Plan**: `/specs/004-auth-db-integration/plan.md`

## Phase 1: Setup / Foundational

### Goal
Initialize project structure, configure environment variables, and set up foundational components for authentication and database integration.

### Independent Test Criteria
- Project structure is properly configured
- Environment variables are set up correctly
- Basic logging and middleware scaffolding is in place

### Implementation Tasks

- [ ] T001 Create project structure for authentication integration per implementation plan
- [ ] T002 Set up Better Auth environment variables in frontend and backend
- [ ] T003 Configure Neon PostgreSQL connection settings in backend
- [ ] T004 Initialize authentication middleware scaffolding in backend
- [ ] T005 Set up logging configuration for authentication events
- [ ] T006 [P] Install Better Auth dependencies in frontend
- [ ] T007 [P] Install database dependencies in backend (asyncpg, SQLModel)
- [ ] T008 Create configuration files for auth and database settings

## Phase 2: Database (Neon)

### Goal
Create database schema for users, conversations, and messages with proper relationships and indexes.

### Independent Test Criteria
- Database tables are created with proper schema
- Relationships between entities are established
- Indexes are created for optimal query performance

### Implementation Tasks

- [ ] T009 Create User model in backend/src/models/user.py
- [ ] T010 Create Conversation model in backend/src/models/conversation.py
- [ ] T011 Create Message model in backend/src/models/message.py
- [ ] T012 [P] Set up database connection pooling in backend/src/config/database.py
- [ ] T013 Create database migration scripts for auth tables
- [ ] T014 Implement database initialization in backend/src/main.py
- [ ] T015 Create indexes for efficient querying in database models
- [ ] T016 Test database connection and schema creation

## Phase 3: Backend Auth Middleware

### Goal
Implement JWT token verification middleware to authenticate requests using Better Auth tokens.

### Independent Test Criteria
- JWT tokens from Better Auth are properly verified
- Invalid tokens are rejected with appropriate error responses
- Authenticated user context is available to protected endpoints

### Implementation Tasks

- [ ] T017 Create JWT verification middleware in backend/src/middleware/auth_middleware.py
- [ ] T018 Implement JWKS fetching and caching for Better Auth tokens
- [ ] T019 Create dependency for authenticated user in backend/src/dependencies/auth.py
- [ ] T020 Protect /agents/run endpoint with authentication middleware
- [ ] T021 Add error handling for unauthorized access in middleware
- [ ] T022 Create utility functions for token validation
- [ ] T023 Test JWT verification with sample Better Auth tokens

## Phase 4: Backend Chat Persistence

### Goal
Modify agent flow to store user messages and agent responses in the database, and create endpoints for conversation history.

### Independent Test Criteria
- User messages are saved to database before agent processing
- Agent responses with RAG sources are saved to database
- Conversation history endpoints return correct data

### Implementation Tasks

- [ ] T024 Modify /agents/run flow to save user message in database
- [ ] T025 Update agent processing to save agent response with sources
- [ ] T026 Create UserService for user management in backend/src/services/user_service.py
- [ ] T027 Create ConversationService for conversation operations in backend/src/services/conversation_service.py
- [ ] T028 Create MessageService for message operations in backend/src/services/message_service.py
- [ ] T029 Implement GET /users/me endpoint
- [ ] T030 Implement GET /conversations endpoint
- [ ] T031 Implement GET /conversations/{session_id} endpoint
- [ ] T032 Implement POST /conversations/{session_id}/messages endpoint
- [ ] T033 Associate all messages with authenticated user and conversation
- [ ] T034 Test chat persistence flow with authenticated users

## Phase 5: Frontend Auth Integration

### Goal
Integrate Better Auth client into frontend, implement login/signup UI with proper redirection, and update API calls to include auth tokens.

### Independent Test Criteria
- Users can log in and out using Better Auth
- Auth tokens are included in API requests
- Chat widget is restricted to logged-in users
- Login/signup pages display correctly with proper navigation

### Implementation Tasks

- [ ] T035 Install Better Auth client dependencies in frontend
- [ ] T036 Create Better Auth client configuration in frontend/src/lib/authClient.ts
- [ ] T037 Create Login page component in frontend/src/pages/login/index.tsx with styles in frontend/src/pages/login/styles.module.css
- [ ] T038 Create Signup page component in frontend/src/pages/signup/index.tsx with styles in frontend/src/pages/signup/styles.module.css
- [ ] T039 Create Forgot Password page component in frontend/src/pages/forgot-password/index.tsx with styles in frontend/src/pages/forgot-password/styles.module.css
- [ ] T040 Create authentication context provider in frontend/src/contexts/AuthContext.tsx
- [ ] T041 Implement login form with validation in frontend/src/components/auth/login-form/index.tsx with styles in frontend/src/components/auth/login-form/styles.module.css
- [ ] T042 Implement signup form with validation in frontend/src/components/auth/signup-form/index.tsx with styles in frontend/src/components/auth/signup-form/styles.module.css
- [ ] T043 Add social login buttons component in frontend/src/components/auth/social-login/index.tsx with styles in frontend/src/components/auth/social-login/styles.module.css
- [ ] T044 Create ProtectedRoute component in frontend/src/components/auth/protected-route/index.tsx with styles in frontend/src/components/auth/protected-route/styles.module.css
- [ ] T045 Create PublicRoute component in frontend/src/components/auth/public-route/index.tsx with styles in frontend/src/components/auth/public-route/styles.module.css
- [ ] T046 Implement redirect logic after login/signup in frontend/src/components/auth/redirect-handler/index.tsx with styles in frontend/src/components/auth/redirect-handler/styles.module.css
- [ ] T047 Update agentClient to include Authorization header in frontend/src/services/agentClient.ts
- [ ] T048 Restrict chat widget access to authenticated users
- [ ] T049 Implement session management in frontend
- [ ] T050 Create navigation guards for auth state in frontend/src/components/auth/auth-navigation/index.tsx with styles in frontend/src/components/auth/auth-navigation/styles.module.css
- [ ] T051 Test frontend authentication flow with UI components

## Phase 6: Frontend Conversation History UI

### Goal
Add UI components to display conversation history with messages and RAG sources.

### Independent Test Criteria
- Users can view their conversation history
- Individual conversations display messages with proper formatting
- RAG sources are displayed for agent responses

### Implementation Tasks

- [ ] T052 Create conversation list component in frontend/src/components/history/conversation-list/index.tsx with styles in frontend/src/components/history/conversation-list/styles.module.css
- [ ] T053 Create conversation viewer component in frontend/src/components/history/conversation-viewer/index.tsx with styles in frontend/src/components/history/conversation-viewer/styles.module.css
- [ ] T054 Update ChatWindow component in frontend/src/components/ChatWidget/ChatWindow/index.tsx with styles in frontend/src/components/ChatWidget/ChatWindow/styles.module.css to integrate with conversation history
- [ ] T055 Update MessageBubble component in frontend/src/components/ChatWidget/MessageBubble/index.tsx with styles in frontend/src/components/ChatWidget/MessageBubble/styles.module.css to display RAG sources for agent responses
- [ ] T056 Implement pagination for conversation history
- [ ] T057 Add search/filter functionality for conversations
- [ ] T058 Test conversation history UI components

## Phase 7: UX & Flow

### Goal
Implement complete user experience flows for authentication, chat, and history management.

### Independent Test Criteria
- Complete authentication and chat flow works end-to-end
- Session management works across page refreshes
- Conversation creation and switching works smoothly

### Implementation Tasks

- [ ] T059 Implement complete chat flow: frontend auth → backend protected call → response
- [ ] T060 Create session persistence across page refreshes
- [ ] T061 Implement conversation creation flow from chat interface
- [ ] T062 Add conversation switching functionality
- [ ] T063 Create loading states for authentication and chat operations
- [ ] T064 Test complete user experience flows
- [ ] T065 Implement error handling for auth and chat failures

## Phase 8: Testing

### Goal
Create comprehensive tests for authentication, chat persistence, and UI components.

### Independent Test Criteria
- Authentication middleware is properly tested
- Protected endpoints reject unauthorized requests
- UI components function correctly with authentication

### Implementation Tasks

- [ ] T066 Create unit tests for auth middleware in backend/tests/unit/test_auth_middleware.py
- [ ] T067 Create integration tests for protected endpoints in backend/tests/integration/test_protected_endpoints.py
- [ ] T068 Write unit tests for UserService in backend/tests/unit/test_user_service.py
- [ ] T069 Write integration tests for conversation endpoints in backend/tests/integration/test_conversations.py
- [ ] T070 Create UI tests for login component in frontend/tests/auth/login.test.tsx
- [ ] T071 Create UI tests for chat widget with auth in frontend/tests/chat/chatWidget.test.tsx
- [ ] T072 Create UI tests for conversation history in frontend/tests/history/conversationHistory.test.tsx
- [ ] T073 Test error handling scenarios for authentication failures

## Phase 9: Deployment & Monitoring

### Goal
Prepare for deployment with proper environment configuration and monitoring.

### Independent Test Criteria
- Environment variables are properly configured for production
- Database migrations run successfully in deployment
- Authentication and chat features work in deployed environment

### Implementation Tasks

- [ ] T074 Update environment variables for production deployment
- [ ] T075 Create deployment scripts for backend with database migrations
- [ ] T076 Set up monitoring for authentication and chat endpoints
- [ ] T077 Update documentation for deployment process
- [ ] T078 Test deployment with staging environment
- [ ] T079 Configure logging for authentication events in production
- [ ] T080 Verify performance metrics after deployment

## Dependencies

- **Phase 2 (Database)** must complete before Phase 3 (Auth Middleware)
- **Phase 3 (Auth Middleware)** must complete before Phase 4 (Chat Persistence)
- **Phase 4 (Chat Persistence)** must complete before Phase 5 (Frontend Auth)
- **Phase 5 (Frontend Auth)** must complete before Phase 6 (History UI)

## Parallel Execution Opportunities

- T006 [P] and T007 [P]: Install frontend and backend dependencies simultaneously
- T017-T023: Backend auth middleware tasks can be developed in parallel after T004
- T026-T028: Service layer tasks can be developed in parallel
- T029-T032: API endpoint tasks can be developed in parallel after services are created
- T037-T039: Page components can be developed in parallel after T036
- T041-T043: Auth form components can be developed in parallel
- T052-T053: History UI components can be developed in parallel

## Implementation Strategy

**MVP Scope**: Focus on Phase 1-4 to deliver core authentication and chat persistence functionality.

**Incremental Delivery**:
1. MVP: Basic auth + chat persistence (Phases 1-4)
2. Frontend auth integration (Phase 5)
3. History UI (Phase 6)
4. Full UX flows and testing (Phases 7-8)
<<<<<<< HEAD
5. Production deployment (Phase 9)
=======
5. Production deployment (Phase 9)
>>>>>>> f99c7079ed7175125910f696e233b326cfa1f439
