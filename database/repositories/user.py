from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from sqlalchemy import select

from api.errors.Exceptions import SQLError
from database.repositories import BaseRepo
from models import User


class UserRepo(BaseRepo):

    model = User

    @classmethod
    def get_by_email(cls,
                     db: Session,
                     email:str
    ) -> User | None:
        try:
            query = select(cls.model).where(cls.model.email == email)
            user = db.scalar(query)
            return user
        except SQLAlchemyError as db_error:
            raise SQLError('Error in',cls.model.__name__, db_error)
