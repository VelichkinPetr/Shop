from fastapi import APIRouter, status
from fastapi.params import Depends
from sqlalchemy.orm import Session

from database.session import get_db
from services.auth import AuthService
from schemas.user import UserCreate


router = APIRouter()

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register_user(user_data: UserCreate, db: Session = Depends(get_db)) -> None:
    AuthService.registration(db, user_data)