from app.core import security
from app.crud.user import crud_user
from app.schemas.user import UserCreate, UserUpdate


def test_user_update_rehashes_password(db):
    user = crud_user.create(
        db,
        obj_in=UserCreate(
            username="pwdup",
            email="pwdup@test.com",
            password="oldpass",
        ),
    )
    old_hash = user.hashed_password

    updated = crud_user.update(
        db,
        db_obj=user,
        obj_in=UserUpdate(
            username=user.username,
            email=user.email,
            password="brandnewpass",
        ),
    )
    assert updated.hashed_password != old_hash
    assert security.verify_password("brandnewpass", updated.hashed_password)
    assert not security.verify_password("oldpass", updated.hashed_password)
