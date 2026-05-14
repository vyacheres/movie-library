# Импорт необходимых модулей для работы с временем
from datetime import timedelta

# Импорт HTTPException и статусов из FastAPI
from fastapi import HTTPException, status

# Импорт модуля безопасности и настроек
from app.core import security
from app.core.config import settings

# Импорт модели пользователя
from app.models.user import User

# Импорт схемы токена
from app.schemas.token import Token

# Импорт CRUD операций для пользователей
from app.crud.user import crud_user


# Функция для аутентификации пользователя
def authenticate_user(db, username: str, password: str) -> User | None:
    # Получаем пользователя из базы данных по имени пользователя
    user = crud_user.get_by_username(db, username=username)
    # Если пользователь не найден, возвращаем None
    if not user:
        return None
    # Проверяем, совпадает ли введенный пароль с хешем в базе данных
    if not security.verify_password(password, user.hashed_password):
        return None
    # Если все проверки пройдены, возвращаем пользователя
    return user


# Функция для входа пользователя в систему
def login_user(db, username: str, password: str) -> Token:
    # Сначала аутентифицируем пользователя
    user = authenticate_user(db, username, password)
    # Если аутентификация не удалась, возвращаем ошибку
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # Устанавливаем время жизни токена
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    # sub — стабильный идентификатор пользователя (не username)
    access_token = security.create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    # Возвращаем токен с типом bearer
    return Token(access_token=access_token, token_type="bearer")