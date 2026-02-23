from sqlalchemy.orm import Session, joinedload
from app.crud.base import CRUDBase
from app.models.movie import Movie
from app.schemas.movie import MovieCreate, MovieUpdate


class CRUDMovie(CRUDBase[Movie, MovieCreate, MovieUpdate]):
    def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100):
        return (
            db.query(self.model)
            .options(joinedload(Movie.genre), joinedload(Movie.director))
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def get(self, db: Session, *, id: int):
        return (
            db.query(self.model)
            .options(joinedload(Movie.genre), joinedload(Movie.director))
            .filter(self.model.id == id)
            .first()
        )


crud_movie = CRUDMovie(Movie)
