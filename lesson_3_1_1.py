from fastapi import FastAPI


app = FastAPI()

@app.get('/users/')
def get_all_users():
    return {"message": "Список пользователей"}


@app.post('/users/')
def add_user():
     return {"message": "Создан новый пользователь"}
 

@app.put('/users/{user_id}')
def update_user(user_id: int):
    return {"message": f"Пользователь {user_id} обновлён"}

@app.delete('/users/{users_id}')
def delete_user(user_id: int):
    return {"message": f"Пользователь {user_id} удалён"}