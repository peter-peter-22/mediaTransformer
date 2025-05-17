from typing import List
from pydantic import BaseModel

class VariantUpload(BaseModel):
    object_name:str
    bucket_name:str
    mime_type:str

class ImageUploadResponse(BaseModel):
    label:str|None=None
    text: str|None=None
    files:List[VariantUpload]

class VideoUploadResponse(BaseModel):
    object_name:str
    bucket_name:str
    mime_type:str
    tags:List[str]|None=None
