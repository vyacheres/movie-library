from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.rate_limit import enforce_login_rate_limit
from app.crud.user import crud_user
from app.db.session import get_db as get_db_session
from app.schemas.token import Token
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


@router.post("/register", response_model=dict)
def register_user(
    user_in: UserCreate,
    db: Session = Depends(get_db_session),
):
    user = crud_user.get_by_username(db, username=user_in.username)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists",
        )
    user = crud_user.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists",
        )
    crud_user.create(db, obj_in=user_in)
    return {"message": "User created successfully"}
