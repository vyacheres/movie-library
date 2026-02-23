# Импорт необходимых модулей FastAPI для создания API
from fastapi import APIRouter, Depends, HTTPException, status

# Импорт SQLAlchemy для работы с базой данных
from sqlalchemy.orm import Session

# Импорт функции для получения сессии базы данных
from app.db.session import get_db as get_db_session

# Импорт модели избранного
from app.models.favorite import Favorite as FavoriteModel

# Импорт модели фильма
from app.models.movie import Movie

# Импорт joinedload для загрузки связанных объектов
from sqlalchemy.orm import joinedload

# Импорт модели пользователя
from app.models.user import User

# Импорт схемы добавления в избранное
from app.schemas.favorite import Favorite as FavoriteSchema, FavoriteCreate

# Импорт CRUD операций для избранных фильмов
from app.crud.favorite import crud_favorite

# Импорт зависимостей для аутентификации
from app.api.dependencies import get_current_active_user

# Создание роутера для эндпоинтов избранных фильмов
router = APIRouter()


# Эндпоинт для добавления фильма в избранное
@router.post("/", status_code=status.HTTP_201_CREATED)
def add_to_favorites(
    # Параметр запроса с данными для добавления в избранное
    favorite_in: FavoriteCreate,
    # Зависимость для получения сессии базы данных
    db: Session = Depends(get_db_session),
    # Зависимость для проверки прав активного пользователя
    current_user: User = Depends(get_current_active_user),
):
    try:
        # Проверяем, не добавлен ли уже этот фильм в избранное для данного пользователя
        existing = crud_favorite.get_by_user_and_movie(
            db, user_id=current_user.id, movie_id=favorite_in.movie_id
        )
        # Если фильм уже в избранном, возвращаем ошибку
        if existing:
            raise HTTPException(status_code=400, detail="Movie already in favorites")
        
        # Создаем новый объект Favorite напрямую
        from datetime import datetime
        favorite = FavoriteModel(
            user_id=current_user.id,
            movie_id=favorite_in.movie_id,
            created_at=datetime.utcnow()
        )
        db.add(favorite)
        db.commit()
        db.refresh(favorite)
        
        # Возвращаем данные в виде dict
        return {
            "id": favorite.id,
            "user_id": favorite.user_id,
            "movie_id": favorite.movie_id,
            "created_at": favorite.created_at.isoformat() if favorite.created_at else None
        }
    except Exception as e:
        print(f"Error in add_to_favorites: {e}")
        raise


# Эндпоинт для получения списка избранных фильмов текущего пользователя
@router.get("/", response_model=list[FavoriteSchema])
def read_favorites(
    # Зависимость для получения текущего активного пользователя
    current_user: User = Depends(get_current_active_user),
    # Зависимость для получения сессии базы данных
    db: Session = Depends(get_db_session),
):
    # Получаем все избранные фильмы текущего пользователя с загрузкой связанных данных о фильме
    favorites = (
        db.query(FavoriteModel)
        .options(joinedload(FavoriteModel.movie).joinedload(Movie.genre), joinedload(FavoriteModel.movie).joinedload(Movie.director))
        .filter(FavoriteModel.user_id == current_user.id)
        .all()
    )
    # Возвращаем список избранных фильмов
    return favorites


# Эндпоинт для удаления фильма из избранного по ID
@router.delete("/{favorite_id}", response_model=dict)
def remove_from_favorites(
    # Параметр пути - ID записи в избранном
    favorite_id: int,
    # Зависимость для получения сессии базы данных
    db: Session = Depends(get_db_session),
    # Зависимость для проверки прав активного пользователя
    current_user: User = Depends(get_current_active_user),
):
    # Получаем запись из избранного по ID
    favorite = crud_favorite.get(db, id=favorite_id)
    # Если запись не найдена, возвращаем ошибку 404
    if not favorite:
        raise HTTPException(status_code=404, detail="Favorite not found")
    # Проверяем, что пользователь пытается удалить только свою запись
    if favorite.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    # Удаляем запись из избранного
    crud_favorite.remove(db, id=favorite_id)
    # Возвращаем сообщение об успешном удалении
    return {"message": "Movie removed from favorites"}


# Эндпоинт для очистки всех избранных фильмов текущего пользователя
@router.delete("/", response_model=dict)
def clear_favorites(
    # Зависимость для получения сессии базы данных
    db: Session = Depends(get_db_session),
    # Зависимость для проверки прав активного пользователя
    current_user: User = Depends(get_current_active_user),
):
    # Получаем все избранные фильмы текущего пользователя
    favorites = db.query(FavoriteModel).filter(FavoriteModel.user_id == current_user.id).all()
    # Удаляем каждую запись из избранного
    for favorite in favorites:
        db.delete(favorite)
    # Фиксируем изменения в базе данных
    db.commit()
    # Возвращаем сообщение об успешном удалении всех фильмов
    return {"message": "All movies removed from favorites"}
