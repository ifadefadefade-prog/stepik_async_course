from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def get_msg():
    return {"message" : "Добро пожаловать в моё приложение FastAPI!"}