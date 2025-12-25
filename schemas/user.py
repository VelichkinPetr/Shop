from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, SecretStr, EmailStr

from models.user import UserStatus
from schemas.profile import Profile, ProfileUpdate


class UserCreate(BaseModel):
    email: EmailStr
    password: SecretStr
    status: UserStatus
    is_admin: bool

class UserBase(BaseModel):
    email: EmailStr
    status: UserStatus
    is_admin: bool

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    password: Optional[SecretStr] = None
    status: Optional[UserStatus] = None
    is_admin: Optional[bool] = None

class User(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    profile: Optional[Profile] = None
    created_at: datetime
    updated_at: datetime

class UserInDB(UserCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
    profile: Optional[Profile] = None
    created_at: datetime
    updated_at: datetime