import json
import random

from conjunction_vectorize import find_similar_conjunctions


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


def generate_conjunction(passage: str):
    conjunction_index = -1
    conjunction = ""
    for conjunction in conjunctions:
        conjunction_index = passage.lower().find(conjunction)
        if conjunction_index != -1:
            break

    if conjunction_index == -1:
        raise Exception("No conjunctions found")
    is_original_uppercase = passage[conjunction_index].isupper()
    original_conjunction = conjunction
    if is_original_uppercase:
        original_conjunction = conjunction.capitalize()

    passage = passage.replace(original_conjunction, "______", 1)
    question = "Which choice completes the text with the most logical transition?"
    similar_conjunctions = find_similar_conjunctions(conjunction)

    unique_selected_indices = random.sample(range(3, 20), 3)
    unique_selected_elements = [
        similar_conjunctions[i] for i in unique_selected_indices
    ]

    for i in range(3):
        if is_original_uppercase:
            unique_selected_elements[i] = unique_selected_elements[i].capitalize()

    choices = [original_conjunction] + unique_selected_elements
    random.shuffle(choices)
    answer = original_conjunction

    return {
        "passage": passage,
        "question": question,
        "choices": choices,
        "answer": answer,
    }

    # 주어진 텍스트
    # text = "In 2019, researcher Patricia Jurado Gonzalez and


print(
    json.dumps(
        generate_conjunction(
            "In 2019, researcher Patricia Jurado Gonzalez and food historian Nawal Nasrallah prepared a stew from a 4,000-year-old recipe found on a Mesopotamian clay tablet. When they tasted the dish, known as pašrūtum (“unwinding”), they found that it had a mild taste and inspired a sense of calm. Therefore, the researchers, knowing that dishes were sometimes named after their intended effects, theorized that the dish’s name, “unwinding,” referred to its function: to help ancient diners relax."
        )
    )
)
# conjunction_index = passage.lower().
