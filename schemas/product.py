from typing import Optional

from pydantic import BaseModel, ConfigDict

from schemas.category import Category
from schemas.reviews import Review


class ProductCreate(BaseModel):
    name: str
    article: str
    preview_text: str
    detail_text: str
    price: int
    category: list[Category]
    reviews: list[Review]

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    article: Optional[str] = None
    preview_text: Optional[str] = None
    detail_text: Optional[str] = None
    price: Optional[int] = None
    
class Product(ProductCreate):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
