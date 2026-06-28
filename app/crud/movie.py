from sqlalchemy.orm import Session, joinedload

from app.crud.base import CRUDBase, MAX_PAGE_SIZE
from app.models.movie import Movie
from app.schemas.movie import MovieCreate, MovieUpdate


class CRUDMovie(CRUDBase[Movie, MovieCreate, MovieUpdate]):
    def get_multi(self, db: Session, *, skip: int = 0, limit: int = 100, sort_new: bool = False):
        skip = max(0, skip)
        limit = min(max(1, limit), MAX_PAGE_SIZE)
        q = db.query(self.model).options(joinedload(Movie.genre), joinedload(Movie.director))
        if sort_new:
            q = q.order_by(self.model.year.desc().nullslast(), self.model.created_at.desc())
        return q.offset(skip).limit(limit).all()

    def get(self, db: Session, *, id: int):
        return (
            db.query(self.model)
            .options(joinedload(Movie.genre), joinedload(Movie.director))
            .filter(self.model.id == id)
            .first()
        )


crud_movie = CRUDMovie(Movie)
