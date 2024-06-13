import config
import openai
from Prompts import *
import streamlit as st

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
프롬프트 번호는 [3]과 같이 리스트 안에 숫자가 있는 형태로 생성하시오. 
적합한 프롬프트가 2개 이상이라면, [1, 2]와 같이 리스트 형태로 출력하시오.

프롬프트 1: 질문 - 답변 적합도 평가
프롬프트 2: 핵심가치 적합도 평가
프롬프트 3: 포지션에 기대하는 역할 생성
프롬프트 4: 자기소개서 바탕의 면접 질문 생성

질문: {natural_query}"""

    print(api_query)
    answer = chatgpt_generate(api_query)
    return answer

def get_answer(natural_query):
    prompts = [prompt_1, prompt_2, prompt_3, prompt_4]

    first_answer = query_to_prompt(natural_query)
    prompt_list = eval(first_answer)

    total_answer = ""
    for prompt_number in prompt_list:
        retrieved_prompt = prompts[prompt_number-1]
        second_answer = chatgpt_generate(retrieved_prompt + personal_statement)
        total_answer += second_answer + "\n\n"

    return total_answer.strip()


st.title("🤖 자기소개서 평가 시스템")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("수행하고자 하는 자기소개서 평가를 입력하세요."):
    st.chat_message("user").markdown(prompt)

    st.session_state.messages.append({"role": "user", "content": prompt})

    response = f"Bot: {get_answer(prompt.strip())}"
    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})