from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.db.session import get_db as get_db_session
from app.models.movie import Movie
from app.schemas.movie import Movie, MovieCreate, MovieUpdate
from app.crud.movie import crud_movie
from app.crud.genre import crud_genre
from app.crud.director import crud_director
from app.models.user import User
from app.api.dependencies import get_current_active_user, get_current_active_superuser
from app.schemas.user import User, UserCreate, UserUpdate

PAGE_SIZE = 12

router = APIRouter()


def get_movie_or_404(db: Session, movie_id: int) -> Movie:
    movie = crud_movie.get(db, id=movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie


def _validate_genre_and_director(db: Session, genre_id: int | None, director_id: int | None) -> None:
    # Без явной проверки SQLAlchemy даёт необработанный IntegrityError (500)
    if genre_id is not None and crud_genre.get(db, id=genre_id) is None:
        raise HTTPException(status_code=400, detail="Genre not found")
    if director_id is not None and crud_director.get(db, id=director_id) is None:
        raise HTTPException(status_code=400, detail="Director not found")


@router.post("/", response_model=Movie, status_code=status.HTTP_201_CREATED)
def create_movie(
    movie_in: MovieCreate,
    current_user: User = Depends(get_current_active_superuser),
    db: Session = Depends(get_db_session),
):
    _validate_genre_and_director(db, movie_in.genre_id, movie_in.director_id)
    return crud_movie.create(db, obj_in=movie_in)


@router.get("/", response_model=list[Movie])
def read_movies(
    db: Session = Depends(get_db_session),
    page: int = Query(1, ge=1, description="Номер страницы"),
    status: Optional[str] = Query(None, description="Фильтр: 'new' — сортировка по новинкам"),
):
    skip = (page - 1) * PAGE_SIZE
    return crud_movie.get_multi(db, skip=skip, limit=PAGE_SIZE, sort_new=(status == "new"))


@router.get("/{movie_id}", response_model=Movie)
def read_movie(movie_id: int, db: Session = Depends(get_db_session)):
    return get_movie_or_404(db, movie_id)


@router.put("/{movie_id}", response_model=Movie)
def update_movie(
    movie_id: int,
    movie_in: MovieUpdate,
    current_user: User = Depends(get_current_active_superuser),
    db: Session = Depends(get_db_session),
):
    movie = get_movie_or_404(db, movie_id)
    _validate_genre_and_director(db, movie_in.genre_id, movie_in.director_id)
    return crud_movie.update(db, db_obj=movie, obj_in=movie_in)


@router.delete("/{movie_id}", response_model=dict)
def delete_movie(
    movie_id: int,
    current_user: User = Depends(get_current_active_superuser),
    db: Session = Depends(get_db_session),
):
    get_movie_or_404(db, movie_id)
    crud_movie.remove(db, id=movie_id)
    return {"message": "Movie deleted successfully"}
