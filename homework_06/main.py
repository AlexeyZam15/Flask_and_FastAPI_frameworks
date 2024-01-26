"""
Необходимо создать базу данных для интернет-магазина.
База данных должна состоять из трёх таблиц: товары, заказы и пользователи.
— Таблица «Товары» должна содержать информацию о доступных товарах, их описаниях и ценах.
— Таблица «Заказы» должна содержать информацию о заказах, сделанных пользователями.
— Таблица «Пользователи» должна содержать информацию о зарегистрированных пользователях магазина.
• Таблица пользователей должна содержать следующие поля: id (PRIMARY KEY), имя, фамилия,
адрес электронной почты и пароль.
• Таблица заказов должна содержать следующие поля: id (PRIMARY KEY), id пользователя (FOREIGN KEY),
id товара (FOREIGN KEY), дата заказа и статус заказа.
• Таблица товаров должна содержать следующие поля: id (PRIMARY KEY), название, описание и цена.

Создайте модели pydantic для получения новых данных
и возврата существующих в БД для каждой из трёх таблиц (итого шесть моделей).
Реализуйте CRUD операции для каждой из таблиц через создание маршрутов, REST API (итого 15 маршрутов).
* Чтение всех
* Чтение одного
* Запись
* Изменение
* Удаление
"""
import logging
from datetime import datetime
from decimal import Decimal
from hashlib import sha256

import databases
import sqlalchemy
import uvicorn
from fastapi import FastAPI
from pandas import DataFrame
from pydantic import BaseModel, Field
from starlette.requests import Request
from starlette.responses import HTMLResponse, JSONResponse
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

DATABASE_URL = "sqlite:///my_database.db"
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()
users = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String),
    sqlalchemy.Column("surname", sqlalchemy.String),
    sqlalchemy.Column("email", sqlalchemy.String, unique=True),
    sqlalchemy.Column("password", sqlalchemy.String),
)
orders = sqlalchemy.Table(
    "orders",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("user_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id")),
    sqlalchemy.Column("product_id", sqlalchemy.Integer, sqlalchemy.ForeignKey("products.id")),
    sqlalchemy.Column("date", sqlalchemy.String),
    sqlalchemy.Column("status", sqlalchemy.String),
)
products = sqlalchemy.Table(
    "products",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String, unique=True),
    sqlalchemy.Column("description", sqlalchemy.String),
    sqlalchemy.Column("price", sqlalchemy.String),
)
engine = sqlalchemy.create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
metadata.create_all(engine)

# inspector = sqlalchemy.inspect(engine)
# tables = {i: eval(i) for i in inspector.get_table_names()}

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

menu = {"Главная": "/",
        "Пользователи": "/users",
        "Товары": "/products",
        "Заказы": "/orders",
        }.items()


class User(BaseModel):
    id: int = Field(gt=0)
    name: str = Field(max_length=32)
    surname: str = Field(max_length=32)
    email: str = Field(max_length=254)
    password: str = Field(min_length=6, max_length=128)


class UserIn(BaseModel):
    name: str = Field(default=None, max_length=32)
    surname: str = Field(default=None, max_length=32)
    email: str = Field(default=None, max_length=254)
    password: str = Field(default=None, min_length=6, max_length=128)


class Order(BaseModel):
    id: int = Field(gt=0)
    user_id: int = Field(gt=0)
    product_id: int = Field(gt=0)
    date: str = Field(default=datetime.now().strftime("%d.%m.%Y %H:%M:%S"))
    status: str = Field(default="new", max_length=16)


class OrderIn(BaseModel):
    user_id: int = Field(default=None, gt=0)
    product_id: int = Field(default=None, gt=0)
    status: str = Field(default=None, max_length=16)


class Product(BaseModel):
    id: int = Field(gt=0)
    name: str = Field(max_length=32)
    description: str = Field(max_length=128)
    price: Decimal = Field(gt=0)


class ProductIn(BaseModel):
    name: str = Field(default=None, max_length=32)
    description: str = Field(default=None, max_length=128)
    price: Decimal = Field(default=None, gt=0)


def json_error_response(error, code):
    """Функция для возврата ошибки в json формате"""
    if isinstance(error, Exception):
        err_type = error.__class__.__name__
    else:
        err_type = "error"
    logger.error(f"{err_type}: {error}")
    message = {f"{err_type}": f"{error}"}
    return JSONResponse(content=message, status_code=code)


