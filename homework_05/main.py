"""
Необходимо создать API для управления списком задач. Каждая задача должна содержать заголовок и описание.
Для каждой задачи должна быть возможность указать статус (выполнена/не выполнена).
API должен содержать следующие конечные точки:
— GET /tasks — возвращает список всех задач.
— GET /tasks/{id} — возвращает задачу с указанным идентификатором.
— POST /tasks — добавляет новую задачу.
— PUT /tasks/{id} — обновляет задачу с указанным идентификатором.
— DELETE /tasks/{id} — удаляет задачу с указанным идентификатором.
Для каждой конечной точки необходимо проводить валидацию данных запроса и ответа.
Для этого использовать библиотеку Pydantic.
"""
import logging
from typing import Optional

from pandas import DataFrame
from pydantic import BaseModel
from starlette.responses import HTMLResponse, JSONResponse
from starlette.templating import Jinja2Templates
from uvicorn import run
from fastapi import FastAPI

templates = Jinja2Templates(directory="templates")

app = FastAPI()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Task(BaseModel):
    title: str
    description: str
    status: Optional[bool] = False


tasks = [Task(title="Task 1", description="Description 1")]

validations_text = {"Title": "Invalid title. Title must be less than 50 characters",
                    "Description": "Invalid description. Description must be less than 100 characters"}


@app.get("/tasks", response_class=HTMLResponse)
async def get_tasks():
    """Возвращает список всех задач."""
    logger.info("Getting tasks")
    table = DataFrame([vars(task) for task in tasks]).to_html()
    return table


@app.get("/tasks/{task_id}", response_model=Task)
async def get_task_by_id(task_id: int):
    try:
        logger.info(f"Getting task with id {task_id}")
        task = tasks[task_id]
    except IndexError:
        return json_error_response(f"Task with id {task_id} was not found", 404)
    return task


def validate_title(title):
    if len(title) > 50:
        return False
    return True


def validate_description(desc):
    if len(desc) > 100:
        return False
    return True


def json_error_response(msg, code):
    logger.error(msg)
    return JSONResponse(msg, code)


@app.post("/tasks", response_model=Task)
async def post_task(task: Task):
    """Добавляет новую задачу."""
    logger.info("Adding new task")
    if not validate_title(task.title):
        return json_error_response("Invalid title. Title must be less than 50 characters", 400)
    if not validate_description(task.description):
        return json_error_response("Invalid description. Description must be less than 100 characters", 400)
    tasks.append(task)
    logger.info(f"Task with id {len(tasks) - 1} was added successfully")
    return task


@app.put("/tasks/{task_id}", response_model=Task)
async def put_task(task_id: int, title: str = None, description: str = None, status: bool = None):
    """Обновляет задачу с указанным идентификатором."""
    logger.info(f"Updating task with id {task_id}")
    if task_id >= len(tasks):
        return json_error_response(f"Task with id {task_id} was not found", 404)
    if title is None and description is None and status is None:
        return json_error_response("No fields to update", 400)
    if title:
        if not validate_title(title):
            return json_error_response("Invalid title. Title must be less than 50 characters", 400)
    else:
        title = tasks[task_id].title
    if description:
        if not validate_description(description):
            return json_error_response("Invalid description. Description must be less than 100 characters", 400)
    else:
        description = tasks[task_id].description
    if status is None:
        status = tasks[task_id].status
    task = Task(title=title, description=description, status=status)
    tasks[task_id] = task
    logger.info(f"Task with id {task_id} was updated successfully")
    return task


@app.delete("/tasks/{task_id}", response_model=Task)
async def delete_task(task_id: int):
    """Удаляет задачу с указанным идентификатором."""
    logger.info(f"Deleting task with id {task_id}")
    try:
        task = tasks[task_id]
        tasks.pop(task_id)
    except IndexError:
        return json_error_response(f"Task with id {task_id} was not found", 404)
    logger.info(f"Task with id {task_id} was deleted successfully")
    return task


if __name__ == '__main__':
    run(app, host='127.0.0.1', port=8000)
