import json
import os
import random

import openai

from category_const import (
    science_categories,
    art_categories,
    history_categories,
    literature_categories,
    social_sciences_categories,
)

dotenv_file = os.path.join(os.path.dirname(__file__), ".env")
if os.path.isfile(dotenv_file):
    from dotenv import load_dotenv

    load_dotenv(dotenv_file)

openai.api_key = os.environ.get("OPENAI_API_KEY")


def generate_passage(subject: str):
    category = generate_category(subject)

    passage_prompt = prompt_generate_passage(category)
    passage_response = openai.ChatCompletion.create(
        model="gpt-4", messages=[{"role": "user", "content": passage_prompt}]
    )
    passage = passage_response["choices"][0]["message"]["content"]

    return passage


def generate_category(subject: str):
    categories = []
    if subject == "science":
        categories = science_categories
    elif subject == "art":
        categories = art_categories
    elif subject == "history":
        categories = history_categories
    elif subject == "literature":
        categories = literature_categories
    elif subject == "social_science":
        categories = social_sciences_categories
    else:
        categories = (
            science_categories
            + art_categories
            + history_categories
            + literature_categories
            + social_sciences_categories
        )
    return random.choice(categories)


def generate_problem(problem_type: str, passage: str):
    prompt = prompt_generate_question(problem_type, passage)
    sat_response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": prompt},
        ],
    )
    return sat_response["choices"][0]["message"]["content"]


def prompt_generate_question(problem_type: str, passage: str):
    prompt = ""
    if problem_type == "blank":
        prompt = prompt_blank(passage)
    if problem_type == "find_subject":
        prompt = prompt_find_subject(passage)
    if problem_type == "grammar":
        prompt = prompt_grammar(passage)
    if problem_type == "conjunction":
        prompt = prompt_conjunction(passage)

    return prompt


def prompt_generate_passage(subject: str):
    return f"""
    You will be provided with a topic, and your task is to generate SAT paragraph.
Show the result in the form of json format
Please Generate a new passage about the topic in 50~ 70 words from journals, research papers, etc..

- Example 1.

{
    json.dumps({
        "passage": '"In ancient Greece, an Epicurean was a follower of Epicurus, a philosopher whose beliefs revolved around the pursuit of pleasure. Epicurus defined pleasure as "the absence of pain in the body and of trouble in the seoul," positing that all life’s virtues derived from this absence."'   
    })
}

- Example 2.
{
    json.dumps({"passage": "The following text is from Maggie Pogue Johnson’s 1910 poem “Poet of Our Race.” In this poem, the speaker is addressing Paul Laurence Dunbar, a Black author. Thou, with stroke of mighty pen, Hast told of joy and mirth, And read the hearts and souls of men. As cradled from their birth. The language of the flowers, Thou hast read them all, And e’en the little brook Responded to thy call."})        
}


- Example 3.
{
    json.dumps({"passage": "Like other tribal nations, the Muscogee (Creek) Nation is self-governing; its National Council generates laws regulating aspects of community life such as land use and healthcare, while the principal chief and cabinet officials implement those laws by devising policies and administering services in accordance with them."})
}


Topic: {subject}"""


def prompt_blank(passage):
    return f"""
You will be provided with a passage, and your task is to generate SAT "fill in the blank" problem.
Just show the result of step3 and step4 in the form of json format
Step 1. Choose a keyword from the given passage.
Step 2. Find different words from the keyword, but the words must not be replacable with the keyword.
Step 3. Print the whole passage with the keyword replaced with blank.
Step 4. Show four answer options, one of them is exactly the keyword.

Note:
- The keyword should not be exposed to the passage.
- The answer must be inferable from the context.
- The format of output should be same as Example.

{
json.dumps({
  "passage":"When Mexican-American archaeologist Zelia Maria Magdalena Nuttall published her 1886 research paper on sculptures found at the ancient Indigenous city of Teotihuacan in present-day Mexico, other researchers readily _______ her work as ground breaking; this recognition stemmed from her convincing demonstration that the sculptures were much older than had previously been thought.",
  "problem":"Which choice completes the text with the most logical and precise word or phrase?",
  "choices":[
     "A) acknowledged",
     "B) ensured",
     "C) denied",
     "D) underestimated",
  ],
  "answer":"B) ensured"  
})
}

- Example 2.

{
json.dumps({
    "passage":"In the early 1800s, the Cherokee scholar Sequoyah created the first script, or writing system, for an Indigenous language in the United States. Because it represented the sounds of spoken Cherokee so accurately, his script was easy to learn and thus quickly achieved _______ use: by 1830, over 90 percent of the Cherokee people could read and write it.",
    "question":"Which choice completes the text with the most logical and precise word or phrase?",
    "choices":[
        "A) widespread",
        "B) careful",
        "C) unintended",
        "D) infrequent"
    ],
    "answer":"A) widespread"
})
}

- Example 3.

{
json.dumps({
    "passage":"Like other tribal nations, the Muscogee (Creek) Nation is self-governing; its National Council generates laws regulating aspects of community life such as land use and healthcare, while the principal chief and cabinet officials _______ those laws by devising policies and administering services in accordance with them.",
    "question":"Which choice completes the text with the most logical and precise word or phrase?",
    "choices":[
        "A) implement",
        "B) presume",
        "C) improvise",
        "D) mimic"
    ],
    "answer":"A) implement"
})
}

input :
{passage}
"""


