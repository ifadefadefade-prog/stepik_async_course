# main.py
from fastapi import FastAPI
from pydantic import BaseModel, Field, field_validator
from typing import Optional
import pymorphy3
import re


morph = pymorphy3.MorphAnalyzer()

app = FastAPI()


class User(BaseModel):
    username: str = Field(min_length=2, max_length=50)
    user_info: str = Field(min_length=10, max_length=500)


class Feedback(BaseModel):
    username: str
    message: str

    @field_validator('message')
    def validate_msg(cls, t: str) -> str:
        words = re.findall(r'\w+', t.lower())
        forbidden_words = {"редиска", "бяка", "козявка"}
        for word in words:
            normal = morph.parse(word)[0].normal_form.lower()
            if normal in forbidden_words:
                raise ValueError("Использование недопустимых слов")
        return t


user_feedback = []

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


@app.post('/feedback')
async def send_feedback(form: Feedback):
    user_feedback.append({
        'name': form.username,
        'message': form.message
    })
    return {"message": f"Feedback received. Thank you, {form.username}."}
