from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse


app = FastAPI()


class ItemsResponse(BaseModel):
    item_id: int


class CustomExceptionModel(BaseModel):
    status_code: int
    er_message: str
    er_detail: str


class CustomException(HTTPException):
    def __init__(self, detail: str, status_code: int, message: str):
        super().__init__(status_code, detail)
        self.message = message


@app.exception_handler(CustomException)
async def custom_exception_handler(request, exc: CustomException) -> JSONResponse:
    error = jsonable_encoder(CustomExceptionModel(status_code=exc.status_code,
                                                  er_detail=exc.detail,
                                                  er_message=exc.message))
    return JSONResponse(status_code=exc.status_code, content=error)


@app.get("/items/{item_id}/", response_model=ItemsResponse)
async def read_item(item_id: int):
    if item_id == 42:
        raise CustomException(detail="Item not found", status_code=404,
                              message="You're trying to get an item that doesn't exist. Try entering a different item_id.")
    return ItemsResponse(item_id=item_id)
