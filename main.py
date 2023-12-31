# pip install SQLAlchemy
# pip install psycopg2
from typing import Union
from enum import Enum
from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import  Column, Integer, String
from sqlalchemy.orm import sessionmaker
from jose import JWTError, jwt

# Подключение к базе данных
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:12345678@localhost/mybasa"

# создаем движок SqlAlchemy
engine = create_engine(SQLALCHEMY_DATABASE_URL)
print(engine)

#создаем базовый класс для моделей
Base = declarative_base()

# создаем модель, объекты которой будут храниться в бд
class Person(Base):
    __tablename__ = "people"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    age = Column(Integer, )

# создаем таблицы
Base.metadata.create_all(bind=engine)

# Завершение работы с базами данных

# Подгтовка к записи в базу данных
# True - изменяет записи
SessionLocal = sessionmaker(autoflush=True, bind=engine)
db = SessionLocal()

class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

app = FastAPI()

# Добавление данных
@app.get("/ins")
async def ins():
    # создаем объект Person для добавления в бд
    tom = Person(name="Tom", age=38)
    db.add(tom)  # добавляем в бд
    db.commit()  # сохраняем изменения

    print(tom.id)

# Получение данных
@app.get("/db")
async def basa():
    people = db.query(Person).all()
    return people

# Обновление данных
@app.get("/update/{user_id}/{name_user}")
async def updater(user_id: int, nmae_user:str):
    # получаем один объект по ID
    result = db.query(Person).filter(Person.id == user_id).first()

    # изменениям значения
    result.name = nmae_user
    result.age = 22

    db.commit()  # сохраняем изменения

    # проверяем, что изменения применены в бд - получаем один объект, у которого имя - Tomas
    return db.query(Person).filter(Person.id == user_id).first()

# Удаление данных
@app.get("/dele/{user_id}")
async def dele(user_id:int):
    object_user = db.query(Person).filter(Person.id == user_id).first()
    db.delete(object_user)  # удаляем объект
    db.commit()  # сохраняем изменения

fake_data = [
    {"id":1,"name": "Harry Potter","city": "London"},
    {"id":2,"name": "Don Quixote","city": "Madrid"},
    {"id":3,"name": "Joan of Arc","city": "Paris"},
    {"id":4,"name": "Rosa Park","city": "Alabama"},
]

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/get_data/{id}")
async def root(id: int):
    return [d for d in fake_data if d.get("id")==id ]

fake_trades = [
    {"id":1,"user_id":1, "currency":"BTC","price": 1000},
    {"id":2,"user_id":1, "currency":"BTC","price": 2000},
    {"id":3,"user_id":1, "currency":"BTC","price": 5000},
    {"id":4,"user_id":1, "currency":"BTC","price": 7000},
]

@app.get("/traders")
async def get_trades(limit:int, offset:int ):
    return fake_trades[offset:][:limit]

@app.post("/get_data/{id}")
async def change_data(id:int,new_currency:str):
    for k in fake_trades:
        if k["id"]==id:
            k["currency"] = new_currency
    return  fake_trades

@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

# http://127.0.0.1:8000/items/?skip=0&limit=10

print(fake_items_db[1:2])

@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    # Обратите внимание тут срез
    return fake_items_db[skip : skip + limit]

@app.get("/itemsbool/{item_id}")
# short - объявлен как логический тип, если запрос будет содержать что-то
# другое, он будет преобразован в логический тип данных

# http://127.0.0.1:8000/itemsbool/foo?short=1
# обратите внимание на параметр q
# http://127.0.0.1:8000/itemsbool/foo?q=example&short=1
async def read_item(item_id: str, q: str | None = None, short: bool = False):
    item = {"item_id": item_id,"short":short}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "Данная запись появилась,т.к bool = False"}
        )
    return item

# Смешивание query-параметров и path-параметров

@app.get("/users/{user_id}/items/{item_id}")
# user_id - int, item_id  -строку
# q можно не указывать, тогда будет None, если указать то строка
# short - bool, по умолчанию False
# http://127.0.0.1:8000/users/12/items/str_item_id?q=example&short=yes
# {"item_id":"str_item_id","owner_id":12,"q":"example"}

async def read_user_item(user_id: int, item_id: str, q: str | None = None, short: bool = False):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "Данная запись появилась,т.к bool = False"}
        )
    return item
##############################################
#                 Тело запроса               #
##############################################

class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None

@app.post("/itemsbasamodel/")
async def create_item(item: Item):
    return item

# Использование модели

@app.post("/itemsmodel/")
async def create_item(item: Item):
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict

@app.post("/test/")
async def testing(login: str, password: str):
    print(login)
    print(password)

    payload = {
        "login": login,
    }
    SECRET_KEY ='saff23r23dfAD32'
    token = jwt.encode(payload, SECRET_KEY,algorithm="HS256")
    return token



# Тело запроса + параметры пути

@app.put("/items/{item_id}")
async def create_item(item_id: int, item: Item):
    return {"item_id": item_id, **item.dict()}

# Тело запроса + параметры пути + параметры запроса

@app.put("/items/{item_id}")
async def create_item(item_id: int, item: Item, q: Union[str, None] = None):
    result = {"item_id": item_id, **item.dict()}
    if q:
        result.update({"q": q})
    return result
