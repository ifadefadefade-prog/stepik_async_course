# main.py
from fastapi import FastAPI, Query
from pydantic import BaseModel, Field, field_validator, EmailStr
from typing import Optional
import pymorphy3
import re


PHONE_VALUE = '1234567890'

morph = pymorphy3.MorphAnalyzer()

app = FastAPI()


class User(BaseModel):
    username: str = Field(min_length=2, max_length=50)
    user_info: str = Field(min_length=10, max_length=500)


class Feedback(BaseModel):
    username: str
    message: str

    @field_validator('message')
    async def validate_msg(cls, t: str) -> str:
        words = re.findall(r'\w+', t.lower())
        forbidden_words = {"редиска", "бяка", "козявка"}
        for word in words:
            normal = morph.parse(word)[0].normal_form.lower()
            if normal in forbidden_words:
                raise ValueError("Использование недопустимых слов")
        return t


class Contact(Feedback):
    email: EmailStr
    phone: Optional[str] = Field(default=None, min_length=7, max_length=15)

    @field_validator('phone')
    def verify_phone(cls, t: str):
        for i in t:
            if i not in PHONE_VALUE:
                raise ValueError('Номер телефона должен' +
                                 'содержать только цифры')
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
async def send_feedback(form: Contact, premium: Optional[bool] = Query(None)):
    user_feedback.append({
        'name': form.username,
        'message': form.message,
        'contact': {'email': form.email,
                    'phone': form.phone
                    }
    })
    if premium:
        return {
                "message": f"Спасибо, {form.username}! Ваш отзыв сохранён." +
                "Ваш отзыв будет рассмотрен в приоритетном порядке."
                }
    else:
        return {"message": f"Feedback received. Thank you, {form.username}."}
