import uvicorn

from fastapi import FastAPI
from starlette.responses import HTMLResponse

app = FastAPI()


@app.get("/", response_class=HTMLResponse)
async def read_root():
    return "<h1>Hello, World!</h1>"


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
