from fastapi import FastAPI

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
