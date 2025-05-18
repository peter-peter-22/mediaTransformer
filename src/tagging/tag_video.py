import torch
from src.common.device import device
from transformers.models.auto.processing_auto import AutoProcessor
from transformers.models.auto.modeling_auto import AutoModelForVision2Seq

model_name="HuggingFaceTB/SmolVLM-Instruct-250M"
processor = AutoProcessor.from_pretrained(model_name)
model = AutoModelForVision2Seq.from_pretrained(
    model_name, torch_dtype=torch.bfloat16,
    _attn_implementation="flash_attention_2" if device == "cuda" else "eager",
).to(device)

def tag_video(video_path:str):
    print("Describing video...")
    messages = [
        {
            "role": "user",
            "content": [
                {"type": "video", "path": video_path},
                {"type": "text", "text": "Describe this video"}
            ]
        },
    ]

    prompt = processor.apply_chat_template(messages, add_generation_prompt=True)
    inputs = processor(text=prompt, return_tensors="pt").to(device)
    
    generated_ids = model.generate(**inputs, max_new_tokens=64)
    generated_texts = processor.batch_decode(
        generated_ids,
        skip_special_tokens=True,
    )

    print("Description: ",generated_texts[0])

