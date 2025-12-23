from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select
from sqlalchemy.orm import Session

from pydantic import BaseModel

from api.errors.Exceptions import SQLError
from models import Base


class BaseRepo:
    '''
    model = None : SQLalchemy модель(таблица) из которой берутся данные
    '''

    model = None

    @classmethod
    def create(cls, db: Session, data: BaseModel) -> Base:
        try:
            model = cls.model(**data.model_dump())
            db.add(model)
            db.commit()
            db.refresh(model)
            return model
        except SQLAlchemyError as db_error:
            raise SQLError('Error in',cls.model.__name__, db_error)


    @classmethod
    def get_all(cls, session: Session) -> list[Base]:
        query = select(cls.model)
        elements = session.scalars(query).all()
        return elements
    
    @classmethod
    def get_by_id(cls, session: Session, current_id:int) -> Base | None:
        query = select(cls.model).where(cls.model.id == current_id)
        element = session.scalar(query)
        return element

    @classmethod
    def delete_by_id(cls, session: Session, current_id: int) -> None:
        try:
            query = select(cls.model).where(cls.model.id == current_id)
            elem = session.scalar(query)
            session.delete(elem)
            session.commit()
        except SQLAlchemyError as db_error:
            raise SQLError('Error in',cls.model.__name__, db_error)

    @classmethod
    def update(cls, session: Session, current_id: int, data: BaseModel) -> Base | None:
        try:
            query = select(cls.model).where(cls.model.id == current_id)
            current_elem = session.scalar(query)
            
            for key, value in data.model_dump().items():
                if value is not None:
                    setattr(current_elem, key, value)

            session.commit()
            session.refresh(current_elem)
            return current_elem
        except SQLAlchemyError as db_error:
            raise SQLError('Error in',cls.model.__name__, db_error)

