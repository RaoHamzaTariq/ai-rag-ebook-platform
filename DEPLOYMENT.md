# Deployment Guide

## Environment Variables Required

Your deployment platform (Railway, Render, Vercel, etc.) needs the following environment variables configured:

### Backend Environment Variables

```bash
# Google Gemini API Key (REQUIRED)
GOOGLE_API_KEY=your_google_api_key_here

# Qdrant Vector Database (REQUIRED)
QDRANT_ENDPOINT=https://your-qdrant-instance.cloud.qdrant.io:6333
QDRANT_API_KEY=your_qdrant_api_key_here

# Optional: Server Configuration
PORT=8080
HOST=0.0.0.0
```

### Frontend Environment Variables

```bash
# Backend API URL
REACT_APP_BACKEND_URL=https://your-backend-url.railway.app
```

## How to Set Environment Variables

### Railway

1. Go to your project dashboard
2. Click on your backend service
3. Go to **Variables** tab
4. Click **+ New Variable**
5. Add each variable:
   - Variable: `GOOGLE_API_KEY`
   - Value: `your_actual_api_key`
6. Click **Add** and repeat for all variables
7. Redeploy your service

### Render

1. Go to your service dashboard
2. Click on **Environment** in the left sidebar
3. Click **Add Environment Variable**
4. Add each variable with its value
5. Click **Save Changes**
6. Render will automatically redeploy

### Vercel

1. Go to your project settings
2. Click on **Environment Variables**
3. Add each variable:
   - Name: `GOOGLE_API_KEY`
   - Value: `your_actual_api_key`
   - Environment: Production (and Preview if needed)
4. Click **Save**
5. Redeploy your project

### Docker / Docker Compose

Create a `.env` file in your backend directory:

```bash
GOOGLE_API_KEY=your_google_api_key_here
QDRANT_ENDPOINT=https://your-qdrant-instance.cloud.qdrant.io:6333
QDRANT_API_KEY=your_qdrant_api_key_here
```

Or pass them via command line:

```bash
docker run -e GOOGLE_API_KEY=your_key \
           -e QDRANT_ENDPOINT=your_endpoint \
           -e QDRANT_API_KEY=your_qdrant_key \
           your-image-name
```

## Getting API Keys

### Google Gemini API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Click **Get API Key**
3. Create a new API key or use an existing one
4. Copy the key and add it to your deployment environment

### Qdrant Cloud

1. Go to [Qdrant Cloud Console](https://cloud.qdrant.io/)
2. Create a cluster or use an existing one
3. Copy the **Cluster URL** (this is your `QDRANT_ENDPOINT`)
4. Go to **API Keys** and create a new key
5. Copy the API key (this is your `QDRANT_API_KEY`)

## Troubleshooting

### Error: "GOOGLE_API_KEY environment variable is not set"

**Solution**: Make sure you've added the `GOOGLE_API_KEY` variable to your deployment platform and redeployed.

### Error: "The api_key client option must be set"

**Solution**: This is the same as above - the API key is missing from your environment.

### Backend starts but crashes immediately

**Solution**: Check your deployment logs. If you see the error about missing API keys, follow the steps above to add them.

### How to verify environment variables are set

Add a health check endpoint or check your deployment logs. The backend will now show a clear error message if the API key is missing.

## Security Best Practices

1. **Never commit API keys** to your repository
2. **Use different keys** for development and production
3. **Rotate keys regularly** for security
4. **Limit API key permissions** if possible
5. **Monitor API usage** to detect unauthorized access

## Example: Complete Railway Setup

```bash
# 1. Install Railway CLI
npm install -g @railway/cli

# 2. Login
railway login

# 3. Link to your project
railway link

# 4. Set environment variables
railway variables set GOOGLE_API_KEY=your_key_here
railway variables set QDRANT_ENDPOINT=https://your-cluster.cloud.qdrant.io:6333
railway variables set QDRANT_API_KEY=your_qdrant_key_here

# 5. Deploy
railway up
```

## Verification

After setting the environment variables and redeploying:

1. Check deployment logs for successful startup
2. Visit your backend URL (e.g., `https://your-app.railway.app`)
3. You should see: `{"status": "ok", "message": "Physical AI RAG Backend is running"}`
4. Check `/docs` endpoint for API documentation

If you see the health check response, your deployment is successful! 🎉
