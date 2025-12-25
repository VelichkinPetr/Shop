from typing import Optional

from pydantic import BaseModel, ConfigDict


class ReviewCreate(BaseModel):
    rate: int
    comment: str

class ReviewUpdate(BaseModel):
    rate: Optional[int] = None
    comment: Optional[str] = None

class Review(ReviewCreate):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    product_id: int
    profile_id: int