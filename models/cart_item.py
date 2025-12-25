from typing import TYPE_CHECKING

from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from models.base import Base
from .mixin import IDMixin, TimeStampMixin

if TYPE_CHECKING:
    from . import Cart, Product

class CartItem(Base, IDMixin, TimeStampMixin):
    __tablename__ = 'cart_items'

    count: Mapped[int] = mapped_column(Integer, nullable=False)
    product_id: Mapped[int] = mapped_column("products", ForeignKey("products.id", ondelete='CASCADE'))
    cart_id: Mapped[int] = mapped_column("carts", ForeignKey("carts.id", ondelete='CASCADE'))

    cart: Mapped['Cart'] = relationship(back_populates='cart_item')
    product: Mapped['Product'] = relationship(back_populates='cart_item')