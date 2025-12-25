# 1. Use Node 20 Alpine (small and fast)
FROM node:20-alpine

# 2. Set working directory
WORKDIR /app

# 3. Copy only package.json & package-lock.json first
# This helps caching and speeds up rebuilds
COPY auth-server/package*.json ./

# 4. Install dependencies
RUN npm install

# 5. Copy all source code
COPY auth-server/ .

# 6. Install TypeScript compiler globally
RUN npm install -g typescript

# 7. Compile TypeScript into dist/
RUN tsc

# 8. Expose internal server port (optional info)
EXPOSE 3001

# 9. Start the app from compiled JS
CMD ["node", "dist/index.js"]
