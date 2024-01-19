import uvicorn

from fastapi import FastAPI

app = FastAPI()


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str = None):
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}


@app.get("/users/{user_id}/orders/{order_id}")
async def read_item(user_id: int, order_id: int):
    # обработка данных
    return {"user_id": user_id, "order_id": order_id}


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
