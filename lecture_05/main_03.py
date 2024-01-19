import logging

import uvicorn
from fastapi import FastAPI

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()


@app.get("/")
async def read_root():
    logger.info('Отработал GET запрос.')
    return {"Hello": "World"}


if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)
