from fastapi import FastAPI

app = FastAPI()

# Пример пользовательских данных (для демонстрационных целей)
fake_users = {
    1: {"username": "john_doe", "email": "john@example.com"},
    2: {"username": "jane_smith", "email": "jane@example.com"},
    3: {"username": "alice_jones", "email": "alice@example.com"},
    4: {"username": "bob_white", "email": "bob@example.com"},
}


@app.get('/users/')
async def read_user(limit: int = 10):
    return dict(list(fake_users.items())[:limit])
