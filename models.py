from pydantic import BaseModel


class Users(BaseModel):
    name: str
    id: int