def prompt_find_subject(passage: str):
    return f"""
You will be provided with a passage, and your task is to generate SAT "find the subject" problem.
Just show the result of step3 and step4 in the form of json format
Step 1. Find the subject of the given paragraph.
Step 2. Find different subjects from the paragraph's subject. The subjects are also about the paragraph but not the major subject.
Step 3. Print the whole passage.
Step 4. Show four answer options from Step2, one of them is exactly the subject.

Note:

- The answer must be inferable from the context.
- The format of output should be same as Example.
- Example 1.

{
    json.dumps({
        "passage":"In 2007, computer scientist Luis von Ahn was working on converting printed books into a digital format. He found that some words were distorted enough that digital scanners couldn’t recognize them, but most humans could easily read them. Based on that finding, von Ahn invented a simple security test to keep automated “bots” out of websites. The first version of the reCAPTCHA test asked users to type one known word and one of the many words scanners couldn’t recognize. Correct answers proved the users were humans and added data to the book-digitizing project.",
        "question":"Which choice best states the main purpose of the text?",
        "choices":[
            "A) To discuss von Ahn’s invention of reCAPTCHA",
            "B) To explain how digital scanners work",
            "C) To call attention to von Ahn’s book-digitizing project",
            "D) To indicate how popular reCAPTCHA is"
        ],
        "answer":"A) To discuss von Ahn’s invention of reCAPTCHA"  
    })
}


- Example 2.

{
    json.dumps({
        "passage":"The following text is from Edith Wharton’s 1905 novel The House of Mirth. Lily Bart and a companion are walking through a park. Lily had no real intimacy with nature, but she had a passion for the appropriate and could be keenly sensitive to a scene which was the fitting background of her own sensations. (underlined sentence) The landscape outspread below her seemed an enlargement of her present mood, and she found something of herself in its calmness, its breadth, its long free reaches. On the nearer slopes the sugar-maples wavered like pyres of light; lower down was a massing of grey orchards, and here and there the lingering green of an oak-grove.",
        "question":"Which choice best describes the function of the underlined sentence in the text as a whole?",
        "choices":[
            "A) It creates a detailed image of the physical setting of the scene.",
            "B) It establishes that a character is experiencing an internal conflict.",
            "C) It makes an assertion that the next sentence then expands on.",
            "D) It illustrates an idea that is introduced in the previous sentence."
        ],
        "answer":"D) It illustrates an idea that is introduced in the previous sentence."
    })
}

- Example 3.

{
    json.dumps({
        "passage": "The following text is from Maggie Pogue Johnson’s 1910 poem “Poet of Our Race.” In this poem, the speaker is addressing Paul Laurence Dunbar, a Black author. Thou, with stroke of mighty pen, Hast told of joy and mirth, And read the hearts and souls of men As cradled from their birth. The language of the flowers, Thou hast read them all, And e’en the little brook Responded to thy call.",
        "question": "Which choice best states the main purpose of the text?",
        "choices": [
            "A) To praise a certain writer for being especially perceptive regarding people and nature",
            "B) To establish that a certain writer has read extensively about a variety of topics",
            "C) To call attention to a certain writer’s careful and elaborately detailed writing process",
            "D) To recount fond memories of an afternoon spent in nature with a certain writer"
        ],

        "answer": "A) To praise a certain writer for being especially perceptive regarding people and nature"
    })
}

input : {passage}
"""


