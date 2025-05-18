from src.common.device import device
from transformers.models.auto.processing_auto import AutoProcessor
from transformers.models.auto.modeling_auto import AutoModelForVision2Seq
from PIL import Image
from transformers.generation.stopping_criteria import StoppingCriteria
import torch

model_name="HuggingFaceTB/SmolVLM-Instruct-250M"
processor = AutoProcessor.from_pretrained(model_name)
model = AutoModelForVision2Seq.from_pretrained(
    model_name, 
    torch_dtype=torch.bfloat16
).to(device)

def describe_image(image:Image.Image,prompt,max_tokens):
    print("Describing image...")

    # Form prompt
    messages = [
        {
            "role": "user",
            "content": [
                {"type": "image"},
                {"type": "text", "text": prompt}
            ]
        },
    ]

    # Preprocess input
    prompt = processor.apply_chat_template(
        messages,
        add_generation_prompt=True,
    )
    inputs = processor(text=prompt, images=[image], return_tensors="pt").to(device)
    
    # Generate
    generated_ids = model.generate(
        **inputs, 
        max_new_tokens=max_tokens,
        do_sample=False,
    )

    # Decode
    generated_texts = processor.batch_decode(
        generated_ids,
        skip_special_tokens=True,
    )

    print("Description: ",generated_texts[0])
    return ""