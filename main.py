import json

from fastapi import FastAPI
import chat_gpt
from sat_model import conjunction, fill_in_the_blank
from generate_sat_model import GeneratePassageModel, GenerateProblemModel

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.post("/sat/passage")
async def generate_passage(data: GeneratePassageModel):
    response = chat_gpt.generate_passage(data.subject)
    response_json = json.loads(
        response,
    )
    return response_json


@app.post("/sat/problem")
async def generate_problem(data: GenerateProblemModel):
    if data.problem_type == "blank":
        response = json.dumps(fill_in_the_blank.generate_blank_problem(data.passage))
    elif data.problem_type == "conjunction":
        response = json.dumps(conjunction.generate_conjunction(data.passage))
    else:
        response = chat_gpt.generate_problem(data.problem_type, data.passage)
    response_json = json.loads(
        response,
    )
    return response_json
