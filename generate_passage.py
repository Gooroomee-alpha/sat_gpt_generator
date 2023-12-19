import csv
import random


def generate_sat_passage(subject: str):
    subjects = ["science", "art", "literature", "social_science"]

    if subject in subjects:
        target = [subject]
    else:
        target = subjects

    passages = []

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

    count = 0
    for subject in target:
        with open(f"data/{subject}.csv", newline="") as file:
            reader = csv.reader(file)
            next(reader)

            for row in reader:
                passages.append(row[1])
                if any(f"{conj}," in row[1].lower() for conj in conjunctions):
                    count += 1

    return random.choice(passages).replace('"', "'")