async def get_note(note_id: int, table: str):
    """Получение записи из таблицы базы данных"""""
    try:
        table = eval(table)
        query = table.select().where(table.c.id == note_id)
        data = await database.fetch_one(query)
    except Exception as e:
        err_text = f"Ошибка при чтении информации из таблицы {table}: {e}"
        return json_error_response(err_text, 400)
    if not data:
        err_text = f"Запись из таблицы {table} с id {note_id} не найдена"
        return json_error_response(err_text, 404)
    return data


def hash_password(password):
    """Хеширование пароля"""
    return sha256(password.encode()).hexdigest()


@app.post("/users/", response_model=User)
async def create_user(user: UserIn):
    """Создание нового пользователя"""
    logger.info(f"Создание нового пользователя: {user}")
    try:
        user.password = hash_password(user.password)
        query = users.insert().values(
            name=user.name,
            surname=user.surname,
            email=user.email,
            password=user.password,
        )
        last_record_id = await database.execute(query)
    except Exception as e:
        err_text = f"Ошибка при записи нового пользователя в БД: {e}"
        return json_error_response(err_text, 400)
    logger.info(f"Новый пользователь создан: {user}")
    return {**user.model_dump(), "id": last_record_id}


@app.post("/orders/", response_model=Order)
async def create_order(order: OrderIn):
    """Создание нового заказа"""
    logger.info(f"Создание нового заказа: {order}")
    user_check = await get_note(order.user_id, "users")
    if isinstance(user_check, JSONResponse):
        return user_check
    product_check = await get_note(order.product_id, "products")
    if isinstance(product_check, JSONResponse):
        return product_check
    try:
        date = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        query = orders.insert().values(
            user_id=order.user_id,
            product_id=order.product_id,
            date=date,
            status=order.status,
        )
        last_record_id = await database.execute(query)
    except Exception as e:
        err_text = f"Ошибка при записи нового заказа в БД: {e}"
        return json_error_response(err_text, 400)
    logger.info(f"Новый заказ создан: {order}")
    return {**order.model_dump(), "id": last_record_id}


