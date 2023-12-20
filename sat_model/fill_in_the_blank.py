import difflib
import json
import os
import random
import re

from dotenv import load_dotenv
from transformers import AutoModelForCausalLM, AutoTokenizer

load_dotenv()

# print(os.getenv('HF_TOKEN'))


def generate_blank_problem(passage: str):
    raw_problem = generate_blank_raw_problem(passage)
    print(raw_problem)

    raw_problem_json = json.loads(
        raw_problem,
    )

    original_passage = passage
    blanked_passage = raw_problem_json["passage"].replace("’", "'")
    question = raw_problem_json["question"]
    distractors = raw_problem_json["distractors"]
    answer = raw_problem_json["answer"]
    print(raw_problem_json)

    blanked_phrase = get_blanked_phrase(original_passage, blanked_passage)
    if blanked_phrase is None:
        blanked_phrase = answer
        blanked_passage = blanked_passage.replace(answer, "_______", 1)
    print(blanked_phrase)

    if blanked_phrase in distractors:
        # random from 0 to 3
        raise ValueError("answer is already on distractors")

    choices = [blanked_phrase] + distractors

    distractors_length = len(distractors[0].split(" "))
    blanked_phrase_length = len(blanked_phrase.split(" "))
    if blanked_phrase_length - distractors_length >= 7:
        raise ValueError("Something went wrong")
    random.shuffle(choices)

    print(
        {
            "passage": blanked_passage,
            "question": question,
            "choices": choices,
            "answer": blanked_phrase,
        }
    )

    return {
        "passage": blanked_passage,
        "question": question,
        "choices": choices,
        "answer": blanked_phrase,
    }


def get_blanked_phrase(original_passage: str, blanked_passage: str):
    original_passage = original_passage.split()
    blanked_passage = blanked_passage.split()

    start = -1
    end = -1

    # 빈칸의 시작 위치 찾기
    pattern = r"_{3,}"  # 3개 이상의 연속된 밑줄 찾기
    for i, word in enumerate(blanked_passage):
        if re.match(pattern, word):
            start = i
            break

    if start == -1:
        return None

    # 빈칸 다음에 오는 단어들 (end_word)
    end_words = blanked_passage[start + 1 :]
    print(end_words)
    # 빈칸이 문장의 마지막에 있는 경우
    if not end_words:
        return " ".join(original_passage[start:])

    # end_word와 일치하는 단어를 original_passage에서 찾기
    for i in range(len(original_passage)):
        if all(
            original_passage[i + idx] == end_words[idx] for idx in range(len(end_words))
        ):
            end = i
            break

    # 빈칸으로 대체된 부분 반환
    return " ".join(original_passage[start:end])


def generate_blank_raw_problem(passage: str):
    model_path = "nyanxyz/fill-in-the-blank-p7-l20-e10-0"

    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForCausalLM.from_pretrained(
        model_path, device_map="auto", torch_dtype="auto"
    ).eval()

    system = prompt_system_blank()
    user = prompt_user_blank(passage)

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
    print(response)
    print("!!")
    pattern = r"\{.*\}"
    match = re.search(pattern, response, re.DOTALL)

    if match:
        json_data = match.group()
        # 문자열을 JSON 객체로 변환
    else:
        raise ValueError("Wrong Output")

    return json_data


#     return """{
#   "passage": "When Mexican-American archaeologist Zelia Maria Magdalena Nuttall published her 1886 research paper on sculptures found at the ancient Indigenous city of Teotihuacan in present-day Mexico, other researchers readily acknowledged her work as ground breaking; this recognition stemmed from her _______ demonstration that the sculptures were much older than had previously been thought.",
#   "question": "Which choice completes the text with the most logical and precise word or phrase?",
#   "choices": "A) compelling B) convincing C) thorough D) cautious",
#   "answer": "convincing"
# } """


def prompt_system_blank():
    prompt = """
You will be provided with passage to use for creating 'fill in the blank' type question.
Your task is to generate 'fill in the blank' SAT-style reading comprehension passage, question, and answer set using the provided passage by following these steps:

Step 1 - Blank Setting: Carefully read the passage and select a key word or sentence that plays a significant role in the context. This word or sentence should be pivotal to the passage's meaning and its removal would significantly impact the flow of the text.
Step 2 - Question Formation: Choose one of the following question formats to use:
'Which choice completes the text with the most logical and precise word or phrase?'
'Which choice most logically completes the text?'
Step 3 - Creating Distractors: Develop three distractors that are contextually or semantically similar to the selected word or sentence from Step 1, but differ slightly. These choices should be plausible within the context yet not the correct answer. Ensure these choices vary in vocabulary complexity.
Step 4 - Output Format: Present the output in JSON format with the following structure:
"passage": The original passage with the key word or sentence replaced by a blank indicated as ________.
"question": The selected question format from step 2.
"answer": The correct answer identified in step 1.
"distractors": The list of distractors developed in step 3, formatted as [{choice1}, {choice2}, {choice3}]. Each choice should not exceed 15 words.

Example:

Given this passage:
"In the early 1800s, the Cherokee scholar Sequoyah created the first script, or writing system, for an Indigenous language in the United States. Because it represented the sounds of spoken Cherokee so accurately, his script was easy to learn and thus quickly achieved widespread use: by 1830, over 90 percent of the Cherokee people could read and write it."

The response should be:

{
  "passage": "In the early 1800s, the Cherokee scholar Sequoyah created the first script, or writing system, for an Indigenous language in the United States. Because it represented the sounds of spoken Cherokee so accurately, his script was easy to learn and thus quickly achieved ________ use: by 1830, over 90 percent of the Cherokee people could read and write it.",
  "question": "Which choice completes the text with the most logical and precise word or phrase?",
  "answer": "widespread",
  "distractors": ["careful", "unintended", "infrequent"]
}
"""

    return prompt


def prompt_user_blank(passage):
    return passage


print(
    # json.dumps(
    generate_blank_problem(
        "The telegraph, a revolutionary communication technology, emerged from the concept of transmitting electric signals across wires, an idea dating back to the early 1700s. Samuel Morse, a New York University professor, significantly advanced this technology by developing Morse Code in 1835 and securing political and financial support for his telegraph system. By 1844, Morse had successfully sent the first message from Washington, D.C., to Baltimore. The telegraph's impact was  profound, shrinking the world by allowing messages to be sent across continents in minutes, reshaping business, politics, and society. Despite initial skepticism and challenges, the telegraph paved the way for future communication innovations, ultimately being overshadowed by the telephone and radio."
    )
    # )
)
