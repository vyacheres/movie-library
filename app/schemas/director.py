from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class DirectorBase(BaseModel):
    first_name: str
    last_name: str
    birth_date: Optional[datetime] = None
    biography: Optional[str] = None


class DirectorCreate(DirectorBase):
    pass


class DirectorUpdate(DirectorBase):
    pass


class DirectorInDBBase(DirectorBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class Director(DirectorInDBBase):
    pass


class DirectorInDB(DirectorInDBBase):
    pass
