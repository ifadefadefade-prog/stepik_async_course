from models import Users
from fastapi import FastAPI

app = FastAPI()

users = []


@app.post('/')
def add_user(user: Users):
    users.append({
        'name': user.name,
        'id': user.id
    })


@app.get('/')
def get_user():
    return users
