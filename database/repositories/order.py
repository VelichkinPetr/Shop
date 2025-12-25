from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from api.errors.Exceptions import SQLError
from database.repositories import ProductRepo, BaseRepo
from models import Order, OrderItem, Cart


class OrderRepo(BaseRepo):

    product_repo = ProductRepo
    model = Order

    @classmethod
    def list_orders(cls,
                    db: Session,
                    profile_id: int
    ) -> list[Order]:
        query = select(cls.model).where(cls.model.profile_id == profile_id)
        orders = db.scalars(query).all()
        return orders

    @classmethod
    def get_order(cls,
                  db: Session,
                  profile_id: int,
                  order_id: int
    ) -> Order:
        query = (select(cls.model).where(cls.model.profile_id == profile_id)
                                  .where(cls.model.id == order_id))
        order = db.scalar(query)
        return order

    @classmethod
    def add_order_items(cls,
                       db: Session,
                       order: Order,
                       my_cart: Cart
    ) -> Order:
        try:
            # счетчик цены
            total_price = order.total_price
            # прошелся по всем позициям корзины и добавил в заказ с подсчетом цены за позицию
            for cart_item in my_cart.cart_item:
                product = cls.product_repo.get_by_id(db, cart_item.product_id)

                cost = cart_item.count * product.price
                total_price += cost
                new_item = OrderItem(
                    quantity=cart_item.count,
                    product_id=cart_item.product_id,
                    price = product.price,
                    cost = cost,
                    order_id = order.id
                )
                order.order_item.append(new_item)
            #добавил общую цену
            order.total_price += total_price
            db.commit()
            db.refresh(order)
            return order
        except SQLAlchemyError as db_error:
            db.rollback()
            raise SQLError('Error in', cls.model.__name__, db_error)
