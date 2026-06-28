import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, joinedload

from app.api.dependencies import get_current_active_user
from app.crud.favorite import crud_favorite
from app.crud.movie import crud_movie
from app.db.session import get_db as get_db_session
from app.models.favorite import Favorite as FavoriteModel
from app.models.movie import Movie
from app.models.user import User
from app.schemas.favorite import Favorite as FavoriteSchema

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/movies/{movie_id}", status_code=status.HTTP_201_CREATED)
def add_to_favorites(
    movie_id: int,
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_active_user),
):
    if not crud_movie.get(db, id=movie_id):
        raise HTTPException(status_code=404, detail="Movie not found")

    if crud_favorite.get_by_user_and_movie(db, user_id=current_user.id, movie_id=movie_id):
        raise HTTPException(status_code=400, detail="Movie already in favorites")

    favorite = FavoriteModel(user_id=current_user.id, movie_id=movie_id)
    try:
        db.add(favorite)
        db.commit()
        db.refresh(favorite)
    except IntegrityError:
        db.rollback()
        logger.warning("IntegrityError adding favorite user_id=%s movie_id=%s", current_user.id, movie_id)
        raise HTTPException(status_code=400, detail="Could not add favorite (duplicate or invalid data)")

    return {
        "id": favorite.id,
        "user_id": favorite.user_id,
        "movie_id": favorite.movie_id,
        "created_at": favorite.created_at.isoformat() if favorite.created_at else None,
    }


@router.get("/", response_model=list[FavoriteSchema])
def read_favorites(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db_session),
):
    return (
        db.query(FavoriteModel)
        .options(
            joinedload(FavoriteModel.movie).joinedload(Movie.genre),
            joinedload(FavoriteModel.movie).joinedload(Movie.director),
        )
        .filter(FavoriteModel.user_id == current_user.id)
        .all()
    )


@router.delete("/movies/{movie_id}", response_model=dict)
def remove_from_favorites(
    movie_id: int,
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_active_user),
):
    favorite = crud_favorite.get_by_user_and_movie(db, user_id=current_user.id, movie_id=movie_id)
    if not favorite:
        raise HTTPException(status_code=404, detail="Favorite not found")
    crud_favorite.remove(db, id=favorite.id)
    return {"message": "Movie removed from favorites"}


@router.delete("/", response_model=dict)
def clear_favorites(
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_active_user),
):
    favorites = db.query(FavoriteModel).filter(FavoriteModel.user_id == current_user.id).all()
    for fav in favorites:
        db.delete(fav)
    db.commit()
    return {"message": "All movies removed from favorites"}
