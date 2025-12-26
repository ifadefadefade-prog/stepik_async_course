import jwt
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from typing import Dict
from datetime import datetime, timezone, timedelta

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')


app = FastAPI()
SECRET_KEY = 'mysecretkey'
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 10

USERS_DATA = [
    {"username": "admin", "password": "adminpass"}
]


def get_user_from_db(username: str):
    for user in USERS_DATA:
        if user.get('username') == username:
            return user
    return None


class User(BaseModel):
    username: str
    password: str


def create_jwt_token(data: Dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(
                                          minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp': expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_jwt_token(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=e)


@app.post('/login')
async def login(user_in: User):
    for user in USERS_DATA:
        if (user.get('username') == user_in.username
                and user.get('password') == user_in.password):
            token = create_jwt_token({'sub': user_in.username})
            return {"access_token": token}
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid credentials")


@app.get('/protected_resource')
async def protected_resource(token: str = Depends(oauth2_scheme)):
    playload = decode_jwt_token(token)
    user_from_playload = playload.get('sub')
    exp = playload.get('exp')
    if (get_user_from_db(user_from_playload)
            and exp >= datetime.now(timezone.utc).timestamp()):
        return {'msg': 'Доступ разрешен'}
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid credentials")
