from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from pydantic import BaseModel

from api.errors.Exceptions import SQLError
from models import Base


class BaseRepo:
    '''
    model = None : SQLalchemy модель(таблица) из которой берутся данные
    '''

    model = None

    @classmethod
    def create(cls,
               db: Session,
               data: BaseModel
    ) -> Base:
        try:
            model = cls.model(**data.model_dump())
            db.add(model)
            db.commit()
            db.refresh(model)
            return model
        except SQLAlchemyError as db_error:
            db.rollback()
            raise SQLError('Error in',cls.model.__name__, db_error)

    @classmethod
    def get_all(cls,
                db: Session
    ) -> list[Base]:
        query = select(cls.model)
        elements = db.scalars(query).all()
        return elements
    
    @classmethod
    def get_by_id(cls,
                  db: Session,
                  current_id:int
    ) -> Base | None:
        query = select(cls.model).where(cls.model.id == current_id)
        element = db.scalar(query)
        return element

    @classmethod
    def delete_by_id(cls,
                     db: Session,
                     current_id: int
    ) -> None:
        try:
            query = select(cls.model).where(cls.model.id == current_id)
            elem = db.scalar(query)
            db.delete(elem)
            db.commit()
        except SQLAlchemyError as db_error:
            db.rollback()
            raise SQLError('Error in',cls.model.__name__, db_error)

    @classmethod
    def update(cls,
               db: Session,
               current_id: int,
               data: BaseModel
    ) -> Base | None:
        try:
            query = select(cls.model).where(cls.model.id == current_id)
            current_elem = db.scalar(query)
            
            for key, value in data.model_dump().items():
                if value is not None:
                    setattr(current_elem, key, value)

            db.commit()
            db.refresh(current_elem)
            return current_elem
        except SQLAlchemyError as db_error:
            db.rollback()
            raise SQLError('Error in',cls.model.__name__, db_error)

