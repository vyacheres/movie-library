from datetime import timedelta

from fastapi import HTTPException, status

from app.core import security
from app.core.config import settings
from app.models.user import User
from app.schemas.token import Token
from app.crud.user import crud_user


def authenticate_user(db, username: str, password: str) -> User | None:
    user = crud_user.get_by_username(db, username=username)
    if not user:
        return None
    if not security.verify_password(password, user.hashed_password):
        return None
    return user


def login_user(db, username: str, password: str) -> Token:
    user = authenticate_user(db, username, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = security.create_access_token(
        data={"sub": str(user.id)},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    refresh_token = security.create_refresh_token(data={"sub": str(user.id)})
    return Token(access_token=access_token, refresh_token=refresh_token, token_type="bearer")
