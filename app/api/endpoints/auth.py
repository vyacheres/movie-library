from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError
from sqlalchemy.orm import Session

from app.core.rate_limit import enforce_login_rate_limit
from app.core import security
from app.crud.user import crud_user
from app.db.session import get_db as get_db_session
from app.schemas.token import Token, RefreshRequest
from app.schemas.user import UserCreate
from app.services.auth import login_user

router = APIRouter()


@router.post("/login", response_model=Token)
def login_for_access_token(
    _rate: None = Depends(enforce_login_rate_limit),
    db: Session = Depends(get_db_session),
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    return login_user(db, form_data.username, form_data.password)


@router.post("/refresh", response_model=Token)
def refresh_tokens(payload: RefreshRequest, db: Session = Depends(get_db_session)):
    credentials_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired refresh token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        data = security.decode_token(payload.refresh_token)
    except JWTError:
        raise credentials_exc

    if data.get("type") != "refresh":
        raise credentials_exc

    user_id = data.get("sub")
    if not user_id:
        raise credentials_exc

    user = crud_user.get(db, id=int(user_id))
    if not user or not user.is_active:
        raise credentials_exc

    from datetime import timedelta
    from app.core.config import settings

    access_token = security.create_access_token(
        data={"sub": str(user.id)},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    new_refresh = security.create_refresh_token(data={"sub": str(user.id)})
    return Token(access_token=access_token, refresh_token=new_refresh, token_type="bearer")


def _ensure_user_is_unique(db: Session, user_in: UserCreate) -> None:
    checks = (
        (crud_user.get_by_username(db, username=user_in.username), "username"),
        (crud_user.get_by_email(db, email=user_in.email), "email"),
    )
    for existing_user, field in checks:
        if existing_user:
            raise HTTPException(
                status_code=400,
                detail=f"The user with this {field} already exists",
            )


@router.post("/register", response_model=dict)
def register_user(user_in: UserCreate, db: Session = Depends(get_db_session)):
    _ensure_user_is_unique(db, user_in)
    crud_user.create(db, obj_in=user_in)
    return {"message": "User created successfully"}
