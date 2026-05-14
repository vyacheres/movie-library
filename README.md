# Movie Library

<a id="readme-russian"></a>

Веб-приложение для каталога фильмов: REST API на **FastAPI**, одностраничный интерфейс на **React** (CDN), JWT-аутентификация, роли пользователей и избранное.

---

## Оглавление

1. [Быстрый старт](#quick-start)
2. [Нововведения и безопасность](#changelog-security)
3. [Функционал](#features)
4. [Технологии](#tech-stack)
5. [Запуск backend и frontend](#run)
6. [Конфигурация (.env)](#configuration)
7. [Учётные данные для тестов](#credentials)
8. [API (кратко)](#api-summary)
9. [Структура проекта](#project-structure)
10. [Тесты](#tests)
11. [Дополнительно](#more)
12. [English (duplicate below)](#english)

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

### Тесты

| Изменение | Описание |
|-----------|----------|
| **`tests/conftest.py`** | Перед импортом приложения выставляется тестовый **`SECRET_KEY`**; для подмены БД используется тот же **`get_db`**, что и в эндпоинтах. |
| **Новый тест** | Проверка, что флаг суперпользователя в теле регистрации **не** повышает права. |

> Старые JWT, где в `sub` было имя пользователя, после обновления **перестают действовать** — выполните вход заново.

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

<a id="credentials"></a>

## Учётные данные для тестов

Для ручной проверки (если пользователь уже создан в вашей БД):

- Логин: `testuser`  
- Пароль: `admin123`  

Роль суперпользователя задаётся в базе, не через публичную регистрацию.

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

<a id="project-structure"></a>

## Структура проекта

```
movie_library_project/
├── app/
│   ├── api/
│   │   ├── api.py
│   │   ├── dependencies.py      # JWT → текущий пользователь
│   │   └── endpoints/             # auth, users, movies, genres, directors, favorites
│   ├── core/
│   │   ├── config.py            # настройки из .env
│   │   ├── rate_limit.py        # лимит запросов на login
│   │   └── security.py          # bcrypt, JWT
│   ├── crud/
│   ├── db/
│   │   ├── session.py           # engine, SessionLocal, get_db
│   │   └── ...
│   ├── models/
│   ├── schemas/
│   ├── services/auth.py
│   └── main.py                  # FastAPI, CORS, /ui/, OpenAPI
├── frontend/
│   └── index.html               # React SPA
├── tests/
├── .env.example
├── requirements.txt
└── README.md
```

---

<a id="tests"></a>

## Тесты

```bash
python -m pytest tests/ -q
```

В CI локально перед прогоном убедитесь, что для импорта приложения задан `SECRET_KEY` (в тестах значение подставляет `conftest.py`).

---

<a id="more"></a>

## Дополнительно

- Учебные материалы: каталог `tutorial/`.
- Англоязычная версия этого README — [ниже на этой же странице](#english).

---

<a id="english"></a>

# English

Short duplicate of this README in English (same project, same steps).

## Table of contents

1. [Quick start](#quick-start-en)
2. [Security changelog](#changelog-security-en)
3. [Features](#features-en)
4. [Tech stack](#tech-stack-en)
5. [Running backend and frontend](#run-en)
6. [Configuration (.env)](#configuration-en)
7. [Test credentials](#credentials-en)
8. [API (short)](#api-summary-en)
9. [Project structure](#project-structure-en)
10. [Tests](#tests-en)
11. [More](#more-en)

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

### Tests

| Change | Description |
|--------|-------------|
| **`tests/conftest.py`** | Sets a test **`SECRET_KEY`** before importing the app; DB override uses the same **`get_db`** as endpoints. |
| **New test** | Ensures a `is_superuser` flag in the registration body does **not** elevate privileges. |

> Older JWTs where `sub` was a username **stop working** after this update — sign in again.

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

<a id="credentials-en"></a>

## Test credentials

For manual testing (if the user already exists in your database):

- Username: `testuser`  
- Password: `admin123`  

Superuser role is set in the database, not via public registration.

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

<a id="project-structure-en"></a>

## Project structure

```
movie_library_project/
├── app/
│   ├── api/
│   │   ├── api.py
│   │   ├── dependencies.py      # JWT → current user
│   │   └── endpoints/             # auth, users, movies, genres, directors, favorites
│   ├── core/
│   │   ├── config.py            # settings from .env
│   │   ├── rate_limit.py        # login rate limit
│   │   └── security.py          # bcrypt, JWT
│   ├── crud/
│   ├── db/
│   │   ├── session.py           # engine, SessionLocal, get_db
│   │   └── ...
│   ├── models/
│   ├── schemas/
│   ├── services/auth.py
│   └── main.py                  # FastAPI, CORS, /ui/, OpenAPI
├── frontend/
│   └── index.html               # React SPA
├── tests/
├── .env.example
├── requirements.txt
└── README.md
```

---

<a id="tests-en"></a>

## Tests

```bash
python -m pytest tests/ -q
```

`conftest.py` sets `SECRET_KEY` for imports; ensure it is available when running tests in CI.

---

<a id="more-en"></a>

## More

- Tutorials: `tutorial/` directory.
- Russian version of this README: [scroll up](#readme-russian).
