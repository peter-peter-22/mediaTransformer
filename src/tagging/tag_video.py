import torch
import torch.nn.functional as F
from pytorchvideo.models.hub import slow_r50
from pytorchvideo.data.encoded_video import EncodedVideo
from torchvision.transforms import Compose, Lambda
from pytorchvideo.transforms import (
    ApplyTransformToKey,
    UniformTemporalSubsample,
    ShortSideScale,
)
from collections import Counter
from torchvision.transforms._transforms_video import (
    CenterCropVideo,
    NormalizeVideo,
)
import json
from typing import Dict
from src.common.device import device
from pytorchvideo.data.video import Video
from typing import List
from src.common.lerp import lerp, inverse_lerp
import math
from pathlib import Path

# Get class names and their ids
json_filename = Path(__file__).parent / Path('kinetics_classnames.json')
with open(json_filename, "r") as f:
    kinetics_classnames:Dict[str,int] = json.load(f)

# Create an id to label name mapping
kinetics_id_to_classname:Dict[int,str] = {}
for k, v in kinetics_classnames.items():
    kinetics_id_to_classname[v] = str(k).replace('"', "") # Remove " symbols

# Load model and preprocessing
model = slow_r50(pretrained=True).to(device)
model = model.eval()

# Video transform parameters
side_size = 256
mean = [0.45, 0.45, 0.45]
std = [0.225, 0.225, 0.225]
crop_size = 256
num_frames = 8

# Create video transformer
transform = ApplyTransformToKey(
    key="video",
    transform=Compose([
        UniformTemporalSubsample(num_frames),
        Lambda(lambda x: x/255.0),
        NormalizeVideo(mean, std),
        ShortSideScale(
            size=side_size
        ),
        CenterCropVideo(crop_size),
    ])
)

def tag_video(video_path:str, top_k:int, min_confidence:float):

    # Load video
    video = EncodedVideo.from_path(video_path)
    video:Video
    
    # Get duration
    total_duration = float(video.duration)
    
    # Calculate clips
    clip_duration = 5 
    clip_count=math.floor(lerp(5,20,inverse_lerp(10,600,total_duration)))
    clip_step=total_duration/clip_count

    # Process video in clips
    print("Processing clips...")
    all_tags:List[str] = []
    for i in range(clip_count):
        # Calculate interval of the clip
        start_time=clip_step * i
        end_time = start_time + clip_duration
        try:
            # Get a clip 
            a = video.get_clip(start_sec=start_time, end_sec=end_time)

            # Transform clip
            clip = transform(a) # type: ignore
            inputs = clip["video"].unsqueeze(0).to(device)  # Add batch dimension

            # Predict
            with torch.no_grad():
                preds = model(inputs)
            probs = F.softmax(preds, dim=1)
        
            # Get top k predictions
            top_probs, top_indices = torch.topk(probs, k=top_k)

            # Format the results
            results=zip(top_probs.tolist()[0],top_indices.tolist()[0])

            # Get the class names of the top k predictions
            pred_class_names = [(kinetics_id_to_classname[int(i)],round(prob,3)) for prob,i in results]
            print(f"Clip {start_time:.1f}-{end_time:.1f}s: {pred_class_names}")

            # Add the tags above the confidence threshold to the list
            all_tags.extend([name for name,prob in pred_class_names if prob>min_confidence])

        except Exception as e:
            print(f"Error processing clip {start_time:.1f}-{end_time:.1f}: {e}")

    # Aggregate and summarize tags 
    tag_counts = Counter(all_tags)
    summary = tag_counts.most_common(top_k)

    print("\n--- Final Top Tags ---")
    for tag, count in summary:
        print(f"{tag}: {count}")

    # Return only the names
    return [e[0] for e in summary]
