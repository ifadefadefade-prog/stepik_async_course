import jwt
from typing import Dict
from datetime import datetime, timezone, timedelta
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException, status, Depends


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15


def create_jwt_token(data: Dict):
    to_encode = data.copy()
    expire = (datetime.now(timezone.utc) +
              timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({'exp': expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_user_from_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        return payload.get('username')
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Токен устарел")  # Токен просрочен
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Ошибка авторизации")
