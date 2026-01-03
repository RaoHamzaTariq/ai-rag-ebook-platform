# 1. Change FROM node:20-alpine to node:20-slim
FROM node:20-slim

# 2. Add build dependencies (required for some Node modules on slim)
RUN apt-get update && apt-get install -y python3 make g++ && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY package*.json ./
RUN npm install
COPY / .
RUN npm install -g typescript
RUN tsc
EXPOSE 3001
CMD ["node", "dist/index.js"]
