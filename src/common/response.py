from typing import List
from pydantic import BaseModel
from dataclasses import dataclass

@dataclass
class VariantUpload:
    object_name:str
    bucket_name:str
    mime_type:str

@dataclass
class UploadResponse:
    files:List[VariantUpload]
    label:str|None=None