import sys

import torch
from PIL import Image

from model import DigitNet
from preprocess import preprocess

# ---------------------------------------
# Device
# ---------------------------------------

device = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)

print(f"Using {device}")

# ---------------------------------------
# Load Model
# ---------------------------------------

model = DigitNet().to(device)

model.load_state_dict(
    torch.load(
        "digit_model.pth",
        map_location=device
    )
)

model.eval()

# ---------------------------------------
# Get Image Path
# ---------------------------------------

if len(sys.argv) != 2:
    print("Usage:")
    print("python predict.py image.png")
    exit()

image_path = sys.argv[1]

# ---------------------------------------
# Load Image
# ---------------------------------------

image = Image.open(image_path)

tensor = preprocess(image)

tensor = tensor.to(device)

# ---------------------------------------
# Predict
# ---------------------------------------

with torch.no_grad():

    output = model(tensor)

    probabilities = torch.softmax(
        output,
        dim=1
    )

confidence, prediction = torch.max(
    probabilities,
    dim=1
)

print("\nPrediction")
print("----------------")

print(f"Digit      : {prediction.item()}")

print(
    f"Confidence : "
    f"{confidence.item()*100:.2f}%"
)