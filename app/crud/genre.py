from typing import Optional

from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.genre import Genre
from app.schemas.genre import GenreCreate, GenreUpdate


class CRUDGenre(CRUDBase[Genre, GenreCreate, GenreUpdate]):
    def get_by_name(self, db: Session, name: str) -> Optional[Genre]:
        return db.query(self.model).filter(self.model.name == name).first()


crud_genre = CRUDGenre(Genre)
