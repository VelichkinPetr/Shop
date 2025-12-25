from typing import Optional
from datetime import datetime

from pydantic import BaseModel, ConfigDict

from schemas.order_items import OrderItem
from models.order import OrderStatus


class OrderCreate(BaseModel):
    status: Optional[OrderStatus] = None
    total_price: Optional[int] = None
    profile_id: int

class OrderUpdate(BaseModel):
    status: Optional[OrderStatus] = None
    total_price: Optional[int] = None
    
class Order(OrderCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
    order_item: list[OrderItem]
    created_at: datetime
    updated_at: datetime