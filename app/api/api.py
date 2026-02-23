# Импорт APIRouter из FastAPI
from fastapi import APIRouter

# Импорт роутеров для различных эндпоинтов
from app.api.endpoints import auth, users, movies, genres, directors, favorites

# Создание основного роутера для API
api_router = APIRouter()

# Подключение роутера аутентификации с префиксом "/auth" и тегом "auth"
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
# Подключение роутера пользователей с префиксом "/users" и тегом "users"
api_router.include_router(users.router, prefix="/users", tags=["users"])
# Подключение роутера фильмов с префиксом "/movies" и тегом "movies"
api_router.include_router(movies.router, prefix="/movies", tags=["movies"])
# Подключение роутера жанров с префиксом "/genres" и тегом "genres"
api_router.include_router(genres.router, prefix="/genres", tags=["genres"])
# Подключение роутера режиссеров с префиксом "/directors" и тегом "directors"
api_router.include_router(directors.router, prefix="/directors", tags=["directors"])
# Подключение роутера избранных фильмов с префиксом "/favorites" и тегом "favorites"
api_router.include_router(favorites.router, prefix="/favorites", tags=["favorites"])
