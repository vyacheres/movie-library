from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class GenreBase(BaseModel):
    name: str
    description: Optional[str] = None


class GenreCreate(GenreBase):
    pass


class GenreUpdate(GenreBase):
    pass


class GenreInDBBase(GenreBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class Genre(GenreInDBBase):
    pass


class GenreInDB(GenreInDBBase):
    pass
