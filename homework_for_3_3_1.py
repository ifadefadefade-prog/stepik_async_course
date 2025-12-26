from fastapi import FastAPI, Header, HTTPException
from typing import Annotated


app = FastAPI()


@app.get('/heades')
async def get_headers(user_agent:  Annotated[str | None, Header()] = None,
                      accept_language:
                      Annotated[str | None, Header()] = None):
    if user_agent and accept_language:
        return {'User-Agent': user_agent,
                'Accept-Language': accept_language}
    else:
        raise HTTPException(status_code=400, detail="<str>")
