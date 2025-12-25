from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from api.errors.Exceptions import HTTPError
from core.security import get_current_user
from database import get_db
from services import CartService, ProductService
from schemas import UserPublic, CartRead, CartItemCreate, CartItemUpdate


router = APIRouter()

@router.get('',
            response_model=CartRead,
            status_code=status.HTTP_200_OK)
def get_cart(
        db: Session = Depends(get_db),
        user: UserPublic = Depends(get_current_user)
) -> CartRead:
    if user.profile is None:
        raise HTTPError.not_found
    cart = CartService.get_cart(db, user.profile.id)
    if cart is None:
        raise HTTPError.not_found
    return cart

@router.post('/items',
             response_model=CartRead,
             status_code=status.HTTP_201_CREATED)
def create_cart_item(
        item_data: CartItemCreate,
        db: Session = Depends(get_db),
        user: UserPublic = Depends(get_current_user)
) -> CartRead:
    product = ProductService.get_product(db, item_data.product_id)
    if product is None or user.profile is None:
        raise HTTPError.not_found
    updated_cart = CartService.add_cart_item(db, user.profile.id, item_data)
    return updated_cart

@router.post('/{item_id}',
             response_model=CartRead,
             status_code=status.HTTP_200_OK)
def update_cart_item(
        item_id: int,
        item_data: CartItemUpdate,
        db: Session = Depends(get_db),
        user: UserPublic = Depends(get_current_user)
) -> CartRead:
    if user.profile is None:
        raise HTTPError.not_found
    updated_item = CartService.update_cart_item(db, user.profile.id, item_id, item_data)
    if updated_item is None:
        raise HTTPError.not_found
    return updated_item

@router.delete('/{item_id}',
               response_model=CartRead,
               status_code=status.HTTP_202_ACCEPTED)
def delete_cart_item(
        item_id: int,
        db: Session = Depends(get_db),
        user: UserPublic = Depends(get_current_user)
) -> CartRead:
    if user.profile is None:
        raise HTTPError.not_found
    updated_card = CartService.delete_cart_item(db, user.profile.id, item_id)
    if updated_card is None:
        raise HTTPError.not_found
    return updated_card

