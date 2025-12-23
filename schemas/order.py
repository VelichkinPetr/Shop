from typing import Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict

from schemas.order_items import OrderItem
from models.order import OrderStatus


class OrderCreate(BaseModel):
    status: OrderStatus
    total_price: int

class OrderUpdate(BaseModel):
    status: Optional[str] = None
    total_price: Optional[int] = None
    
class Order(OrderCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
    order_item: list[OrderItem]
    profile_id: int
    created_at: datetime
    updated_at: datetime