# Импорт необходимых модулей FastAPI для создания API
from fastapi import APIRouter, Depends, HTTPException, status

# Импорт SQLAlchemy для работы с базой данных
from sqlalchemy.orm import Session

# Импорт функции для получения сессии базы данных
from app.db.session import get_db as get_db_session

# Импорт модели режиссера
from app.models.director import Director

# Импорт модели пользователя
from app.models.user import User

# Импорт схем режиссера (для запроса и ответа)
from app.schemas.director import Director, DirectorCreate, DirectorUpdate

# Импорт CRUD операций для режиссеров
from app.crud.director import crud_director

# Импорт зависимостей для аутентификации
from app.api.dependencies import get_current_active_superuser

# Создание роутера для эндпоинтов режиссеров
router = APIRouter()


# Эндпоинт для создания нового режиссера
@router.post("/", response_model=Director, status_code=status.HTTP_201_CREATED)
def create_director(
    # Параметр запроса с данными нового режиссера
    director_in: DirectorCreate,
    # Зависимость для получения сессии базы данных
    db: Session = Depends(get_db_session),
    # Зависимость для проверки прав суперпользователя
    current_user: User = Depends(get_current_active_superuser),
):
    # Создаем нового режиссера в базе данных
    director = crud_director.create(db, obj_in=director_in)
    # Возвращаем созданного режиссера
    return director


# Эндпоинт для получения списка режиссеров
@router.get("/", response_model=list[Director])
def read_directors(
    # Зависимость для получения сессии базы данных
    db: Session = Depends(get_db_session),
    # Параметр для пропуска записей (пагинация)
    skip: int = 0,
    # Параметр для ограничения количества записей (пагинация)
    limit: int = 100,
):
    # Получаем список режиссеров из базы данных
    directors = crud_director.get_multi(db, skip=skip, limit=limit)
    # Возвращаем список режиссеров
    return directors


# Эндпоинт для получения режиссера по ID
@router.get("/{director_id}", response_model=Director)
def read_director(
    # Параметр пути - ID режиссера
    director_id: int,
    # Зависимость для получения сессии базы данных
    db: Session = Depends(get_db_session),
):
    # Получаем режиссера из базы данных по ID
    director = crud_director.get(db, id=director_id)
    # Если режиссер не найден, возвращаем ошибку 404
    if not director:
        raise HTTPException(status_code=404, detail="Director not found")
    # Возвращаем найденного режиссера
    return director


# Эндпоинт для обновления режиссера по ID
@router.put("/{director_id}", response_model=Director)
def update_director(
    # Параметр пути - ID режиссера
    director_id: int,
    # Параметр запроса с данными для обновления
    director_in: DirectorUpdate,
    # Зависимость для получения сессии базы данных
    db: Session = Depends(get_db_session),
    # Зависимость для проверки прав суперпользователя
    current_user: User = Depends(get_current_active_superuser),
):
    # Получаем режиссера из базы данных по ID
    director = crud_director.get(db, id=director_id)
    # Если режиссер не найден, возвращаем ошибку 404
    if not director:
        raise HTTPException(status_code=404, detail="Director not found")
    # Обновляем данные режиссера
    director = crud_director.update(db, db_obj=director, obj_in=director_in)
    # Возвращаем обновленные данные
    return director


# Эндпоинт для удаления режиссера по ID
@router.delete("/{director_id}", response_model=dict)
def delete_director(
    # Параметр пути - ID режиссера
    director_id: int,
    # Зависимость для получения сессии базы данных
    db: Session = Depends(get_db_session),
    # Зависимость для проверки прав суперпользователя
    current_user: User = Depends(get_current_active_superuser),
):
    # Получаем режиссера из базы данных по ID
    director = crud_director.get(db, id=director_id)
    # Если режиссер не найден, возвращаем ошибку 404
    if not director:
        raise HTTPException(status_code=404, detail="Director not found")
    # Удаляем режиссера из базы данных
    crud_director.remove(db, id=director_id)
    # Возвращаем сообщение об успешном удалении
    return {"message": "Director deleted successfully"}
