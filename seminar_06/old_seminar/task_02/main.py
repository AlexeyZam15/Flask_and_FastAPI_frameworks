"""
Создать API для получения списка фильмов по жанру. Приложение должно
иметь возможность получать список фильмов по заданному жанру.
Создайте модуль приложения и настройте сервер и маршрутизацию.
Создайте класс Movie с полями id, title, description и genre.
Создайте список movies для хранения фильмов.
Создайте маршрут для получения списка фильмов по жанру (метод GET).
Реализуйте валидацию данных запроса и ответа.
"""
import logging
from random import randint

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
genres = sqlalchemy.Table(
    "genres",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String(32), unique=True),
)
movies = sqlalchemy.Table(
    "movies",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("title", sqlalchemy.String(32), unique=True),
    sqlalchemy.Column("description", sqlalchemy.String(128)),
    sqlalchemy.Column("genre_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("genres.id"))
)
engine = sqlalchemy.create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
metadata.create_all(engine)

app = FastAPI()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Genre(BaseModel):
    id: int = Field(default=None, primary_key=True, index=True)
    name: str = Field(max_length=32)


class GenreIn(BaseModel):
    name: str = Field(max_length=32)


class Movie(BaseModel):
    id: int = Field(default=None, primary_key=True, index=True)
    title: str = Field(max_length=32)
    description: str = Field(max_length=128)
    genre_id: int = Field(default=None)


class MoviePost(BaseModel):
    title: str = Field(max_length=32)
    description: str = Field(max_length=128)
    genre_id: int = Field(default=None)


class MoviePut(BaseModel):
    title: str = Field(default=None, max_length=32)
    description: str = Field(default=None, max_length=128)
    genre_id: int = Field(default=None)


def json_error_response(error, code):
    if isinstance(error, Exception):
        err_type = error.__class__.__name__
    else:
        err_type = "error"
    logger.error(f"{err_type}: {error}")
    message = {f"{err_type}": f"{error}"}
    return JSONResponse(content=message, status_code=code)


async def get_genre_note(genre_id):
    """Получение записи жанра из таблицы жанров"""
    try:
        query = genres.select().where(genres.c.id == genre_id)
        genre = await database.fetch_one(query)
    except Exception as e:
        err_text = f"Ошибка при получении списка жанров: {e}"
        return json_error_response(error=err_text, code=500)
    if not genre:
        err_text = f'Жанр {genre_id} не найден'
        return json_error_response(error=err_text, code=404)
    return genre


async def get_movie_note(movie_id):
    """Проверка на наличие фильма в таблице фильмов"""
    try:
        query = movies.select().where(movies.c.id == movie_id)
        movie = await database.fetch_one(query)
    except Exception as e:
        err_text = f"Ошибка при получении списка фильмов: {e}"
        return json_error_response(error=err_text, code=500)
    if not movie:
        err_text = f'Фильм {movie_id} не найден'
        return json_error_response(error=err_text, code=404)
    return movie


@app.post("/genres/", response_model=Genre)
async def create_genre(genre: GenreIn):
    """Создание жанра"""
    logging.info(f"Создание жанра {genre.name}")
    try:
        query = genres.insert().values(name=genre.name)
        # Получение id добавленного жанра
        genre_id = await database.execute(query)
    except Exception as e:
        err_text = f"Ошибка при создании жанра: {e}"
        return json_error_response(error=err_text, code=500)
    return {**genre.model_dump(), "id": genre_id}


@app.post("/movies/", response_model=Movie)
async def create_movie(movie: MoviePost):
    """Создание фильма"""
    logging.info(f"Создание фильма {movie.title}")
    genre_check = await get_genre_note(movie.genre_id)
    if isinstance(genre_check, JSONResponse):
        return genre_check
    try:
        query = movies.insert().values(title=movie.title, description=movie.description, genre_id=movie.genre_id)
        # Получение id добавленного фильма
        movie_id = await database.execute(query)
    except Exception as e:
        err_text = f"Ошибка при создании фильма: {e}"
        return json_error_response(error=err_text, code=500)
    return {**movie.model_dump(), "id": movie_id}


@app.post("/genres/fakes/{count}")
async def create_fake_genres(count: int):
    """Создание фейковых жанров для тестирования"""
    for i in range(1, count + 1):
        query = genres.insert().values(name=f'genre_{i}')
        await database.execute(query)
    return {'message': f'{count} fake genres created'}


@app.post("/movies/fakes/{count}")
async def create_fake_movies(count: int):
    """Создание фейковых фильмов для тестирования"""
    genres_count = await database.fetch_all(genres.select())
    for i in range(1, count + 1):
        query = movies.insert().values(title=f'Movie_{i}', description=f'Description_{i}',
                                       genre_id=randint(1, len(genres_count)))
        await database.execute(query)
    return {'message': f'{count} fake movies created'}


@app.get("/genres/", response_class=HTMLResponse)
async def get_genres():
    """Получение списка жанров"""
    logging.info("Получение списка жанров")
    try:
        query = genres.select()
        genres_list = await database.fetch_all(query)
    except Exception as e:
        err_text = f"Ошибка при получении списка жанров: {e}"
        return json_error_response(error=err_text, code=500)
    table = DataFrame(genres_list)
    return table.to_html(index=False)


@app.get("/genres/{genre_id}", response_model=Genre)
async def get_genre_by_id(genre_id: int):
    """Получение жанра по id"""
    logging.info(f"Получение жанра c id {genre_id}")
    genre = await get_genre_note(genre_id)
    if not genre:
        err_text = f'Жанр {genre_id} не найден'
        return json_error_response(error=err_text, code=404)
    return genre


@app.get("/movies/", response_class=HTMLResponse)
async def get_movies():
    """Получение списка фильмов"""
    logging.info("Получение списка фильмов")
    # Join запрос между таблицами movies и genres
    try:
        query = sqlalchemy.select([movies.c.id, movies.c.title, movies.c.description, genres.c.name]). \
            select_from(movies.join(genres, movies.c.genre_id == genres.c.id))
        movies_list = await database.fetch_all(query)
    except Exception as e:
        err_text = f"Ошибка при получении списка фильмов: {e}"
        return json_error_response(error=err_text, code=500)
    table = DataFrame(movies_list)
    return table.to_html(index=False)


@app.get("/movies/{movie_id}", response_model=Movie)
async def get_movie_by_id(movie_id: int):
    """Получение фильма по id"""
    logging.info(f"Получение фильма c id {movie_id}")
    movie = await get_movie_note(movie_id)
    if not movie:
        err_text = f'Фильм {movie_id} не найден'
        return json_error_response(error=err_text, code=404)
    return movie


@app.get("/movies/genre/{genre_name}", response_class=HTMLResponse)
async def get_movies_by_genre(genre_name: str):
    """Получение списка фильмов по жанру"""
    logging.info(f"Получение списка фильмов по жанру {genre_name}")
    # Join запрос между таблицами movies и genres
    try:
        query = sqlalchemy.select([movies.c.id, movies.c.title, movies.c.description, genres.c.name]). \
            select_from(movies.join(genres, movies.c.genre_id == genres.c.id)).where(genres.c.name == genre_name)
        movies_list = await database.fetch_all(query)
    except Exception as e:
        err_text = f"Ошибка при получении списка фильмов по жанру: {e}"
        return json_error_response(error=err_text, code=500)
    if not movies_list:
        err_text = f'Фильмов по жанру {genre_name} не найдено'
        return json_error_response(error=err_text, code=404)
    table = DataFrame(movies_list)
    return table.to_html(index=False)


@app.delete("/movies/{movie_id}")
async def delete_movie(movie_id: int):
    """Удаление фильма"""
    logging.info(f"Удаление фильма с id {movie_id}")
    movie_check = await get_movie_note(movie_id)
    if isinstance(movie_check, JSONResponse):
        return movie_check
    try:
        query = movies.delete().where(movies.c.id == movie_id)
        await database.execute(query)
    except Exception as e:
        err_text = f"Ошибка при удалении фильма: {e}"
        return json_error_response(error=err_text, code=500)
    return {'message': f'Фильм {movie_id} удалён'}


@app.delete("/genres/{genre_id}")
async def delete_genre(genre_id: int):
    """Удаление жанра"""
    logging.info(f"Удаление жанра с id {genre_id}")
    genre_check = await get_genre_note(genre_id)
    if isinstance(genre_check, JSONResponse):
        return genre_check
    try:
        query = genres.select().where(genres.c.id == genre_id)
        genre_count = await database.fetch_all(query)
    except Exception as e:
        err_text = f"Ошибка при получении списка жанров: {e}"
        return json_error_response(error=err_text, code=500)
    if not genre_count:
        err_text = f'Жанр {genre_id} не найден'
        return json_error_response(error=err_text, code=404)
    try:
        query = genres.delete().where(genres.c.id == genre_id)
        await database.execute(query)
    except Exception as e:
        err_text = f"Ошибка при удалении жанра: {e}"
        return json_error_response(error=err_text, code=500)
    return {'message': f'Жанр c id {genre_id} удалён'}


@app.put("/movies/{movie_id}", response_model=Movie)
async def update_movie(movie_id: int, new_movie: MoviePut):
    """Обновление фильма"""
    logging.info(f"Обновление фильма {movie_id}")
    movie_check = await get_movie_note(movie_id)
    if isinstance(movie_check, JSONResponse):
        return movie_check
    if not new_movie.title and not new_movie.description and not new_movie.genre_id:
        err_text = f'Не заданы данные для обновления фильма'
        return json_error_response(error=err_text, code=400)
    if not new_movie.title:
        new_movie.title = movie_check.title
    if not new_movie.description:
        new_movie.description = movie_check.description
    if not new_movie.genre_id:
        new_movie.genre_id = movie_check.genre_id
    else:
        genre_check = await get_genre_note(new_movie.genre_id)
        if isinstance(genre_check, JSONResponse):
            return genre_check
    try:
        query = movies.update().where(movies.c.id == movie_id).values(title=new_movie.title,
                                                                      description=new_movie.description,
                                                                      genre_id=new_movie.genre_id)
        await database.execute(query)
    except Exception as e:
        err_text = f"Ошибка при обновлении фильма: {e}"
        return json_error_response(error=err_text, code=500)
    logging.info(f"Фильм c id {movie_id} успешно обновлён")
    return {**new_movie.model_dump(), "id": movie_id}


@app.put("/genres/{genre_id}", response_model=Genre)
async def update_genre(genre_id: int, genre: GenreIn):
    """Обновление жанра"""
    logging.info(f"Обновление жанра {genre_id}")
    genre_check = await get_genre_note(genre_id)
    if isinstance(genre_check, JSONResponse):
        return genre_check
    try:
        query = genres.update().where(genres.c.id == genre_id).values(name=genre.name)
        await database.execute(query)
    except Exception as e:
        err_text = f"Ошибка при обновлении жанра: {e}"
        return json_error_response(error=err_text, code=500)
    return {**genre.model_dump(), "id": genre_id}


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
