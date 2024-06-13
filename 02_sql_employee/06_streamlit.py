import config
import openai
import pymysql
import streamlit as st

open_ai_key = config.OPENAI_API_KEY
openai.api_key = open_ai_key
model = "gpt-4o"

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

def query_to_sql(natural_query):
    api_query = f"""데이터베이스의 테이블 정보가 아래와 같이 주어졌을 때, 쿼리에 해당하는 SQL 문을 작성하시오.

# 테이블 1
테이블 명: employees
테이블 컬럼:
('id', 'int(11)', 'NO', 'PRI', None, 'auto_increment')
('name', 'varchar(50)', 'YES', '', None, '')
('age', 'int(11)', 'YES', '', None, '')
('position', 'varchar(20)', 'YES', '', None, '')
('department', 'varchar(20)', 'YES', '', None, '')
('skill', 'varchar(50)', 'YES', '', None, '')
('education', 'varchar(20)', 'YES', '', None, '')
('years_at_company', 'int(11)', 'YES', '', None, '')
('hobby', 'varchar(50)', 'YES', '', None, '')
('marital_status', 'varchar(10)', 'YES', '', None, '')
('certification', 'varchar(50)', 'YES', '', None, '')
('award', 'varchar(50)', 'YES', '', None, '')
('address', 'varchar(100)', 'YES', '', None, '')

# 테이블 2
테이블 명: employees_info
테이블 컬럼:
('id', 'int(11)', 'NO', 'PRI', None, 'auto_increment')
('name', 'varchar(50)', 'YES', '', None, '')
('age', 'int(11)', 'YES', '', None, '')
('department', 'varchar(50)', 'YES', '', None, '')
('phone', 'varchar(20)', 'YES', '', None, '')
('email', 'varchar(100)', 'YES', '', None, '')

쿼리: {natural_query}"""
    answer = chatgpt_generate(api_query)
    return answer

def go_db(sql):
    conn = pymysql.connect(host='127.0.0.1', user='root', password='1234', db='hr_db', charset='utf8')
    with conn.cursor() as cur:
        cur.execute(sql)
        result = cur.fetchall()
    return result

def make_natural_answer(natural_query, sql_result):
    sql_result = [str(item) for item in sql_result]
    sql_result = "\n".join(sql_result)
    prompt = f"""다음과 같은 쿼리가 주어졌을 때, 쿼리로 데이터베이스를 조회한 결과가 있다.
쿼리와 데이터베이스 조회 결과로 답변 문장을 자연스럽게 생성하시오.

쿼리: {natural_query}
데이터베이스 조회 결과:
{sql_result}
"""
    print(prompt)
    print('-----------------------------')

    answer = chatgpt_generate(prompt)
    return answer

def get_answer(query):

    answer = query_to_sql(query)
    start = answer.index("SELECT")
    end = answer.index(";")
    sql = answer[start:end+1]
    print(sql)
    print('------------------------')
    sql_result = go_db(sql)
    natural_answer = make_natural_answer(query, sql_result)
    return natural_answer

st.title("🤖 직원 정보 조회 시스템")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.markdown(message['content'])

if prompt := st.chat_input("조회하고자하는 정보를 입력하세요."):
    st.chat_message("user").markdown(prompt)

    st.session_state.messages.append({"role": "user", "content": prompt})

    response = f"Bot: {get_answer(prompt.strip())}"

    with st.chat_message("assistant"):
        st.markdown(response)
    
    st.session_state.messages.append({"role": "assistant", "content": response})