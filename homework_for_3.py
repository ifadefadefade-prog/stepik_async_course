from fastapi import FastAPI
from pydantic import BaseModel, EmailStr, Field
from typing import Optional


app = FastAPI()


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    age: Optional[int] = Field(default=None,gt=0) 
    is_subscribed : bool = False


@app.post('/create_user/')
async def create_user(user: UserCreate):
    return {'name': user.name,
            'email': user.email,
            'age': user.age,
            'is_subscribed': user.is_subscribed}
