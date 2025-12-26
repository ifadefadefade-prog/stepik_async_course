from fastapi import FastAPI, Form


app = FastAPI()


@app.post('/submit/')
async def submit_form(username: str Form(),
                      password: str = Form()):
    return {"username": username, "password_length": len(password)} 


@app.post("/register/")
async def register_user(
    username: str = Form(),
    email: str = Form(),
    age: int = Form(),
    password: str = Form()
):
    return {
        "username": username, 
        "email": email, 
        "age": age, 
        "password_length": len(password)
    }