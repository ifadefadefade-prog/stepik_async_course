from fastapi import FastAPI, Header, HTTPException
from typing import Annotated
from pydantic import BaseModel, field_validator
import re
from datetime import datetime


MINIMUM_APP_VERSION = "0.0.2"
MINIMUM_APP_VERSION_LIST = MINIMUM_APP_VERSION.split('.')
app = FastAPI()


class CommonHeaders(BaseModel):
    user_agent: str | None = None
    accept_language: str | None = None
    x_current_version: str | None = None

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

    @field_validator('x_current_version')
    @classmethod
    def validate_x_current_version(cls, v: str | None) -> str | None:
        if v is None:
            return v
        pattern = r'^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$'
        if not re.fullmatch(pattern, v):
            raise ValueError("Требуется обновить приложение")
        return v


def is_version_compatible(current: str, minimum: str) -> bool:
    current_parts = list(map(int, current.split('.')))
    min_parts = list(map(int, minimum.split('.')))
    for cur, min_val in zip(current_parts, min_parts):
        if cur < min_val:
            return False
        elif cur > min_val:
            return True
    return True


@app.get('/headers')
async def get_headers(user_agent: Annotated[str | None, Header()] = None,
                      accept_language: Annotated[str | None, Header()] = None,
                      x_current_version:
                      Annotated[str | None, Header()] = None):
    headers = CommonHeaders(user_agent=user_agent,
                            accept_language=accept_language,
                            x_current_version=x_current_version)
    if headers.user_agent and headers.accept_language and x_current_version:
        if not is_version_compatible(x_current_version, MINIMUM_APP_VERSION):
            raise HTTPException(status_code=422,
                                detail="ValueError(Требуется"
                                "обновить приложение")
    else:
        return {'User-Agent': headers.user_agent,
                'Accept-Language': headers.accept_language}


@app.get('/info')
async def get_info(user_agent: Annotated[str | None, Header()] = None,
                   accept_language: Annotated[str | None, Header()] = None,
                   x_server_time: Annotated[str | None, Header()] = None,
                   x_current_version: Annotated[str | None, Header()] = None):
    headers = CommonHeaders(user_agent=user_agent,
                            accept_language=accept_language,
                            x_current_version=x_current_version)
    if headers.user_agent and headers.accept_language and x_current_version:
        if not is_version_compatible(x_current_version, MINIMUM_APP_VERSION):
            raise HTTPException(status_code=422,
                                detail="ValueError(Требуется"
                                "обновить приложение")
        else:
            server_time = (x_server_time if x_server_time
                           else datetime.now().isoformat())
            return {'message': 'Добро пожаловать! Ваши заголовки ' +
                    'успешно обработаны.',
                    'User-Agent': headers.user_agent,
                    'Accept-Language': headers.accept_language,
                    'X-Server-Time': server_time,
                    'X-Current-Version': x_current_version}

    else:
        raise HTTPException(status_code=400, detail="<str>")
