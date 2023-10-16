import os
import openai


dotenv_file = os.path.join(os.path.dirname(__file__), ".env")
if os.path.isfile(dotenv_file):
    from dotenv import load_dotenv

    load_dotenv(dotenv_file)

openai.api_key = os.environ.get("OPENAI_API_KEY")


def generate_response(type: str, subject: str):
    prompt = ""

    if type == "blank":
        prompt = prompt_blank(subject)
    if type == "find_subject":
        prompt = prompt_find_subject(subject)
    if type == "grammar":
        prompt = prompt_grammar(subject)
    if type == "conjunction":
        prompt = prompt_conjunction(subject)

    sat_response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": "You will be provided with subjects, and your task is to generate SAT passage and problems.",
            },
            {"role": "user", "content": prompt},
        ],
    )

    return sat_response["choices"][0]["message"]["content"]


def prompt_blank(subject: str):
    return f"""
⌨️ You will be provided with subjects, and your task is to generate SAT passage and problems.

Step 0.
Topic : {subject}

Step 1.
Please Generate new passage about subject from journals, research papers, etc
The paragraph length must be about 50 words

Step 2.
Generate a "Fill in the blank word finding exercise" problem from the passage.
Choose a keyword verb, noun, adverb, or adjective from the passage, and exchange with blank.
And print the whole passage with blank.
The blank word should be one word.
The answer must be inferable from the context.
The format of problem should be same as Example.

Step 3.
Show what is the answer.

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

Topic : `Ancient earth`

Step 1.
Please Generate new passage about subject from journals, research papers, etc
The paragraph length must be about 100 words

Step 2.
Generate a problem from the passage.
Problem type must be similar with examples.
The answer must be inferable from the context.
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


def prompt_grammar(subject: str):
    return f"""
⌨️ You will be provided with subjects, and your task is to generate SAT passage and problems.

Topic : {subject}

Step 1.
Please Generate new passage about subject from journals, research papers, etc
The paragraph length must be about 50 words

Step 2.
Generate a grammar exercise from the passage.
First, choose a verb from the passage and make options with the verb's other tense and form so that there exists only one grammatically correct answer.
Second, Replace the chosen verb with blank.
Last, Print the whole passage with blank.

The chosen verb tense should not be trivial.
Problem type must be similar with examples.
The answer must be inferable from the context.
The format of problem should be same as Example.

Step 3.
Show what is the answer.

- Example 1.

In ancient Greece, an Epicurean was a follower of
Epicurus, a philosopher whose beliefs revolved
around the pursuit of pleasure. Epicurus defined
pleasure as “the absence of pain in the body and of
trouble in the _______ that all life’s virtues derived
from this absence.
Which choice completes the text so that it conforms
to the conventions of Standard English?
A) soul,” positing
B) soul”: positing
C) soul”; positing
D) soul.” Positing

- Example 2.

British scientists James Watson and Francis Crick
won the Nobel Prize in part for their 1953 paper
announcing the double helix structure of DNA, but it
is misleading to say that Watson and Crick
discovered the double helix. _______ findings were
based on a famous X-ray image of DNA fibers,
“Photo 51,” developed by X-ray crystallographer
Rosalind Franklin and her graduate student
Raymond Gosling.
Which choice completes the text so that it conforms
to the conventions of Standard English?
A) They’re
B) It’s
C) Their
D) Its

- Example 3.

In 1637, the price of tulips skyrocketed in
Amsterdam, with single bulbs of rare varieties
selling for up to the equivalent of $200,000 in today’s
US dollars. Some historians _______ that this “tulip
mania” was the first historical instance of an asset
bubble, which occurs when investors drive prices to
highs not supported by actual demand.
Which choice completes the text so that it conforms
to the conventions of Standard English?
A) claiming
B) claim
C) having claimed
D) to claim
"""


def prompt_conjunction(subject: str):
    return f"""
⌨️ You will be provided with subjects, and your task is to generate SAT passage and problems.

Topic : {subject}

Step 1.
Please Generate new passage about subject from journals, research papers, etc
The paragraph length must be about 50 words
Show the whole paragraph

Step 2.
Generate a "Find the correct conjunctions" exercise from the passage.
First, choose a conjunction from the passage and make options with other conjunctions so that there exists only one correct answer.
Second, Replace the chosen conjunction with blank.
Last, Print the whole passage with blank.

Problem type must be similar with examples.
The answer must be inferable from the context.
The format of problem should be same as Example.

Step 3.
Show what is the answer.

- Example 1.

Although novels and poems are considered distinct
literary forms, many authors have created hybrid
works that incorporate elements of both. Bernardine
Evaristo’s The Emperor's Babe, _______ is a verse
novel, a book-length narrative complete with
characters and a plot but conveyed in short, crisp
lines of poetry rather than prose.
Which choice completes the text with the most
logical transition?
A) by contrast,
B) consequently,
C) secondly,
D) for example,

- Example 2.

At two weeks old, the time their critical socialization
period begins, wolves can smell but cannot yet see or
hear. Domesticated dogs, _______ can see, hear, and
smell by the end of two weeks. This relative lack of
sensory input may help explain why wolves behave
so differently around humans than dogs do: from a
very young age, wolves are more wary and less
exploratory.
Which choice completes the text with the most
logical transition?
A) in other words,
B) for instance,
C) by contrast,
D) accordingly

- Example 3.

Researchers Helena Mihaljević-Brandt, Lucía
Santamaría, and Marco Tullney report that while
mathematicians may have traditionally worked
alone, evidence points to a shift in the opposite
direction. _______ mathematicians are choosing to
collaborate with their peers—a trend illustrated by a
rise in the number of mathematics publications
credited to multiple authors.
Which choice completes the text with the most
logical transition?
A) Similarly,
B) For this reason,
C) Furthermore,
D) Increasingly,
"""
