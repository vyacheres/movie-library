from app.core import security
from app.core.security import get_password_hash
from app.crud.user import crud_user
from app.schemas.user import UserCreate


def test_user_update_rehashes_password(db):
    user = crud_user.create(
        db,
        obj_in=UserCreate(
            username="pwdup",
            email="pwdup@test.com",
            password="oldpassword",
        ),
    )
    old_hash = user.hashed_password

    updated = crud_user.update(
        db,
        db_obj=user,
        obj_in={"hashed_password": get_password_hash("brandnewpass")},
    )
    assert updated.hashed_password != old_hash
    assert security.verify_password("brandnewpass", updated.hashed_password)
    assert not security.verify_password("oldpassword", updated.hashed_password)
