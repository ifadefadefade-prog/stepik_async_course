import jwt


SECRET_KEY = "mysecretkey"
ALGORITHM = 'HS256'

USER_DATA = [
    {'username': 'admin', 'password': 'adminpass'}
]


def create_jwt_token(data: str):
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)


def get_user_from_token(token: str):
    try:
        playload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        print(playload)
        return playload.get('sub')
    except jwt.ExpiredSignatureError:
        raise 'логика обработки ошибки истечения срока действия токена'
    except jwt.InvalidTokenError:
        raise 'логика обработки ошибки декодирования токена'


def get_user(username: str):
    for user in USER_DATA:
        if user.get('username') == username:
            return user
    return None


token = create_jwt_token({'sub': 'admin'})
print(token)

username = get_user_from_token(token)
print(username)

current_user = get_user(username)
print(current_user)
