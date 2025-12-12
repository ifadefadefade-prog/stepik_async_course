from fastapi import FastAPI
from fastapi import Query
from typing import Optional

app = FastAPI()

@app.post('/calculate')

def calculate(num1: int, num2: int):
    return {f'results: {num1+num2}'}