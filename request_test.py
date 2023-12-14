import requests

API_URL = "https://api-inference.huggingface.co/models/nyanxyz/fill-in-the-blank-prompt-4-lr-20-e-5-ma-0"
headers = {"Authorization": "Bearer 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"}


def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()


output = query(
    {
        "system": """You will be provided with passage to use for creating 'fill in the blank' type question.
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
""",
        "inputs": "Cryptography, in digital age, has become a cornerstone of secure communication protocols. Fundamental to a wide array of services, it involves the conversion of readable data into unintelligible code to prevent unauthorised access. Cryptographers develop algorithms and systems to encrypt and decrypt data, reinforcing digital security by maintaining the confidentiality and integrity of information transferred over networks.",
    }
)

print(output)
