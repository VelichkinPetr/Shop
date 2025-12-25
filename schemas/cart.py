from datetime import datetime

from pydantic import BaseModel, ConfigDict

from schemas.cart_item import CartItem


class CartCreate(BaseModel):
    profile_id: int

class Cart(CartCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
    cart_item: list[CartItem]
    created_at: datetime
    updated_at: datetime