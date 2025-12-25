from sqlalchemy.orm import Session

from database.repositories import OrderRepo, CartRepo
from schemas import OrderRead, OrderCreate


class OrderService:

    cart_repo = CartRepo
    order_repo = OrderRepo
    order_schema = OrderRead

    @classmethod
    def create_order(cls,
                     db: Session,
                     profile_id: int
    ) -> OrderRead | None:

    #получил корзину и проверил не пуста ли она
        my_cart = cls.cart_repo.get_my_cart(db, profile_id)
        if not my_cart.cart_item:
            return None
    #создал пустой заказ если корзина не пуста
        order_data = OrderCreate(profile_id=profile_id)
        new_order = cls.order_repo.create(db, order_data)
    #добавил в заказ вск позиции корзины
        ready_order = cls.order_repo.add_order_items(db, new_order, my_cart)
    #очистил корзину
        cls.cart_repo.delete_cart(db, my_cart)

        return cls.order_schema.model_validate(ready_order)

    @classmethod
    def list_orders(cls,
                    db: Session,
                    profile_id: int
    ) -> list[OrderRead]:
        orders = cls.order_repo.list_orders(db, profile_id)
        if not orders:
            return []
        orders_out = []
        for order in orders:
            orders_out.append(cls.order_schema.model_validate(order))
        return orders_out

    @classmethod
    def get_order(cls,
                  db: Session,
                  profile_id: int,
                  order_id: int
    ) -> OrderRead | None:
        order = cls.order_repo.get_order(db, profile_id, order_id)
        if order is None:
            return None
        return cls.order_schema.model_validate(order)