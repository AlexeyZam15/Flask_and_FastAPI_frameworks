import uvicorn

import logging

from fastapi import FastAPI
from typing import Optional

from fastapi.openapi.utils import get_openapi
from pydantic import BaseModel

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()


@app.get("/hello/{name}")
async def read_item(name: str, age: int):
    return {"Hello": name, "Age": age}


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Text",
        version="1.5.0",
        description="This is a very custom OpenAPI schema",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)
