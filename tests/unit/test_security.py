import pytest
from datetime import datetime, timedelta
from jose import jwt
from app.core import security, config
from app.schemas.token import TokenPayload


def test_password_hashing():
    password = "testpassword"
    hashed = security.get_password_hash(password)
    assert security.verify_password(password, hashed)
    assert not security.verify_password("wrongpassword", hashed)


def test_jwt_creation():
    data = {"sub": "testuser"}
    expires = timedelta(minutes=30)
    token = security.create_access_token(data, expires_delta=expires)
    payload = jwt.decode(
        token, config.settings.SECRET_KEY, algorithms=[config.settings.ALGORITHM]
    )
    token_data = TokenPayload(**payload)
    assert token_data.sub == "testuser"
