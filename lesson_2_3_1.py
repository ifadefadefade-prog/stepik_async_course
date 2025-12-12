from fastapi import FastAPI
from typing import Optional


app = FastAPI()

fake_users = {
    1: {"username": "john_doe", "email": "john@example.com"},
    2: {"username": "jane_smith", "email": "jane@example.com"},
}


@app.get('/user/{user_id}')
async def get_user_by_id(user_id: Optional[int] = None):
    if user_id in fake_users:
        return fake_users[user_id]
    return {'error': 'User not found'}
