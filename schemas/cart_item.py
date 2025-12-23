from typing import Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict



class CartItemCreate(BaseModel):
    count: int
    product_id: int

class CartItem(CartItemCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime