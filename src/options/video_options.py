from pydantic import BaseModel,ConfigDict
from typing import Literal
from src.options.common import Vector2Int

type VideoFormat=Literal["mp4","webm"]

class FfmpegSettings(BaseModel):
    model_config = ConfigDict(strict=True)

    vf:str|None=None
    vcodec:str|None=None
    acodec:str|None=None


class VideoOptions(BaseModel):
    model_config = ConfigDict(strict=True)

    bucket_name: str
    object_name: str
    mime_type: str|None=None
    upload_mime_type:str
    convertTo: VideoFormat|None=None
    bitrate: str|None=None
    limit_resolution: Vector2Int|None=None
    max_size: int|None=None
    tag:bool=False
    tagging_min_confidence:float=0.7
    tagging_top_k:int=5    
    ffmpeg_settings:FfmpegSettings|None=None

    