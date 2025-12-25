from sqlalchemy import and_, select
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from api.errors.Exceptions import SQLError
from database.repositories import BaseRepo
from models import Category, Product, Review


class ProductRepo(BaseRepo):

    model = Product

    @classmethod
    def get_by_filter(
                        cls, 
                        db: Session,
                        category_id: str = None,
                        min_price: int = None,
                        max_price: int = None,
                        limit: int = 20,
                        offset: int = 0
    ) -> list[Product]:

        query = select(cls.model)# стандартная модель получения данных, !!!без фильтра!!!

        filters = []# список фильтров

        if category_id is not None:
                # Если есть фильтр по категории, делаем JOIN
                query = query.join(cls.model.category)
                filters.append(Category.id == category_id)

        if min_price is not None:
                # если есть ограничение цены, добавляем его в список фильтров
                filters.append(cls.model.price >= min_price)
        
        if max_price is not None:
                # если есть ограничение цены, добавляем его в список фильтров
                filters.append(cls.model.price <= max_price)
        
        if filters:
                # применяем все фильтры сразу
                query = query.where(and_(*filters))
        # добавляем срезы
        query = query.offset(offset).limit(limit)
        # получаем результат
        products = db.scalars(query).all()
        return products

    @classmethod
    def add_category(cls,
                     db: Session,
                     product: Product,
                     category: Category,
    ) -> Product:
        try:
            product.category.append(category)
            db.commit()
            db.refresh(product)
            return product
        except SQLAlchemyError as db_error:
            db.rollback()
            raise SQLError('Error in',cls.model.__name__, db_error)

    @classmethod
    def add_review(cls,
                   db: Session,
                   product: Product,
                   review: Review
    ) -> Product:
        try:
            product.reviews.append(review)
            db.commit()
            db.refresh(product)
            return product
        except SQLAlchemyError as db_error:
            db.rollback()
            raise SQLError('Error in', cls.model.__name__, db_error)
