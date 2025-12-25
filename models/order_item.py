from typing import TYPE_CHECKING

from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from models.base import Base
from .mixin import IDMixin

if TYPE_CHECKING:
    from . import Order, Product

class OrderItem(Base, IDMixin):
    __tablename__ = 'order_items'

    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False)
    cost: Mapped[int] = mapped_column(Integer, nullable=False)

    product_id: Mapped[int] = mapped_column(ForeignKey("products.id", ondelete='CASCADE'))
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id", ondelete='CASCADE'))

    product: Mapped['Product'] = relationship(back_populates='order_item')
    order: Mapped['Order'] = relationship(back_populates='order_item')