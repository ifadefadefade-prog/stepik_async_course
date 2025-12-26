from fastapi import FastAPI, HTTPException

app = FastAPI()


class CustomException(HTTPException):
    def __init__(self, detail: str, status_code: int = 400) -> None:
        super().__init__(status_code=status_code, detail=detail)


@app.get('/items/{item_id}')
async def read_item(item_id: int):
    if item_id == 42:
        raise CustomException(detail='pizda', status_code=404)
    return {'item_id': item_id}
