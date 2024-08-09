# RAG


# Introduction

RAG(Retrieval-Augmented Generation)는 대규모 언어 모델의 출력을 최적화하여 응답을 생성하기 전에 학습 데이터 소스 외부의 신뢰할 수 있는 지식 베이스를 참조하도록 하는 프로세스입니다. 대규모 언어 모델(LLM)은 방대한 양의 데이터를 기반으로 학습되며 수십억 개의 매개 변수를 사용하여 질문에 대한 답변, 언어 번역, 문장 완성과 같은 작업에 대한 독창적인 결과를 생성합니다. RAG는 이미 강력한 LLM의 기능을 특정 도메인이나 조직의 내부 지식 기반으로 확장하므로 모델을 다시 교육할 필요가 없습니다. 이는 LLM 결과를 개선하여 다양한 상황에서 관련성, 정확성 및 유용성을 유지하기 위한 비용 효율적인 접근 방식입니다.

출처: https://aws.amazon.com/ko/what-is/retrieval-augmented-generation/

## Plain Generative LM Pipeline

1. User Input + Parametric memory

2. Generation: Generation based on parametric memory

## RAG Pipeline

1. Indexing: 외부 데이터를 모아서 데이터베이스에 저장

    Document chunking 

    Embeding

2. User Input

    2024년 최저 시급이 얼마야?

    mac OS의 최신 버전은?

3. Retrieval: 이전에 가공해두었던 외부의 메모리를 보면서 User input과 비슷한 것을 골라서 전달

    Retrieve corresponding document

4. Generation

    Retrieved Document + User query

<img src="/images/ai/rag/2.png" />

출처: https://fastcampus.co.kr

# RAG with LlamaIndex

[Tutorial](https://github.com/seilylook/LlamdaIndex_with_OpenAI)
