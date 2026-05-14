from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

from app.schemas.movie import Movie


class FavoriteBase(BaseModel):
    movie_id: int


class FavoriteCreate(FavoriteBase):
    """Только movie_id; user_id выставляется сервером из JWT."""

    pass


class FavoriteInDBBase(BaseModel):
    id: int
    user_id: int
    movie_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class Favorite(FavoriteInDBBase):
    movie: Optional[Movie] = None


class FavoriteInDB(FavoriteInDBBase):
    pass
