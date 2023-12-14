import difflib
import json
import random
import re

from transformers import AutoModelForCausalLM, AutoTokenizer


# {
#   "passage": "When Mexican-American archaeologist Zelia Maria Magdalena Nuttall published her 1886 research paper on sculptures found at the ancient Indigenous city of Teotihuacan in present-day Mexico, other researchers readily acknowledged her work as ground breaking; this recognition stemmed from her _______ demonstration that the sculptures were much older than had previously been thought.",
#   "question": "Which choice completes the text with the most logical and precise word or phrase?",
#   "choices": "A) compelling B) convincing C) thorough D) cautious",
#   "answer": "convincing"
# }
def generate_blank_problem(passage: str):
    raw_problem = generate_blank_raw_problem(passage)
    raw_problem_json = json.loads(
        raw_problem,
    )
    original_passage = passage
    blanked_passage = raw_problem_json["passage"]
    question = raw_problem_json["question"]
    choices = raw_problem_json["choices"]

    blanked_phrase = get_blanked_phrase(original_passage, blanked_passage)

    # 결과 리스트 초기화
    pattern = r"A\)(.+?)B\)(.+?)C\)(.+?)D\)(.+)"

    # 정규식 검색
    matches = re.search(pattern, choices)

    # 결과 추출
    if matches:
        choices = list(map(lambda x: x.strip(), (matches.groups())))
    else:
        raise Exception("No matches")

    if blanked_phrase not in choices:
        # random from 0 to 3
        random_index = random.randint(0, 3)
        choices[random_index] = blanked_phrase

    return {
        "passage": blanked_passage,
        "question": question,
        "choices": choices,
        "answer": blanked_phrase,
    }


def get_blanked_phrase(original_passage: str, blanked_passage: str):
    original_passage = original_passage.split()
    blanked_passage = blanked_passage.split()

    s = difflib.SequenceMatcher(None, original_passage, blanked_passage)
    blocks = s.get_matching_blocks()

    # 빈칸으로 대체된 부분 출력
    for i in range(len(blocks) - 1):
        a_start = blocks[i].a + blocks[i].size
        a_end = blocks[i + 1].a

        if a_end > a_start:
            missing = original_passage[a_start:a_end]
            return " ".join(missing)


def generate_blank_raw_problem(passage: str):
    model_path = "nyanxyz/fill-in-the-blank-lr-2-e-5-0"

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
        input_ids.to("cuda"), max_length=1024, temperature=0.0, do_sample=False
    )
    response = tokenizer.decode(
        output_ids[0][input_ids.shape[1] :], skip_special_tokens=True
    )

    print(response)
    return response


#     return """{
#   "passage": "When Mexican-American archaeologist Zelia Maria Magdalena Nuttall published her 1886 research paper on sculptures found at the ancient Indigenous city of Teotihuacan in present-day Mexico, other researchers readily acknowledged her work as ground breaking; this recognition stemmed from her _______ demonstration that the sculptures were much older than had previously been thought.",
#   "question": "Which choice completes the text with the most logical and precise word or phrase?",
#   "choices": "A) compelling B) convincing C) thorough D) cautious",
#   "answer": "convincing"
# } """


def prompt_system_blank():
    prompt = """You will be provided with passage to use for creating 'fill in the blank' type question.
Your task is to create 'fill in the blank' questions using the provided passage by following these steps:

Step 1 - Blank Setting: Carefully read the passage and select a key word or sentence that plays a significant role in the context. This word or sentence should be pivotal to the passage's meaning and its removal would significantly impact the flow of the text.
Step 2 - Question Formation: Choose one of the following question formats to use:
'Which choice completes the text with the most logical and precise word or phrase?'
'Which choice most logically completes the text?'
Step 3 - Creating Choices: Develop three incorrect choices that are contextually or semantically similar to the selected word or sentence from Step 1, but differ slightly. These choices should be plausible within the context yet not the correct answer. Ensure these choices vary in vocabulary complexity.
Step 4 - Output Format: Present the output in JSON format with the following structure:
"passage": The original passage with the key word or sentence replaced by a blank indicated as ________.
"question": The selected question format from step 2.
"choices": The list of choices developed in step 3, formatted as "A) {choice1} B) {choice2} C) {choice3} D) {choice4}".
"answer": The correct answer, corresponding to one of the choices A, B, C, or D, as identified in step 1.

Example:

Given this passage:
"In the early 1800s, the Cherokee scholar Sequoyah created the first script, or writing system, for an Indigenous language in the United States. Because it represented the sounds of spoken Cherokee so accurately, his script was easy to learn and thus quickly achieved widespread use: by 1830, over 90 percent of the Cherokee people could read and write it."

The response should be:

{
  "passage": "In the early 1800s, the Cherokee scholar Sequoyah created the first script, or writing system, for an Indigenous language in the United States. Because it represented the sounds of spoken Cherokee so accurately, his script was easy to learn and thus quickly achieved ________ use: by 1830, over 90 percent of the Cherokee people could read and write it.",
  "question": "Which choice completes the text with the most logical and precise word or phrase?",
  "choices": "A) widespread B) careful C) unintended D) infrequent",
  "answer": "widespread"
}
"""

    return prompt


def prompt_user_blank(passage):
    return passage


print(
    generate_blank_problem(
        "When Mexican-American archaeologist Zelia Maria Magdalena Nuttall published her 1886 research paper on sculptures found at the ancient Indigenous city of Teotihuacan in present-day Mexico, other researchers readily acknowledged her work as ground breaking; this recognition stemmed from her convincing demonstration that the sculptures were much older than had previously been thought."
    )
)
