from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from api.errors.Exceptions import HTTPError
from core.security import get_current_user, get_current_admin
from database import get_db
from services import ProductService
from schemas import UserPublic, ProductRead, ProductUpdate, ProductCreate, ReviewRead, ReviewCreate


router = APIRouter()

@router.post('',
             response_model=ProductRead,
             status_code=status.HTTP_201_CREATED)
def create_product(
            product_data: ProductCreate,
            db: Session = Depends(get_db),
            admin: UserPublic = Depends(get_current_admin)
) -> ProductRead:
    new_product = ProductService.create_product(db, product_data)
    return new_product

@router.get('',
            response_model=list[ProductRead],
            status_code=status.HTTP_200_OK)
def list_products(
            category_id: str = None,
            min_price: int = None,
            max_price: int = None,
            limit: int = 20,
            offset: int = 0,
            db: Session = Depends(get_db),
            user: UserPublic = Depends(get_current_user)
) -> list[ProductRead]:
    products = ProductService.get_by_filter(db, category_id, min_price, max_price, limit, offset)
    return products

@router.get('/{product_id}',
            response_model=ProductRead,
            status_code=status.HTTP_200_OK)
def get_product(
            product_id: int,
            db: Session = Depends(get_db),
            user: UserPublic = Depends(get_current_user)
) -> ProductRead:
    product = ProductService.get_product(db, product_id)
    if product is None:
        raise HTTPError.not_found
    return product

@router.put('/{product_id}',
            response_model=ProductRead,
            status_code=status.HTTP_202_ACCEPTED)
def update_product(
            product_id: int,
            product_data: ProductUpdate,
            category_id: int = None,
            db: Session = Depends(get_db),
            admin: UserPublic = Depends(get_current_admin)
) -> ProductRead:
    if category_id is not None:
        ProductService.add_category(db, product_id, category_id)
    updated_product = ProductService.update_product(db, product_id, product_data)
    if updated_product is None:
        raise HTTPError.not_found
    return updated_product

@router.put('/{product_id}/review',
            response_model=ProductRead,
            status_code=status.HTTP_202_ACCEPTED)
def add_review(
            product_id: int,
            review_data: ReviewCreate,
            db: Session = Depends(get_db),
            user: UserPublic = Depends(get_current_user)
) -> ProductRead:
    updated_product = ProductService.add_review(db, user.profile.id, product_id, review_data)
    if updated_product is None:
        raise HTTPError.not_found
    return updated_product

@router.get('/{product_id}/review',
            response_model=list[ReviewRead],
            status_code=status.HTTP_200_OK)
def get_reviews(
            product_id: int,
            db: Session = Depends(get_db),
            user: UserPublic = Depends(get_current_user)
) -> list[ReviewRead]:
    reviews = ProductService.get_reviews(db, product_id)
    if reviews is None:
        raise HTTPError.not_found
    return reviews

@router.delete('/{product_id}',
               status_code=status.HTTP_202_ACCEPTED)
def delete_product(
            product_id: int,
            db: Session = Depends(get_db),
            admin: UserPublic = Depends(get_current_admin)
):
    is_delete = ProductService.delete_product(db, product_id)
    if not is_delete:
        raise HTTPError.not_found