# syntax = docker/dockerfile:1

# ---------- Stage 1: Backend ----------
FROM python:3.11-slim AS backend
WORKDIR /app

# Install build dependencies (if any) and runtime deps
COPY deployment/backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend source code
COPY deployment/backend/app ./app
COPY deployment/backend/start.sh ./
RUN chmod +x ./start.sh

# ---------- Stage 2: Frontend ----------
FROM node:18-alpine AS frontend
WORKDIR /frontend
COPY frontend/package.json frontend/package-lock.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build

# ---------- Stage 3: Final Image ----------
FROM python:3.11-slim
WORKDIR /app

# Copy backend runtime from stage 1
COPY --from=backend /app ./app
COPY --from=backend /start.sh ./start.sh
RUN chmod +x ./start.sh

# Install nginx for serving static files
RUN apt-get update && apt-get install -y nginx && rm -rf /var/lib/apt/lists/*

# Copy built React static assets from stage 2
COPY --from=frontend /frontend/build /usr/share/nginx/html

# Expose ports: 8000 for API, 80 for UI
EXPOSE 8000 80

# Start both services: nginx (in background) and FastAPI via start.sh
CMD sh -c "service nginx start && ./start.sh"
