from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import Integer, String, Date, ForeignKey
from sqlalchemy.orm import mapped_column, relationship, Mapped

from models.base import Base
from .mixin import IDMixin

if TYPE_CHECKING:
    from . import User, Cart, Order, Review


class Profile(Base, IDMixin):
    __tablename__ = 'profiles'

    name: Mapped[str] = mapped_column(String, nullable=False)
    surname: Mapped[str] = mapped_column(String, nullable=False)
    phone: Mapped[str] = mapped_column(String, nullable=False)
    birthday: Mapped[date] = mapped_column(Date, nullable=False)
    photo: Mapped[str] = mapped_column(String, default='')
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id', ondelete='CASCADE'))

    user: Mapped['User'] = relationship(back_populates='profile')
    cart: Mapped['Cart'] = relationship(back_populates='profile', cascade="all, delete")
    order: Mapped[list['Order']] = relationship(back_populates='profile', cascade="all, delete-orphan")
    reviews: Mapped[list['Review']] = relationship(back_populates='profile', cascade="all, delete-orphan")
