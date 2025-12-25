from typing import Optional
from datetime import date

from pydantic import BaseModel, ConfigDict


class ProfileCreate(BaseModel):
    name: str
    surname: str
    phone: str
    birthday: date
    photo: str
    user_id: int

class ProfileUpdate(BaseModel):
    name: Optional[str] = None
    surname: Optional[str] = None
    phone: Optional[str] = None
    birthday: Optional[date] = None
    photo: Optional[str] = None

class Profile(ProfileCreate):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
