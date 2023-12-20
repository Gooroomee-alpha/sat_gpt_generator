import difflib
import json
import os
import random
import re

from dotenv import load_dotenv
from transformers import AutoModelForCausalLM, AutoTokenizer

load_dotenv()

# print(os.getenv('HF_TOKEN'))


def generate_grammar_problem(passage: str):
    raw_problem = generate_grammar_raw_problem(passage)
    print(raw_problem)
    raw_problem_json = json.loads(
        raw_problem,
    )
    question = raw_problem_json["question"]
    distractors = raw_problem_json["distractors"]
    answer = raw_problem_json["answer"]

    choices = [answer] + distractors
    random.shuffle(choices)

    return {
        "passage": passage,
        "question": question,
        "choices": choices,
        "answer": answer,
    }


def generate_grammar_raw_problem(passage: str):
    model_path = "Formid322/09lo-xqb3-fi6r-0"

    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForCausalLM.from_pretrained(
        model_path, device_map="auto", torch_dtype="auto"
    ).eval()

    system = prompt_system_grammar()
    user = prompt_user_grammar(passage)

    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": user},
    ]

    input_ids = tokenizer.apply_chat_template(
        conversation=messages,
        tokenize=True,
        add_generation_prompt=True,
        return_tensors="pt",
    )
    output_ids = model.generate(
        input_ids.to("cuda"), max_length=1300, temperature=0.0, do_sample=False
    )
    response = tokenizer.decode(
        output_ids[0][input_ids.shape[1] :], skip_special_tokens=True
    )

    pattern = r"\{.*\}"
    match = re.search(pattern, response, re.DOTALL)

    if match:
        json_data = match.group()
        # 문자열을 JSON 객체로 변환
    else:
        raise ValueError("Wrong Output")

    return (
        json_data.replace('"[', "[")
        .replace(']"', "]")
        .replace(
            """,
}""",
            """
}""",
        )
    )


def prompt_system_grammar():
    prompt = """
You will be provided with passages to use for creating 'grammar' type questions. Your task is to generate questions focusing on standard English punctuation, verb tenses, and forms by following these steps:

Step 1 - Identifying the key element:
Carefully read the passage and identify a key usage of standard English punctuation, verb tenses, or forms. Replace this key element with a blank, indicated as ________. The position of the blank should be such that its removal significantly impacts the sentence's grammatical integrity. When the blank is replaced with the correct answer, it must exactly match the original text.

Step 2 - Question Formation:
Formulate a question using the following format:
“Which choice completes the text so that it conforms to the conventions of Standard English?”

Step 3 - Creating Distractors:

Develop three distractors using different tenses of the correct verb as distractors, such as past or present continuous forms. For verbs, switch between active and passive voice to create plausible, yet incorrect, choices.

Step 4 - Output Format: Present the output in JSON format with the following structure:
"passage": The original passage with the key word or sentence replaced by a blank indicated as ________. 
"question": The selected question format from step 2.
"answer": The correct answer identified in step 1.
"distractors": The list of distractors developed in step 3, formatted as [{choice1}, {choice2}, {choice3}]. Each choice should not exceed 15 words.

Example:

  Given this passage:
  "The Progressive Era in the United States witnessed the rise of numerous Black women’s clubs, local organizations that advocated for racial and gender equality. Among the clubs’ leaders was Josephine St. Pierre Ruffin, founder of the Women’s Era Club of Boston."

  The response should be:

  {
    "passage": "The Progressive Era in the United States witnessed the rise of numerous Black women’s clubs, local organizations that advocated for racial and gender equality. Among the clubs’ leaders ______ Josephine St. Pierre Ruffin, founder of the Women’s Era Club of Boston.",
    "question": "Which choice completes the text so that it conforms to the conventions of Standard English?",
    "answer": "was",
    "distractors": ["were", "are", "have been"]
  }
"""

    return prompt


def prompt_user_grammar(passage):
    return passage


print(
    json.dumps(
        generate_grammar_problem(
            "In 1908, the first edition of a now-classic novel was published, captivating readers with its rich narrative. This paperback, spanning 119 pages, has since become a treasured piece in literary collections. Over a century later, it remains a testament to the enduring power of storytelling, as acknowledged by Goodreads, Inc. in 2023."
        )
    )
)
