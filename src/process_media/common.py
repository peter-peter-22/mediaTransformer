from pydantic import BaseModel

class Vector2Int(BaseModel):
    x:int
    y:int