def prompt_grammar(passage: str):
    return f"""
You will be provided with a paragraph, and your task is to generate SAT grammar problem.
Just show the result of step3, step 4, and step5 in the form of json format

Step 1. Select a grammatically important keyword, for example, to-infinitive, plural, tense... etc
Step 2. Find some different words or different form of the keyword such as the past tense of the keyword.
Step 3. Print the whole passage with the chosen keyword replaced with blank.
Step 4. Show four answer options from Step2, one of them is exactly the subject.
Step 5.  Show the answer.

Note:

- The answer must be inferable from the context.
- The format of output should be same as Example.
- Example 1.

{
json.dumps({
    "passage":"In ancient Greece, an Epicurean was a follower of Epicurus, a philosopher whose beliefs revolved around the pursuit of pleasure. Epicurus defined pleasure as “the absence of pain in the body and of trouble in the _______ that all life’s virtues derived from this absence.",
    "question":"Which choice completes the text so that it conforms to the conventions of Standard English?",
    "choices":[
        "A) soul,” positing",
        "B) soul”: positing",
        "C) soul”; positing",
        "D) soul.” Positing",
    ],
    "answer":"A) soul,” positing"
})
}

- Example 2.
{
json.dumps({
    "passage":"British scientists James Watson and Francis Crick won the Nobel Prize in part for their 1953 paper announcing the double helix structure of DNA, but it is misleading to say that Watson and Crick discovered the double helix. _______ findings were based on a famous X-ray image of DNA fibers, “Photo 51,” developed by X-ray crystallographer Rosalind Franklin and her graduate student Raymond Gosling.",
    "question":"Which choice completes the text so that it conforms to the conventions of Standard English?",
    "choices":[
        "A) They’re",
        "B) It’s",
        "C) Their",
        "D) Its",
    ],
    "answer":"C) Their"

})
}

- Example 3.

{
json.dumps({
    "passage":"In 1637, the price of tulips skyrocketed in Amsterdam, with single bulbs of rare varieties selling for up to the equivalent of $200,000 in today’s US dollars. Some historians _______ that this “tulip mania” was the first historical instance of an asset bubble, which occurs when investors drive prices to highs not supported by actual demand.",
    "question":"Which choice completes the text so that it conforms to the conventions of Standard English?",
    "choices":[
        "A) claim",
        "B) claiming",
        "C) having claimed",
        "D) to claim",
    ],
    "answer":"B) claim"
})
}

input : {passage}
"""


def prompt_conjunction(passage: str):
    return f"""
You will be provided with a passage, and your task is to generate SAT "find the conjunction" problem.
Just show the result of step3, step 4, and step5 in the form of json format

Step 1. Select a conjunction from the given paragraph.
Step 2. Find different conjunctions from the chosen conjunction. The conjunctions are not the synonym from the chosen conjunction.
Step 3. Print the whole passage with the chosen conjunction replaced with blank.
Step 4. Show four answer options from Step2, one of them is exactly the subject.
Step 5. Show the answer.

Note:

- The answer must be inferable from the context.
- The format of output should be same as Example.
- Example 1.

{
json.dumps({
    "passage":"Although novels and poems are considered distinct literary forms, many authors have created hybrid works that incorporate elements of both. Bernardine Evaristo’s The Emperor's Babe, _______ is a verse novel, a book-length narrative complete with characters and a plot but conveyed in short, crisp lines of poetry rather than prose.",
    "question":"Which choice completes the text with the most logical transition?",
    "choices":[
        "A) by contrast,",
        "B) consequently,",
        "C) secondly,",
        "D) for example,",
    ],
    "answer":"D) for example,"
})
}


- Example 2.

{
json.dumps({
    "passage":"At two weeks old, the time their critical socialization period begins, wolves can smell but cannot yet see or hear. Domesticated dogs, _______ can see, hear, and smell by the end of two weeks. This relative lack of sensory input may help explain why wolves behave so differently around humans than dogs do: from a very young age, wolves are more wary and less exploratory.",
    "question":"Which choice completes the text with the most logical transition?",
    "choices":[
        "A) in other words,",
        "B) for instance,",
        "C) by contrast,",
        "D) accordingly",
    ],
    "answer":"C) by contrast,"
})
}

- Example 3.

{
json.dumps({
    "passage":"Researchers Helena Mihaljević-Brandt, Lucía Santamaría, and Marco Tullney report that while mathematicians may have traditionally worked alone, evidence points to a shift in the opposite direction. Increasingly mathematicians are choosing to collaborate with their peers—a trend illustrated by a rise in the number of mathematics publications credited to multiple authors.",
    "question":"Which choice completes the text with the most logical transition?",
    "choices":[
        "A) Similarly,",
        "B) For this reason,",
        "C) Furthermore,",
        "D) Increasingly,",
    ],
    "answer":"D) Increasingly,"
})
}

input:{passage}
"""
