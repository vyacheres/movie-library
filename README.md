# Movie Library

<a id="readme-russian"></a>

Веб-приложение для каталога фильмов: REST API на **FastAPI**, одностраничный интерфейс на **React** (CDN), JWT-аутентификация, роли пользователей и избранное.

---

## Оглавление

1. [Функционал](#features)
2. [Технологии](#tech-stack)
3. [API (кратко)](#api-summary)
4. [Быстрый старт](#quick-start)
5. [Запуск backend и frontend](#run)
6. [Конфигурация (.env)](#configuration)
7. [Нововведения и безопасность](#changelog-security)
8. [Структура проекта](#project-structure)
9. [Тесты](#tests)
10. [English (duplicate below)](#english)

---

<a id="features"></a>

## Функционал

### Backend (FastAPI)

- Вход и регистрация, JWT, профиль текущего пользователя.
- CRUD: пользователи, фильмы, жанры, режиссёры, избранное.
- Разделение прав: обычный пользователь и суперпользователь (создание/изменение каталога, жанров, режиссёров).
- SQLite по умолчанию; смена строки подключения через `DATABASE_URL` в `.env`.
- Swagger UI и ReDoc.

### Frontend (React SPA)

- Тёмная тема, карточки фильмов, избранное, модальные окна.
- Разделы жанров и режиссёров и добавление фильмов — у суперпользователя.

---

<a id="tech-stack"></a>

## Технологии

| Слой | Стек |
|------|------|
| Backend | FastAPI, SQLAlchemy 2, Pydantic v2, python-jose, Passlib (bcrypt), uvicorn |
| Данные | SQLite (по умолчанию) |
| Frontend | React 18 (UMD), Bootstrap 5, Babel standalone |

---

<a id="api-summary"></a>

## API (кратко)

Префикс версии: **`/api/v1`**.

| Метод | Путь | Назначение |
|--------|------|------------|
| POST | `/auth/register` | Регистрация |
| POST | `/auth/login` | Получение JWT |
| GET | `/users/me` | Текущий пользователь |
| GET/POST | `/movies/` | Список / создание фильма |
| GET/POST/PUT/DELETE | `/genres/`, `/genres/{id}` | Жанры |
| GET/POST/PUT/DELETE | `/directors/`, `/directors/{id}` | Режиссёры |
| GET/POST/DELETE | `/favorites/` | Избранное |

Полное описание полей и схем — в **Swagger**: `/docs`.

---

<a id="quick-start"></a>

## Быстрый старт

```bash
cd movie_library_project
pip install -r requirements.txt
copy .env.example .env   # Windows; на Linux/macOS: cp .env.example .env
```

Откройте `.env` и задайте **`SECRET_KEY`** не короче 32 символов (см. комментарий в `.env.example`).

```bash
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Интерфейс: [http://127.0.0.1:8000/ui/](http://127.0.0.1:8000/ui/) — тот же origin, что и API (удобно для CORS). Документация API: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

---

<a id="run"></a>

## Запуск backend и frontend

**Вариант A — один сервер (рекомендуется)**  
Backend отдаёт UI по адресу `/ui/`:

```bash
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Откройте [http://127.0.0.1:8000/ui/](http://127.0.0.1:8000/ui/).

**Вариант B — отдельный статический сервер для HTML**  
Например, порт 8080:

```bash
cd frontend
python -m http.server 8080
```

Добавьте origin фронта в **`BACKEND_CORS_ORIGINS`** в `.env` (например `http://127.0.0.1:8080`), иначе браузер заблокирует запросы с авторизацией.

Альтернатива backend:

```bash
python run.py
```

---

<a id="configuration"></a>

## Конфигурация (.env)

| Переменная | Назначение |
|------------|------------|
| `SECRET_KEY` | Обязательно, ≥ 32 символов, подпись JWT. |
| `DATABASE_URL` | Опционально, по умолчанию SQLite в корне проекта. |
| `BACKEND_CORS_ORIGINS` | Список origin через запятую для CORS. |

Полный пример см. в **`.env.example`**.

---

<a id="changelog-security"></a>

## Нововведения и безопасность

Ниже перечислены изменения, направленные на устранение уязвимостей, стабильность API и согласованность с фронтендом.

### Аутентификация и токены

| Изменение | Описание |
|-----------|----------|
| **JWT `sub` = id пользователя** | В токен записывается числовой id, а не имя пользователя: стабильная привязка к записи в БД и корректная работа после возможной смены username. |
| **Ответ при невалидном токене** | Неверный или просроченный JWT даёт **401 Unauthorized** и заголовок `WWW-Authenticate: Bearer` (вместо 403), что соответствует ожиданиям клиентов и OpenAPI. |
| **Обязательный `SECRET_KEY`** | Ключ подписи JWT не хранится в коде: задаётся через переменные окружения / `.env`, минимальная длина 32 символа. Шаблон значений — в `.env.example`. |

### Регистрация и роли

| Изменение | Описание |
|-----------|----------|
| **Нельзя стать суперпользователем через API** | Поле `is_superuser` убрано из схемы регистрации; при создании пользователя сервер всегда выставляет `is_superuser=False`. Попытка передать лишнее поле в JSON не даст повышения прав. |

### CORS и окружение

| Изменение | Описание |
|-----------|----------|
| **Явный список origin** | Вместо `allow_origins=["*"]` используется настраиваемая строка **`BACKEND_CORS_ORIGINS`** (origins через запятую). Это совместимо с `allow_credentials=True` и безопаснее для продакшена. |
| **Пример конфигурации** | В репозитории добавлен **`.env.example`** с пояснениями по `SECRET_KEY` и CORS. |

### Данные и CRUD

| Изменение | Описание |
|-----------|----------|
| **Исправлено обновление сущностей (CRUD)** | Базовый `update` больше не вызывает `model_dump()` у SQLAlchemy-моделей; обновление идёт по колонкам маппера — корректно работает, в том числе **PUT `/api/v1/users/me`**. |
| **Пароль при обновлении профиля** | В `CRUDUser.update` поле `password` из схемы преобразуется в **`hashed_password`** с bcrypt. |
| **Пагинация** | В списках ограничен максимальный **`limit`** (защита от чрезмерно тяжёлых запросов). |

### Избранное

| Изменение | Описание |
|-----------|----------|
| **Проверка фильма** | Перед добавлением в избранное проверяется существование фильма; при отсутствии — **404**. |
| **Ошибки БД** | Нарушение уникальности / FK обрабатывается предсказуемо (**400**), без «сырых» 500 и без `print` в коде; используется логирование. |
| **Схема запроса** | В **`FavoriteCreate`** для клиента остаётся только **`movie_id`**; `user_id` всегда берётся из JWT. |

### Нагрузка и обслуживание

| Изменение | Описание |
|-----------|----------|
| **Лимит попыток входа** | Для **`POST /api/v1/auth/login`** включено ограничение числа запросов с одного IP за окно времени (см. `app/core/rate_limit.py`), чтобы усложнить перебор паролей. |
| **Документация OpenAPI** | Схема **Bearer** в Swagger не навешивается на публичные маршруты (логин, регистрация, корень, `/docs` и т.д.). |
| **Дубликат модуля БД** | Удалён неиспользуемый `app/db/database.py`; единая точка — `app/db/session.py`. |
| **Раздача UI с backend** | Статика фронтенда смонтирована по пути **`/ui/`**; в ответе **`GET /`** есть подсказка ссылкой на UI и на `/docs`. |

### Код безопасности

| Изменение | Описание |
|-----------|----------|
| **`app/core/security.py`** | Оставлены хеширование паролей и выпуск JWT; дублирующая логика аутентификации и неиспользуемые схемы убраны (единая реализация в `app/services/auth.py`). |
| **Время жизни JWT** | Для поля **`exp`** используется timezone-aware UTC. |

### Фронтенд (совместимость с API)

| Изменение | Описание |
|-----------|----------|
| **Базовый URL API** | При открытии страницы с `file://` запросы идут на `http://127.0.0.1:8000`; при открытии с того же хоста, что и сервер (в т.ч. `/ui/`), используется **`window.location.origin`**. |
| **Ошибки FastAPI** | Разбор ответа, когда **`detail`** — массив (например, ошибки валидации 422), и когда это строка. |
| **Сессия после 401** | После неавторизованного ответа токен сбрасывается и страница перезагружается без «мигания» состояния пользователя. |
| **Регистрация** | На сервер уходит явный набор полей без лишних ключей из формы. |
| **Кнопка «Add Movie»** | Отображается только у **суперпользователя**; справочники жанров и режиссёров для формы подгружаются также только ему. |

> Старые JWT, где в `sub` было имя пользователя, после обновления **перестают действовать** — выполните вход заново.

---

<a id="project-structure"></a>

## Структура проекта

```
movie_library_project/
├── main.py                      # запуск uvicorn на 0.0.0.0:8000
├── run.py                       # dev-запуск с autoreload на 127.0.0.1
├── requirements.txt             # зависимости Python
├── .env.example                 # образец переменных окружения (без секретов)
├── app/
│   ├── main.py                  # FastAPI: CORS, корень /, раздача /ui/, OpenAPI
│   ├── api/
│   │   ├── api.py               # подключение роутеров под /api/v1
│   │   ├── dependencies.py      # JWT → текущий пользователь / суперпользователь
│   │   └── endpoints/
│   │       ├── auth.py          # регистрация и логин
│   │       ├── users.py         # профиль /me и управление пользователями
│   │       ├── movies.py        # список и CRUD фильмов (права супера)
│   │       ├── genres.py        # жанры
│   │       ├── directors.py     # режиссёры
│   │       └── favorites.py     # избранное
│   ├── core/
│   │   ├── config.py            # настройки из .env (SECRET_KEY, CORS, БД)
│   │   ├── rate_limit.py        # ограничение частоты POST /login по IP
│   │   └── security.py          # bcrypt и выпуск JWT
│   ├── crud/
│   │   ├── base.py              # базовый CRUD по модели
│   │   ├── user.py              # операции с пользователями
│   │   ├── movie.py             # операции с фильмами
│   │   ├── genre.py
│   │   ├── director.py
│   │   └── favorite.py
│   ├── db/
│   │   ├── base.py              # регистрация моделей в metadata
│   │   ├── base_class.py        # DeclarativeBase для ORM
│   │   └── session.py           # engine, SessionLocal, зависимость get_db
│   ├── models/
│   │   ├── __init__.py          # экспорт моделей SQLAlchemy
│   │   ├── user.py
│   │   ├── movie.py
│   │   ├── genre.py
│   │   ├── director.py
│   │   └── favorite.py
│   ├── schemas/
│   │   ├── user.py              # Pydantic-схемы пользователя
│   │   ├── movie.py
│   │   ├── genre.py
│   │   ├── director.py
│   │   ├── favorite.py
│   │   └── token.py             # схемы токена и payload
│   └── services/
│       └── auth.py              # аутентификация и формирование токена
├── frontend/
│   └── index.html               # React SPA (CDN), стили, вызовы API
├── tests/
│   ├── conftest.py              # SQLite для тестов, TestClient, сброс rate limit
│   ├── api/
│   │   ├── test_auth.py         # HTTP-регистрация и логин
│   │   ├── test_users_api.py    # JWT и /users/me
│   │   ├── test_movies_authz.py # права на создание фильма
│   │   ├── test_favorites_api.py# избранное: 404, дубликат, чужая запись
│   │   └── test_login_rate_limit.py  # ответ 429 при перегрузке логина
│   ├── crud/
│   │   ├── test_user_crud.py    # создание и чтение пользователя
│   │   └── test_user_update.py  # обновление пароля через CRUD
│   └── unit/
│       └── test_security.py     # bcrypt и JWT без HTTP
└── README.md
```

---

<a id="tests"></a>

## Тесты

Запуск:

```bash
python -m pytest tests/ -q
```

**Инфраструктура:** `tests/conftest.py` — отдельная SQLite, транзакция на тест с откатом, подмена `get_db` у приложения для `TestClient`; задаётся тестовый `SECRET_KEY`. Перед/после каждого теста сбрасывается in-memory счётчик **rate limit** на `/auth/login`, чтобы сценарии не мешали друг другу. В CI убедитесь, что при импорте приложения доступен `SECRET_KEY` (в репозитории для локального прогона его задаёт `conftest.py`).

**Вспомогательная функция** `api_login(client, username, password)` — получение `access_token` после успешного логина.

**Учётные данные для ручной проверки** (если в вашей БД уже есть такой пользователь): логин `testuser`, пароль `admin123`. Роль суперпользователя задаётся в базе, не через публичную регистрацию.

### Перечень тестов (что покрывают)

| Файл | Тест | Назначение |
|------|------|------------|
| `tests/api/test_auth.py` | `test_register_user` | Успешная регистрация через HTTP, запись пользователя в БД. |
| | `test_login_user` | Логин по OAuth2 form-data, в ответе есть `access_token` и тип `bearer`. |
| | `test_register_ignores_superuser_flag` | В теле регистрации передан `is_superuser: true` — в БД пользователь **не** суперпользователь. |
| `tests/api/test_users_api.py` | `test_users_me_without_token_returns_401` | `GET /users/me` без заголовка `Authorization` → 401. |
| | `test_users_me_with_invalid_token_returns_401` | Невалидный JWT → 401. |
| | `test_users_me_with_valid_token_and_jwt_sub_is_user_id` | Валидный токен: в payload `sub` — числовой id; `GET /users/me` возвращает того же пользователя. |
| `tests/api/test_movies_authz.py` | `test_create_movie_forbidden_for_regular_user` | Обычный пользователь не может `POST /movies/` (ожидается 403). |
| | `test_create_movie_allowed_for_superuser` | Суперпользователь успешно создаёт фильм (`201`). |
| `tests/api/test_favorites_api.py` | `test_add_favorite_movie_not_found` | Добавление в избранное с несуществующим `movie_id` → 404. |
| | `test_add_favorite_duplicate_returns_400` | Повторное добавление того же фильма → 400. |
| | `test_delete_other_users_favorite_returns_403` | Пользователь B не может удалить запись избранного пользователя A → 403. |
| `tests/api/test_login_rate_limit.py` | `test_login_rate_limit_returns_429` | 30 неудачных попыток логина → 401; 31-я с того же клиента → **429** (лимит по IP). |
| `tests/crud/test_user_crud.py` | `test_create_user` | CRUD-создание пользователя, поля и `is_superuser is False`. |
| | `test_get_user` | Чтение пользователя по `id` после создания. |
| `tests/crud/test_user_update.py` | `test_user_update_rehashes_password` | `CRUDUser.update` с новым паролем обновляет `hashed_password`; старый пароль не проходит проверку, новый — да. |
| `tests/unit/test_security.py` | `test_password_hashing` | bcrypt: хеширование и `verify_password`. |
| | `test_jwt_creation` | Создание JWT с `sub`, успешное декодирование. |

Всего **17** тестов.

---

<a id="english"></a>

# English

Short duplicate of this README in English (same project, same steps). [Russian version above](#readme-russian).

## Table of contents

1. [Features](#features-en)
2. [Tech stack](#tech-stack-en)
3. [API (short)](#api-summary-en)
4. [Quick start](#quick-start-en)
5. [Running backend and frontend](#run-en)
6. [Configuration (.env)](#configuration-en)
7. [Security changelog](#changelog-security-en)
8. [Project structure](#project-structure-en)
9. [Tests](#tests-en)
10. [Russian (above)](#readme-russian)

---

<a id="features-en"></a>

## Features

### Backend (FastAPI)

- Login, registration, JWT, current user profile.
- CRUD: users, movies, genres, directors, favorites.
- Roles: regular user vs superuser (catalog, genres, directors).
- SQLite by default; override with `DATABASE_URL` in `.env`.
- Swagger UI and ReDoc.

### Frontend (React SPA)

- Dark theme, movie cards, favorites, modals.
- Genres, directors, and “add movie” — superuser only.

---

<a id="tech-stack-en"></a>

## Tech stack

| Layer | Stack |
|-------|-------|
| Backend | FastAPI, SQLAlchemy 2, Pydantic v2, python-jose, Passlib (bcrypt), uvicorn |
| Data | SQLite (default) |
| Frontend | React 18 (UMD), Bootstrap 5, Babel standalone |

---

<a id="api-summary-en"></a>

## API (short)

Version prefix: **`/api/v1`**.

| Method | Path | Purpose |
|--------|------|---------|
| POST | `/auth/register` | Register |
| POST | `/auth/login` | Obtain JWT |
| GET | `/users/me` | Current user |
| GET/POST | `/movies/` | List / create movie |
| GET/POST/PUT/DELETE | `/genres/`, `/genres/{id}` | Genres |
| GET/POST/PUT/DELETE | `/directors/`, `/directors/{id}` | Directors |
| GET/POST/DELETE | `/favorites/` | Favorites |

Full schemas: **Swagger** at `/docs`.

---

<a id="quick-start-en"></a>

## Quick start

```bash
cd movie_library_project
pip install -r requirements.txt
cp .env.example .env          # Linux / macOS
# copy .env.example .env      # Windows (cmd/PowerShell)
```

Edit `.env` and set **`SECRET_KEY`** to at least 32 characters (see `.env.example`).

```bash
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

UI: [http://127.0.0.1:8000/ui/](http://127.0.0.1:8000/ui/) (same origin as the API, CORS-friendly). API docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

---

<a id="run-en"></a>

## Running backend and frontend

**Option A — single server (recommended)**  
The backend serves the UI at `/ui/`:

```bash
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Open [http://127.0.0.1:8000/ui/](http://127.0.0.1:8000/ui/).

**Option B — separate static server for HTML**  
Example on port 8080:

```bash
cd frontend
python -m http.server 8080
```

Add the frontend origin to **`BACKEND_CORS_ORIGINS`** in `.env` (e.g. `http://127.0.0.1:8080`), otherwise the browser will block credentialed requests.

Another way to run the API:

```bash
python run.py
```

---

<a id="configuration-en"></a>

## Configuration (.env)

| Variable | Purpose |
|----------|---------|
| `SECRET_KEY` | Required, ≥ 32 characters, JWT signing. |
| `DATABASE_URL` | Optional; default SQLite in the project root. |
| `BACKEND_CORS_ORIGINS` | Comma-separated allowed origins for CORS. |

See **`.env.example`** for a full template.

---

<a id="changelog-security-en"></a>

## Security changelog

Changes focused on vulnerabilities, API stability, and frontend alignment.

### Authentication and tokens

| Change | Description |
|--------|-------------|
| **JWT `sub` = user id** | The token stores the numeric user id, not the username: stable binding to the DB row and correct behavior if the username changes later. |
| **Invalid token response** | Invalid or expired JWT returns **401 Unauthorized** with `WWW-Authenticate: Bearer` (instead of 403), matching client and OpenAPI expectations. |
| **Required `SECRET_KEY`** | The JWT signing key is not hardcoded: set via environment / `.env`, minimum length 32 characters. See **`.env.example`**. |

### Registration and roles

| Change | Description |
|--------|-------------|
| **No superuser via public API** | `is_superuser` was removed from the registration schema; the server always sets `is_superuser=False` on create. Extra JSON fields cannot grant admin rights. |

### CORS and environment

| Change | Description |
|--------|-------------|
| **Explicit origins** | Instead of `allow_origins=["*"]`, a configurable **`BACKEND_CORS_ORIGINS`** string (comma-separated origins) is used. Works with `allow_credentials=True` and is safer for production. |
| **Sample config** | **`.env.example`** documents `SECRET_KEY` and CORS. |

### Data and CRUD

| Change | Description |
|--------|-------------|
| **Entity updates fixed** | Base `update` no longer calls `model_dump()` on SQLAlchemy models; updates use mapper columns, including **PUT `/api/v1/users/me`**. |
| **Password on profile update** | In `CRUDUser.update`, schema `password` is hashed into **`hashed_password`** (bcrypt). |
| **Pagination** | List endpoints cap the maximum **`limit`** to avoid overly heavy requests. |

### Favorites

| Change | Description |
|--------|-------------|
| **Movie check** | Before adding a favorite, the movie must exist; otherwise **404**. |
| **DB errors** | Unique/FK violations return predictable **400** responses, no raw 500s or `print`; logging is used. |
| **Request schema** | **`FavoriteCreate`** exposes only **`movie_id`**; `user_id` always comes from the JWT. |

### Load and maintenance

| Change | Description |
|--------|-------------|
| **Login rate limit** | **`POST /api/v1/auth/login`** is rate-limited per IP over a time window (see `app/core/rate_limit.py`) to slow down password guessing. |
| **OpenAPI docs** | Bearer security in Swagger is not applied to public routes (login, register, root, `/docs`, etc.). |
| **Duplicate DB module** | Removed unused `app/db/database.py`; single entry point: `app/db/session.py`. |
| **UI from backend** | Frontend static files are mounted at **`/ui/`**; **`GET /`** includes pointers to the UI and `/docs`. |

### Security code

| Change | Description |
|--------|-------------|
| **`app/core/security.py`** | Password hashing and JWT issuance only; duplicate auth logic removed (single flow in `app/services/auth.py`). |
| **JWT `exp`** | Timezone-aware UTC for the **`exp`** claim. |

### Frontend (API compatibility)

| Change | Description |
|--------|-------------|
| **API base URL** | For `file://` pages, requests go to `http://127.0.0.1:8000`; when served from the same host as the API (including `/ui/`), **`window.location.origin`** is used. |
| **FastAPI errors** | Parses **`detail`** as either an array (e.g. 422 validation) or a string. |
| **Session after 401** | On unauthorized responses, the token is cleared and the page reloads without briefly setting an undefined user. |
| **Registration** | Only the intended fields are sent (no stray keys from the form). |
| **“Add Movie” button** | Shown only for **superusers**; genre and director lists for the create form load only for them. |

> Older JWTs where `sub` was a username **stop working** after this update — sign in again.

---

<a id="project-structure-en"></a>

## Project structure

```
movie_library_project/
├── main.py                      # uvicorn entry (0.0.0.0:8000)
├── run.py                       # dev server with autoreload (127.0.0.1)
├── requirements.txt             # Python dependencies
├── .env.example                 # sample env vars (no real secrets)
├── app/
│   ├── main.py                  # FastAPI app: CORS, /, /ui/ static, OpenAPI
│   ├── api/
│   │   ├── api.py               # mounts routers under /api/v1
│   │   ├── dependencies.py      # JWT → current user / superuser
│   │   └── endpoints/
│   │       ├── auth.py          # register and login
│   │       ├── users.py         # /me profile and user management
│   │       ├── movies.py        # movie list and CRUD (superuser rules)
│   │       ├── genres.py        # genres
│   │       ├── directors.py     # directors
│   │       └── favorites.py     # favorites
│   ├── core/
│   │   ├── config.py            # settings from .env (SECRET_KEY, CORS, DB)
│   │   ├── rate_limit.py        # rate limit for POST /login by IP
│   │   └── security.py          # bcrypt and JWT helpers
│   ├── crud/
│   │   ├── base.py              # generic CRUD base class
│   │   ├── user.py              # user persistence
│   │   ├── movie.py             # movie persistence
│   │   ├── genre.py
│   │   ├── director.py
│   │   └── favorite.py
│   ├── db/
│   │   ├── base.py              # imports models into metadata
│   │   ├── base_class.py        # SQLAlchemy declarative base
│   │   └── session.py           # engine, SessionLocal, get_db dependency
│   ├── models/
│   │   ├── __init__.py          # exports ORM models
│   │   ├── user.py
│   │   ├── movie.py
│   │   ├── genre.py
│   │   ├── director.py
│   │   └── favorite.py
│   ├── schemas/
│   │   ├── user.py              # Pydantic user schemas
│   │   ├── movie.py
│   │   ├── genre.py
│   │   ├── director.py
│   │   ├── favorite.py
│   │   └── token.py             # token / payload schemas
│   └── services/
│       └── auth.py              # login flow and access token
├── frontend/
│   └── index.html               # React SPA (CDN), styles, API calls
├── tests/
│   ├── conftest.py              # test DB, TestClient, rate-limit reset
│   ├── api/
│   │   ├── test_auth.py         # HTTP register and login
│   │   ├── test_users_api.py    # JWT and /users/me
│   │   ├── test_movies_authz.py # movie create authorization
│   │   ├── test_favorites_api.py# favorites: 404, duplicate, foreign delete
│   │   └── test_login_rate_limit.py  # 429 when login flood
│   ├── crud/
│   │   ├── test_user_crud.py    # user create and read
│   │   └── test_user_update.py  # password update via CRUD
│   └── unit/
│       └── test_security.py     # bcrypt and JWT without HTTP
└── README.md
```

---

<a id="tests-en"></a>

## Tests

Run:

```bash
python -m pytest tests/ -q
```

**Infrastructure:** `tests/conftest.py` — isolated SQLite, per-test transaction rollback, `get_db` override for `TestClient`, test `SECRET_KEY`. The in-memory **login rate limit** bucket is cleared before and after every test so scenarios do not interfere. In CI, ensure `SECRET_KEY` is available when importing the app (the repo’s `conftest.py` sets a default for local runs).

**Helper:** `api_login(client, username, password)` returns an `access_token` after a successful login.

**Manual check credentials** (if that user exists in your DB): username `testuser`, password `admin123`. Superuser role is set in the database, not via public registration.

### Test inventory (coverage)

| File | Test | Purpose |
|------|------|---------|
| `tests/api/test_auth.py` | `test_register_user` | HTTP registration succeeds and persists the user. |
| | `test_login_user` | OAuth2 form login returns `access_token` and `bearer` type. |
| | `test_register_ignores_superuser_flag` | Body contains `is_superuser: true` but DB user is **not** a superuser. |
| `tests/api/test_users_api.py` | `test_users_me_without_token_returns_401` | `GET /users/me` with no `Authorization` → 401. |
| | `test_users_me_with_invalid_token_returns_401` | Invalid JWT → 401. |
| | `test_users_me_with_valid_token_and_jwt_sub_is_user_id` | Valid token: payload `sub` is numeric id; `GET /users/me` matches that user. |
| `tests/api/test_movies_authz.py` | `test_create_movie_forbidden_for_regular_user` | Regular user cannot `POST /movies/` (403). |
| | `test_create_movie_allowed_for_superuser` | Superuser creates a movie successfully (`201`). |
| `tests/api/test_favorites_api.py` | `test_add_favorite_movie_not_found` | Favorite with unknown `movie_id` → 404. |
| | `test_add_favorite_duplicate_returns_400` | Adding the same movie twice → 400. |
| | `test_delete_other_users_favorite_returns_403` | User B cannot delete user A’s favorite row → 403. |
| `tests/api/test_login_rate_limit.py` | `test_login_rate_limit_returns_429` | 30 failed logins → 401; 31st from the same client → **429** (per-IP limit). |
| `tests/crud/test_user_crud.py` | `test_create_user` | CRUD user create, fields, `is_superuser is False`. |
| | `test_get_user` | Fetch user by `id` after create. |
| `tests/crud/test_user_update.py` | `test_user_update_rehashes_password` | `CRUDUser.update` with a new password updates `hashed_password`; old password fails verification, new one passes. |
| `tests/unit/test_security.py` | `test_password_hashing` | bcrypt hash and `verify_password`. |
| | `test_jwt_creation` | JWT with `sub` encodes and decodes correctly. |

**17** tests total.
