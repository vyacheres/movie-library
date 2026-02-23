from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

from app.schemas.movie import Movie


class FavoriteBase(BaseModel):
    movie_id: int


class FavoriteCreate(BaseModel):
    user_id: Optional[int] = None
    movie_id: int


class FavoriteInDBBase(BaseModel):
    id: int
    user_id: int
    movie_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class Favorite(FavoriteInDBBase):
    movie: Optional[Movie] = None

    model_config = ConfigDict(from_attributes=True)


class FavoriteInDB(FavoriteInDBBase):
    pass
