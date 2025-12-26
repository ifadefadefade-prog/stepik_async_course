from fastapi import FastAPI, Response, HTTPException, Cookie
from pydantic import BaseModel, Field
from itsdangerous import URLSafeSerializer
import uuid
import time


SECRET_KEY = '123123123'
token = URLSafeSerializer(SECRET_KEY)


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
        'session_token': None,
        'user_id': None,
        'timestamp': None
    })
    return {'success': True,
            'msg': 'User add!'}


@app.post('/login')
async def get_login(login: Login, response: Response):
    if login.username and login.password:
        for i in log_session:
            if i['username'] == login.username \
                    and i['password'] == login.password:
                timestamp = int(time.time())
                i['timestamp'] = timestamp
                i['user_id'] = str(uuid.uuid4())
                session_token = token.dumps({'user_id': i['user_id'],
                                             'timestamp': timestamp})
                i['session_token'] = session_token
                response.set_cookie(
                        key="session_token",
                        value=session_token,
                        httponly=True,
                        secure=False,
                        samesite="lax",
                        max_age=300
                    )
                return {"message": "Logged in"}
        else:
            raise HTTPException(status_code=401,
                                detail="Invalid credentials")


@app.get('/user')
async def get_user_info(session_token: str = Cookie(None)):
    for i in log_session:
        user_data = token.loads(session_token)
        user_id = user_data['user_id']
        if i['user_id'] == user_id:
            return i
    raise HTTPException(status_code=401,
                        detail="Unauthorized")


@app.get("/profile")
async def get_profile(response: Response, session_token: str = Cookie(None)):
    try:
        user_data = token.loads(session_token, max_age=300)
    except Exception:
        raise HTTPException(status_code=401, detail="Unauthorized")
    for i in log_session:
        user_id = user_data['user_id']
        if i['user_id'] == user_id:
            new_timestamp = int(time.time())
            if i['timestamp'] is None:
                i['timestamp'] = new_timestamp
            temp = new_timestamp - i['timestamp']
            if 180 <= temp <= 300:
                i['timestamp'] = new_timestamp
                new_token = token.dumps({'user_id': i['user_id'],
                                         'timestamp': i['timestamp']})
                i['session_token'] = new_token
                response.set_cookie(
                    key="session_token",
                    value=new_token,
                    httponly=True,
                    secure=False,
                    samesite="lax",
                    max_age=300
                )
            elif temp > 300:
                raise HTTPException(status_code=401, detail="session close")
            return i
    raise HTTPException(status_code=401, detail="Unauthorized")


@app.get('/get_all_users')
async def get_all_users():
    return log_session
