from pydantic import BaseModel,ConfigDict
from typing import Literal, List
from src.process_media.common import Vector2Int

type ImageFormat=Literal["WEBP","JPEG"]

class ImageVariant(BaseModel):
    object_name: str
    bucket_name: str|None=None
    convert_to: ImageFormat|None=None
    quality: int|None=None
    limit_resolution: Vector2Int|None=None
    upload_mime_type:str|None=None

class ImageOptions(BaseModel):
    model_config = ConfigDict(strict=True)

    bucket_name: str
    object_name: str
    mime_type: str|None=None
    upload_mime_type:str
    convert_to: ImageFormat|None=None
    quality: int|None=None
    limit_resolution: Vector2Int|None=None
    max_size: int|None=None
    describe: bool=False
    prompt:str="briefly describe the image, be short and to the point"
    prompt_max_tokens: int=32
    variants: List[ImageVariant]=[]
    skip_upload: bool=False
    