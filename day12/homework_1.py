from typing import Any, Dict
from typing_extensions import Annotated
from annotated_doc import Doc
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse


app = FastAPI()


class UsernameResponse(BaseModel):
    username: str


class CustomExceptionModelA(BaseModel):
    status_code: int
    er_message: str
    er_detail: str

class CustomExceptionModelB(CustomExceptionModelA):
    status_code: int
    er_message: str
    er_detail: str
    errors: list


class CustomExceptionA(HTTPException):
    def __init__(self, detail: str, message, status_code: int = 400):
        super().__init__(status_code, detail)
        self.message = message


class CustomExceptionB(HTTPException):
    def __init__(self, detail: str, message, errors: list, status_code: int = 401):
        super().__init__(status_code, detail)
        self.message = message
        self.errors = errors


@app.exception_handler(CustomExceptionA)
async def custom_exception_handler_for_a(request, exc: CustomExceptionA):
    error = jsonable_encoder(CustomExceptionA(status_code=exc.status_code,
                                              message=exc.message,
                                              detail=exc.detail))
    return JSONResponse(content=error, status_code=exc.status_code)


@app.exception_handler(CustomExceptionB)
async def custom_exception_handler_for_b(request, exc: CustomExceptionB):
    error = jsonable_encoder(CustomExceptionB(status_code=exc.status_code,
                                              message=exc.message,
                                              detail=exc.detail,
                                              errors=exc.errors))
    return JSONResponse(status_code=exc.status_code, content=error)


@app.get('/users/{username}', response_model=UsernameResponse)
async def get_username(username: str):
    errors = ['pizda', 'xyi']
    if len(username) >= 20:
        raise CustomExceptionA(detail='Слишком много символов',
                               message='Максимальная длинна username 20 символов',
                               status_code=400)
    elif username in errors:
        raise CustomExceptionB(detail='Username вход в число недопустимых слов',
                               message='Не испольуейте это слово в качестве юзернейма',
                               status_code=401,
                               errors=errors)
    else:
        return UsernameResponse(username=username)
