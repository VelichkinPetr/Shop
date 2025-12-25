from sqlalchemy import select, delete
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from api.errors.Exceptions import SQLError
from database.repositories import BaseRepo
from models import Cart, CartItem
from schemas import CartItemCreate, CartItemUpdate


class CartRepo(BaseRepo):

    model = Cart
    cart_item_model = CartItem

    @classmethod
    def get_my_cart(cls,
               db: Session,
               profile_id: int
    ) -> Cart:
       query = select(cls.model).where(cls.model.profile_id == profile_id)
       elem = db.scalar(query)
       return elem

    @classmethod
    def add_cart_item(cls,
                    db: Session,
                    my_cart: Cart,
                    cart_item_data: CartItemCreate
    ) -> Cart:
        try:
            new_item = cls.cart_item_model(**cart_item_data.model_dump(), cart_id = my_cart.id)
            my_cart.cart_item.append(new_item)
            db.commit()
            db.refresh(my_cart)
            return my_cart
        except SQLAlchemyError as db_error:
            db.rollback()
            raise SQLError('Error in', cls.model.__name__, db_error)

    @classmethod
    def get_item(cls,
                 db: Session,
                 profile_id: int,
                 product_id: int
    ) -> CartItem:
       query = (select(cls.cart_item_model).join(cls.model)
                .where(cls.model.profile_id == profile_id)
                .where(cls.cart_item_model.product_id == product_id))
       cart_item = db.scalar(query)
       return cart_item

    @classmethod
    def update_item(cls,
                    db: Session,
                    item_id: int,
                    new_item: CartItemUpdate
    ) -> CartItem | None:
        try:
           query = (select(cls.cart_item_model)
                    .where(cls.cart_item_model.id == item_id))
           cart_item = db.scalar(query)
           if cart_item is not None:
               for key, value in new_item.model_dump().items():
                   if value is not None:
                    setattr(cart_item, key, value)
               db.commit()
               db.refresh(cart_item)
               return cart_item
           return None
        except SQLAlchemyError as db_error:
            db.rollback()
            raise SQLError('Error in', cls.model.__name__, db_error)

    @classmethod
    def delete_item(cls,
                    db: Session,
                    item_id: int
    ) -> bool:
        try:
           query = (select(cls.cart_item_model)
                    .where(cls.cart_item_model.id == item_id))
           cart_item = db.scalar(query)
           if cart_item is not None:
               db.delete(cart_item)
               db.commit()
               return True
           return False
        except SQLAlchemyError as db_error:
            db.rollback()
            raise SQLError('Error in', cls.model.__name__, db_error)

    @classmethod
    def delete_cart(cls,
                    db: Session,
                    my_cart: Cart
    ) -> Cart:
        try:
            query = (delete(cls.cart_item_model)
                     .where(cls.cart_item_model.cart_id == my_cart.id))
            db.execute(query)
            db.commit()
            db.refresh(my_cart)
            return my_cart
        except SQLAlchemyError as db_error:
            db.rollback()
            raise SQLError('Error in', cls.model.__name__, db_error)

