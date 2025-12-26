from fastapi import FastAPI, Response


app = FastAPI()


@app.get('/')
async def root():
    data = 'HELLOHELLOHELLOHELLO'
    return Response(content=data, media_type="text/plain",
                    headers={"Secret-Code": "123459"})
