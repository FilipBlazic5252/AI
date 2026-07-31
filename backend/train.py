import torch
import torch.nn as nn
import torch.optim as optim

from torchvision import datasets
from torchvision import transforms
from torch.utils.data import DataLoader

from model import DigitNet

# ---------------------------------------
# Device
# ---------------------------------------

device = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)

print(f"Using {device}")

# ---------------------------------------
# Hyperparameters
# ---------------------------------------

BATCH_SIZE = 64
EPOCHS = 5
LEARNING_RATE = 0.001

# ---------------------------------------
# Dataset
# ---------------------------------------

transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.1307,), (0.3081,))
])

train_dataset = datasets.MNIST(
    "./data",
    train=True,
    download=True,
    transform=transform
)

test_dataset = datasets.MNIST(
    "./data",
    train=False,
    download=True,
    transform=transform
)

train_loader = DataLoader(
    train_dataset,
    batch_size=BATCH_SIZE,
    shuffle=True
)

test_loader = DataLoader(
    test_dataset,
    batch_size=BATCH_SIZE
)

# ---------------------------------------
# Model
# ---------------------------------------

model = DigitNet().to(device)

loss_function = nn.CrossEntropyLoss()

optimizer = optim.Adam(
    model.parameters(),
    lr=LEARNING_RATE
)

# ---------------------------------------
# Training Loop
# ---------------------------------------

for epoch in range(EPOCHS):

    model.train()
    running_loss = 0

    for images, labels in train_loader:

        images = images.to(device)
        labels = labels.to(device)

        optimizer.zero_grad()

        outputs = model(images)

        loss = loss_function(outputs, labels)

        loss.backward()

        optimizer.step()

        running_loss += loss.item()

    # --------------------------
    # Evaluate
    # --------------------------

    model.eval()

    correct = 0
    total = 0

    with torch.no_grad():

        for images, labels in test_loader:

            images = images.to(device)
            labels = labels.to(device)

            outputs = model(images)

            predictions = outputs.argmax(1)

            correct += (predictions == labels).sum().item()

            total += labels.size(0)

    accuracy = 100 * correct / total

    print(
        f"Epoch {epoch+1}/{EPOCHS}"
        f" | Loss {running_loss:.2f}"
        f" | Accuracy {accuracy:.2f}%"
    )

# ---------------------------------------
# Save Model
# ---------------------------------------

torch.save(
    model.state_dict(),
    "digit_model.pth"
)

print("Model saved as digit_model.pth")