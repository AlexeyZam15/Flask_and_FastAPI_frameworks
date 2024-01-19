import logging

import uvicorn
from fastapi import FastAPI

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()


@app.post("/items/")
async def create_item(item: Item):
    logger.info('Отработал POST запрос.')
    return item


if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)
