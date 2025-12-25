# Use Node.js 18
FROM node:18-alpine

# Create app directory
WORKDIR /app

# Copy package files
COPY auth-server/package*.json ./

# Install dependencies
RUN npm install

# Copy all source code
COPY auth-server/ .

# Install TypeScript globally (optional)
RUN npm install -g typescript

# Build TypeScript files to dist/
RUN tsc

# Expose the internal container port
EXPOSE 3001

# Start the server
CMD ["node", "dist/index.js"]
