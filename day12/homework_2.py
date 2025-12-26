# main.py
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import random
from loguru import logger
import sys

app = FastAPI()


logger.remove()


logger.add(sys.stdout, serialize=True, level='INFO')
logger.add("app.log",
           serialize=True,
           rotation="10 MB",
           retention="7 days")


class CustomAppError(Exception):
    def __init__(self, message: str, code: int = 400):
        self.message = message
        self.code = code
        super().__init__(message)


@app.exception_handler(CustomAppError)
async def custom_app_error(request: Request, exc: CustomAppError):
    logger.bind(
        method=request.method,
        path=request.url.path,
        code=exc.code
    ).exception(exc.message)
    return JSONResponse(
        status_code=exc.code,
        content={
            "status_code": 500,
            "message": exc.message
        }
    )


@app.exception_handler(Exception)
async def global_exception(request: Request, exc: Exception):
    logger.bind(
        method=request.method,
        path=request.url.path
    ).exception(exc)
    return JSONResponse(
        status_code=500,
        content={
            "status_code": 500,
            "message": "Internal server error"
        }
    )


@app.get("/ok")
async def ok():
    return {"status": "ok"}


@app.get("/error")
async def error():
    raise CustomAppError("Демонстрационная ошибка", code=418)


@app.get("/boom")
async def boom():
    def div_by_zero():
        return 1 / 0

    def key_err():
        return {}["missing"]

    def value_err():
        return int("not-an-int")

    def runtime_err():
        raise RuntimeError("Случайная ошибка")

    random.choice([div_by_zero, key_err, value_err, runtime_err])()
    return {"status": "unreachable"}
