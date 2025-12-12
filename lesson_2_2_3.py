from pydantic import BaseModel
from fastapi import FastAPI

app = FastAPI()

class User(BaseModel):
    username: str
    message: str
 
users = []   

@app.get('/')
async def get_users():
    return users
    
@app.post('/')
async def new_user(user:User):
    users.append(user)
    return {"User add": "success"}

    