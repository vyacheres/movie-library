from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    PROJECT_NAME: str = "Movie Library"
    API_V1_STR: str = "/api/v1"

    DATABASE_URL: str = "sqlite:///./movie_library.db"

    # Обязательный ключ подписи JWT (минимум 32 символа). Задайте в .env для любого окружения.
    SECRET_KEY: str = Field(..., min_length=32)
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Список origin для CORS через запятую (нельзя использовать * вместе с credentials).
    BACKEND_CORS_ORIGINS: str = Field(
        default=(
            "http://127.0.0.1:5500,http://localhost:5500,"
            "http://127.0.0.1:8000,http://localhost:8000,"
            "http://127.0.0.1:3000,http://localhost:3000"
        )
    )

    @property
    def cors_origins_list(self) -> list[str]:
        return [o.strip() for o in self.BACKEND_CORS_ORIGINS.split(",") if o.strip()]

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def strip_cors_string(cls, v: object) -> object:
        if isinstance(v, str):
            return v.strip()
        return v


settings = Settings()
