from PIL import Image, ImageOps
from torchvision import transforms

# Same normalization values used during training
transform = transforms.Compose([
    transforms.Resize((28, 28)),
    transforms.ToTensor(),
    transforms.Normalize((0.1307,), (0.3081,))
])


def preprocess(image: Image.Image):
    """
    Convert a user image into a tensor suitable
    for DigitNet.
    """

    # Convert to grayscale
    image = image.convert("L")

    # Make sure digit is white on black background.
    # Remove this line if your frontend already draws
    # white digits on a black canvas.
    image = ImageOps.invert(image)

    # Resize to MNIST size
    tensor = transform(image)

    # Add batch dimension
    tensor = tensor.unsqueeze(0)

    return tensor