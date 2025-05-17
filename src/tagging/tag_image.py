from src.common.device import device
from PIL import Image
from transformers.models.auto.processing_auto import AutoProcessor
from transformers.models.blip import BlipForConditionalGeneration

processor = AutoProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
model.eval()
model.to(device)  # type: ignore

def describe_image(image: Image.Image, text:str|None):
    # Preprocess inputs
    inputs = processor(images=image, text=text, return_tensors="pt").to(device)

    # Inference
    generated_ids = model.generate(**inputs)

    # Decode the output
    generated_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
    return str(generated_text)
