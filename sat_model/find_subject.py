import difflib
import json
import os
import random
import re

from dotenv import load_dotenv
from transformers import AutoModelForCausalLM, AutoTokenizer

load_dotenv()

# print(os.getenv('HF_TOKEN'))


def generate_find_subject_problem(passage: str):
    raw_problem = generate_subject_raw_problem(passage)
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


def generate_subject_raw_problem(passage: str):
    model_path = "nyanxyz/find-the-subject-p10-l10-e10-0"

    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForCausalLM.from_pretrained(
        model_path, device_map="auto", torch_dtype="auto"
    ).eval()

    system = prompt_system_find_subject()
    user = prompt_user_find_subject(passage)

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

    return json_data


def prompt_system_find_subject():
    prompt = """
You will be provided with passage to use for creating 'find main purpose' type question.
Your task is to generate 'find main purpose' SAT-style reading comprehension passage, question, and answer set using the provided passage by following these steps:

Step 1 - Identifying main purpose: Carefully read the passage to identify the main subject or theme. Consider what the author is primarily discussing or arguing about. This main subject should be the focal point of the passage.
Step 2 - Question Formation: Use the format 'Which choice best states the main purpose of the text?'
Step 3 - Providing ㅇistractors: Develop three distractors that are related to the passage's content but do not accurately represent its main purpose. These distractors should be plausible to ensure the question is challenging. Ensure these distractors vary in the aspect of the passage they refer to.
Step 4 - Output Format: Present the output in JSON format with the following structure:
"passage": The original passage.
"question": "Which choice best states the main purpose of the text?"
"answer": The main purpose identified in step 1. Answer should not exceed 15 words.
"distractors": The list of distractors developed in step 3, formatted as [{choice1}, {choice2}, {choice3}]. Each choice should not exceed 15 words.

Example:

Given this passage:
The following text is from Sarah Orne Jewett’s 1899 short story “Martha’s Lady.” Martha is employed by Miss Pyne as a maid. <quote> Miss Pyne sat by the window watching, in her best dress, looking stately and calm; she seldom went out now, and it was almost time for the carriage. Martha was just coming in from the garden with the strawberries, and with more flowers in her apron. It was a bright cool evening in June, the golden robins sang in the elms, and the sun was going down behind the apple-trees at the foot of the garden. The beautiful old house stood wide open to the long-expected guest. </quote>

The response should be:

{
  "passage": "The following text is from Sarah Orne Jewett’s 1899 short story “Martha’s Lady.” Martha is employed by Miss Pyne as a maid. <quote> Miss Pyne sat by the window watching, in her best dress, looking stately and calm; she seldom went out now, and it was almost time for the carriage. Martha was just coming in from the garden with the strawberries, and with more flowers in her apron. It was a bright cool evening in June, the golden robins sang in the elms, and the sun was going down behind the apple-trees at the foot of the garden. The beautiful old house stood wide open to the long-expected guest. </quote>",
  "question": "Which choice best states the main purpose of the text?",
  "answer": "To depict the setting as the characters await a visitor’s arrival",
  "distractors": ["To convey the worries brought about by a new guest", "To describe how the characters have changed over time", "To contrast the activity indoors with the stillness outside"]
}
"""

    return prompt


def prompt_user_find_subject(passage):
    return passage


print(
    json.dumps(
        generate_find_subject_problem(
            "Musician Joni Mitchell, who is also a painter, uses images she creates for her album covers to emphasize ideas expressed in her music. For the cover of her album <em>Turbulent Indigo</em> (1994), Mitchell painted a striking self-portrait that closely resembles Vincent van Gogh’s <em>Self-Portrait with Bandaged Ear</em> (1889). The image calls attention to the album’s title song, in which Mitchell sings about the legacy of the postimpressionist painter. In that song, Mitchell also hints that she feels a strong artistic connection to Van Gogh—an idea that is reinforced by her imagery on the cover."
        )
    )
)
