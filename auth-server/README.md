# Auth Server

This is a Node.js server running Better Auth to handle authentication for the platform.
It bridges the Docusaurus frontend and the Neon PostgreSQL database.

## Setup

1. Copy `.env.example` to `.env` (create it if missing) and fill in your values:

```
DATABASE_URL=postgres://user:password@host:port/dbname
BETTER_AUTH_SECRET=your_generated_secret
FRONTEND_URL=http://localhost:3000
PORT=3001
```

2. Install dependencies:
```bash
npm install
```

3. Run the server:
```bash
npm start
```

## API

The server exposes Better Auth endpoints at `/api/auth/*`.
It also provides JWKS for the Python backend to verify tokens.
