USERS_DATA = [
    {"username": "admin", "password": "adminpass"}
]


def get_user(username: str):
    for user in USERS_DATA:
        if user.get('username') == username:
            return user
    return None