@app.post("/products/", response_model=Product)
async def create_product(product: ProductIn):
    """Создание нового товара"""
    logger.info(f"Создание нового товара: {product}")
    try:
        query = products.insert().values(
            name=product.name,
            description=product.description,
            price=product.price
        )
        last_record_id = await database.execute(query)
    except Exception as e:
        err_text = f"Ошибка при записи нового заказа в БД: {e}"
        return json_error_response(err_text, 400)
    logger.info(f"Новый товар создан: {product}")
    return {**product.model_dump(), "id": last_record_id}


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Главная страница"""
    logger.info("Открытие главной страницы")
    context = {"request": request, "menu": menu, "title": "Главная", "text": "Добро пожаловать на сайт!"}
    return templates.TemplateResponse("index.html", context)


@app.get("/users/", response_class=HTMLResponse)
async def get_users(request: Request):
    """Чтение всех пользователей"""
    logger.info("Чтение всех пользователей")
    try:
        query = users.select()
        users_data = await database.fetch_all(query)
    except Exception as e:
        err_text = f"Ошибка при получении списка пользователей: {e}"
        return json_error_response(err_text, 400)
    table = DataFrame(users_data).to_html(index=False)
    logger.info("Список пользователей получен")
    context = {"request": request, "menu": menu, "title": "Пользователи", "text": "Список пользователей",
               "table": table}
    return templates.TemplateResponse("table.html", context)


@app.get("/orders/", response_class=HTMLResponse)
async def get_orders(request: Request):
    """Чтение всех заказов"""
    logger.info("Чтение всех заказов")
    # Join запрос между таблицами orders, users и products
    try:
        query = (sqlalchemy.select(
            [orders.c.id, users.c.id.label("user_id"), users.c.name, users.c.surname,
             products.c.id.label("product_id"), products.c.name.label("product_name"), orders.c.date, orders.c.status])
                 .select_from(orders.join(users).join(products)))
        orders_data = await database.fetch_all(query)
    except Exception as e:
        err_text = f"Ошибка при получении списка заказов: {e}"
        return json_error_response(err_text, 400)
    logger.info("Список заказов получен")
    table = DataFrame(orders_data).to_html(index=False)
    context = {"request": request, "menu": menu, "title": "Заказы", "text": "Список заказов", "table": table}
    return templates.TemplateResponse("table.html", context)


@app.get("/products/", response_class=HTMLResponse)
async def get_products(request: Request):
    """Чтение всех товаров"""
    logger.info("Чтение всех товаров")
    try:
        query = products.select()
        products_data = await database.fetch_all(query)
    except Exception as e:
        err_text = f"Ошибка при получении списка товаров: {e}"
        return json_error_response(err_text, 400)
    logger.info("Список товаров получен")
    table = DataFrame(products_data).to_html(index=False)
    context = {"request": request, "menu": menu, "title": "Товары", "text": "Список товаров", "table": table}
    return templates.TemplateResponse("table.html", context)


@app.get("/users/{user_id}", response_model=User)
async def get_user(user_id: int):
    """Чтение информации о пользователе по id"""
    logger.info(f"Чтение информации о пользователе с id {user_id}")
    user = await get_note(user_id, "users")
    logger.info(f"Информация о пользователе с id {user_id} получена")
    return user


@app.get("/orders/{order_id}", response_model=Order)
async def get_order(order_id: int):
    """Чтение информации о заказе по id"""
    logger.info(f"Чтение информации о заказе с id {order_id}")
    order = await get_note(order_id, "orders")
    logger.info(f"Информация о заказе с id {order_id} получена")
    return order


@app.get("/products/{product_id}", response_model=Product)
async def get_product(product_id: int):
    """Чтение информации о товаре по id"""
    logger.info(f"Чтение информации о товаре с id {product_id}")
    product = await get_note(product_id, "products")
    logger.info(f"Информация о товаре с id {product_id} получена")
    return product


@app.put("/users/{user_id}", response_model=User)
async def update_user(user_id: int, user: UserIn):
    """Обновление информации о пользователе"""
    logger.info(f"Обновление информации о пользователе с id {user_id}")
    user_check = await get_note(user_id, "users")
    if isinstance(user_check, JSONResponse):
        return user_check
    try:
        for field in user.model_dump():
            if getattr(user, field) is None:
                setattr(user, field, getattr(user_check, field))
        user.password = hash_password(user.password)

        query = users.update().where(users.c.id == user_id).values(
            name=user.name,
            surname=user.surname,
            email=user.email,
            password=user.password,
        )
        await database.execute(query)
    except Exception as e:
        err_text = f"Ошибка при обновлении информации о пользователе: {e}"
        return json_error_response(err_text, 400)
    logger.info(f"Информация о пользователе с id {user_id} обновлена")
    return {**user.model_dump(), "id": user_id}


@app.put("/orders/{order_id}", response_model=Order)
async def update_order(order_id: int, order: OrderIn):
    """Обновление информации о заказе"""
    logger.info(f"Обновление информации о заказе с id {order_id}")
    order_check = await get_note(order_id, "orders")
    if isinstance(order_check, JSONResponse):
        return order_check
    if order.user_id:
        user_check = await get_note(order.user_id, "users")
        if isinstance(user_check, JSONResponse):
            return user_check
    if order.product_id:
        product_check = await get_note(order.product_id, "products")
        if isinstance(product_check, JSONResponse):
            return product_check
    try:
        for field in order.model_dump():
            if getattr(order, field) is None:
                setattr(order, field, getattr(order_check, field))

        query = orders.update().where(orders.c.id == order_id).values(
            user_id=order.user_id,
            product_id=order.product_id,
            status=order.status
        )
        await database.execute(query)
    except Exception as e:
        err_text = f"Ошибка при обновлении информации о заказе: {e}"
        return json_error_response(err_text, 400)
    logger.info(f"Информация о заказе с id {order_id} обновлена")
    return {**order.model_dump(), "id": order_id}


@app.put("/products/{product_id}", response_model=Product)
async def update_product(product_id: int, product: ProductIn):
    """Обновление информации о товаре"""
    logger.info(f"Обновление информации о товаре с id {product_id}")
    product_check = await get_note(product_id, "products")
    if isinstance(product_check, JSONResponse):
        return product_check
    for field in product.model_dump():
        if getattr(product, field) is None:
            setattr(product, field, getattr(product_check, field))
    try:
        query = products.update().where(products.c.id == product_id).values(
            name=product.name,
            description=product.description,
            price=product.price
        )
        await database.execute(query)
    except Exception as e:
        err_text = f"Ошибка при обновлении информации о товаре: {e}"
        return json_error_response(err_text, 400)
    logger.info(f"Информация о товаре с id {product_id} обновлена")
    return {**product.model_dump(), "id": product_id}


@app.delete("/users/{user_id}", response_model=User)
async def delete_user(user_id: int):
    """Удаление пользователя"""
    logger.info(f"Удаление пользователя с id {user_id}")
    user = await get_note(user_id, "users")
    if isinstance(user, JSONResponse):
        return user
    try:
        query = users.delete().where(users.c.id == user_id)
        await database.execute(query)
    except Exception as e:
        err_text = f"Ошибка при удалении пользователя: {e}"
        return json_error_response(err_text, 400)
    logger.info(f"Пользователь с id {user_id} удален")
    return user


@app.delete("/orders/{order_id}", response_model=Order)
async def delete_order(order_id: int):
    """Удаление заказа"""
    logger.info(f"Удаление заказа с id {order_id}")
    order = await get_note(order_id, "orders")
    if isinstance(order, JSONResponse):
        return order
    try:
        query = orders.delete().where(orders.c.id == order_id)
        await database.execute(query)
    except Exception as e:
        err_text = f"Ошибка при удалении заказа: {e}"
        return json_error_response(err_text, 400)
    logger.info(f"Заказ с id {order_id} удален")
    return order


@app.delete("/products/{product_id}", response_model=Product)
async def delete_product(product_id: int):
    """Удаление товара"""
    logger.info(f"Удаление товара с id {product_id}")
    product = await get_note(product_id, "products")
    if isinstance(product, JSONResponse):
        return product
    try:
        query = products.delete().where(products.c.id == product_id)
        await database.execute(query)
    except Exception as e:
        err_text = f"Ошибка при удалении товара: {e}"
        return json_error_response(err_text, 400)
    logger.info(f"Товар с id {product_id} удален")
    return product


@app.get("/orders/user/{user_id}", response_class=HTMLResponse)
async def get_user_orders(user_id: int):
    """Чтение информации о заказах пользователя по id"""
    logger.info(f"Чтение информации о заказах пользователя с id {user_id}")
    user = await get_note(user_id, "users")
    if isinstance(user, JSONResponse):
        return user
    try:
        query = sqlalchemy.select(
            [orders.c.id, orders.c.product_id, products.c.name.label("product_name"), orders.c.date,
             orders.c.status]).where(
            orders.c.user_id == user_id).join(products, orders.c.product_id == products.c.id)
        orders_data = await database.fetch_all(query)
    except Exception as e:
        err_text = f"Ошибка при получении списка заказов пользователя: {e}"
        return json_error_response(err_text, 400)
    table = DataFrame(orders_data)
    logger.info("Список заказов пользователя получен")
    return table.to_html(index=False)


@app.get("/orders/product/{product_id}", response_class=HTMLResponse)
async def get_product_orders(product_id: int):
    """Чтение информации о заказах товара по id"""
    logger.info(f"Чтение информации о заказах товара с id {product_id}")
    product = await get_note(product_id, "products")
    if isinstance(product, JSONResponse):
        return product
    try:
        query = sqlalchemy.select(
            [orders.c.id, orders.c.user_id, users.c.name.label("user_name"), orders.c.date, orders.c.status]).where(
            orders.c.product_id == product_id).join(users, orders.c.user_id == users.c.id)
        orders_data = await database.fetch_all(query)
    except Exception as e:
        err_text = f"Ошибка при получении списка заказов товара: {e}"
        return json_error_response(err_text, 400)
    table = DataFrame(orders_data)
    logger.info("Список заказов товара получен")
    return table.to_html(index=False)


@app.get("/orders/status/{status}", response_class=HTMLResponse)
async def get_orders_by_status(status: str):
    """Чтение информации о заказах по статусу"""
    logger.info(f"Чтение информации о заказах по статусу {status}")
    try:
        query = (sqlalchemy.select(
            [orders.c.id, orders.c.user_id, users.c.name.label("user_name"), orders.c.product_id,
             products.c.name.label("product_name"), orders.c.date])
                 .where(orders.c.status == status)
                 .join(users, orders.c.user_id == users.c.id)
                 .join(products, orders.c.product_id == products.c.id))
        orders_data = await database.fetch_all(query)
    except Exception as e:
        err_text = f"Ошибка при получении списка заказов по статусу: {e}"
        return json_error_response(err_text, 400)
    table = DataFrame(orders_data)
    logger.info("Список заказов по статусу получен")
    return table.to_html(index=False)


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
