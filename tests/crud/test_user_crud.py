from sqlalchemy.orm import Session
from app.schemas.user import UserCreate
from app.crud.user import crud_user


def test_create_user(db: Session):
    user_in = UserCreate(
        username="newuser",
        email="new@user.com",
        password="password",
        full_name="New User",
    )
    user = crud_user.create(db, obj_in=user_in)
    assert user.username == user_in.username
    assert user.email == user_in.email
    assert user.full_name == user_in.full_name
    assert hasattr(user, "hashed_password")


def test_get_user(db: Session):
    user_in = UserCreate(username="getuser", email="get@user.com", password="password")
    user = crud_user.create(db, obj_in=user_in)
    stored_user = crud_user.get(db, id=user.id)
    assert stored_user
    assert user.username == stored_user.username
    assert user.email == stored_user.email
    assert user.id == stored_user.id
