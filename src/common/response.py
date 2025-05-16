from typing import List
from pydantic import BaseModel

class VariantUpload(BaseModel):
    objectName:str
    bucketName:str
    mimeType:str

class UploadResponse(BaseModel):
    tags:List[str]|None = None
    files:List[VariantUpload]
