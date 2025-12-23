from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from api.errors.Exceptions import HTTPError
from core.security import get_current_user

from database.session import get_db


from models import User, Category
from schemas import CategoryRead, CategoryCreate, CategoryUpdate

from services.category import CategoryService

router = APIRouter()



@router.post('',
             response_model=CategoryRead,
             status_code=status.HTTP_201_CREATED)
def create_category(
    category_data: CategoryCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
) -> CategoryRead:
    new_category = CategoryService.create_category(db, category_data)
    return new_category


@router.get('',
            response_model=list[CategoryRead],
            status_code=status.HTTP_200_OK)
def list_categories(
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
) -> list[CategoryRead]:
    categories = CategoryService.list_categories(db)
    if categories is None:
        raise HTTPError.not_found
    return categories

@router.get('/{category_id}', status_code=status.HTTP_200_OK)
def get_category(
        category_id: int,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
) -> CategoryRead:
    category = CategoryService.get_category(db, category_id)
    if category is None:
        raise HTTPError.not_found
    return category

@router.put('/{category_id}',
            response_model=CategoryRead,
            status_code=status.HTTP_200_OK)
def update_category(
        category_id: int,
        category_data: CategoryUpdate,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
) -> CategoryRead:

    updated_category = CategoryService.update_category(db,category_id, category_data)
    if updated_category is None:
        raise HTTPError.not_found
    return updated_category

@router.delete('/{category_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_category(
        category_id: int,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    is_delete = CategoryService.delete_category(db, category_id)
    if not is_delete:
        raise HTTPError.not_found