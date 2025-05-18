from typing import List
from pydantic import BaseModel
from dataclasses import dataclass

@dataclass
class VariantUpload:
    object_name:str
    bucket_name:str
    mime_type:str

@dataclass
class ImageUploadResponse:
    files:List[VariantUpload]
    label:str|None=None
    text: str|None=None

@dataclass
class VideoUploadResponse:
    files:List[VariantUpload]
    label:str|None=None
