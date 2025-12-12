from fastapi import FastAPI
from logger import logger

app = FastAPI()


@app.get('/')
def read_root():
    logger.info("Hanling request to root endpoint")
    return {"msg": "Hellow world"}
