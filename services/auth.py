from sqlalchemy.orm import Session

from api.errors.Exceptions import HTTPError, SQLError
from core.security import password_hash
from schemas import UserCreate, UserPublic, CartCreate
from services.cart import CartService
from services.user import UserService


class AuthService:
    user_service = UserService
    cart_service = CartService

    @classmethod
    def registration(cls,
                     db: Session,
                     user_data: UserCreate
    ) -> UserPublic:
        hashed_password = password_hash.hash(user_data.password.get_secret_value())
        user_data.password = hashed_password
        try:
            new_user = cls.user_service.create_user(db, user_data)
            empty_profile = cls.user_service.create_profile(db, new_user.id)
            cart_data = CartCreate(profile_id=empty_profile.id)
            new_cart = cls.cart_service.create_cart(db, cart_data)
            return UserPublic(**new_user.model_dump(exclude={'password'}))
        except SQLError:
            raise HTTPError.exist
