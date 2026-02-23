# Movie Library

Веб-приложение для управления библиотекой фильмов с системой аутентификации пользователей, CRUD-операциями для фильмов, жанров, режиссёров и избранного.

## Функционал

### Backend (FastAPI)
- Аутентификация пользователей с использованием JWT токенов
- CRUD операции для пользователей, фильмов, жанров, режиссёров и избранного
- Разграничение прав доступа (обычные пользователи и суперпользователи)
- База данных SQLite
- Интерактивная API документация (Swagger UI / ReDoc)

### Frontend (React SPA)
- Современный UI с тёмной темой в стиле Netflix
- Аутентификация (вход/регистрация)
- Просмотр каталога фильмов с карточками
- Добавление фильмов в избранное
- Просмотр и управление избранным
- Модальные окна для детальной информации о фильмах
- Управление жанрами (для суперпользователей)
- Управление режиссёрами (для суперпользователей)
- Добавление новых фильмов (для суперпользователей)

## Технологии

### Backend
- **FastAPI** — веб-фреймворк
- **SQLAlchemy** — ORM
- **Pydantic** — валидация данных
- **JWT** — аутентификация
- **SQLite** — база данных
- **Passlib + bcrypt** — хеширование паролей

### Frontend
- **React 18** — UI библиотека (через CDN)
- **Bootstrap 5** — CSS фреймворк
- **Babel** — транспиляция JSX

## Установка и запуск

1. Перейдите в папку проекта:
   ```bash
   cd movie_library_project
   ```

2. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

3. Запустите backend сервер:
   ```bash
   python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
   ```

4. Запустите frontend сервер (в отдельном терминале):
   ```bash
   cd frontend
   python -m http.server 8080
   ```

5. Откройте в браузере:
   - **Frontend**: http://127.0.0.1:8080
   - **API документация**: http://127.0.0.1:8000/docs

## Учётные данные

Для тестирования доступен суперпользователь:
- **Логин**: `testuser`
- **Пароль**: `admin123`

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | /api/v1/auth/register | Регистрация пользователя |
| POST | /api/v1/auth/login | Вход, получение токена |
| GET | /api/v1/users/me | Информация о текущем пользователе |
| GET | /api/v1/movies/ | Список всех фильмов |
| POST | /api/v1/movies/ | Создание фильма |
| GET | /api/v1/genres/ | Список жанров |
| POST | /api/v1/genres/ | Создание жанра |
| DELETE | /api/v1/genres/{id} | Удаление жанра |
| GET | /api/v1/directors/ | Список режиссёров |
| POST | /api/v1/directors/ | Создание режиссёра |
| DELETE | /api/v1/directors/{id} | Удаление режиссёра |
| GET | /api/v1/favorites/ | Избранное пользователя |
| POST | /api/v1/favorites/ | Добавить в избранное |
| DELETE | /api/v1/favorites/{id} | Удалить из избранного |

## Структура проекта

```
movie_library_project/
├── app/                          # Backend приложение
│   ├── api/
│   │   ├── __init__.py
│   │   ├── api.py                # Подключение роутеров
│   │   └── endpoints/
│   │       ├── __init__.py
│   │       ├── auth.py           # Аутентификация
│   │       ├── users.py          # Пользователи
│   │       ├── movies.py         # Фильмы
│   │       ├── genres.py         # Жанры
│   │       ├── directors.py      # Режиссёры
│   │       └── favorites.py      # Избранное
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py             # Конфигурация приложения
│   │   └── security.py           # Безопасность (JWT)
│   ├── crud/
│   │   ├── __init__.py
│   │   ├── base.py               # Базовый CRUD класс
│   │   ├── user.py               # CRUD пользователей
│   │   ├── movie.py              # CRUD фильмов
│   │   ├── genre.py              # CRUD жанров
│   │   ├── director.py           # CRUD режиссёров
│   │   └── favorite.py           # CRUD избранного
│   ├── db/
│   │   ├── __init__.py
│   │   ├── base.py               # Базовые классы SQLAlchemy
│   │   ├── base_class.py         # Базовый класс моделей
│   │   └── session.py            # Сессия базы данных
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py               # Модель пользователя
│   │   ├── movie.py              # Модель фильма
│   │   ├── genre.py              # Модель жанра
│   │   ├── director.py           # Модель режиссёра
│   │   └── favorite.py           # Модель избранного
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py               # Pydantic схемы пользователя
│   │   ├── movie.py              # Pydantic схемы фильма
│   │   ├── genre.py              # Pydantic схемы жанра
│   │   ├── director.py           # Pydantic схемы режиссёра
│   │   ├── favorite.py           # Pydantic схемы избранного
│   │   └── token.py              # Pydantic схемы токена
│   └── main.py                   # Точка входа приложения
├── frontend/                     # Frontend приложение
│   └── index.html                # React SPA (единый файл)
├── movie_library.db              # База данных SQLite
├── requirements.txt              # Python зависимости
└── README.md                     # Документация
```
