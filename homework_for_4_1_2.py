from fastapi import FastAPI, Depends, status, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
from passlib.context import CryptContext
import secrets


app = FastAPI()
security = HTTPBasic()
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
print(security)


class UserBase(BaseModel):
    username: str


class User(UserBase):
    password: str


class UserInDB(UserBase):
    hashed_password: str


fake_users_db = []


def get_user_from_db(username: str):
    for user in fake_users_db:
        if secrets.compare_digest(user.username, username):
            return user
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                        detail='Логин или пароль не найдены',
                        headers={"WWW-Authenticate": "Basic"})


def verify_user_input_pass(password, password_hash):
    return bcrypt_context.verify(password, password_hash)


def reg_hash_pass(password):
    return bcrypt_context.hash(password)


def auth_user(credentials: HTTPBasicCredentials = Depends(security)):
    user = get_user_from_db(credentials.username)
    is_correct = verify_user_input_pass(credentials.password,
                                        user.hashed_password)
    if not is_correct:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Логин или пароль не найдены',
                            headers={"WWW-Authenticate": "Basic"})
    return user


@app.get('/login')
def login(user: UserInDB = Depends(auth_user)):
    return {"msg": f"You got my secret, welcome, {user.username}"}


@app.get('/get_db')
def get_db():
    print(fake_users_db)
    return fake_users_db


@app.post('/register')
def register(user: User):
    for existing_user in fake_users_db:
        if secrets.compare_digest(existing_user.username, user.username):
            raise HTTPException(status_code=400, detail="User already exists")
    fake_users_db.append(UserInDB(
                        username=user.username,
                        hashed_password=reg_hash_pass(user.password)
                        ))
    return {"message": f"User {user.username} created"}
