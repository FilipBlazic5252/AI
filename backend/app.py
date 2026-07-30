from io import BytesIO

import torch
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from PIL import Image

from model import DigitNet
from preprocess import preprocess


# -----------------------------------------
# FastAPI App
# -----------------------------------------

app = FastAPI()

# Allow requests from the React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------------------
# Device
# -----------------------------------------

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

print(f"Using device: {device}")

# -----------------------------------------
# Load Model
# -----------------------------------------

model = DigitNet().to(device)

try:
    model.load_state_dict(
        torch.load("digit_model.pth", map_location=device)
    )
    model.eval()

except FileNotFoundError:
    print("digit_model.pth not found.")
    print("Run train.py first.")
    raise

# -----------------------------------------
# Routes
# -----------------------------------------

@app.get("/dist")
def root():
    return {
        "message": "AI Digit Recognizer API",
        "device": str(device),
        "status": "running"
    }


@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    """
    Predict a handwritten digit.
    """

    try:
        contents = await file.read()

        image = Image.open(BytesIO(contents))

        tensor = preprocess(image)

        tensor = tensor.to(device)

        with torch.no_grad():

            output = model(tensor)

            probabilities = torch.softmax(output, dim=1)

            confidence, prediction = torch.max(
                probabilities,
                dim=1
            )
        return {
            "digit": int(prediction.item()),
            "confidence": round(
                confidence.item() * 100,
                2
            )
        }

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


