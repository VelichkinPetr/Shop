from pydantic import BaseModel, ConfigDict


class OrderItemCreate(BaseModel):
    quantity: int
    product_id: int


class OrderItem(OrderItemCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
    price: int
    cost: int
    order_id: int