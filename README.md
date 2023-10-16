# sat_gpt_generator

POST `/sat/problem`
request body
```
{
  "problem_type": "blank" | "find_subject" | "grammar" | "conjunction",
  "subject": can be any string
}
```

`poetry install` 로 python package들을 설치해주세요

.env 파일을 project root에 만들고 OPENAI_API_KEY={OPEN_API_KEY}를 세팅해주세요

`uvicorn main:app --reload`을 통해서 로컬에 서버를 띄워주세요

POST http://127.0.0.1:8000/sat/problem/ 을 통해서 generate되는 과정을 볼 수 있습니다.
