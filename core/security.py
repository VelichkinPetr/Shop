from fastapi import Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import Session
from pwdlib import PasswordHash

from api.errors.Exceptions import HTTPError
from database import get_db
from services import UserService
from schemas import UserPublic


basic_auth = HTTPBasic()
password_hash = PasswordHash.recommended()

def get_current_user(
        db: Session = Depends(get_db),
        credentials: HTTPBasicCredentials = Depends(basic_auth)
) -> UserPublic:
    user = UserService.get_me(db, email=credentials.username)
    if user is None or not password_hash.verify(credentials.password, user.password.get_secret_value()):
        raise HTTPError.unauthorized
    return UserPublic(**user.model_dump(exclude={'password'}))

def get_current_admin(
        db: Session = Depends(get_db),
        credentials: HTTPBasicCredentials = Depends(basic_auth)
) -> UserPublic:
    user = get_current_user(db, credentials=credentials)
    if not user.is_admin:
        raise HTTPError.unavailable
    return UserPublic(**user.model_dump(exclude={'password'}))