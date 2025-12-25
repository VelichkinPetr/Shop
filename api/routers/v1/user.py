from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from api.errors.Exceptions import HTTPError
from core.security import get_current_user, password_hash
from database import get_db
from services import UserService
from schemas import UserUpdate, UserPublic, ProfileUpdate, ProfileRead, UserRead


router = APIRouter()

@router.get('/me',
            response_model=UserPublic,
            status_code=status.HTTP_200_OK)
def get_me(user = Depends(get_current_user)):
    return user

@router.put('/me',
            response_model=UserPublic,
            status_code=status.HTTP_200_OK)
def update_me(
            user_data: UserUpdate,
            db: Session = Depends(get_db),
            user: UserPublic = Depends(get_current_user)
) -> UserRead:
    if user_data.password is not None:
        hashed_password = password_hash.hash(user_data.password.get_secret_value())
        user_data.password = hashed_password

    updated_user = UserService.update_me(db, user.id, user_data)
    if updated_user is None:
        raise HTTPError.not_found
    return updated_user

@router.put('/me/profile',
            response_model=ProfileRead,
            status_code=status.HTTP_200_OK)
def update_my_profile(
            profile_data: ProfileUpdate,
            db: Session = Depends(get_db),
            user: UserPublic = Depends(get_current_user)
) -> ProfileRead:
    profile = UserService.update_me_profile(db, user.id, profile_data)
    if profile is None:
        raise HTTPError.not_found
    return profile

@router.delete('/me/profile',
               status_code=status.HTTP_204_NO_CONTENT)
def delete_my_profile(
            db: Session = Depends(get_db),
            user: UserPublic = Depends(get_current_user)
) -> None:
    is_delete = UserService.delete_profile(db, user.id)
    if not is_delete:
        raise HTTPError.not_found