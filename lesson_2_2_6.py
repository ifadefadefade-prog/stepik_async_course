from models_1 import Users
from fastapi import FastAPI

app = FastAPI()

users = []


@app.post('/')
def add_user(user: Users):
    t = ({
        'name': user.name,
        'age': user.age,
        'is_adult': True if user.age >= 18 else False
    })
    users.append(t)
    return t


@app.get('/')
def get_user():
    return users
