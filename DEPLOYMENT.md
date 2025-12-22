# Deployment Guide

## 1. Auth Server (Railway)

We recommend deploying the Auth Server to Railway as a separate service alongside your backend.

1.  **Create New Service** on Railway from GitHub Repo.
2.  Select `/auth-server` as the **Root Directory** in Railway settings.
3.  Set the following Environment Variables in Railway:
    *   `DATABASE_URL`: Connection string to your detailed Neon DB (same as Backend).
    *   `BETTER_AUTH_SECRET`: Generate a random string.
    *   `FRONTEND_URL`: Your Vercel frontend URL (e.g., `https://your-app.vercel.app`).
    *   `PORT`: `3001` (or let Railway assign one and use that).

## 2. Backend (Railway)

1.  Update your existing Backend service on Railway.
2.  Set Environment Variables:
    *   `BETTER_AUTH_URL`: The public URL of your deployed Auth Server (e.g., `https://auth-server-production.up.railway.app`).
    *   `DATABASE_URL`: Same Neon DB URL.

## 3. Frontend (Vercel)

1.  Update your Vercel project.
2.  Set Environment Variables:
    *   `NEXT_PUBLIC_BETTER_AUTH_URL`: The public URL of your deployed Auth Server (e.g., `https://auth-server-production.up.railway.app`).

## Local Development linking

*   **Auth Server**: `http://localhost:3001`
*   **Backend**: `http://localhost:8000`
*   **Frontend**: `http://localhost:3000`

Ensure all `.env` files point to these local ports when developing.
