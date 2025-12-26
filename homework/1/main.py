from pydantic import BaseModel
from database import get_db
from fastapi import FastAPI, Depends
import sqlite3


app = FastAPI()


class Users(BaseModel):
    username: str
    password: str


@app.post('/register')
async def register(user: Users):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT COALESCE(MAX(id), 0) FROM users")
    max_id = cursor.fetchone()[0]
    id = max_id + 1
    cursor.execute('''INSERT INTO users
                   (id, username, password) VALUES (?, ?, ?)''',
                   (id, user.username, user.password))

    conn.commit()
    conn.close()

    return {"message": "Item added successfully!"}
