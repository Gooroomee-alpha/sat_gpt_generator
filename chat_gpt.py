import os
import openai
from langchain.agents import load_tools, initialize_agent, AgentType, create_csv_agent
from langchain.chains import llm, LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.llms import OpenAI

dotenv_file = os.path.join(os.path.dirname(__file__), ".env")
if os.path.isfile(dotenv_file):
    from dotenv import load_dotenv

    load_dotenv(dotenv_file)

openai.api_key = os.environ.get("OPENAI_API_KEY")


def generate_response(type: str, subject: str):
    passage = ""
    prompt = ""

    if type == "blank":
        passage_response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "You will be provided with subjects,"
                    + " and your task is to generate SAT passage",
                },
                {"role": "user", "content": prompt_passage(subject, 50)},
            ],
        )
        passage = passage_response["choices"][0]["message"]["content"]
        print(passage_response)
        print(passage)
        prompt = prompt_blank(passage)
    if type == "find_subject":
        prompt = prompt_find_subject(subject)

    problem_response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": "You will be provided with passage,"
                + " and your task is to generate SAT question and problems regarding to the passage.",
            },
            {"role": "user", "content": prompt},
        ],
    )

    return problem_response["choices"][0]["message"]["content"]


def prompt_passage(subject: str, words_count: int):
    return f"""
    ⌨️ 

    Step 0.
    Topic : {subject}

    Step 1.
    Please Generate new passage about {subject} from journals, research papers, etc
    The paragraph length must be about {words_count} words 
    The paragraph must be at most {words_count + 10} words
    The difficulty of the passage should be fit for SAT."""


def prompt_blank(passage: str):
    return f"""
⌨️ You will be provided with subjects, and your task is to generate SAT passage and problems.

Step 1.
Use the passage below.
{passage}

Step 2.
Generate a "Fill in the blank word finding exercise" problem from the passage.
Choose a keyword verb, noun, adverb, or adjective from the passage, and exchange with blank.
The blank word should be one word.
The answer must be inferable from the context.
The format of problem should be same as Example.

Step 3.
Return in the Format
Passage

Question

A. Choice 1
B. Choice 2
C. Choice 3
D. Choice 4

Answer

- Example 1.

When Mexican-American archaeologist Zelia Maria
Magdalena Nuttall published her 1886 research
paper on sculptures found at the ancient Indigenous
city of Teotihuacan in present-day Mexico, other
researchers readily _______ her work as ground
breaking; this recognition stemmed from her
convincing demonstration that the sculptures were
much older than had previously been thought.

Which choice completes the text with the most
logical and precise word or phrase?

A) acknowledged
B) ensured
C) denied
D) underestimated

- Example 2.

In the early 1800s, the Cherokee scholar Sequoyah
created the first script, or writing system, for an
Indigenous language in the United States. Because it
represented the sounds of spoken Cherokee so
accurately, his script was easy to learn and thus
quickly achieved _______ use: by 1830, over
90 percent of the Cherokee people could read and
write it.

Which choice completes the text with the most
logical and precise word or phrase?

A) widespread
B) careful
C) unintended
D) infrequent

- Example 3.

Like other tribal nations, the Muscogee (Creek)
Nation is self-governing; its National Council
generates laws regulating aspects of community life
such as land use and healthcare, while the principal
chief and cabinet officials _______ those laws by
devising policies and administering services in
accordance with them.
Which choice completes the text with the most
logical and precise word or phrase?
A) implement
B) presume
C) improvise
D) mimic
"""


def prompt_find_subject(subject: str):
    return f"""
⌨️ You will be provided with subjects, and your task is to generate SAT passage and problems.

Step 0.
Topic : {subject}

Step 1.
Please find a passage about {subject} from journals, research papers, etc from the internet.
The difficulty of the passage should be fit for SAT.
The paragraph length must be about 100 words

Step 2.
Generate a "Find subject" problem from the passage.
And print the whole passage.
The question should be "Which choice best states the main purpose of the
text?". or Which choice best describes the function of the
underlined sentence in the text as a whole? or Which choice best states the main purpose of the
text?. 
The problem is in multiple choices with A,B,C,D.
The answer must be inferable from the context.
The problems should be relative to the passage and question.
The format of problem should be same as Example.


Step 3.
Show what is the answer.

- Example 1.

In 2007, computer scientist Luis von Ahn was
working on converting printed books into a digital
format. He found that some words were distorted
enough that digital scanners couldn’t recognize
them, but most humans could easily read them.
Based on that finding, von Ahn invented a simple
security test to keep automated “bots” out of
websites. The first version of the reCAPTCHA test
asked users to type one known word and one of the
many words scanners couldn’t recognize. Correct
answers proved the users were humans and added
data to the book-digitizing project.
Which choice best states the main purpose of the
text?
A) To discuss von Ahn’s invention of reCAPTCHA
B) To explain how digital scanners work
C) To call attention to von Ahn’s book-digitizing
project
D) To indicate how popular reCAPTCHA is

- Example 2.

The following text is from Edith Wharton’s 1905
novel The House of Mirth. Lily Bart and a companion
are walking through a park.
Lily had no real intimacy with nature, but she
had a passion for the appropriate and could be
keenly sensitive to a scene which was the fitting
background of her own sensations. (underlined sentence) The
landscape outspread below her seemed an
enlargement of her present mood, and she found
something of herself in its calmness, its breadth,
its long free reaches. On the nearer slopes the
sugar-maples wavered like pyres of light; lower
down was a massing of grey orchards, and here
and there the lingering green of an oak-grove.
Which choice best describes the function of the
underlined sentence in the text as a whole?
A) It creates a detailed image of the physical setting
of the scene.
B) It establishes that a character is experiencing an
internal conflict.
C) It makes an assertion that the next sentence then
expands on.
D) It illustrates an idea that is introduced in the
previous sentence.

- Example 3.

The following text is from Maggie Pogue Johnson’s
1910 poem “Poet of Our Race.” In this poem, the
speaker is addressing Paul Laurence Dunbar, a Black
author.
Thou, with stroke of mighty pen,
Hast told of joy and mirth,
And read the hearts and souls of men
As cradled from their birth.
The language of the flowers,
Thou hast read them all,
And e’en the little brook
Responded to thy call.
Which choice best states the main purpose of the
text?
A) To praise a certain writer for being especially
perceptive regarding people and nature
B) To establish that a certain writer has read
extensively about a variety of topics
C) To call attention to a certain writer’s careful and
elaborately detailed writing process
D) To recount fond memories of an afternoon spent
in nature with a certain write
"""
