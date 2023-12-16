# 임베딩을 생성하는 함수 수정
from pydantic_settings import BaseSettings
from transformers import AutoTokenizer, AutoModel
import torch
from sklearn.metrics.pairwise import cosine_similarity
import chromadb

model_path = "roberta-base"

tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModel.from_pretrained(model_path)
print(type(model))

print(tokenizer.vocab_size)


# # 임베딩을 생성하는 함수 수정
# def get_embedding(inputs):
#     inputs = tokenizer(inputs, return_tensors="pt")
#     outputs = model.forward(inputs)
#     return outputs.last_hidden_state.mean(dim=1).detach().numpy()[0].tolist()  # 리스트로 변환

class EmbeddingModel:
    def __init__(self, model, tokenizer):
        self.model = model
        self.tokenizer = tokenizer

    def __call__(self, input):
        inputs = tokenizer(input, return_tensors="pt")
        outputs = model(**inputs)
        return outputs.last_hidden_state.mean(dim=1).detach().numpy()[0].tolist()


# Initialize the embedding model
embedding_model = EmbeddingModel(model, tokenizer)

client = chromadb.PersistentClient(path="./conjunctions.db")
db = client.get_or_create_collection(
    name="conjunctions", embedding_function=embedding_model
)

# 접속사 목록
conjunction_list = [
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


# 각 접속사에 대한 임베딩 생성 및 저장
# for conj in conjunction_list:
#     embedding = embedding_model(conj)
#     db.add(documents=[conj], ids=[conj], embeddings=[embedding])  # 임베딩을 명시적으로 제공

# 주어진 단어에 대해 가장 유사한 접속사 찾기
def find_similar_conjunctions(word):
    query_embedding = embedding_model(word)
    results = db.query(query_embeddings=query_embedding, n_results=20)
    return (
        results["documents"][0] if results["documents"] else "No similar word found"
    )


# 주어진 단어
word = "In contrast"

# 가장 유사한 접속사 찾기
most_similar_conj = find_similar_conjunctions(word)
print("Most similar conjunction to", word, ":", most_similar_conj)
