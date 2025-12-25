from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from database import get_db
from services import AuthService
from schemas import UserPublic, UserCreate


router = APIRouter()

@router.post("/register",
             response_model=UserPublic,
             status_code=status.HTTP_201_CREATED)
def register_user(
        user_data: UserCreate,
        db: Session = Depends(get_db)
) -> UserPublic:
    new_user = AuthService.registration(db, user_data)
    return new_user