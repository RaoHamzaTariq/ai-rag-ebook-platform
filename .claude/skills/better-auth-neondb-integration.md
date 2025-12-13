# Better Auth and NeonDB Integration Guide

This document provides comprehensive information about integrating Better Auth with NeonDB for authentication and user data management in your AI RAG ebook platform.

## Table of Contents
1. [Overview](#overview)
2. [Better Auth Installation and Setup](#better-auth-installation-and-setup)
3. [NeonDB Configuration](#neondb-configuration)
4. [Database Schema and Models](#database-schema-and-models)
5. [Backend Implementation](#backend-implementation)
6. [Frontend Integration](#frontend-integration)
7. [Security Considerations](#security-considerations)
8. [Best Practices](#best-practices)

## Overview

Better Auth is a framework-agnostic authentication and authorization library for TypeScript that provides comprehensive features including email/password authentication, social providers, session management, and plugin support for advanced functionalities like 2FA and SSO.

NeonDB is a serverless PostgreSQL platform that offers autoscaling, branching, and instant restore capabilities, making it an ideal database solution for modern applications.

## Better Auth Installation and Setup

### Installation

```bash
npm install better-auth
npm install pg @types/pg  # For PostgreSQL integration
```

### Basic Server Configuration

```typescript
import { betterAuth } from "better-auth";
import { Pool } from "pg";

export const auth = betterAuth({
  database: new Pool({
    connectionString: process.env.NEON_DATABASE_URL
  }),
  emailAndPassword: {
    enabled: true,
    requireEmailVerification: false, // Set to true for production
  },
  socialProviders: {
    // Add social providers as needed
  },
  session: {
    expiresIn: 7 * 24 * 60 * 60, // 7 days
    updateAge: 24 * 60 * 60, // 24 hours
  },
});
```

### Environment Variables

```env
NEON_DATABASE_URL=postgresql://username:password@ep-xxx.us-east-1.aws.neon.tech/dbname?sslmode=require
BETTER_AUTH_URL=http://localhost:3000
BETTER_AUTH_SECRET=your-super-secret-jwt-signing-key
```

## NeonDB Configuration

### Basic NeonDB Connection

```typescript
import { betterAuth } from "better-auth";
import { Pool } from "pg";

export const auth = betterAuth({
  database: new Pool({
    connectionString: process.env.NEON_DATABASE_URL,
  }),
});
```

### NeonDB Serverless Driver (for Edge Functions)

```typescript
import { neon } from '@neondatabase/serverless';
import { Pool } from 'pg';

// For serverless environments
const pool = new Pool({
  connectionString: process.env.NEON_DATABASE_URL,
});

export const auth = betterAuth({
  database: pool,
});
```

### NeonDB Configuration with Custom Schema

```typescript
import { betterAuth } from "better-auth";
import { Pool } from "pg";

export const auth = betterAuth({
  database: new Pool({
    connectionString: `${process.env.NEON_DATABASE_URL}?options=-c search_path=auth`,
  }),
});
```

## Database Schema and Models

Better Auth automatically creates the necessary tables for authentication. For your AI RAG ebook platform, you'll need additional tables for users, conversations, and messages.

### User Model (extends Better Auth user)

```typescript
// backend/src/models/user.ts
import { InferSelectModel } from "drizzle-orm";
import { users } from "better-auth/db/schema";

export type User = InferSelectModel<typeof users> & {
  // Additional fields specific to your app
  preferences?: Record<string, any>;
  createdAt: Date;
  updatedAt: Date;
};
```

### Conversation Model

```typescript
// backend/src/models/conversation.ts
import { sql } from "drizzle-orm";
import { pgTable, serial, text, timestamp, integer } from "drizzle-orm/pg-core";

export const conversations = pgTable("conversations", {
  id: serial("id").primaryKey(),
  userId: text("user_id").notNull(),
  title: text("title").notNull(),
  createdAt: timestamp("created_at").default(sql`CURRENT_TIMESTAMP`),
  updatedAt: timestamp("updated_at").default(sql`CURRENT_TIMESTAMP`),
});

export type Conversation = typeof conversations.$inferSelect;
```

### Message Model

```typescript
// backend/src/models/message.ts
import { sql } from "drizzle-orm";
import { pgTable, serial, text, timestamp, integer, json } from "drizzle-orm/pg-core";

export const messages = pgTable("messages", {
  id: serial("id").primaryKey(),
  conversationId: integer("conversation_id").notNull(),
  userId: text("user_id").notNull(),
  role: text("role").notNull(), // 'user' or 'assistant'
  content: text("content").notNull(),
  sources: json("sources"), // For RAG sources
  createdAt: timestamp("created_at").default(sql`CURRENT_TIMESTAMP`),
});

export type Message = typeof messages.$inferSelect;
```

## Backend Implementation

### Auth Middleware Setup

```typescript
// backend/src/middleware/auth_middleware.ts
import { auth } from "../auth";
import { verifyRequestOrigin } from "better-auth/utils";

export async function authMiddleware(request: Request) {
  // Verify CSRF for non-GET requests
  if (request.method !== "GET") {
    const origin = request.headers.get("Origin");
    const host = request.headers.get("Host");
    if (!origin || !host || !verifyRequestOrigin(origin, [host])) {
      return new Response("Invalid origin", { status: 403 });
    }
  }

  // Get session from request
  const session = await auth.api.getSession({
    headers: request.headers,
  });

  return {
    session: session?.session,
    user: session?.user,
  };
}
```

### Protecting API Routes

```typescript
// backend/src/routes/protected.ts
import { auth } from "../auth";
import { Hono } from "hono";

const app = new Hono();

app.get("/api/protected", auth.handle, async (c) => {
  const session = c.get("session");
  if (!session) {
    return c.json({ error: "Unauthorized" }, 401);
  }

  return c.json({ message: "Protected content", user: session.user });
});

export default app;
```

### Database Services

```typescript
// backend/src/services/conversation_service.ts
import { db } from "../db";
import { conversations, messages } from "../models";
import { eq, desc } from "drizzle-orm";

export class ConversationService {
  static async create(userId: string, title: string) {
    const [conversation] = await db
      .insert(conversations)
      .values({ userId, title })
      .returning();

    return conversation;
  }

  static async getByUserId(userId: string) {
    return await db
      .select()
      .from(conversations)
      .where(eq(conversations.userId, userId))
      .orderBy(desc(conversations.createdAt));
  }

  static async getById(id: number, userId: string) {
    const result = await db
      .select()
      .from(conversations)
      .where(eq(conversations.id, id))
      .limit(1);

    if (result.length === 0 || result[0].userId !== userId) {
      return null;
    }

    return result[0];
  }
}
```

## Frontend Integration

### Auth Client Setup

```typescript
// frontend/src/lib/authClient.ts
import { createAuthClient } from "better-auth/client";

export const authClient = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_BETTER_AUTH_URL || "http://localhost:3000",
});

export const { signIn, signUp, useSession, signOut } = authClient;
```

### Authentication Context

```typescript
// frontend/src/contexts/AuthContext.tsx
import React, { createContext, useContext, ReactNode } from "react";
import { useSession } from "../lib/authClient";

interface AuthContextType {
  user: any;
  isLoading: boolean;
  isAuthenticated: boolean;
  signIn: any;
  signOut: any;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const { data: session, isLoading } = useSession();

  const value: AuthContextType = {
    user: session?.user,
    isLoading,
    isAuthenticated: !!session?.user,
    signIn,
    signOut,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
};
```

### Protected Route Component

```typescript
// frontend/src/components/auth/protected-route/index.tsx
import React from "react";
import { useAuth } from "../../../contexts/AuthContext";
import { Navigate, useLocation } from "react-router-dom";

interface ProtectedRouteProps {
  children: React.ReactNode;
  redirectTo?: string;
}

const ProtectedRoute: React.FC<ProtectedRouteProps> = ({
  children,
  redirectTo = "/login"
}) => {
  const { isAuthenticated, isLoading } = useAuth();
  const location = useLocation();

  if (isLoading) {
    return <div>Loading...</div>;
  }

  if (!isAuthenticated) {
    return <Navigate to={redirectTo} state={{ from: location }} replace />;
  }

  return <>{children}</>;
};

export default ProtectedRoute;
```

### Login Component

```typescript
// frontend/src/components/auth/login-form/index.tsx
import React, { useState } from "react";
import { signIn } from "../../../lib/authClient";

const LoginForm: React.FC = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    try {
      const response = await signIn.email({
        email,
        password,
        callbackURL: "/dashboard", // Redirect after login
      });

      if (!response) {
        setError("Invalid email or password");
      }
    } catch (err) {
      setError("An error occurred during login");
      console.error(err);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <label htmlFor="email">Email</label>
        <input
          id="email"
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
      </div>
      <div>
        <label htmlFor="password">Password</label>
        <input
          id="password"
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
      </div>
      {error && <p style={{ color: "red" }}>{error}</p>}
      <button type="submit">Sign In</button>
    </form>
  );
};

export default LoginForm;
```

## Security Considerations

### JWT Token Security

- Use strong secrets for JWT signing: `BETTER_AUTH_SECRET`
- Set appropriate token expiration times
- Implement proper CSRF protection
- Use HTTPS in production

### Database Security

- Use parameterized queries to prevent SQL injection
- Implement proper access controls
- Regularly update dependencies
- Use connection pooling with appropriate limits

### Session Management

```typescript
// Example session configuration
export const auth = betterAuth({
  session: {
    expiresIn: 7 * 24 * 60 * 60, // 7 days
    updateAge: 24 * 60 * 60, // 24 hours
    rememberMe: true,
    cookie: {
      secure: process.env.NODE_ENV === "production",
      sameSite: "lax",
    },
  },
});
```

## Best Practices

1. **Environment Configuration**:
   - Use different database URLs for development and production
   - Store secrets in environment variables
   - Never commit secrets to version control

2. **Error Handling**:
   - Implement proper error handling for authentication failures
   - Provide user-friendly error messages
   - Log authentication events for monitoring

3. **Performance Optimization**:
   - Use connection pooling for database connections
   - Implement caching for frequently accessed data
   - Optimize database queries with proper indexing

4. **Testing**:
   - Write unit tests for authentication middleware
   - Test protected routes with unauthorized requests
   - Verify session management functionality

5. **Monitoring**:
   - Log authentication events
   - Monitor failed login attempts
   - Track session usage patterns

## Common Integration Patterns

### Checking Authentication in API Routes

```typescript
// In your API route handler
export async function GET(request: Request) {
  const session = await auth.api.getSession({
    headers: request.headers,
  });

  if (!session) {
    return new Response("Unauthorized", { status: 401 });
  }

  // Continue with authenticated user logic
  return new Response(JSON.stringify({ user: session.user }));
}
```

### Including Auth Token in Frontend Requests

```typescript
// In your API client
import { authClient } from "./lib/authClient";

export async function makeAuthenticatedRequest(url: string, options = {}) {
  const session = await authClient.getSession();

  return fetch(url, {
    ...options,
    headers: {
      ...options.headers,
      "Authorization": `Bearer ${session?.session.token}`,
    },
  });
}
```

This guide provides the foundation for integrating Better Auth with NeonDB in your AI RAG ebook platform. The implementation will follow the tasks outlined in your project, starting with basic authentication setup and progressing to full chat history persistence with user accounts.
