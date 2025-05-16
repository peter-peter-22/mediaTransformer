from PIL import Image
import torch
from torchvision import models
from typing import NamedTuple

# Type for the tags
class Tag(NamedTuple):
    """
    Tag paired with accuracy.
    Attributes:
        category (str): The predicted category of the image.
        probability (float): The confidence score for the predicted category.
    """
    category: str
    probability: float

# Get device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Device: {device}")

# Load the pre-trained ResNet50 model with IMAGENET1K_V2 weights
model = models.resnet50(weights=models.ResNet50_Weights.IMAGENET1K_V2).to(device)
model.eval()

# Define the preprocessing pipeline
preprocess = models.ResNet50_Weights.IMAGENET1K_V2.transforms()

async def tag_image(image: Image.Image, top_k: int = 5, min_confidence: float = 0.2):
    """
    Predict the image's category using a pre-trained ResNet model.
    Args:
        image (PIL.Image): The input image
    Returns:
        dict: A dictionary containing the predicted category and its probability.
    """
    # Convert to RGB if necessary
    if image.mode != "RGB":
        image = image.convert("RGB")

    # Preprocess the image
    input_tensor = preprocess(image).unsqueeze(0).to(device)

    # Perform inference
    with torch.no_grad():
        outputs = model(input_tensor)

    # Get top 5 predictions
    probabilities = torch.nn.functional.softmax(outputs[0], dim=0)
    top5_prob, top5_catid = torch.topk(probabilities, top_k)

    # Map category IDs to labels
    labels = models.ResNet50_Weights.IMAGENET1K_V2.meta["categories"]
    top5_labels = [labels[catid] for catid in top5_catid]

    # Format the results and filter out the too inconfident predictions
    return [
        Tag(label,round(prob.item(), 4))
        for label, prob in zip(top5_labels, top5_prob)
        if prob.item()>=min_confidence
    ]