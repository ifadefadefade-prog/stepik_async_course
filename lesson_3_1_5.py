from fastapi import FastAPI, Query


app = FastAPI()


@app.get('/items/')
async def read_item(
    skip: int = Query(0, alias='start', ge=0),
    limit: int = Query(10, le=10)   
):
    return 