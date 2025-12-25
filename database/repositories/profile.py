from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from sqlalchemy import select

from api.errors.Exceptions import SQLError
from database.repositories import BaseRepo
from models import Profile
from schemas import ProfileRead


class ProfileRepo(BaseRepo):

    model = Profile

    @classmethod
    def get_by_user_id(cls,
                       db: Session,
                       user_id:int
    ) -> ProfileRead | None:
        try:
            query = select(cls.model).where(cls.model.user_id == user_id)
            profile = db.scalar(query)
            return profile
        except SQLAlchemyError as db_error:
            raise SQLError('Error in',cls.model.__name__, db_error)
