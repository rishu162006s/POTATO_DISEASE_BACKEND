# Potato Disease Prediction – Dockerized Deployment

## Overview
This folder contains everything needed to build and run a production‑ready container for the potato‑disease prediction app.

- **Backend** – FastAPI (Python) serving a `/predict` endpoint that loads a Keras model.
- **Frontend** – React UI (already present in `frontend/`) built into static files served by Nginx.
- **Docker** – Multi‑stage Dockerfile builds the backend, compiles the React app, and assembles a lightweight runtime image.
- **docker‑compose.yml** – Optional convenience wrapper to run backend and Nginx together.

## Prerequisites
- Docker Engine (or Docker Desktop) installed.
- (Optional) Docker Compose v2.

## Build & Run
```bash
# From the project root
cd "c:/kritagya work/deep learning/potato disease prediction"
# Build the image (the image tag can be changed as desired)
docker build -t potato-app ./deployment

# Run the container (model file is mounted from the host)
docker run -d \
  -p 80:80 -p 8000:8000 \
  -v "$(pwd)/api/1.keras:/model/1.keras:ro" \
  --name potato_app \
  potato-app
```
The UI will be reachable at `http://localhost` and the API docs at `http://localhost:8000/docs`.

## Using Docker Compose (recommended for local dev)
```bash
cd deployment
docker compose up --build
```
This starts two services:
- **backend** – FastAPI on port 8000, with the model mounted.
- **frontend** – Nginx on port 80 serving the compiled React app.

## Swapping the Model
Replace the file `api/1.keras` on the host with a new trained model and restart the backend container:
```bash
docker compose restart backend   # or docker restart potato_app
```
No rebuild is required because the model is mounted as a volume.

## Testing the API
```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"image_base64": "<base64‑encoded‑png>"}'
```
You should receive a JSON response like:
```json
{ "prediction": "Early blight" }
```

## Troubleshooting
- **Port conflict** – If port 80 or 8000 is already in use, edit `docker-compose.yml` (or the `docker run` command) to map to different host ports.
- **GPU required** – This deployment is CPU‑only. To use GPU, replace the base Python image with a CUDA image and install `tensorflow-gpu`.

---
*Happy deploying!*
