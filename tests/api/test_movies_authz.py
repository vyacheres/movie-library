from app.core.config import settings
from app.crud.director import crud_director
from app.crud.genre import crud_genre
from app.crud.user import crud_user
from app.schemas.director import DirectorCreate
from app.schemas.genre import GenreCreate
from app.schemas.user import UserCreate
from tests.conftest import api_login


def _seed_genre_director(db):
    g = crud_genre.create(db, obj_in=GenreCreate(name="Test Genre"))
    d = crud_director.create(
        db, obj_in=DirectorCreate(first_name="Ann", last_name="Director")
    )
    return g.id, d.id


def test_create_movie_forbidden_for_regular_user(client, db):
    genre_id, director_id = _seed_genre_director(db)
    client.post(
        f"{settings.API_V1_STR}/auth/register",
        json={
            "username": "regularmov",
            "email": "regularmov@test.com",
            "password": "secret123",
        },
    )
    token = api_login(client, "regularmov", "secret123")
    r = client.post(
        f"{settings.API_V1_STR}/movies/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "title": "Blocked",
            "genre_id": genre_id,
            "director_id": director_id,
        },
    )
    assert r.status_code == 403


def test_create_movie_allowed_for_superuser(client, db):
    genre_id, director_id = _seed_genre_director(db)
    user_in = UserCreate(
        username="supermov",
        email="supermov@test.com",
        password="secret123",
    )
    user = crud_user.create(db, obj_in=user_in)
    user.is_superuser = True
    db.add(user)
    db.commit()
    db.refresh(user)

    token = api_login(client, "supermov", "secret123")
    r = client.post(
        f"{settings.API_V1_STR}/movies/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "title": "Allowed Film",
            "description": "d",
            "genre_id": genre_id,
            "director_id": director_id,
        },
    )
    assert r.status_code == 201, r.text
    body = r.json()
    assert body["title"] == "Allowed Film"
    assert body["id"] >= 1
