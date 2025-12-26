from fastapi import FastAPI, Depends, status, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel


app = FastAPI()
security = HTTPBasic()
print(security)


class User(BaseModel):
    username: str
    password: str


USER_DATA = [
    User(**{"username": "user1", "password": "pass1"}),
    User(**{"username": "user2", "password": "pass2"})
]


def get_user_from_db(username: str):
    for user in USER_DATA:
        if user.username == username:
            return user
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='Логин не найден')


def auth_user(credetials: HTTPBasicCredentials = Depends(security)):
    user = get_user_from_db(credetials.username)
    if user is None or user.password != credetials.password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Логин или пароль не найдены')
    return user


@app.get('/login')
def login(user: User = Depends(auth_user)):
    return {"msg": "You got my secret, welcome",
            "userinfo": user}
