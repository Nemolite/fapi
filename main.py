from enum import Enum
from fastapi import FastAPI

class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

app = FastAPI()

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
    return fake_items_db[skip : skip + limit]


