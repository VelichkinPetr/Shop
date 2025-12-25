from typing import Optional
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class CartItemCreate(BaseModel):
    count: int
    product_id: int

class CartItemUpdate(BaseModel):
    count: Optional[int] = None

class CartItem(CartItemCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
    cart_id: int
    created_at: datetime
    updated_at: datetime