from pydantic import BaseModel,ConfigDict
from typing import Literal, List
from src.options.common import Vector2Int

type ImageFormat=Literal["WEBP","JPEG"]

class ImageVariant(BaseModel):
    object_name: str
    bucket_name: str|None=None
    convert_to: ImageFormat|None=None
    quality: int|None=None
    limit_resolution: Vector2Int|None=None
    max_size: int|None=None
    upload_mime_type:str|None=None

class ImageOptions(BaseModel):
    model_config = ConfigDict(strict=True)

    bucket_name: str
    object_name: str
    mime_type: str|None=None
    upload_mime_type:str
    convertTo: ImageFormat|None=None
    quality: int|None=None
    limit_resolution: Vector2Int|None=None
    max_size: int|None=None
    tag:bool=False
    tagging_min_confidence:float=0.2
    tagging_top_k:int=5
    variants: List[ImageVariant]=[]
    ocr: bool=False
    ocr_min_confidence: float=0.8
    

    