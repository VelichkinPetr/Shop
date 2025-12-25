from typing import TYPE_CHECKING

from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import mapped_column, relationship, Mapped

from models.base import Base
from .associative import products_categories
from .mixin import IDMixin

if TYPE_CHECKING:
    from . import Product


class Category(Base, IDMixin):
    __tablename__ = 'categories'

    name: Mapped[str] = mapped_column(String, nullable=False)
    slug: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, default=None)
    photo: Mapped[str] = mapped_column(String, default= '')
    sort: Mapped[int] = mapped_column(Integer, nullable=False)
    parent_id: Mapped[int] = mapped_column(Integer, ForeignKey('categories.id'), nullable=True)

    category_parent: Mapped['Category'] = relationship('Category', remote_side='Category.id', back_populates='category_child')
    category_child: Mapped[list['Category']] = relationship('Category', back_populates='category_parent')
    
    product: Mapped[list['Product']] = relationship(
        secondary=products_categories,
        back_populates="category"
    )