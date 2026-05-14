from app.core.config import settings


def test_login_rate_limit_returns_429(client, db):
    """31-й запрос на /login с того же «хоста» получает 429 (лимит 30/мин)."""
    from app.crud.user import crud_user
    from app.schemas.user import UserCreate

    crud_user.create(
        db,
        obj_in=UserCreate(
            username="ratelim",
            email="ratelim@test.com",
            password="rightpass",
        ),
    )
    url = f"{settings.API_V1_STR}/auth/login"
    last_status = None
    for i in range(31):
        r = client.post(
            url,
            data={"username": "ratelim", "password": "wrongpass"},
        )
        last_status = r.status_code
        if i < 30:
            assert r.status_code == 401, f"i={i} body={r.text}"
        else:
            assert r.status_code == 429, r.text
    assert last_status == 429
