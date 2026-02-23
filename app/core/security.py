# Импорт необходимых модулей для работы с датами и временем
from datetime import datetime, timedelta

# Импорт Optional для аннотаций типов
from typing import Optional

# Импорт библиотеки jose для работы с JWT
from jose import jwt, JWTError

# Импорт CryptContext из passlib для хеширования паролей
from passlib.context import CryptContext

# Импорт зависимостей FastAPI
from fastapi import Depends, HTTPException

# Импорт OAuth2PasswordBearer для аутентификации
from fastapi.security import OAuth2PasswordBearer

# Импорт BaseModel из Pydantic для создания схем данных
from pydantic import BaseModel

# Импорт настроек приложения
from app.core.config import settings


# Схема данных для информации в токене
class TokenData(BaseModel):
    username: Optional[str] = None


# Схема данных для пользователя
class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None


# Схема данных для пользователя в базе данных (с хешем пароля)
class UserInDB(User):
    hashed_password: str


# Схема данных для токена
class Token(BaseModel):
    access_token: str
    token_type: str


# Контекст для хеширования паролей с использованием bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Создание экземпляра OAuth2PasswordBearer с указанием URL для входа
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")


# Функция для проверки пароля
# Сравнивает введенный пароль с его хешем
# Возвращает True, если пароли совпадают, иначе False
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# Функция для хеширования пароля
# Принимает пароль в открытом виде и возвращает его хеш
# Используется при регистрации и изменении пароля
def get_password_hash(password):
    return pwd_context.hash(password)


# Функция для создания JWT токена доступа
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    # Создаем копию данных, которые нужно закодировать в токен
    to_encode = data.copy()
    # Устанавливаем время истечения токена
    if expires_delta:
        # Если указано время жизни токена, используем его
        expire = datetime.utcnow() + expires_delta
    else:
        # Иначе устанавливаем время жизни по умолчанию - 15 минут
        expire = datetime.utcnow() + timedelta(minutes=15)
    # Добавляем время истечения в данные токена
    to_encode.update({"exp": expire})
    # Кодируем данные в JWT токен с использованием секретного ключа и алгоритма из настроек
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    # Возвращаем закодированный токен
    return encoded_jwt


# Функция для аутентификации пользователя
def authenticate_user(db, username: str, password: str) -> User | None:
    # Локальный импорт для избежания циклической зависимости
    from app.crud.user import crud_user
    # Получаем пользователя из базы данных по имени пользователя
    user = crud_user.get_by_username(db, username=username)
    # Если пользователь не найден, возвращаем None
    if not user:
        return None
    # Проверяем, совпадает ли введенный пароль с хешем в базе данных
    if not verify_password(password, user.hashed_password):
        return None
    # Если все проверки пройдены, возвращаем пользователя
    return user
