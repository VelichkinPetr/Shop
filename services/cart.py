from sqlalchemy.orm import Session

from database.repositories import CartRepo
from models import Cart
from schemas import CartRead, CartCreate, CartItemCreate, CartItemRead, CartItemUpdate


class CartService:

    cart_repo = CartRepo
    cart_schema = CartRead

    cart_item_schema = CartItemRead

    @classmethod
    def create_cart(cls,
                    db: Session,
                    cart_data: CartCreate
    ) -> CartRead:
        new_cart = cls.cart_repo.create(db, cart_data)
        return cls.cart_schema.model_validate(new_cart)

    @classmethod
    def get_cart(cls,
                 db: Session,
                 profile_id: int
    ) -> CartRead | None:
        my_cart = cls.cart_repo.get_my_cart(db, profile_id)
        if my_cart is not None:
            return cls.cart_schema.model_validate(my_cart)
        return None

    @classmethod
    def add_cart_item(cls,
                      db: Session,
                      profile_id: int,
                      cart_item_data: CartItemCreate
    ) -> CartRead | None:
        my_cart = cls.cart_repo.get_my_cart(db, profile_id)
        updated_cart = cls.cart_repo.add_cart_item(db, my_cart, cart_item_data)
        if updated_cart is not None:
            return cls.cart_schema.model_validate(updated_cart)
        return None

    @classmethod
    def update_cart_item(cls,
                         db: Session,
                         profile_id: int,
                         item_id: int,
                         cart_item_data: CartItemUpdate
    ) -> CartRead | None:

        updated_cart_item = cls.cart_repo.update_item(db, item_id, cart_item_data)
        if updated_cart_item is not None:
            updated_cart = cls.cart_repo.get_my_cart(db, profile_id)
            return cls.cart_schema.model_validate(updated_cart)
        return None

    @classmethod
    def get_cart_item(cls,
                       db: Session,
                       profile_id: int,
                       item_id: int
    ) -> CartItemRead | None:
        cart_item = cls.cart_repo.get_item(db, profile_id, item_id)
        if cart_item is not None:
            return cls.cart_item_schema.model_validate(cart_item)
        return None

    @classmethod
    def delete_cart_item(cls,
                         db: Session,
                         profile_id: int,
                         item_id: int
    ) -> CartRead | None:
        deleted_cart_item = cls.cart_repo.delete_item(db, item_id)
        if deleted_cart_item:
            updated_cart = cls.cart_repo.get_my_cart(db, profile_id)
            return cls.cart_schema.model_validate(updated_cart)
        return None

    @classmethod
    def clear_cart(cls,
                   db: Session,
                   my_cart: Cart
    ) -> CartRead | None:
        clear_cart = cls.cart_repo.delete_cart(db, my_cart)
        return cls.cart_schema.model_validate(clear_cart)