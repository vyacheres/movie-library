from fastapi import APIRouter

from app.api.endpoints import auth, users, movies, genres, directors, favorites

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(movies.router, prefix="/movies", tags=["movies"])
api_router.include_router(genres.router, prefix="/genres", tags=["genres"])
api_router.include_router(directors.router, prefix="/directors", tags=["directors"])
api_router.include_router(favorites.router, prefix="/favorites", tags=["favorites"])
