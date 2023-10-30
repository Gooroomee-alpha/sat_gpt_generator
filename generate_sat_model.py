from pydantic import BaseModel


class GeneratePassageModel(BaseModel):
    subject: str


class GenerateProblemModel(BaseModel):
    passage: str
    problem_type: str
