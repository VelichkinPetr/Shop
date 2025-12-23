from typing import TYPE_CHECKING
from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import mapped_column, relationship, Mapped

from models.base import Base
from .associative import products_categories
from .mixin import IDMixin

if TYPE_CHECKING:
    from . import Category, CartItem, OrderItem, Review


class Product(Base, IDMixin):
    __tablename__ = 'products'
    
    name: Mapped[str] = mapped_column(String, nullable=False)
    article: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    preview_text: Mapped[str] = mapped_column(Text)
    detail_text: Mapped[str] = mapped_column(Text)
    price: Mapped[int] = mapped_column(Integer, nullable=False)

    category: Mapped[list['Category']] = relationship(
        secondary=products_categories, 
        back_populates="product"
    )

    reviews: Mapped[list['Review']] = relationship(back_populates='product')
    order_item: Mapped[list['OrderItem']] = relationship(back_populates='product')
    cart_item: Mapped[list['CartItem']] = relationship(back_populates='product')