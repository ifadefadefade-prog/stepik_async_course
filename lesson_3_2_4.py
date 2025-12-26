from fastapi import FastAPI, Response


app = FastAPI()


@app.get('/set-cookie')
def set_cookie(response: Response):
    response.set_cookie(key='user_id', value='12345',
                        max_age=3600, httponly=False)
    return {"message": "Cookie has been set!"}
