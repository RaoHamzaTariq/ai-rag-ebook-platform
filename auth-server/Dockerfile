# 1. Use Node 20 Alpine
FROM node:20-slim
# 2. Set working directory inside container
WORKDIR /app

# 3. Copy package files FROM the sub-directory
# We change this to look into the auth-server folder
COPY auth-server/package*.json ./

# 4. Install dependencies
RUN npm install

# 5. Copy the rest of the auth-server files
COPY auth-server/ .

# 6. Install TypeScript globally
RUN npm install -g typescript

# 7. Compile TypeScript into dist/
RUN tsc

# 8. Expose the internal port
EXPOSE 3001

# 9. Start the server
CMD ["node", "dist/index.js"]
