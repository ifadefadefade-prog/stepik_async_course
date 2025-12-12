# main.py
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

@app.get('/custom')
def get_custom_msg():
    return {"message": "This is a custom message!"}

