from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .schemas import PredictionRequest, PredictionResponse
from .model import predict
from tensorflow.keras.models import load_model
import os

app = FastAPI(title="Potato Disease API")

# Load model path (Render/Docker safe)
MODEL_PATH = "model/1.keras"
model = None


@app.on_event("startup")
def load_model():
    global model
    model = load_model(MODEL_PATH)
    print("Model loaded successfully")


# CORS for Vercel frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten later in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/predict", response_model=PredictionResponse)
def predict_image(req: PredictionRequest):
    try:
        result = predict(req.image_base64, model)
        return PredictionResponse(prediction=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
def health():
    return {"status": "ok"}
