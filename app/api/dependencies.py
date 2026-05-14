from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.core import config
from app.crud.user import crud_user
from app.db.session import get_db as get_db_session
from app.models.user import User
from app.schemas.token import TokenData

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{config.settings.API_V1_STR}/auth/login"
)


def get_current_user(
    db: Session = Depends(get_db_session),
    token: str = Depends(reusable_oauth2),
) -> User:
    credentials_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, config.settings.SECRET_KEY, algorithms=[config.settings.ALGORITHM]
        )
        sub = payload.get("sub")
        if sub is None:
            raise credentials_exc
        user_id = int(sub)
        token_data = TokenData(user_id=user_id)
    except (JWTError, ValidationError, TypeError, ValueError):
        raise credentials_exc

    user = crud_user.get(db, id=token_data.user_id)
    if not user:
        raise credentials_exc
    return user


def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def get_current_active_superuser(
    current_user: User = Depends(get_current_user),
) -> User:
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=403, detail="The user doesn't have enough privileges"
        )
    return current_user
