from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from api.errors.Exceptions import HTTPError
from core.security import get_current_user
from database import get_db
from services import OrderService
from schemas import UserPublic, OrderRead


router = APIRouter()

@router.post('',
             response_model=OrderRead,
             status_code=status.HTTP_201_CREATED)
def create_order(
    db: Session = Depends(get_db),
    user: UserPublic = Depends(get_current_user)
) -> OrderRead:
    if user.profile is None:
        raise HTTPError.not_found
    new_order = OrderService.create_order(db, user.profile.id)
    if new_order is None:
        raise HTTPError.not_found
    return new_order

@router.get('',
            response_model=list[OrderRead],
            status_code=status.HTTP_200_OK)
def list_my_orders(
    db: Session = Depends(get_db),
    user: UserPublic = Depends(get_current_user)
) -> list[OrderRead]:
    if user.profile is None:
        raise HTTPError.not_found
    orders = OrderService.list_orders(db, user.profile.id)
    return orders

@router.get('/{order_id}',
            response_model=OrderRead,
            status_code=status.HTTP_200_OK)
def get_my_order(
        order_id: int,
        db: Session = Depends(get_db),
        user: UserPublic = Depends(get_current_user)
) -> OrderRead:
    if user.profile is None:
        raise HTTPError.not_found
    order = OrderService.get_order(db, user.profile.id, order_id)
    if order is None:
        raise HTTPError.not_found
    return order
