import enum
from typing import TYPE_CHECKING

from sqlalchemy import Integer, ForeignKey, Enum
from sqlalchemy.orm import mapped_column, relationship, Mapped

from models.base import Base
from .mixin import IDMixin, TimeStampMixin

if TYPE_CHECKING:
    from . import Profile, OrderItem


class OrderStatus(enum.Enum):
    new = 'new'
    processed = 'processed'
    delivered = 'delivered'
    canceled = 'canceled'


class Order(Base, IDMixin, TimeStampMixin):
    __tablename__ = 'orders'

    status: Mapped[OrderStatus] = mapped_column(Enum(OrderStatus), nullable=False, default= OrderStatus.new)
    total_price: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    profile_id: Mapped[int] = mapped_column(Integer, ForeignKey('profiles.id', ondelete='CASCADE'))

    profile: Mapped['Profile'] = relationship(back_populates='order')
    order_item: Mapped[list['OrderItem']] = relationship(back_populates='order', cascade="all, delete-orphan")