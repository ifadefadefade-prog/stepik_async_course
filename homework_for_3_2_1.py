from fastapi import FastAPI, Response, HTTPException, Cookie
from pydantic import BaseModel, Field
import secrets


app = FastAPI()

log_session = []


class Login(BaseModel):
    username: str = Field(max_length=20, min_length=5,
                          description='Введите логие')
    password: str = Field(min_length=8, max_length=16,
                          description='Введите пароль')


@app.post('/set_user')
async def add_user(user: Login):
    log_session.append({
        'username': user.username,
        'password': user.password,
        'session_token': None
    })
    return {'success': True,
            'msg': 'User add!'}


@app.post('/login')
async def get_login(login: Login, response: Response):
    if login.username and login.password:
        for i in log_session:
            if i['username'] == login.username \
                    and i['password'] == login.password:
                session_token = secrets.token_urlsafe(32)
                i['session_token'] = session_token
                response.set_cookie(
                        key="session_token",
                        value=session_token,
                        httponly=True,
                        secure=True,
                        samesite="lax",
                        max_age=3600
                    )
                return {"message": "Logged in"}
        else:
            raise HTTPException(status_code=401,
                                detail="Invalid credentials")


@app.get('/user')
async def get_user_info(session_token: str = Cookie(None)):
    for i in log_session:
        if i['session_token'] == session_token:
            return i
    raise HTTPException(status_code=401,
                        detail="Unauthorized")
