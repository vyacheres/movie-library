from app.core.config import settings
from app.crud.director import crud_director
from app.crud.genre import crud_genre
from app.crud.movie import crud_movie
from app.crud.user import crud_user
from app.schemas.director import DirectorCreate
from app.schemas.genre import GenreCreate
from app.schemas.movie import MovieCreate
from app.schemas.user import UserCreate
from tests.conftest import api_login


def _movie_setup(db):
    g = crud_genre.create(db, obj_in=GenreCreate(name="Fav Genre"))
    d = crud_director.create(
        db, obj_in=DirectorCreate(first_name="Bob", last_name="Dir")
    )
    m = crud_movie.create(
        db,
        obj_in=MovieCreate(
            title="Fav Movie",
            genre_id=g.id,
            director_id=d.id,
        ),
    )
    return m.id


def test_add_favorite_movie_not_found(client, db):
    crud_user.create(
        db,
        obj_in=UserCreate(
            username="favnf", email="favnf@test.com", password="secret123"
        ),
    )
    token = api_login(client, "favnf", "secret123")
    r = client.post(
        f"{settings.API_V1_STR}/favorites/",
        headers={"Authorization": f"Bearer {token}"},
        json={"movie_id": 999_999},
    )
    assert r.status_code == 404


def test_add_favorite_duplicate_returns_400(client, db):
    mid = _movie_setup(db)
    crud_user.create(
        db,
        obj_in=UserCreate(
            username="favdup", email="favdup@test.com", password="secret123"
        ),
    )
    token = api_login(client, "favdup", "secret123")
    h = {"Authorization": f"Bearer {token}"}
    r1 = client.post(
        f"{settings.API_V1_STR}/favorites/", headers=h, json={"movie_id": mid}
    )
    assert r1.status_code == 201
    r2 = client.post(
        f"{settings.API_V1_STR}/favorites/", headers=h, json={"movie_id": mid}
    )
    assert r2.status_code == 400


def test_delete_other_users_favorite_returns_403(client, db):
    mid = _movie_setup(db)
    crud_user.create(
        db,
        obj_in=UserCreate(
            username="ownerf", email="ownerf@test.com", password="secret123"
        ),
    )
    crud_user.create(
        db,
        obj_in=UserCreate(
            username="otherf", email="otherf@test.com", password="secret123"
        ),
    )
    token_a = api_login(client, "ownerf", "secret123")
    r_add = client.post(
        f"{settings.API_V1_STR}/favorites/",
        headers={"Authorization": f"Bearer {token_a}"},
        json={"movie_id": mid},
    )
    assert r_add.status_code == 201
    fav_id = r_add.json()["id"]

    token_b = api_login(client, "otherf", "secret123")
    r_del = client.delete(
        f"{settings.API_V1_STR}/favorites/{fav_id}",
        headers={"Authorization": f"Bearer {token_b}"},
    )
    assert r_del.status_code == 403
