from fastapi import FastAPI, Depends, status, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel


app = FastAPI()
security = HTTPBasic()


class User(BaseModel):
    username: str
    password: str


USER_DATA = [
    User(**{"username": "user1", "password": "pass1"}),
    User(**{"username": "user2", "password": "pass2"})
]


def get_user_from_db(username: str):
    for user in USER_DATA:
        print(user)
        if user.username == username:
            return user
    return None


def auth_user(credentials: HTTPBasicCredentials = Depends(security)):
    print(credentials)
    user = get_user_from_db(credentials.username)
    if user is None or user.password != credentials.password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Invalid credentials')
    return user


@app.get('/protected_resource/')
def get_protected_resource(user: User = Depends(auth_user)):
    return {"message": "You have access to the protected resource!",
            "user_info": user}
