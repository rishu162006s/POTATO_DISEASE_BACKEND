# backend/app/main.py

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from .schemas import PredictionRequest, PredictionResponse
from .model import predict

app = FastAPI(title="Potato Disease Prediction API", version="1.0.0")

# Allow all origins for simplicity – adjust for production as needed
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/predict", response_model=PredictionResponse)
def get_prediction(req: PredictionRequest):
    try:
        result = predict(req.image_base64)
        return PredictionResponse(prediction=result)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        # Generic error for debugging – in production hide details
        raise HTTPException(status_code=500, detail="Prediction failed")

# Optional health check
@app.get("/health")
def health_check():
    return JSONResponse(content={"status": "ok"})
