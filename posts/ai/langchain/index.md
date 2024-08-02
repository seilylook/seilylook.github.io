# Lang_chain


# Introduction

**LangChain**은 LLM을 활용한 애플리케이션 개발을 단순화하기 위해 설계돈 오픈 소스 프레임워크이다. 다양한 LLM과 상호 작용하고, 여러 모델을 연결해 복잡한 AI 애플리케이션을 구축하는 데 도움을 주는 도구이다. 주로 LLM 자체를 개발하는 것보다는 만들어진 LLM(ChatGPT)을 사용해 여러 텍스트 분석 기능, 챗봇 개발 등에 사용된다.

<img src="/images/ai/lang_chain/1.webp" />

source: https://js.langchain.com/v0.1/docs/get_started/introduction/

<img src="/images/ai/lang_chain/2.png" />

Source : https://aws.amazon.com/ko/what-is/langchain/

특히 LangChaindms `RAG(Retrieval Augmented Generation)` 같은 학습으로 모든 입력을 처리할 수 없는 케이스에 많이 사용된다. 실제로 LLM을 서비스할 때는 모든 데이터를 항상 실시간으로 학습시켜 놓을 수도 없고, *사용자가 원하는 질문을 정확하게 답변하기 위해서* 여러 추가적인 지식이 필요하기 때문에 이러한 방식을 주로 사용한다.

참고 : https://www.skelterlabs.com/blog/2024-year-of-the-rag

## LangChain으로 개발할 수 있는 서비스

### Chatbot

<img src="/images/ai/lang_chain/3.png" />

Source : https://python.langchain.com/docs/use_cases/chatbots/

### QA Engine(특정 데이터베이스를 활용해 질의응답이 가능한 챗봇) with **RAG**

<img src="/images/ai/lang_chain/4.png" />

<img src="/images/ai/lang_chain/5.png" />

Source : https://python.langchain.com/docs/use_cases/question_answering/quickstart/

RAG는 Knowledge Base(KB)를 구축해야 사용할 수 있다. 이 때 KB는 Vector DB/Vector Store/Vector Index라 불리는 *embedding vector를 저장하는 전용 데이터베이스*가 있어야 한다.

Vector DB에는 ChromaDB, Pinecone, Milvus 등이 있는데, Langchain은 주로 `ChromaDB`를 사용한다.

<img src="/images/ai/lang_chain/6.png" />

Source : https://python.langchain.com/docs/use_cases/sql/quickstart/

Langchain에는 Prompt ↔ SQL query로 변환해주는 SQL chain이 있기 때문에 SQL을 직접 사용해서 QA engine을 만들 수도 있다.

→ RDBMS를 KB로 사용하겠다! (RAG)

#### 예시

Question(input prompt, text) → LLM(text-to-**sql**) → SQL query → RDBMS(retrieval) → Question + **table(Augmented) →** LLM(answer generation)

e.g. Q. 학교에 다니는 학생 수는 몇명인가요? 다음은 학교 데이터입니다. 학교 데이터를 보고 질문에 대한 알맞은 답변을 해주세요.

|STUDENT_ID|NAME|
|:------------:|:------:|
|1|Kim|
|2|Lee|

e.g. Q. 학교에 다니는 학생 수는 몇명인가요?

→ (LLM이 text를 SQL로 변환)

```sql
SELECT COUNT(*)
from student;
```

→ MySQL에 쿼리 전송

→ 답변 8

→ Q. 학교에 다니는 학생 수는 몇명인가요? 8

→ A. 8명입니다.
