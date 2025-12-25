# Use Node 18 (stable + small image)
FROM node:18-alpine

# Working directory
WORKDIR /app

# Copy only package files first (faster builds)
COPY auth-server/package*.json ./

# Install dependencies
RUN npm install

# Copy entire auth-server
COPY auth-server/ .

# Build TypeScript into dist/
RUN npm install -g typescript
RUN tsc

# Expose port internally
EXPOSE 3001

# Start server from compiled JS
CMD ["node", "dist/index.js"]
