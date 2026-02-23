# Movie Library

A web application for managing a movie library with user authentication, CRUD operations for movies, genres, directors, and favorites.

## Features

### Backend (FastAPI)
- User authentication with JWT tokens
- CRUD operations for users, movies, genres, directors, and favorites
- Role-based access control (regular users and superusers)
- SQLite database
- Interactive API documentation (Swagger UI / ReDoc)

### Frontend (React SPA)
- Modern dark theme UI in Netflix style
- Authentication (login/register)
- Movie catalog viewing with cards
- Adding movies to favorites
- Viewing and managing favorites
- Modal windows for detailed movie information
- Genre management (for superusers)
- Director management (for superusers)
- Adding new movies (for superusers)

## Technologies

### Backend
- **FastAPI** — web framework
- **SQLAlchemy** — ORM
- **Pydantic** — data validation
- **JWT** — authentication
- **SQLite** — database
- **Passlib + bcrypt** — password hashing

### Frontend
- **React 18** — UI library (via CDN)
- **Bootstrap 5** — CSS framework
- **Babel** — JSX transpilation

## Installation and Running

1. Navigate to the project folder:
   ```bash
   cd movie_library_project
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the backend server:
   ```bash
   python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
   ```

4. Run the frontend server (in a separate terminal):
   ```bash
   cd frontend
   python -m http.server 8080
   ```

5. Open in browser:
   - **Frontend**: http://127.0.0.1:8080
   - **API Documentation**: http://127.0.0.1:8000/docs

## Credentials

A superuser is available for testing:
- **Username**: `testuser`
- **Password**: `admin123`

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | /api/v1/auth/register | User registration |
| POST | /api/v1/auth/login | Login, get token |
| GET | /api/v1/users/me | Current user info |
| GET | /api/v1/movies/ | List all movies |
| POST | /api/v1/movies/ | Create movie |
| GET | /api/v1/genres/ | List genres |
| POST | /api/v1/genres/ | Create genre |
| DELETE | /api/v1/genres/{id} | Delete genre |
| GET | /api/v1/directors/ | List directors |
| POST | /api/v1/directors/ | Create director |
| DELETE | /api/v1/directors/{id} | Delete director |
| GET | /api/v1/favorites/ | User's favorites |
| POST | /api/v1/favorites/ | Add movie to favorites |
| DELETE | /api/v1/favorites/{id} | Remove from favorites |

## Project Structure

```
movie_library_project/
├── app/                          # Backend application
│   ├── api/
│   │   ├── __init__.py
│   │   ├── api.py                # Router configuration
│   │   └── endpoints/
│   │       ├── __init__.py
│   │       ├── auth.py           # Authentication
│   │       ├── users.py          # Users
│   │       ├── movies.py         # Movies
│   │       ├── genres.py         # Genres
│   │       ├── directors.py      # Directors
│   │       └── favorites.py      # Favorites
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py             # Application configuration
│   │   └── security.py           # Security (JWT)
│   ├── crud/
│   │   ├── __init__.py
│   │   ├── base.py               # Base CRUD class
│   │   ├── user.py               # User CRUD
│   │   ├── movie.py              # Movie CRUD
│   │   ├── genre.py              # Genre CRUD
│   │   ├── director.py           # Director CRUD
│   │   └── favorite.py           # Favorite CRUD
│   ├── db/
│   │   ├── __init__.py
│   │   ├── base.py               # SQLAlchemy base classes
│   │   ├── base_class.py         # Base model class
│   │   └── session.py            # Database session
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py               # User model
│   │   ├── movie.py              # Movie model
│   │   ├── genre.py              # Genre model
│   │   ├── director.py           # Director model
│   │   └── favorite.py           # Favorite model
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py               # User Pydantic schemas
│   │   ├── movie.py              # Movie Pydantic schemas
│   │   ├── genre.py              # Genre Pydantic schemas
│   │   ├── director.py           # Director Pydantic schemas
│   │   ├── favorite.py           # Favorite Pydantic schemas
│   │   └── token.py              # Token Pydantic schemas
│   └── main.py                   # Application entry point
├── frontend/                     # Frontend application
│   └── index.html                # React SPA (single file)
├── movie_library.db              # SQLite database
├── requirements.txt              # Python dependencies
└── README.md                     # Documentation
```
