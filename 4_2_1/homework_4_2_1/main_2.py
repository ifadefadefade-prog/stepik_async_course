import jwt
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi import Request
from pydantic import BaseModel
from typing import Dict
from datetime import datetime, timezone, timedelta
from passlib.context import CryptContext


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
limiter = Limiter(key_func=get_remote_address)


app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


SECRET_KEY = 'mysecretkey'
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 10


def verify_user_input_pass(password, password_hash):
    return bcrypt_context.verify(password, password_hash)


def reg_hash_pass(password):
    return bcrypt_context.hash(password)


USERS_DATA = [
    {"username": "admin", "password": "adminpass"}
]


for db in USERS_DATA:
    db['password'] = reg_hash_pass(db['password'])


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
@limiter.limit('5/minute')
async def login(user_in: User, request: Request):
    user = get_user_from_db(user_in.username)
    if user and verify_user_input_pass(user_in.password, user.get('password')):
        token = create_jwt_token({'sub': user_in.username})
        return {"access_token": token,
                "sub": user_in.username}
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid credentials")


@app.get('/protected_resource')
async def protected_resource(token: str = Depends(oauth2_scheme)):
    payload = decode_jwt_token(token)
    user_from_payload = payload.get('sub')
    exp = payload.get('exp')
    if (get_user_from_db(user_from_payload)
            and exp >= datetime.now(timezone.utc).timestamp()):
        return {'msg': 'Доступ разрешен'}
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid credentials")


@app.post('/register')
@limiter.limit('1/minute')
async def register(user: User, request: Request):
    for i in USERS_DATA:
        if user.username == i.get('username'):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail="User already exists")
    USERS_DATA.append({'username': user.username,
                       'password': reg_hash_pass(user.password)})
    return {
            "status_code": status.HTTP_201_CREATED,
            "detail": {
                'success': True,
                'message': f'{user.username} was created'
            }
            }
