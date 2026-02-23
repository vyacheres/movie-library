# Импорт необходимых модулей FastAPI
from fastapi import Depends, HTTPException, status

# Импорт OAuth2PasswordBearer дл�� аутентификации
from fastapi.security import OAuth2PasswordBearer

# Импорт библиотеки jose для работы с JWT
from jose import JWTError, jwt

# Импорт Pydantic для валидации данных
from pydantic import ValidationError

# Импорт SQLAlchemy для работы с базой данных
from sqlalchemy.orm import Session

# Импорт модуля безопасности и конфигурации
from app.core import security, config

# Импорт функции для получения сессии базы данных
from app.db.session import get_db as get_db_session

# Импорт модели пользователя
from app.models.user import User

# Импорт схемы данных токена
from app.schemas.token import TokenData

# Создание экземпляра OAuth2PasswordBearer с указанием URL для входа
reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{config.settings.API_V1_STR}/auth/login"
)


# Функция для получения текущего пользователя из JWT токена
def get_current_user(
    # Зависимость для получения сессии базы данных
    db: Session = Depends(get_db_session),
    # Зависимость для получения токена из запроса
    token: str = Depends(reusable_oauth2),
) -> User:
    # Пытаемся декодировать и проверить JWT токен
    try:
        # Декодируем токен с использованием секретного ключа и алгоритма из конфигурации
        payload = jwt.decode(
            token, config.settings.SECRET_KEY, algorithms=[config.settings.ALGORITHM]
        )
        # Создаем объект TokenData с именем пользователя из токена
        token_data = TokenData(username=payload.get("sub"))
    # Если токен недействителен или поврежден, возвращаем ошибку
    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    # Импортируем CRUD операции для пользователей
    from app.crud.user import crud_user

    # Получаем пользователя из базы данных по имени пользователя из токена
    user = crud_user.get_by_username(db, username=token_data.username)
    # Если пользователь не найден, возвращаем ошибку
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    # Возвращаем найденного пользователя
    return user


# Функция для получения активного пользователя
def get_current_active_user(
    # Зависимость для получения текущего пользователя
    current_user: User = Depends(get_current_user),
) -> User:
    # Проверяем, что пользователь активен
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    # Возвращаем активного пользователя
    return current_user


# Функция для получения суперпользователя
def get_current_active_superuser(
    # Зависимость для получения текущего пользователя
    current_user: User = Depends(get_current_user),
) -> User:
    # Проверяем, что пользователь является суперпользователем
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    # Возвращаем суперпользователя
    return current_user
