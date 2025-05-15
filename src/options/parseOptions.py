from pydantic import BaseModel,ConfigDict
from typing import Literal

ImageFormat=Literal["WEBP","JPEG"]

class Vector2Int(BaseModel):
    x:int
    y:int

class ImageOptions(BaseModel):
    model_config = ConfigDict(strict=True)

    bucketName: str
    objectName: str
    mineType: str|None=None
    convertTo: ImageFormat|None=None
    rgbOnly:bool=False
    quality: float|None=None
    maxResolution: Vector2Int|None=None
    maxSize: int|None=None
    # TODO add variants

    