"""
Создать веб-страницу для отображения списка пользователей. Приложение
должно использовать шаблонизатор Jinja для динамического формирования HTML
страницы.
Создайте модуль приложения и настройте сервер и маршрутизацию.
Создайте класс User с полями id, name, email и password.
Создайте список users для хранения пользователей.
Создайте HTML шаблон для отображения списка пользователей.
Шаблон должен содержать заголовок страницы, таблицу со списком пользователей и кнопку для
добавления нового пользователя.
Создайте маршрут для отображения списка пользователей (метод GET).
Реализуйте вывод списка пользователей через шаблонизатор Jinja.
"""
import logging
from hashlib import sha256
from typing import Optional, Annotated

import uvicorn
from fastapi import FastAPI, Request, Form
from pydantic import BaseModel
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

menu = {"Главная": "/",
        "Пользователи": "/users/",
        "Добавить пользователя": "/add_user",
        }


class User(BaseModel):
    """Класс User с полями id, name, email и password."""
    id: Optional[int] = None
    name: str
    email: str
    password: str


users = [User(id=1, name="John Doe", email="john@example.com", password="password123")]


class MyError(Exception):
    """Класс для обработки ошибок."""
    pass


class ValidationError(MyError):
    """Класс для обработки ошибок валидации."""
    pass


def validate_email(email):
    """Валидация email."""
    if not "@" in email:
        raise ValidationError("Invalid email address")
    return email.lower()


def hash_password(password):
    """Хэширование пароля."""
    return sha256(password.encode()).hexdigest()


def validate_password(password):
    """Валидация пароля."""
    if len(password) < 6:
        raise ValidationError("Password must be at least 6 characters long")
    return hash_password(password)


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """Метод для отображения главной страницы."""
    context = {"request": request, "menu": menu.items(), "title": "Главная", "text": "Добро пожаловать на сайт!"}
    return templates.TemplateResponse("index.html", context)


@app.get("/users/", response_class=HTMLResponse)
async def get_users(request: Request):
    """Метод для получения списка пользователей."""
    context = {"request": request, "users": users, "menu": menu.items(), "title": "Пользователи"}
    return templates.TemplateResponse("users.html", context)


def json_error_response(error, code):
    if isinstance(error, Exception):
        err_type = error.__class__.__name__
    else:
        err_type = "error"
    logger.error(f"{err_type}: {error}")
    message = {f"{err_type}": f"{error}"}
    return JSONResponse(content=message, status_code=code)


def check_user_id(user_id):
    """Проверка нового id пользователя."""
    user = filter(lambda u: u.id == user_id, users)
    if user:
        if users:
            return max(user.id for user in users) + 1
        else:
            return 1
    return user_id


@app.post("/users/", response_model=User)
async def create_user(user: User):
    """Метод для создания нового пользователя."""
    user_id = len(users) + 1
    user.id = check_user_id(user_id)
    user.name = user.name.title()
    try:
        user.email = validate_email(user.email)
        user.password = validate_password(user.password)
    except ValidationError as e:
        return json_error_response(e, 400)
    users.append(user)
    logger.info(f'Creating user with ID {user.id}')
    return user


@app.get("/users/{user_id}", response_model=User)
async def get_user_by_id(user_id: int):
    """Метод для получения пользователя по ID."""
    for user in users:
        if user.id == user_id:
            return user
    logger.error(f"User with ID {user_id} not found")
    return json_error_response(f"User with ID {user_id} not found", 404)


@app.put("/users/{user_id}", response_model=User)
async def update_item(user_id: int, user: User):
    try:
        user.email = validate_email(user.email)
        user.password = validate_password(user.password)
    except ValidationError as e:
        return JSONResponse(e, 400)
    for i, u in enumerate(users):
        if u.id == user_id:
            users[i] = user
            break
    else:
        logger.error(f"User with ID {user_id} not found")
        message = {"error": "User not found"}
        return JSONResponse(content=message, status_code=404)
    logger.info(f'Updating user with ID {user_id}')
    return user


@app.delete("/users/{user_id}", response_model=User)
async def delete_user(user_id: int):
    for i, u in enumerate(users):
        if u.id == user_id:
            user = u
            del users[i]
            break
    else:
        logger.error(f"User with ID {user_id} not found")
        message = {"error": "User not found"}
        return JSONResponse(content=message, status_code=404)
    logger.info(f'Deleting user with ID {user_id}')
    return user


@app.get("/add_user", response_class=HTMLResponse)
async def add_user(request: Request):
    """Метод для отображения страницы добавления пользователя."""
    context = {"request": request, "menu": menu.items(), "title": "Добавление пользователя"}
    return templates.TemplateResponse("add_user.html", context)


@app.post("/users/add", response_class=HTMLResponse)
async def add_user_post(request: Request, name: Annotated[str, Form()], email: Annotated[str, Form()],
                        password: Annotated[str, Form()]):
    """Метод для добавления пользователя."""
    user = User(name=name, email=email, password=password)
    await create_user(user)
    context = {"request": request, "menu": menu.items(), "title": "Добавление пользователя",
               "text": "Пользователь успешно добавлен!"}
    return templates.TemplateResponse("add_user.html", context)


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
