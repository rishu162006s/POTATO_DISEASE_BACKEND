# backend/app/model.py

import os
import base64
import io
from typing import Any

import numpy as np
from PIL import Image
from tensorflow.keras.models import load_model

# Load the model once when the module is imported.
# The model file is expected to be mounted at /model/1.keras inside the container.
MODEL_PATH = os.getenv("MODEL_PATH", "/app/model/1.keras")
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Model file not found at {MODEL_PATH}")



# Determine expected input size from the model's first layer if possible.
# Fallback to 224x224.
try:
    input_shape = model.input_shape  # e.g., (None, 224, 224, 3)
    _, height, width, channels = input_shape
except Exception:
    height, width, channels = 224, 224, 3

def preprocess_image(image: Image.Image) -> np.ndarray:
    """Resize and normalize a PIL image to the model's expected input.

    Returns a NumPy array with shape (1, height, width, channels).
    """
    img = image.convert("RGB").resize((width, height))
    arr = np.asarray(img).astype("float32") / 255.0
    arr = np.expand_dims(arr, axis=0)
    return arr

def predict(image_base64: str) -> str:
    """Run inference on a base64‑encoded image and return the predicted class name.

    The implementation assumes the model outputs a softmax over class indices and that a
    ``class_names.txt`` file exists next to the model file with one class name per line.
    If the file is missing, the numeric index is returned instead.
    """
    # Decode base64 string
    try:
        decoded = base64.b64decode(image_base64)
        image = Image.open(io.BytesIO(decoded))
    except Exception as e:
        raise ValueError("Invalid base64 image data") from e

    input_arr = preprocess_image(image)
    preds = model.predict(input_arr)
    class_idx = int(np.argmax(preds, axis=1)[0])

    # Try to map to class name
    class_file = os.path.join(os.path.dirname(MODEL_PATH), "class_names.txt")
    if os.path.exists(class_file):
        with open(class_file, "r", encoding="utf-8") as f:
            classes = [line.strip() for line in f.readlines()]
        if 0 <= class_idx < len(classes):
            return classes[class_idx]
    # Fallback
    return str(class_idx)
