# 기존 LM 사용해서 QA시스템을 만든다
query = "패스트캠퍼스는 어떤 회사인가요?"
answer = model(query)

# Naive RAG
query = "패스트캠퍼스는 어떤 회사인가요?"

# 질문과 적절한 문서를 찾는 과정
documents = retriever(query)

# 질문과 검색된 문서를 함께 전달
answer = model(query, documents[:k])

# 아래 문서를 기반으로 주어진 질문에 답변하시오.
# 질문: 패스트캠퍼스는 어떤 회사인가요?

# 문서 1: 패스트캠퍼스 (회사) - 위키피디아...

# Modular RAG
query = "패스트캠퍼스는 어떤 회사인가요?"

# 예를 들어, 인터넷 검색 모듈
search_query = model(query) # 패스트캠퍼스 회사

def internet_search(query_term):
    docs = google(query_term)
    return docs

documents = internet_search(search_query)

answer = model(query, documents[:k])