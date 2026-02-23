from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate
from app.crud.user import crud_user
from app.core.config import settings
from app.models.user import User


def test_register_user(client: TestClient, db: Session):
    response = client.post(
        f"{settings.API_V1_STR}/auth/register",
        json={
            "username": "testuser",
            "email": "test@test.com",
            "password": "testpassword",
            "full_name": "Test User",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "User created successfully"
    user = crud_user.get_by_username(db, username="testuser")
    assert user
    assert user.email == "test@test.com"
    assert user.full_name == "Test User"


def test_login_user(client: TestClient, db: Session):
    # Сначала регистрируем пользователя
    user_in = UserCreate(
        username="testlogin", email="login@test.com", password="testpassword"
    )
    crud_user.create(db, obj_in=user_in)

    # Затем пробуем войти
    response = client.post(
        f"{settings.API_V1_STR}/auth/login",
        data={"username": "testlogin", "password": "testpassword"},
    )
    assert response.status_code == 200
    tokens = response.json()
    assert "access_token" in tokens
    assert tokens["token_type"] == "bearer"
