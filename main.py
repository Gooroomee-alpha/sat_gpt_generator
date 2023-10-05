from fastapi import FastAPI
import chat_gpt

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.post("/sat/problem")
async def sat_problem():
    chat_gpt.generate_response()
