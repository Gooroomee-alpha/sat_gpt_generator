import os
import openai
from langchain.agents import load_tools, initialize_agent, AgentType, create_csv_agent
from langchain.chains import llm
from langchain.llms import OpenAI

dotenv_file = os.path.join(os.path.dirname(__file__), ".env")
if os.path.isfile(dotenv_file):
    from dotenv import load_dotenv

    load_dotenv(dotenv_file)

openai.api_key = os.environ.get("OPENAI_API_KEY")


def generate_response():
    # print current working directory
    agent = create_csv_agent(
        OpenAI(model_name="gpt-4", temperature=0),
        ["./sample/SAT_1_Reading Passages.csv", "./sample/SAT_1_Reading Questions.csv"],
        verbose=True,
    )

    agent.run(
        "The given csv file is a example SAT problems."
        + " Generate a new SAT Reading Problem including passage and questions."
        + "The question should be multiple choice and the answer should be one of the choices."
        + "The passage should be at least 100 words long."
        + "The question should be related to the passage."
    )
