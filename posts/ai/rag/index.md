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

## KNN-LM

* 다음 단어 예측에 KNN 모델을 사용

* 드물게 등장하는 패턴을 다룰 때 유용

* decoder-only Transformer

{{<admonition info>}}
K-최근접 유사 항목(kNN) 정의

kNN(K-최근접 유사 항목 알고리즘)은 근접성을 사용하여 하나의 데이터 요소를 예측을 위해 학습되고 기억된 데이터 세트와 비교하는 머신 러닝 알고리즘입니다. 이 인스턴스 기반 학습은 kNN에 '지연 학습'이라는 명칭을 부여하고 알고리즘이 분류 또는 회귀 문제를 수행할 수 있도록 합니다. kNN은 유사한 지점이 서로 근처에서 발견될 수 있다는, 즉, 같은 종류의 새들이 함께 모인다는 가정을 바탕으로 작동합니다.

분류 알고리즘으로서 kNN은 유사 항목 내의 다수 세트에 새로운 데이터 요소를 할당합니다. 회귀 알고리즘인 kNN은 쿼리 지점에 **가장 가까운 값의 평균**(유클리디안 거리를 바탕으로 측정)을 기반으로 예측을 수행합니다.

kNN은 지도 학습 알고리즘으로, 'k'는 분류 또는 회귀 문제에서 고려되는 최근접 유사 항목의 수를 나타내고, 'NN'은 k에 대해 선택된 수에 대한 최근접 유사 항목을 나타냅니다.

출처: https://www.elastic.co/kr/what-is/knn
{{</admonition>}}

<img src="/images/ai/rag/3.png" />

<img src="/images/ai/rag/4.png" />

<img src="/images/ai/rag/5.png" />

출처: https://fastcampus.co.kr


