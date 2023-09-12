from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

data = [
    {"id":1,"name": "Harry Potter","city": "London","price":100},
    {"id":2,"name": "Don Quixote","city": "Madrid","price":200},
    {"id":3,"name": "Joan of Arc","city": "Paris","price":560},
    {"id":4,"name": "Rosa Park","city": "Alabama","price":1000},
]

class Trades(BaseModel):
    id:int
    name: str
    city:str
    price:int

@app.post("/trades")
def add_data(trades:list[Trades]):
    data.extend(trades)
    return {"status":200, "data":data}

users = [

]

class User(BaseModel):
    id:int
    name: str
    city: str
    price:int

@app.get("/users/{user_id}",response_model=list[User])
def get_user(user_id:int):
    return [ user for user in data if user.get("id")==user_id]
