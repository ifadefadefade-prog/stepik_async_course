import jwt
from datetime import datetime, timezone, timedelta
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from typing import Dict


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = 'mysecretkey'
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15


def create_jwt_token(data: Dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(
                                          minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp': expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_user_from_token(token: str = Depends(oauth2_scheme)):
    try:
        playload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        print(f'playload: {playload}')
        return playload.get('sub')
    except Exception as e:
        raise e
