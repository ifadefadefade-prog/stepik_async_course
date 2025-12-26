from databases import Database
from fastapi import FastAPI, HTTPException, status
from contextlib import asynccontextmanager
from pydantic import BaseModel


DATABASE_URL = "postgresql://myuser:mypassword@localhost/mydatabase"

database = Database(DATABASE_URL)


class UserBase(BaseModel):
    username: str
    email: str


class UserCreate(UserBase):
    pass


class UserReturn(UserBase):
    id: int


class UserCreateWithPassword(UserCreate):
    password: str
    password_confirm: str


@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    yield
    await database.disconnect()


app = FastAPI(lifespan=lifespan)


@app.post("/users", response_model=UserReturn)
async def create_user(user: UserCreate):
    query = """
            INSERT INTO users (username, email)
            VALUES (:username, :email)
            RETURNING id
            """
    try:
        user_id = await database.execute(
            query=query,
            values=user.model_dump(mode='json')
        )
        return UserReturn(
            id=user_id,
            **user.model_dump(mode="json")
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при создании пользователя: {str(e)}"
        )


@app.get("/users/{user_id}", response_model=UserReturn)
async def get_user(user_id: int):
    query = """
            SELECT id, username, email
            FROM users
            WHERE id = :user_id
            """
    try:
        result = await database.fetch_one(
            query=query,
            values={'user_id': user_id}
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка получения пользователя: {str(e)}"
        )

    if not result:
        raise HTTPException(
            status_code=404,
            detail="Пользователь с указанным ID не найден"
        )

    return UserReturn(
        id=result["id"],
        username=result["username"],
        email=result["email"]
    )


@app.put("/users/{user_id}", response_model=UserReturn)
async def update_user(user_id: int, user: UserCreate):
    query = """
            UPDATE users
            SET username = :username, email = :email
            WHERE id = :user_id
            RETURNING id
            """
    values = {
        "user_id": user_id,
        "username": user.username,
        "email": user.email
    }

    try:
        result = await database.execute(query=query, values=values)

        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Пользователь с указанным ID не найден"
            )
        return UserReturn(**user.model_dump(), id=result,)
    except HTTPException as he:
        raise he

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка обновления пользователя: {str(e)}"
        )


@app.delete("/users/{user_id}", response_model=dict)
async def delete_user(user_id: int):
    query = """
            DELETE FROM users
            WHERE id = :user_id
            RETURNING id
            """
    try:
        deleted_id = await database.execute(
            query=query,
            values={"user_id": user_id}
        )

        if not deleted_id:
            raise HTTPException(
                status_code=404,
                detail="Пользователь с указанным ID не найден"
            )
        return {"message": "Пользователь успешно удален"}
    except HTTPException as he:
        raise he

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка удаления пользователя: {str(e)}"
        )
