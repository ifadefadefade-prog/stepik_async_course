# db.py
from models import User

product_list = []

USERS_DATA = [
    {
        "username": "admin",
        "password": "adminpass",
        "roles": ["admin"],
        "full_name": "Admin User",
        "email": "admin@example.com",
        "disabled": False
    },
    {
        "username": "user",
        "password": "userpass",
        "roles": ["user"],
        "full_name": "Regular User",
        "email": "user@example.com",
        "disabled": False
    },
    {
        "username": "guest",
        "password": "guestpass",
        "roles": ["guest"],
        "full_name": "Regular User",
        "email": "guest@example.com",
        "disabled": False
    }
]

def get_user(username: str) -> User | None:
    for user_data in USERS_DATA:
        if user_data["username"] == username:
            return User(**{k: v for k, v in user_data.items() if k != "password"})
    return None
