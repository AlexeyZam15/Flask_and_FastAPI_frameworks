"""
Создать API для управления списком задач. Приложение должно иметь
возможность создавать, обновлять, удалять и получать список задач.
Создайте модуль приложения и настройте сервер и маршрутизацию.
Создайте класс Task с полями id, title, description и status.
Создайте список tasks для хранения задач.
Создайте маршрут для получения списка задач (метод GET).
Создайте маршрут для создания новой задачи (метод POST).
Создайте маршрут для обновления задачи (метод PUT).
Создайте маршрут для удаления задачи (метод DELETE).
Реализуйте валидацию данных запроса и ответа.
"""
from typing import List

import databases
import sqlalchemy
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel, Field

DATABASE_URL = "sqlite:///my_database.db"
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()
tasks = sqlalchemy.Table(
    "tasks",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("title", sqlalchemy.String(32)),
    sqlalchemy.Column("description", sqlalchemy.String(128)),
    sqlalchemy.Column("status", sqlalchemy.Boolean)
)
engine = sqlalchemy.create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
metadata.create_all(engine)

app = FastAPI()


class Task(BaseModel):
    id: int
    title: str = Field(max_length=32)
    description: str = Field(max_length=128)
    status: bool = False


class TaskIn(BaseModel):
    title: str = Field(max_length=32)
    description: str = Field(max_length=128)
    status: bool = False


# @app.post("/fake_tasks/{count}")
# async def create_note(count: int):
#     for i in range(count):
#         query = tasks.insert().values(title=f'task{i}', description=f'description{i}', status=False)
#         await database.execute(query)
#     return {'message': f'{count} fake tasks created'}


@app.get("/tasks/", response_model=List[Task])
async def get_tasks():
    query = tasks.select()
    return await database.fetch_all(query)


@app.post("/tasks/", response_model=Task)
async def post_task(task: TaskIn):
    query = tasks.insert().values(**task.model_dump())
    last_record_id = await database.execute(query)
    return {**task.model_dump(), "id": last_record_id}


@app.put("/tasks/{task_id}", response_model=Task)
async def put_task(task_id: int, new_task: TaskIn):
    query = tasks.update().where(tasks.c.id == task_id).values(**new_task.model_dump())
    await database.execute(query)
    return {**new_task.model_dump(), "id": task_id}


@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int):
    query = tasks.delete().where(tasks.c.id == task_id)
    await database.execute(query)
    return {'message': f'Task deleted'}


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
