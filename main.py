import json

from fastapi import FastAPI
import chat_gpt
from generate_sat_model import GenerateSatModel

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.get("/sat/problem")
async def sat_problem(subject: str, problem_type: str):
    response = chat_gpt.generate_response(problem_type, subject)
    response_json = json.loads(
        response,
    )
    return response_json
