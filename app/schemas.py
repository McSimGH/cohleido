from pydantic import BaseModel
from typing import List

class ImageInput(BaseModel):
    name: str
    type: int
    tags: str

class ImagesList(BaseModel):
    images: List[ImageInput]
    