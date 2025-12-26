from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from database import get_db_connection
from typing import Optional
import asyncpg


app = FastAPI()


class Todo(BaseModel):
    title: str
    description: str


class User(Todo):
    username: str
    title: Optional[str] = None
    description: Optional[str] = None


@app.post('/add-user')
async def add_user(user: User, db: asyncpg.Connection =
                   Depends(get_db_connection)):
    result = await db.fetchval("SELECT COALESCE(MAX(id), 0) FROM users")
    if result is None:
        id = 1
    else:
        id = result + 1

    try:
        await db.execute("""
                        INSERT INTO users
                        (id, username)
                        VALUES($1, $2)""",
                         id, user.username)
        return {'message': f'{user.username} - add success',
                'user_id': f'{id}'}
    except Exception as e:
        print(e)


async def verify_user(temp: str | int, db):
    if type(temp) is str:
        user_id = await db.fetchval("SELECT id FROM users WHERE username = $1",
                                    temp)
        if user_id:
            return True
        else:
            return False

    elif type(temp) is int:
        username = await db.fetchval("SELECT username FROM users " +
                                     "WHERE id = $1",
                                     temp)
        if username:
            return True
        else:
            return False


@app.delete("/users/{user_id}")
async def del_user(user_id: int,
                   db: asyncpg.Connection =
                   Depends(get_db_connection)):
    if not await verify_user(user_id, db):
        raise HTTPException(
         status_code=status.HTTP_404_NOT_FOUND,
         detail='User not found'
        )
    res = await db.execute("""
                     DELETE FROM users
                     WHERE id = $1
                     """, user_id)
    if res == 'DELETE 1':
        return {'message': f'User {user_id} delete success'}
    else:
        return {'message': f'User {user_id} delete error'}


@app.post('/add-task')
async def add_task(todo: User, db: asyncpg.Connection =
                   Depends(get_db_connection)):

    result = await db.fetchval("SELECT COALESCE(MAX(id), 0) FROM todoList")
    if result is None:
        id = 1
    else:
        id = result + 1

    user_id = await db.fetchval("SELECT id FROM users WHERE username = $1",
                                todo.username)
    if not user_id:
        raise HTTPException(
         status_code=status.HTTP_404_NOT_FOUND,
         detail='User not found'
        )

    completed = False

    await db.execute('''
                     INSERT INTO todoList
                     (id, title, description, completed, user_id)
                     VALUES($1, $2, $3, $4, $5)''',
                     id, todo.title, todo.description, completed, user_id)
    return {
              "id": id,
              "title": todo.title,
              "description": todo.description,
              "completed": completed,
              "user_id": user_id
            }


@app.get('/todoList/{task_id}')
async def get_task_by_id(task_id: int,
                         db: asyncpg.Connection =
                         Depends(get_db_connection)):
    if task_id is None:
        return {'message': 'Вы не ввели task_id'}

    task = await db.fetchrow("SELECT * FROM todoList WHERE id = $1",
                             task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    else:
        task_dict = dict(task)

        return {
            "message": "Task found",
            "task": task_dict
        }


@app.put('/update')
async def update_completed(task_update: User,
                           db: asyncpg.Connection =
                           Depends(get_db_connection)):

    if not await verify_user(task_update.username, db):
        raise HTTPException(
         status_code=status.HTTP_404_NOT_FOUND,
         detail='User not found'
        )

    result = await db.fetchrow("""
                              UPDATE todoList t
                              SET completed = true
                              FROM users u
                              WHERE title = $1
                                AND description = $2
                                AND u.username = $3
                                AND t.user_id = u.id
                              RETURNING *
                              """, task_update.title, task_update.description,
                                   task_update.username)
    if not result:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )
    return {
        "message": "Task completed",
        "task": dict(result)
    }


@app.delete('/item-del/{username}/{task_id}')
async def del_item(task_id: int,
                   username: str,
                   db: asyncpg.Connection =
                   Depends(get_db_connection)):

    if not await verify_user(username, db):
        raise HTTPException(
         status_code=status.HTTP_404_NOT_FOUND,
         detail='User not found'
        )

    res = await db.execute("""
                     DELETE FROM todoList t
                     USING users u
                     WHERE t.id = $1
                        AND u.username = $2
                        AND t.user_id = u.id
                     """, task_id, username)
    if res == 'DELETE 1':
        return {'message': f'task {task_id} delete success'}
    else:
        raise HTTPException(
            404,
            detail=f'Task {task_id} not found or does ' +
                   f'not belong to user {username}'
        )
