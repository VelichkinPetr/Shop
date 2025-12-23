from sqlalchemy.orm import Session

from database.repositories import UserRepo
from database.repositories.profile import ProfileRepo
from schemas import UserRead, UserUpdate, ProfileRead, ProfileUpdate, ProfileCreate


class UserService:
    user_repo = UserRepo
    profile_repo = ProfileRepo
    user_schema = UserRead
    profile_schema = ProfileRead

    @classmethod
    def get_me(cls, db: Session, email:str) -> UserRead:
        me = cls.user_repo.get_by_email(session=db, email=email)
        return cls.user_schema.model_validate(me)

    @classmethod
    def update_me(cls, session: Session, user_id: int, data: UserUpdate) -> UserRead:
        updated_me = cls.user_repo.update(session, user_id, data)
        return cls.user_schema.model_validate(updated_me)

    @classmethod
    def update_me_profile(cls, db: Session, user_id: int, data: ProfileUpdate) -> ProfileRead:
        my_profile = cls.profile_repo.get_by_user_id(session=db, user_id=user_id)
        data = ProfileCreate(**data.model_dump(), user_id=user_id)
        if my_profile is None:
            new_profile = cls.profile_repo.create(db, data)
        else:
            new_profile = cls.profile_repo.update(db, my_profile.id, data)
        return cls.profile_schema.model_validate(new_profile)

    @classmethod
    def delete_profile(cls, db: Session, user_id: int) -> bool:
        my_profile = cls.profile_repo.get_by_user_id(session=db, user_id=user_id)
        if my_profile is not None:
            cls.profile_repo.delete_by_id(db, my_profile.id)
            return True
        return False

