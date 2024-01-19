import uvicorn

from fastapi import FastAPI
from starlette.responses import JSONResponse

app = FastAPI()


@app.get("/message")
async def read_message():
    message = {"message": "Hello, World!"}
    return JSONResponse(content=message, status_code=200)


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
