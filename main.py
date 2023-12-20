import json

from fastapi import FastAPI
import chat_gpt
from generate_passage import generate_sat_passage
from sat_model import conjunction, fill_in_the_blank, find_subject, grammar
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
    conjunctions = [
        "finally",
        "currently",
        "in comparison",
        "in fact",
        "second",
        "afterward",
        "subsequently",
        "by contrast",
        "specifically",
        "moreover",
        "furthermore",
        "therefore",
        "alternatively",
        "secondly",
        "thus",
        "in addition",
        "for this reason",
        "additionally",
        "as a result",
        "accordingly",
        "alternately",
        "regardless",
        "for instance",
        "indeed",
        "nevertheless",
        "to conclude",
        "increasingly",
        "consequently",
        "meanwhile",
        "actually",
        "similarly",
        "however",
        "for example",
        "likewise",
        "in other words",
        "still",
        "in contrast",
        "besides",
        "instead",
    ]

    passage = generate_sat_passage(data.subject)
    has_conjunction = any(f"{conj}," in passage.lower() for conj in conjunctions)
    response_json = {"passage": passage, "has_conjunction": has_conjunction}
    return response_json


@app.post("/sat/problem")
async def generate_problem(data: GenerateProblemModel):
    print(data)
    # try:
    if data.problem_type == "blank":
        response = json.dumps(fill_in_the_blank.generate_blank_problem(data.passage))
    elif data.problem_type == "conjunction":
        response = json.dumps(conjunction.generate_conjunction(data.passage))
    elif data.problem_type == "find_subject":
        response = json.dumps(find_subject.generate_find_subject_problem(data.passage))
    elif data.problem_type == "grammar":
        print("!")
        response = json.dumps(grammar.generate_grammar_problem(data.passage))
    else:
        response = chat_gpt.generate_problem(data.problem_type, data.passage)
    # except:
    #     response = chat_gpt.generate_problem(data.problem_type, data.passage)

    print(response)
    response_json = json.loads(
        response,
    )
    return response_json
