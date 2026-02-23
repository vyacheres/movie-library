# Импорт необходимых модулей FastAPI для создания API
from fastapi import APIRouter, Depends, HTTPException, status

# Импорт SQLAlchemy для работы с базой данных
from sqlalchemy.orm import Session

# Импорт функции для получения сессии базы данных
from app.db.session import get_db as get_db_session

# Импорт модели фильма
from app.models.movie import Movie

# Импорт схем фильма (для запроса и ответа)
from app.schemas.movie import Movie, MovieCreate, MovieUpdate

# Импорт CRUD операций для фильмов
from app.crud.movie import crud_movie

# Импорт модели пользователя
from app.models.user import User

# Импорт зависимостей для проверки прав доступа
from app.api.dependencies import get_current_active_user, get_current_active_superuser

# Импорт схем пользователя (для запроса и ответа)
from app.schemas.user import User, UserCreate, UserUpdate


# Создание роутера для эндпоинтов фильмов
router = APIRouter()


# Эндпоинт для создания нового фильма
@router.post("/", response_model=Movie, status_code=status.HTTP_201_CREATED)
def create_movie(
    # Параметр запроса с данными нового фильма
    movie_in: MovieCreate,
    # Зависимость для получения текущего суперпользователя (для проверки прав доступа)
    current_user: User = Depends(get_current_active_superuser),
    # Зависимость для получения сессии базы данных
    db: Session = Depends(get_db_session),
):
    # Создаем новый фильм в базе данных
    movie = crud_movie.create(db, obj_in=movie_in)
    # Возвращаем созданный фильм
    return movie


# Эндпоинт для получения списка фильмов
@router.get("/", response_model=list[Movie])
def read_movies(
    # Зависимость для получения сессии базы данных
    db: Session = Depends(get_db_session),
    # Параметр для пропуска записей (пагинация)
    skip: int = 0,
    # Параметр для ограничения количества записей (пагинация)
    limit: int = 100,
):
    # Получаем список фильмов из базы данных
    movies = crud_movie.get_multi(db, skip=skip, limit=limit)
    # Возвращаем список фильмов
    return movies


# Эндпоинт для получения фильма по ID
@router.get("/{movie_id}", response_model=Movie)
def read_movie(
    # Параметр пути - ID фильма
    movie_id: int,
    # Зависимость для получения сессии базы данных
    db: Session = Depends(get_db_session),
):
    # Получаем фильм из базы данных по ID
    movie = crud_movie.get(db, id=movie_id)
    # Если фильм не найден, возвращаем ошибку 404
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    # Возвращаем найденный фильм
    return movie


# Эндпоинт для обновления фильма по ID
@router.put("/{movie_id}", response_model=Movie)
def update_movie(
    # Параметр пути - ID фильма
    movie_id: int,
    # Параметр запроса с данными для обновления
    movie_in: MovieUpdate,
    # Зависимость для получения текущего суперпользователя (для проверки прав доступа)
    current_user: User = Depends(get_current_active_superuser),
    # Зависимость для получения сессии базы данных
    db: Session = Depends(get_db_session),
):
    # Получаем фильм из базы данных по ID
    movie = crud_movie.get(db, id=movie_id)
    # Если фильм не найден, возвращаем ошибку 404
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    # Обновляем данные фильма
    movie = crud_movie.update(db, db_obj=movie, obj_in=movie_in)
    # Возвращаем обновленные данные
    return movie


# Эндпоинт для удаления фильма по ID
@router.delete("/{movie_id}", response_model=dict)
def delete_movie(
    # Параметр пути - ID фильма
    movie_id: int,
    # Зависимость для получения текущего суперпользователя (для проверки прав доступа)
    current_user: User = Depends(get_current_active_superuser),
    # Зависимость для получения сессии базы данных
    db: Session = Depends(get_db_session),
):
    # Получаем фильм из базы данных по ID
    movie = crud_movie.get(db, id=movie_id)
    # Если фильм не найден, возвращаем ошибку 404
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    # Удаляем фильм из базы данных
    crud_movie.remove(db, id=movie_id)
    # Возвращаем сообщение об успешном удалении
    return {"message": "Movie deleted successfully"}
