# Импорт необходимых модулей FastAPI для создания API
from fastapi import APIRouter, Depends, HTTPException, status

# Импорт SQLAlchemy для работы с базой данных
from sqlalchemy.orm import Session

# Импорт функции для получения сессии базы данных
from app.db.session import get_db as get_db_session

# Импорт модели пользователя
from app.models.user import User

# Импорт схем пользователя (для запроса и ответа)
from app.schemas.user import User, UserCreate, UserUpdate

# Импорт зависимостей для проверки прав доступа
from app.api.dependencies import get_current_active_user, get_current_active_superuser

# Импорт CRUD операций для пользователей
from app.crud.user import crud_user

# Создание роутера для эндпоинтов пользователей
router = APIRouter()


# Эндпоинт для получения данных текущего пользователя
@router.get("/me", response_model=User)
def read_user_me(
    # Зависимость для получения текущего активного пользователя
    current_user: User = Depends(get_current_active_user),
):
    # Возвращаем данные текущего пользователя
    return current_user


# Эндпоинт для получения пользователя по ID
@router.get("/{user_id}", response_model=User)
def read_user(
    # Параметр пути - ID пользователя
    user_id: int,
    # Зависимость для получения текущего суперпользователя (для проверки прав доступа)
    current_user: User = Depends(get_current_active_superuser),
    # Зависимость для получения сессии базы данных
    db: Session = Depends(get_db_session),
):
    # Получаем пользователя из базы данных по ID
    user = crud_user.get(db, id=user_id)
    # Если пользователь не найден, возвращаем ошибку 404
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    # Возвращаем найденного пользователя
    return user


# Эндпоинт для обновления данных текущего пользователя
@router.put("/me", response_model=User)
def update_user_me(
    # Параметр запроса с данными для обновления
    user_in: UserUpdate,
    # Зависимость для получения текущего активного пользователя
    current_user: User = Depends(get_current_active_user),
    # Зависимость для получения сессии базы данных
    db: Session = Depends(get_db_session),
):
    # Обновляем данные текущего пользователя
    user = crud_user.update(db, db_obj=current_user, obj_in=user_in)
    # Возвращаем обновленные данные
    return user


# Эндпоинт для обновления данных пользователя по ID
@router.put("/{user_id}", response_model=User)
def update_user(
    # Параметр пути - ID пользователя
    user_id: int,
    # Параметр запроса с данными для обновления
    user_in: UserUpdate,
    # Зависимость для получения текущего суперпользователя (для проверки прав доступа)
    current_user: User = Depends(get_current_active_superuser),
    # Зависимость для получения сессии базы данных
    db: Session = Depends(get_db_session),
):
    # Получаем пользователя из базы данных по ID
    user = crud_user.get(db, id=user_id)
    # Если пользователь не найден, возвращаем ошибку 404
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    # Обновляем данные пользователя
    user = crud_user.update(db, db_obj=user, obj_in=user_in)
    # Возвращаем обновленные данные
    return user


# Эндпоинт для удаления пользователя по ID
@router.delete("/{user_id}", response_model=dict)
def delete_user(
    # Параметр пути - ID пользователя
    user_id: int,
    # Зависимость для получения текущего суперпользователя (для проверки прав доступа)
    current_user: User = Depends(get_current_active_superuser),
    # Зависимость для получения сессии базы данных
    db: Session = Depends(get_db_session),
):
    # Получаем пользователя из базы данных по ID
    user = crud_user.get(db, id=user_id)
    # Если пользователь не найден, возвращаем ошибку 404
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    # Удаляем пользователя из базы данных
    crud_user.remove(db, id=user_id)
    # Возвращаем сообщение об успешном удалении
    return {"message": "User deleted successfully"}
