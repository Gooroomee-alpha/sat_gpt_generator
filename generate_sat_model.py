from pydantic import BaseModel


class GenerateSatModel(BaseModel):
    subject: str
    problem_type: str
