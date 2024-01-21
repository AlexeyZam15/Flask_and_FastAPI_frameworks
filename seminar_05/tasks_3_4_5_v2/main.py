"""
Задача 3

Создать API для обновления информации о пользователе в базе данных.
Приложение должно иметь возможность принимать PUT запросы с данными
пользователей и обновлять их в базе данных.
Создайте модуль приложения и настройте сервер и маршрутизацию.
Создайте класс User с полями id, name, email и password.
Создайте список users для хранения пользователей.
Создайте маршрут для обновления информации о пользователе (метод PUT).
Реализуйте валидацию данных запроса и ответа

Задача 4

Создать API для обновления информации о пользователе в базе данных.
Приложение должно иметь возможность принимать PUT запросы с данными
пользователей и обновлять их в базе данных.
Создайте модуль приложения и настройте сервер и маршрутизацию.
Создайте класс User с полями id, name, email и password.
Создайте список users для хранения пользователей.
Создайте маршрут для обновления информации о пользователе (метод PUT).
Реализуйте валидацию данных запроса и ответа

Задание 5

Создать API для удаления информации о пользователе из базы данных.
Приложение должно иметь возможность принимать DELETE запросы и
удалять информацию о пользователе из базы данных.
Создайте модуль приложения и настройте сервер и маршрутизацию.
Создайте класс User с полями id, name, email и password.
Создайте список users для хранения пользователей.
Создайте маршрут для удаления информации о пользователе (метод DELETE).
Реализуйте проверку наличия пользователя в списке и удаление его из
списка.
"""
import logging
from hashlib import sha256
from threading import Thread
from typing import Optional

import uvicorn
from fastapi import FastAPI
from pandas import DataFrame
from pydantic import BaseModel
from starlette.responses import JSONResponse, HTMLResponse

app = FastAPI()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class User(BaseModel):
    """Класс User с полями id, name, email и password."""
    id: Optional[int] = None
    name: str
    email: str
    password: str


class MyError(Exception):
    """Класс для обработки ошибок."""
    pass


class ValidationError(MyError):
    """Класс для обработки ошибок валидации."""
    pass


users = [User(id=1, name="John Doe", email="john@example.com", password="password123")]


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
async def root():
    return "<h1>Hello, World!</h1>"


@app.get("/users/", response_class=HTMLResponse)
async def get_users():
    """Метод для получения списка пользователей."""
    users_table = DataFrame([vars(user) for user in users]).to_html(index=False)
    return users_table


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
async def get_users(user_id: int):
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


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
