from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional


class GenreBase(BaseModel):
    name: str


class Genre(GenreBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class DirectorBase(BaseModel):
    first_name: str
    last_name: str
    biography: Optional[str] = None


class Director(DirectorBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class MovieBase(BaseModel):
    title: str
    description: Optional[str] = None
    release_date: Optional[datetime] = None
    duration: Optional[int] = None
    rating: Optional[float] = None
    poster_url: Optional[str] = None


class MovieCreate(MovieBase):
    genre_id: int
    director_id: int


class MovieUpdate(MovieBase):
    genre_id: Optional[int] = None
    director_id: Optional[int] = None


class MovieInDBBase(MovieBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    genre_id: int
    director_id: int

    class Config:
        from_attributes = True


class Movie(MovieInDBBase):
    genre: Optional[Genre] = None
    director: Optional[Director] = None


class MovieInDB(MovieInDBBase):
    pass
