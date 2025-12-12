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
def read_users(username: str = None, email: str = None, limit: int = 10):
    filtered_users = fake_users
    if username:
        filtered_users = {key: user for key, user in filtered_users.items()
                          if username.lower() in user['username'].lower()}
    if email:
        filtered_users = {key: user for key, user in filtered_users.items()
                          if email.lower() in user['email'].lower()}

    return filtered_users
