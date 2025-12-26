from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse


app = FastAPI()


class CustomExcetion(HTTPException):
    def __init__(self, detail: str, status_code: int = 400,):
        super().__init__(status_code, detail)


@app.exception_handler(CustomExcetion)
async def custom_exception_handler(request, exc: CustomExcetion):
    return JSONResponse(content={'error': exc.detail,
                                 'status_code': exc.status_code})


@app.exception_handler(Exception)
async def global_exception_handler(reques: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={'error': 'Internal server error'}
    )


@app.get("/items/{item_id}")
async def read_item(item_id: int):
    result = 1 / 0
    return {"item_id": item_id}
