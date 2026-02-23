# app/db/session.py

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Создание движка базы данных
engine = create_engine(
    settings.DATABASE_URL, connect_args={"check_same_thread": False}  # только для SQLite
)

# Фабрика сессий
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовый класс для моделей
Base = declarative_base()

# Зависимость для получения сессии БД в FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()