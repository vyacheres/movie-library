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
from app.schemas.favorite import Favorite as FavoriteSchema, FavoriteCreate

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED)
def add_to_favorites(
    favorite_in: FavoriteCreate,
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_active_user),
):
    movie = crud_movie.get(db, id=favorite_in.movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    existing = crud_favorite.get_by_user_and_movie(
        db, user_id=current_user.id, movie_id=favorite_in.movie_id
    )
    if existing:
        raise HTTPException(status_code=400, detail="Movie already in favorites")

    favorite = FavoriteModel(user_id=current_user.id, movie_id=favorite_in.movie_id)
    try:
        db.add(favorite)
        db.commit()
        db.refresh(favorite)
    except IntegrityError:
        db.rollback()
        logger.warning(
            "IntegrityError adding favorite user_id=%s movie_id=%s",
            current_user.id,
            favorite_in.movie_id,
        )
        raise HTTPException(
            status_code=400,
            detail="Could not add favorite (duplicate or invalid data)",
        )

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
    favorites = (
        db.query(FavoriteModel)
        .options(
            joinedload(FavoriteModel.movie).joinedload(Movie.genre),
            joinedload(FavoriteModel.movie).joinedload(Movie.director),
        )
        .filter(FavoriteModel.user_id == current_user.id)
        .all()
    )
    return favorites


@router.delete("/{favorite_id}", response_model=dict)
def remove_from_favorites(
    favorite_id: int,
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_active_user),
):
    favorite = crud_favorite.get(db, id=favorite_id)
    if not favorite:
        raise HTTPException(status_code=404, detail="Favorite not found")
    if favorite.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    crud_favorite.remove(db, id=favorite_id)
    return {"message": "Movie removed from favorites"}


@router.delete("/", response_model=dict)
def clear_favorites(
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_active_user),
):
    favorites = (
        db.query(FavoriteModel).filter(FavoriteModel.user_id == current_user.id).all()
    )
    for favorite in favorites:
        db.delete(favorite)
    db.commit()
    return {"message": "All movies removed from favorites"}
