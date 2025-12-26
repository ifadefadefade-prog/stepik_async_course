from fastapi import FastAPI, Depends
from security import create_jwt_token, get_user_from_token
from models import User
from db import get_user, USERS_DATA


app = FastAPI()


@app.post('/login')
async def login(user_in: User):
    for user in USERS_DATA:
        if (user.get("username") == user_in.username
                and user.get("password") == user_in.password):
            token = create_jwt_token({'sub': user_in.username})
            return {"access_token": token, "token_type": "bearer"}


@app.get('/about_me')
async def about_me(current_user: str = Depends(get_user_from_token)):
    user = get_user(current_user)
    if user:
        return user
    return {"error": "User not found"}
