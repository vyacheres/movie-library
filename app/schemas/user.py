from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserBase(BaseModel):
    username: str
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class UserCreate(UserBase):
    # bcrypt не поддерживает пароли длиннее 72 байт — ограничиваем на уровне схемы
    password: str = Field(..., min_length=8, max_length=72)
    favorite_genre_id: Optional[int] = None


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    favorite_genre_id: Optional[int] = None


class PasswordChange(BaseModel):
    current_password: str
    new_password: str = Field(..., min_length=8, max_length=72)


class UserInDBBase(UserBase):
    id: int
    created_at: datetime
    is_active: bool
    is_superuser: bool
    favorite_genre_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


class User(UserInDBBase):
    pass


class UserInDB(UserInDBBase):
    hashed_password: str
