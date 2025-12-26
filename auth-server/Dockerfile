# Replace alpine with node:20-slim
FROM node:20-slim

# The rest of your Dockerfile remains the same
WORKDIR /app
COPY auth-server/package*.json ./
RUN npm install
COPY auth-server/ .
RUN npm install -g typescript
RUN tsc
EXPOSE 3001
CMD ["node", "dist/index.js"]
