# Импорт FastAPI для создания веб-приложения
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware

# Импорт роутера API
from app.api.api import api_router

# Импорт настроек приложения
from app.core.config import settings

# Создание экземпляра FastAPI с названием проекта и версией из настроек
app = FastAPI(title=settings.PROJECT_NAME, version="1.0.0")

# Настройка CORS для разрешения запросов с фронтенда
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение роутера API с префиксом из настроек (обычно "/api/v1")
app.include_router(api_router, prefix=settings.API_V1_STR)


# Настройка Swagger с OAuth2 авторизацией
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "Bearer Auth": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "JWT token. Example: Bearer your_token_here"
        }
    }
    # Добавляем security ко всем роутерам
    for path in openapi_schema["paths"]:
        for method in openapi_schema["paths"][path]:
            if method in ["get", "post", "put", "delete", "patch"]:
                openapi_schema["paths"][path][method]["security"] = [{"Bearer Auth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


# Эндпоинт для главной страницы
@app.get("/")
def read_root():
    # Возвращает приветственное сообщение
    return {"message": "Welcome to Movie Library API"}
