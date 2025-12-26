from fastapi import FastAPI, Header, HTTPException
from typing import Annotated
from pydantic import BaseModel, field_validator
import re
from datetime import datetime


app = FastAPI()


class CommonHeaders(BaseModel):
    user_agent: str | None = None
    accept_language: str | None = None

    @field_validator('accept_language')
    @classmethod
    def validate_accept_language(cls, v: str | None) -> str | None:
        if v is None:
            return v
        pattern = r'^(?i:(?:\*|[a-z\-]{2,5})(?:;q=\d\.\d)?,)*(?:\*|[a-z\-]{2,5})(?:;q=\d\.\d)?$'
        if not re.fullmatch(pattern, v):
            raise ValueError(
                'Некорректный формат Accept-Language. '
                'Пример: "en", "en-US;q=0.9",' +
                '"en-US,en;q=0.9,ru;q=0.8,*;q=0.5"'
            )
        return v


@app.get('/headers')
async def get_headers(user_agent: Annotated[str | None, Header()] = None,
                      accept_language: Annotated[str | None, Header()] = None):
    headers = CommonHeaders(user_agent=user_agent,
                            accept_language=accept_language)
    if headers.user_agent and headers.accept_language:
        return {'User-Agent': headers.user_agent,
                'Accept-Language': headers.accept_language}
    else:
        raise HTTPException(status_code=400, detail="<str>")


@app.get('/info')
async def get_info(user_agent: Annotated[str | None, Header()] = None,
                   accept_language: Annotated[str | None, Header()] = None,
                   x_server_time: Annotated[str | None, Header()] = None):
    headers = CommonHeaders(user_agent=user_agent,
                            accept_language=accept_language)
    if headers.user_agent and headers.accept_language:
        now = datetime.now()
        return {'message': 'Добро пожаловать! Ваши заголовки ' +
                'успешно обработаны.',
                'User-Agent': headers.user_agent,
                'Accept-Language': headers.accept_language,
                'X-Server-Time': x_server_time if x_server_time
                is not None else now}

    else:
        raise HTTPException(status_code=400, detail="<str>")
