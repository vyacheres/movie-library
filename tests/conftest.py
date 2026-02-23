import os
import sys
from pathlib import Path
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.base_class import Base
from app.core.config import settings

# Импортируем приложение
from app.main import app

# Добавляем корневую директорию проекта в sys.path
project_root = str(Path(__file__).parent.parent)
if project_root not in sys.path:
    sys.path.insert(0, project_root)
# from app.db.session import engine, SessionLocal - не используется в тестах


# Создаем отдельную базу данных для тестов
test_engine = create_engine(
    "sqlite:///./test_movie_library.db", connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


@pytest.fixture(scope="session")
def db_engine():
    Base.metadata.create_all(bind=test_engine)
    yield test_engine
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture(scope="function")
def db(db_engine):
    connection = test_engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client(db):
    from fastapi.testclient import TestClient
    from app.db.session import get_db_session

    # Создаем новое приложение для тестов, чтобы не влиять на основное
    test_app = app

    # Сохраняем оригинальную зависимость
    original_get_db = test_app.dependency_overrides.get(get_db_session, None)
    test_app.dependency_overrides[get_db_session] = lambda: db

    with TestClient(test_app) as test_client:
        yield test_client

    # Восстанавливаем оригинальную зависимость
    if original_get_db is not None:
        test_app.dependency_overrides[get_db_session] = original_get_db
    else:
        test_app.dependency_overrides.pop(get_db_session, None)
