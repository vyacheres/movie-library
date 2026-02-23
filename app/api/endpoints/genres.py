# Импорт необходимых модулей FastAPI для создания API
from fastapi import APIRouter, Depends, HTTPException, status

# Импорт SQLAlchemy для работы с базой данных
from sqlalchemy.orm import Session

# Импорт функции для получения сессии базы данных
from app.db.session import get_db as get_db_session

# Импорт модели жанра
from app.models.genre import Genre

# Импорт модели пользователя
from app.models.user import User

# Импорт схем жанра (для запроса и ответа)
from app.schemas.genre import Genre, GenreCreate, GenreUpdate

# Импорт CRUD операций для жанров
from app.crud.genre import crud_genre

# Импорт зависимостей для аутентификации
from app.api.dependencies import get_current_active_superuser

# Создание роутера для эндпоинтов жанров
router = APIRouter()


# Эндпоинт для создания нового жанра
@router.post("/", response_model=Genre, status_code=status.HTTP_201_CREATED)
def create_genre(
    # Параметр запроса с данными нового жанра
    genre_in: GenreCreate,
    # Зависимость для получения сессии базы данных
    db: Session = Depends(get_db_session),
    # Зависимость для проверки прав суперпользователя
    current_user: User = Depends(get_current_active_superuser),
):
    # Проверяем, существует ли уже жанр с таким названием
    genre = crud_genre.get_by_name(db, name=genre_in.name)
    # Если жанр с таким названием уже существует, возвращаем ошибку
    if genre:
        raise HTTPException(status_code=400, detail="Genre already exists")
    # Создаем новый жанр в базе данных
    genre = crud_genre.create(db, obj_in=genre_in)
    # Возвращаем созданный жанр
    return genre


# Эндпоинт для получения списка жанров
@router.get("/", response_model=list[Genre])
def read_genres(
    # Зависимость для получения сессии базы данных
    db: Session = Depends(get_db_session),
    # Параметр для пропуска записей (пагинация)
    skip: int = 0,
    # Параметр для ограничения количества записей (пагинация)
    limit: int = 100,
):
    # Получаем список жанров из базы данных
    genres = crud_genre.get_multi(db, skip=skip, limit=limit)
    # Возвращаем список жанров
    return genres


# Эндпоинт для получения жанра по ID
@router.get("/{genre_id}", response_model=Genre)
def read_genre(
    # Параметр пути - ID жанра
    genre_id: int,
    # Зависимость для получения сессии базы данных
    db: Session = Depends(get_db_session),
):
    # Получаем жанр из базы данных по ID
    genre = crud_genre.get(db, id=genre_id)
    # Если жанр не найден, возвращаем ошибку 404
    if not genre:
        raise HTTPException(status_code=404, detail="Genre not found")
    # Возвращаем найденный жанр
    return genre


# Эндпоинт для обновления жанра по ID
@router.put("/{genre_id}", response_model=Genre)
def update_genre(
    # Параметр пути - ID жанра
    genre_id: int,
    # Параметр запроса с данными для обновления
    genre_in: GenreUpdate,
    # Зависимость для получения сессии базы данных
    db: Session = Depends(get_db_session),
    # Зависимость для проверки прав суперпользователя
    current_user: User = Depends(get_current_active_superuser),
):
    # Получаем жанр из базы данных по ID
    genre = crud_genre.get(db, id=genre_id)
    # Если жанр не найден, возвращаем ошибку 404
    if not genre:
        raise HTTPException(status_code=404, detail="Genre not found")
    # Обновляем данные жанра
    genre = crud_genre.update(db, db_obj=genre, obj_in=genre_in)
    # Возвращаем обновленные данные
    return genre


# Эндпоинт для удаления жанра по ID
@router.delete("/{genre_id}", response_model=dict)
def delete_genre(
    # Параметр пути - ID жанра
    genre_id: int,
    # Зависимость для получения сессии базы данных
    db: Session = Depends(get_db_session),
    # Зависимость для проверки прав суперпользователя
    current_user: User = Depends(get_current_active_superuser),
):
    # Получаем жанр из базы данных по ID
    genre = crud_genre.get(db, id=genre_id)
    # Если жанр не найден, возвращаем ошибку 404
    if not genre:
        raise HTTPException(status_code=404, detail="Genre not found")
    # Удаляем жанр из базы данных
    crud_genre.remove(db, id=genre_id)
    # Возвращаем сообщение об успешном удалении
    return {"message": "Genre deleted successfully"}
