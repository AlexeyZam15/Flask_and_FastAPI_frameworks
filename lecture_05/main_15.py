import uvicorn

from fastapi import FastAPI, Request
from starlette.responses import HTMLResponse
from starlette.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory="templates")


@app.get("/{name}", response_class=HTMLResponse)
async def read_item(request: Request, name: str):
    print(request)
    return templates.TemplateResponse("item.html", {"request": request, "name": name})


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
