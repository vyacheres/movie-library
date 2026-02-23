# Импорт необходимых модулей FastAPI для создания API
from fastapi import APIRouter, Depends, HTTPException, status

# Импорт SQLAlchemy для работы с базой данных
from sqlalchemy.orm import Session

# Импорт функции для получения сессии базы данных
from app.db.session import get_db as get_db_session

# Импорт схемы токена для ответа
from app.schemas.token import Token

# Импорт схемы создания пользователя
from app.schemas.user import UserCreate

# Импорт сервиса аутентификации
from app.services.auth import login_user

# Импорт CRUD операций для пользователей
from app.crud.user import crud_user

# Импорт OAuth2PasswordRequestForm для обработки формы входа
from fastapi.security import OAuth2PasswordRequestForm

# Создание роутера для эндпоинтов аутентификации
router = APIRouter()


# Эндпоинт для входа пользователя в систему
@router.post("/login", response_model=Token)
def login_for_access_token(
    # Зависимость для получения сессии базы данных
    db: Session = Depends(get_db_session),
    # Зависимость для получения данных формы входа
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    # Вызов сервиса аутентификации с данными пользователя
    return login_user(db, form_data.username, form_data.password)


# Эндпоинт для регистрации нового пользователя
@router.post("/register", response_model=dict)
def register_user(
    # Параметр запроса с данными нового пользователя
    user_in: UserCreate,
    # Зависимость для получения сессии базы данных
    db: Session = Depends(get_db_session),
):
    # Проверка существования пользователя с таким именем
    user = crud_user.get_by_username(db, username=user_in.username)
    if user:
        # Если пользователь с таким именем уже существует, возвращаем ошибку
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists",
        )
    # Проверка существования пользователя с такой почтой
    user = crud_user.get_by_email(db, email=user_in.email)
    if user:
        # Если пользователь с такой почтой уже существует, возвращаем ошибку
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists",
        )
    # Создание нового пользователя в базе данных
    user = crud_user.create(db, obj_in=user_in)
    # Возвращаем успешный ответ
    return {"message": "User created successfully"}
