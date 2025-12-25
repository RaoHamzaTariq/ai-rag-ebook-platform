# 1. Use Node 20 Alpine
FROM node:20-alpine

# 2. Set working directory inside container
WORKDIR /app

# 3. Copy only package.json and package-lock.json
COPY package*.json ./

# 4. Install dependencies
RUN npm install

# 5. Copy all project files
COPY auth-server/ .

# 6. Install TypeScript globally
RUN npm install -g typescript

# 7. Compile TypeScript into dist/
RUN tsc

# 8. Expose the internal port
EXPOSE 3001

# 9. Start the server using compiled JS
CMD ["node", "dist/index.js"]
