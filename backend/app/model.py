import os
import base64
import io
import numpy as np
from PIL import Image


MODEL_PATH = "model/1.keras"


def preprocess_image(image: Image.Image):
    image = image.convert("RGB").resize((224, 224))
    arr = np.array(image).astype("float32") / 255.0
    return np.expand_dims(arr, axis=0)


def predict(image_base64: str, model):

    if "," in image_base64:
        image_base64 = image_base64.split(",")[1]

    decoded = base64.b64decode(image_base64)
    image = Image.open(io.BytesIO(decoded))

    input_arr = preprocess_image(image)

    preds = model.predict(input_arr)[0]  # softmax output

    class_idx = int(np.argmax(preds))
    confidence = float(np.max(preds))

    class_file = os.path.join("model", "class_names.txt")

    if os.path.exists(class_file):
        with open(class_file, "r") as f:
            classes = [line.strip() for line in f.readlines()]
        class_name = classes[class_idx]
    else:
        class_name = str(class_idx)

    return {
        "class": class_name,
        "confidence": confidence
    }
