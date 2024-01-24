"""
Задание 1

Разработать API для управления списком пользователей с
использованием базы данных SQLite. Для этого создайте
модель User со следующими полями:
○ id: int (идентификатор пользователя, генерируется
автоматически)
○ username: str (имя пользователя)
○ email: str (электронная почта пользователя)
○ password: str (пароль пользователя)
Задание №1 (продолжение)

API должно поддерживать следующие операции:
○ Получение списка всех пользователей: GET /users/
○ Получение информации о конкретном пользователе: GET /users/{user_id}/
○ Создание нового пользователя: POST /users/
○ Обновление информации о пользователе: PUT /users/{user_id}/
○ Удаление пользователя: DELETE /users/{user_id}/
Для валидации данных используйте параметры Field модели User.
Для работы с базой данных используйте SQLAlchemy и модуль databases.
"""
import logging
from hashlib import sha256

import databases
import sqlalchemy
import uvicorn
from fastapi import FastAPI
from pandas import DataFrame
from pydantic import BaseModel, Field
from starlette.responses import HTMLResponse, JSONResponse

DATABASE_URL = "sqlite:///my_database.db"
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()
users = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("username", sqlalchemy.String(32), unique=True),
    sqlalchemy.Column("email", sqlalchemy.String(128), unique=True),
    sqlalchemy.Column("password", sqlalchemy.String(128)),
)

engine = sqlalchemy.create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
metadata.create_all(engine)

app = FastAPI()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class User(BaseModel):
    id: int = Field(default=None, primary_key=True, index=True)
    username: str = Field(max_length=32)
    email: str = Field(max_length=128)
    password: str = Field(min_length=6, max_length=128)


class UserIn(BaseModel):
    username: str = Field(max_length=32)
    email: str = Field(max_length=128)
    password: str = Field(min_length=6, max_length=128)


def json_error_response(error, code):
    if isinstance(error, Exception):
        err_type = error.__class__.__name__
    else:
        err_type = "error"
    logger.error(f"{err_type}: {error}")
    message = {f"{err_type}": f"{error}"}
    return JSONResponse(content=message, status_code=code)


async def get_user_note(user_id: int):
    try:
        query = users.select().where(users.c.id == user_id)
        user = await database.fetch_one(query)
    except Exception as e:
        err_text = f"Ошибка при получении информации о пользователе: {e}"
        return json_error_response(err_text, 400)
    if not user:
        err_text = f"Пользователь с id {user_id} не найден"
        return json_error_response(err_text, 404)
    return user


@app.get("/users/", response_class=HTMLResponse)
async def get_users():
    """Получение списка всех пользователей"""
    query = await database.fetch_all(users.select())
    table = DataFrame(query)
    return table


@app.get("/users/{user_id}", response_model=User)
async def get_user(user_id: int):
    """Получение информации о конкретном пользователе"""
    user = await get_user_note(user_id)
    return user


def hash_password(password):
    """Хеширование пароля"""
    return sha256(password.encode()).hexdigest()


@app.post("/users/", response_model=User)
async def create_user(user: UserIn):
    """Создание нового пользователя"""
    try:
        query = users.insert().values(username=user.username, email=user.email, password=hash_password(user.password))
        # Получение id добавленного пользователя
        user_id = await database.execute(query)
    except Exception as e:
        err_text = f"Ошибка при создании пользователя: {e}"
        return json_error_response(err_text, 400)
    return {**user.model_dump(), "id": user_id}


@app.put("/users/{user_id}", response_model=User)
async def update_user(user_id: int, user: UserIn):
    """Обновление информации о пользователе"""
    # Проверка наличия пользователя с таким id
    check_user = await get_user_note(user_id)
    if isinstance(check_user, JSONResponse):
        return check_user
    try:
        query = users.update().where(users.c.id == user_id).values(username=user.username,
                                                                   email=user.email,
                                                                   password=hash_password(user.password))
        await database.execute(query)
    except Exception as e:
        err_text = f"Ошибка при обновлении информации о пользователе: {e}"
        return json_error_response(err_text, 400)
    return {**user.model_dump(), "id": user_id}


@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    """Удаление пользователя"""
    # Проверка наличия пользователя с таким id
    check_user = await get_user_note(user_id)
    if isinstance(check_user, JSONResponse):
        return check_user
    try:
        query = users.delete().where(users.c.id == user_id)
        await database.execute(query)
    except Exception as e:
        err_text = f"Ошибка при удалении пользователя: {e}"
        return json_error_response(err_text, 400)
    return {"message": f"Пользователь с id {user_id} удален"}


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
