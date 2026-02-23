from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.favorite import Favorite
from app.schemas.favorite import FavoriteCreate


class CRUDFavorite(CRUDBase[Favorite, FavoriteCreate, FavoriteCreate]):
    def get_by_user_and_movie(
        self, db: Session, *, user_id: int, movie_id: int
    ) -> Favorite | None:
        return (
            db.query(Favorite)
            .filter(Favorite.user_id == user_id, Favorite.movie_id == movie_id)
            .first()
        )

    def remove_by_user_and_movie(
        self, db: Session, *, user_id: int, movie_id: int
    ) -> Favorite | None:
        obj = self.get_by_user_and_movie(db, user_id=user_id, movie_id=movie_id)
        if obj:
            db.delete(obj)
            db.commit()
        return obj


crud_favorite = CRUDFavorite(Favorite)
