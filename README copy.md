You are implementing authentication and conversation persistence for an AI RAG eBook platform using the **current approved architecture**.

### **Before Writing Any Code**

1. **Audit the repository first**

   * Read all existing files.
   * Identify files, folders, phases, or code paths created for **older plans or deprecated approaches**.
   * Compare them against the **current `plan.md`, `task.md`, `research.md`, and `data-model.md`**.

2. **Remove or deprecate outdated artifacts**

   * Delete or clearly mark as deprecated:

     * Old auth implementations (custom JWT, session-based auth, OAuth remnants).
     * Phases or folders that assume BetterAuth runs inside FastAPI.
     * Any database models not aligned with the current data model.
     * Middleware, services, or utilities that conflict with JWKS-based JWT verification.
   * Do **not** introduce backward compatibility for removed approaches.

3. **Validate system alignment**

   * Ensure the system follows this exact stack:

     * **Frontend**: BetterAuth (JWT plugin enabled)
     * **Backend**: FastAPI (JWT verification only, no auth state)
     * **Database**: Neon PostgreSQL (users, conversations, messages)
     * **Vector Store**: Qdrant
     * **AI Layer**: OpenAI Agents SDK
   * No additional frameworks, auth providers, or databases are allowed.

### **Implementation Rules**

* FastAPI **must never** handle login, signup, or sessions.
* FastAPI **must only**:

  * Verify JWT tokens via BetterAuth JWKS
  * Extract user identity from `sub`, `email`, and `name`
  * Persist and query conversation data in NeonDB
* User records must be **created or updated lazily** on first authenticated request.
* Conversations and messages must always be scoped to the authenticated user.
* Messages are immutable after creation.

### **Execution Order**

1. Clean up outdated phases and files.
2. Confirm database schema matches `data-model.md`.
3. Implement JWT verification middleware using JWKS.
4. Implement user sync logic from JWT payload.
5. Implement conversation & message persistence.
6. Connect RAG responses with stored message sources.
7. Validate end-to-end flow (login → chat → stored history).

### **Quality Constraints**

* No duplicate auth logic.
* No hardcoded secrets.
* Async database access only.
* Clear separation between auth, business logic, and AI agents.
* Code must match documentation exactly — documentation is the source of truth.

### **Final Check**

Before marking the task complete:

* All legacy files are removed or deprecated.
* No file contradicts the current plan.
* Auth, chat, and storage flow works end-to-end with BetterAuth JWTs.
