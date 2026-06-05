# backend/app/schemas.py

from pydantic import BaseModel

class PredictionRequest(BaseModel):
    image_base64: str  # base64‑encoded PNG/JPEG image

class PredictionResponse(BaseModel):
    prediction: str
