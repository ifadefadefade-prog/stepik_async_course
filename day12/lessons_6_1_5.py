from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse


app = FastAPI()


class ItemsResponse(BaseModel):
    item_id: int


class CustomException(HTTPException):
    def __init__(self, detail: str, status_code: int = 400,):
        super().__init__(status_code, detail)


@app.exception_handler(CustomException)
async def custom_exception_handler(request, exc: CustomException):
    return JSONResponse(content={'error': exc.detail,
                                 'status_code': exc.status_code})


@app.get("/items/{item_id}", response_model=ItemsResponse)
async def read_item(item_id: int):
    if item_id == 42:
        raise CustomException(detail="Item not found", status_code=404)
    return ItemsResponse(item_id=item_id)
