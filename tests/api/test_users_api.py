from jose import jwt

from app.core.config import settings
from tests.conftest import api_login


def test_users_me_without_token_returns_401(client):
    r = client.get(f"{settings.API_V1_STR}/users/me")
    assert r.status_code == 401


def test_users_me_with_invalid_token_returns_401(client):
    r = client.get(
        f"{settings.API_V1_STR}/users/me",
        headers={"Authorization": "Bearer not-a-real-jwt"},
    )
    assert r.status_code == 401


def test_users_me_with_valid_token_and_jwt_sub_is_user_id(client, db):
    client.post(
        f"{settings.API_V1_STR}/auth/register",
        json={
            "username": "jwtme",
            "email": "jwtme@test.com",
            "password": "secret123",
        },
    )
    token = api_login(client, "jwtme", "secret123")
    payload = jwt.decode(
        token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
    )
    assert payload.get("sub") is not None
    assert str(payload["sub"]).isdigit()

    r = client.get(
        f"{settings.API_V1_STR}/users/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert r.status_code == 200
    data = r.json()
    assert data["username"] == "jwtme"
    assert data["id"] == int(payload["sub"])
