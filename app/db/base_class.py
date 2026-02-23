# Импорт declarative_base из SQLAlchemy для создания базового класса моделей
from sqlalchemy.ext.declarative import declarative_base

# Создание базового класса для всех моделей
# Все модели в проекте будут наследоваться от этого класса
# Это позволяет SQLAlchemy управлять таблицами и отношениями между ними
Base = declarative_base()
