# main.py
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI()


class User(BaseModel):
    username: str
    user_info: str


fake_db = [
    {"username": "vasya", "user_info": "любит колбасу"},
    {"username": "katya", "user_info": "любит петь"}
]


@app.get('/users/{username}')
async def get_user_by_username(username: Optional[str] = None):
    for user in fake_db:
        if user['username'] == username:
            return user
    return {'error': 'user not found'}


@app.get('/users/')
async def get_all_users(limit: int = 10):
    return fake_db[:limit]


@app.post('/add_user', response_model=User)
async def add_user(user: User):
    fake_db.append({
        'username': user.username,
        'user_info': user.user_info
    })
    return user
