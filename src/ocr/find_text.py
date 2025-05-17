from src.common.device import device
from PIL import Image
import numpy as np
from typing import List
from transformers.pipelines import pipeline
from transformers.models.auto.processing_auto import AutoProcessor
from transformers.models.blip import BlipForConditionalGeneration

processor = AutoProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

def test(image: Image.Image, text:str):
    
    inputs = processor(images=image, text=text, return_tensors="pt")

    generated_ids = model.generate(**inputs)

    generated_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
    print(generated_text)
