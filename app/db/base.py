# Импорт Base для создания таблиц
from app.db.base_class import Base

# Импорт всех моделей для регистрации в Base.metadata
from app.models import User, Movie, Genre, Director, Favorite
