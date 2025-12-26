import logging
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse


logging.basicConfig(level=logging.INFO)


app = FastAPI()


class CustomExcetion(HTTPException):
    def __init__(self, detail: str, status_code: int = 400,):
        super().__init__(status_code, detail)


@app.exception_handler(CustomExcetion)
async def custom_exception_handler(request, exc: CustomExcetion):
    logging.error(f'Ошибка: {exc.detail}, Статус: {exc.status_code}')
    return JSONResponse(content={'error': exc.detail,
                                 'status_code': exc.status_code})


@app.get('/items/{item_id}')
async def read_item(item_id: int):
    if item_id == 42:
        raise CustomExcetion(detail='item not found',
                             status_code=404)
    return {'item_id': item_id}
