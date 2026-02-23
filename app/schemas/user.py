from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None


class UserCreate(UserBase):
    password: str
    favorite_genre: Optional[str] = None
    is_superuser: bool = False


class UserUpdate(UserBase):
    full_name: Optional[str] = None
    favorite_genre: Optional[str] = None
    password: Optional[str] = None


class UserInDBBase(UserBase):
    id: int
    created_at: datetime
    is_active: bool
    is_superuser: bool
    favorite_genre: Optional[str] = None

    class Config:
        from_attributes = True


class User(UserInDBBase):
    pass


class UserInDB(UserInDBBase):
    hashed_password: str
