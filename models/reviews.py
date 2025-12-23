from typing import TYPE_CHECKING
from sqlalchemy import Integer, ForeignKey, Text
from sqlalchemy.orm import mapped_column, Mapped, relationship

from models.base import Base
from .mixin import IDMixin

if TYPE_CHECKING:
    from . import Profile, Product


class Review(Base, IDMixin):
    __tablename__ = 'reviews'

    rate: Mapped[int] = mapped_column(Integer, nullable=False)
    comment: Mapped[str] = mapped_column(Text, nullable=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    profile_id: Mapped[int] = mapped_column(ForeignKey("profiles.id"))
    
    # Связи с основной моделью
    profile: Mapped['Profile'] = relationship(back_populates='reviews')
    product: Mapped['Product'] = relationship(back_populates='reviews')