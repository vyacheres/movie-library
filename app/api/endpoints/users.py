from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db as get_db_session
from app.models.user import User
from app.schemas.user import User, UserCreate, UserUpdate, PasswordChange
from app.api.dependencies import get_current_active_user, get_current_active_superuser
from app.crud.user import crud_user
from app.core.security import verify_password, get_password_hash

router = APIRouter()


@router.get("/me", response_model=User)
def read_user_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@router.put("/me", response_model=User)
def update_user_me(
    user_in: UserUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db_session),
):
    return crud_user.update(db, db_obj=current_user, obj_in=user_in)


@router.put("/me/password", response_model=dict)
def change_password(
    payload: PasswordChange,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db_session),
):
    if not verify_password(payload.current_password, current_user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect current password")
    crud_user.update(db, db_obj=current_user, obj_in={"hashed_password": get_password_hash(payload.new_password)})
    return {"message": "Password updated successfully"}


@router.get("/{user_id}", response_model=User)
def read_user(
    user_id: int,
    current_user: User = Depends(get_current_active_superuser),
    db: Session = Depends(get_db_session),
):
    user = crud_user.get(db, id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/{user_id}", response_model=User)
def update_user(
    user_id: int,
    user_in: UserUpdate,
    current_user: User = Depends(get_current_active_superuser),
    db: Session = Depends(get_db_session),
):
    user = crud_user.get(db, id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return crud_user.update(db, db_obj=user, obj_in=user_in)


@router.delete("/{user_id}", response_model=dict)
def delete_user(
    user_id: int,
    current_user: User = Depends(get_current_active_superuser),
    db: Session = Depends(get_db_session),
):
    user = crud_user.get(db, id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    crud_user.remove(db, id=user_id)
    return {"message": "User deleted successfully"}
