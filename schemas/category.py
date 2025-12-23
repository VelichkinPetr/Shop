from typing import Optional
from pydantic import BaseModel,ConfigDict

class CategoryCreate(BaseModel):
    name: str
    slug: str
    description: str
    photo: str
    sort: int
    parent_id: int|None

class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    slug: Optional[str] = None
    description: Optional[str] = None
    photo: Optional[str] = None
    sort: Optional[int] = None
    parent_id: Optional[int] = None
    
class Category(CategoryCreate):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
