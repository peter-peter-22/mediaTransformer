from PIL import Image
import torch
from typing import NamedTuple
from src.common.device import device
from transformers.models.vit import ViTImageProcessor, ViTForImageClassification

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

# Get the model and the preprocessor
processor = ViTImageProcessor.from_pretrained('google/vit-base-patch16-224')
model = ViTForImageClassification.from_pretrained('google/vit-base-patch16-224')
model.to(device) # type: ignore
model.eval()

def classify_image(image: Image.Image):
    # Preprocess the image
    inputs = processor(image,return_tensors="pt").to(device)

    # Perform inference
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits

    # Make the label readable
    predicted_class_idx = logits.argmax(-1).item()
    label=model.config.id2label[predicted_class_idx]
    print("Predicted class:", label)

    # Return the result
    if(isinstance(label, str)):
        return label