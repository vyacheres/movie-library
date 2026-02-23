# Импорт BaseSettings из pydantic_settings для создания класса настроек
from pydantic_settings import BaseSettings


# Класс настроек приложения, наследующий BaseSettings
# Позволяет загружать настройки из переменных окружения и .env файла
class Settings(BaseSettings):
    # Название проекта
    PROJECT_NAME: str = "Movie Library"
    # Префикс для версии API
    API_V1_STR: str = "/api/v1"

    # Настройки базы данных
    DATABASE_URL: str = "sqlite:///./movie_library.db"

    # Настройки безопасности
    # Секретный ключ для подписи JWT токенов (должен быть сложным и секретным в продакшене)
    SECRET_KEY: str = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    # Алгоритм шифрования для JWT
    ALGORITHM: str = "HS256"
    # Время жизни токена доступа в минутах
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30


# Создание экземпляра настроек
# При создании экземпляра BaseSettings автоматически загружает значения из:
# 1. Переменных окружения
# 2. Файла .env в корне проекта
# 3. Значений по умолчанию, указанных в классе
settings = Settings()
