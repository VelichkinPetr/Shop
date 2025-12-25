import datetime

from sqlalchemy.orm import Session

from database.repositories import UserRepo, ProfileRepo
from schemas import (UserRead, UserUpdate, UserCreate, UserPublic,
                    ProfileRead, ProfileUpdate, ProfileCreate)


class UserService:

    user_repo = UserRepo
    profile_repo = ProfileRepo
    user_schema = UserRead
    user_public = UserPublic
    profile_schema = ProfileRead

    @classmethod
    def create_user(cls,
                    db: Session,
                    user_data: UserCreate
    ) -> UserRead:
        new_user = cls.user_repo.create(db, user_data)
        return cls.user_schema.model_validate(new_user)

    @classmethod
    def get_me(cls,
               db: Session,
               email:str
    ) -> UserRead | None:
        me = cls.user_repo.get_by_email(db, email)
        if me is None:
            return None
        return cls.user_schema.model_validate(me)

    @classmethod
    def update_me(cls,
                  session: Session,
                  user_id: int,
                  user_data: UserUpdate
    ) -> UserPublic:
        updated_me = cls.user_repo.update(session, user_id, user_data)
        return cls.user_public.model_validate(updated_me)

    @classmethod
    def create_profile(cls,
                       db: Session,
                       user_id: int,
                       profile_data: ProfileUpdate = None
    ) -> ProfileRead | None:
        my_profile = cls.profile_repo.get_by_user_id(db, user_id)
        if my_profile is not None:
            return None
        if profile_data is None:
            profile_data = ProfileCreate(name='', surname='', phone='',
                                         birthday=datetime.date(1970, 1, 1),
                                         photo='', user_id=user_id)
        else:
            profile_data = ProfileCreate(**profile_data.model_dump(), user_id=user_id)
        new_profile = cls.profile_repo.create(db, profile_data)
        return cls.profile_schema.model_validate(new_profile)

    @classmethod
    def update_me_profile(cls,
                          db: Session,
                          user_id: int,
                          profile_data: ProfileUpdate
    ) -> ProfileRead | None:
        my_profile = cls.profile_repo.get_by_user_id(db, user_id)
        if my_profile is None:
            return None
        data = ProfileCreate(**profile_data.model_dump(), user_id=user_id)
        update_profile = cls.profile_repo.update(db, my_profile.id, data)
        return cls.profile_schema.model_validate(update_profile)

    @classmethod
    def delete_profile(cls,
                       db: Session,
                       user_id: int
    ) -> bool:
        my_profile = cls.profile_repo.get_by_user_id(db, user_id)
        if my_profile is not None:
            cls.profile_repo.delete_by_id(db, my_profile.id)
            return True
        return False

