import config
import openai
from Prompts import *

open_ai_key = config.OPENAI_API_KEY
openai.api_key = open_ai_key
model = 'gpt-4o'

def chatgpt_generate(query):

    messages = [{
        "role": "system",
        "content": "You are a helpful assistant."
    },{
        "role": "user",
        "content": query
    }]

    response = openai.ChatCompletion.create(model=model, messages=messages)
    answer = response['choices'][0]['message']['content']
    return answer

def query_to_prompt(natural_query):
    api_query = f"""각 기능 별 프롬프트 명이 아래와 같을 때, 주어진 질문을 수행하는 데에 적합한 프롬프트 번호를 생성하시오.
반드시 숫자 하나만을 생성하시오.

프롬프트 1: 질문 - 답변 적합도 평가
프롬프트 2: 핵심가치 적합도 평가
프롬프트 3: 포지션에 기대하는 역할 생성
프롬프트 4: 자기소개서 바탕의 면접 질문 생성

질문: {natural_query}"""

    print(api_query)
    answer = chatgpt_generate(api_query)
    return answer

first_answer = query_to_prompt("지원자가 입사하게 되면 어떤 일을 할 수 있을지 예측해보고 싶어.")
prompt_number = int(first_answer.strip())
prompts = [prompt_1, prompt_2, prompt_3, prompt_4]
retrieved_prompt = prompts[prompt_number-1]
print(retrieved_prompt)
second_answer = chatgpt_generate(retrieved_prompt + personal_statement)
print(second_answer)