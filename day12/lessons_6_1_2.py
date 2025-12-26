from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse


app = FastAPI()


class CustomException(HTTPException):
    def __init__(self, detail: str, status_code: int = 400) -> None:
        super().__init__(status_code=status_code, detail=detail)


@app.exception_handler(CustomException)
async def custom_exception_handler(reques: Request, exc: CustomException):
    return JSONResponse(
        status_code=exc.status_code,
        content={'error': exc.detail}
    )


@app.get("/items/{item_id}/")
async def read_item(item_id: int):
    if item_id == 42:
        raise CustomException(detail="Item not found", status_code=404)
    return {"item_id": item_id}
