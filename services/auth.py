from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from api.errors.Exceptions import HTTPError
from core.security import password_hash
from database.repositories import UserRepo
from models import User
from schemas import UserCreate


class AuthService:
    user_model: User

    @classmethod
    def registration(cls, session: Session, user_data: UserCreate):
        # 1. Создать хэш пароля
        hashed_password = password_hash.hash(user_data.password.get_secret_value())
        # 2. Сохранить данные в БД
        user_data.password = hashed_password
        try:
            UserRepo().create(session, user_data)
        except IntegrityError:
            raise HTTPError.exist
        return None
