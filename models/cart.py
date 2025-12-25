from typing import TYPE_CHECKING

from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import mapped_column, relationship, Mapped

from models.base import Base
from .mixin import IDMixin, TimeStampMixin

if TYPE_CHECKING:
    from . import Profile, CartItem 

class Cart(Base, IDMixin, TimeStampMixin):
    __tablename__ = 'carts'

    profile_id: Mapped[int] = mapped_column(Integer, ForeignKey('profiles.id', ondelete='CASCADE'))

    profile: Mapped['Profile'] = relationship(back_populates='cart')
    cart_item: Mapped[list['CartItem']] = relationship(back_populates='cart', cascade="all, delete-orphan")