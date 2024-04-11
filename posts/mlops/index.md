# MLOps


# Introduction

개발과 운영을 따로 나누지 않고 개발의 생산성과 운영의 안정성을 최적화하기 위한 문화이지 방법론이 `DevOps`이며, 이를 `ML` 시스템에 적용한 것이 `MLOps`이다.

MLOps는 ML의 전체 Lifecycle를 관리해야 한다.

MLOps란 단순히 ML 모델뿐만 아니라, 데이터를 수집하고 분석하는 단계(Data Collection, Ingestion, Analysis, Labeling, Validation, Preparation), 그리고 ML 모델을 학습하고 배포하는 단계(Model Training, Validation, Deployment)까지 전 과정을 AI Lifecycle로 보고, MLOps의 대상으로 보고 있다.
ML에 기여하는 Engineer들(Data Scientist, Data Engineer, SW Engineer)이 이 Lifecycle을 관리하고 모니터링해야 한다.

<img src="/images/mlops2.webp" />

머신러닝을 엔터프라이즈 레벨에서 서비스에 구현하고자 한다면, MLOps는 선택이 아니라 반드시 구현해야하는 방향이다. 최고수준 모범사례까지는 못하더라도 최소한 어느 정도 수준까지는. 따라서 MLOps라는 키워드 자체는 시간이 지나면 바뀔 수도 있겠지만, 최소한 그 지향점은 바뀌지 않을 필수적인 것으로 생각된다.

# ML 시스템 요소

머신러닝 시스템을 프로덕션 환경에 적용하고 운영하기 위해서는 단순히 좋은 머신러닝 모델만으로 가능한 것이 아니다. 머신러닝 모델이 ML 시스템의 핵심이기는 하지만, 전체 프로덕션 ML 시스템의 운영을 고려하면 모델 학습 자체는 오히려 작은 부분을 차지한다고 이야기하기도 한다. 모델을 운영하기 위해 기반 데이터와 인프라를 포함한 모든 시스템이 유기적으로 돌아가야 한다.

<img src="/images/mlops3.webp" />

# DevOps vs MLOps

MLOps는 아래와 같은 점들에서 소프트웨어 시스템과 차이를 가진다.

- Testing

  일반적인 단위, 통합 테스트 외에 데이터 검증, 학습된 모델 품질 평가, 모델 검증이 추가로 필요하다.

- Deployment

  오프라인에서 학습된 ML모델을 배포하는 수준에 그치는 것이 아니라, 새 모델을 재학습하고, 검증하는 과정을 자동화해야 한다.

- Production

  일반적으로 알고리즘과 로직의 최적화를 통해 최적의 성능을 낼 수 있는 소프트웨어 시스템과 달리, ML 모델은 이에 더해서 지속적으로 진화하는 data profile 자체만으로도 성능이 저하될 수 있다.
  즉, 기존 소프트웨어 시스템보다 더 다양한 이유로 성능이 손상될 수 있으므로, 데이터의 summary statistics를 꾸준히 추적하고, 모델의 온라인 성능을 모니터링하여 값이 기대치를 벗어나면 알림을 전송하거나 롤백을 할 수 있어야 한다.

- CI (Continuous Integration)

  CI는 code와 components뿐만 아니라 data, data schema, model에 대해 모두 테스트되고 검증되어야 한다.

- CD (Continuous Delivery)

  단일 소프트웨어 패키지가 아니라 ML 학습 파이프라인 전체를 배포해야한다.

- CT (Continuous Training)

  ML 시스템만의 속성으로, 모델을 자동으로 학습시키고 평가하는 단계이다.

# Data science steps for ML

먼저 business use case와 success criteria들을 정하고 나서 ML 모델을 프로덕션에 배포하기까지, 수동이든 자동이든, 모든 ML 프로젝트에는 다음과 같은 스텝들이 수반된다.

1. Data Extraction(데이터 추출)

   데이터 소스에서 관련 데이터 추출

2. Data Analysis(데이터 분석)

   데이터의 이해를 위한 탐사적 데이터 분석(EDA) 수행
   모델에 필요한 데이터 스키마 및 특성 이해

3. Data Preparation(데이터 준비)

   데이터의 학습, 검증, 테스트 세트 분할

4. Model Training(모델 학습)

   다양한 알고리즘 구현, 하이퍼 파라미터 조정 및 적용
   output은 학습된 모델.

5. Model Evaluation(모델 평가)

   holdout test set에서 모델을 평가
   output은 모델의 성과 평가 metric.

6. Model Validation(모델 검증)

   기준치 이상의 모델 성능이 검증되고, 배포에 적합한 수준인지 검증

7. Model Serving(모델 서빙)

   - 온라인 예측을 제공하기 위해 REST API가 포함된 마이크로 서비스
   - 배치 예측 시스템
   - 모바일 서비스의 embedded 모델

8. Model Monitoring(모델 모니터링)

   모델의 예측 성능을 모니터링

# MLOps level 0: Manual Process

<img src="/images/mlops4.webp" />

- 데이터 추출과 분석, 모델 학습, 검증을 포함한 모든 단계가 수동

- ML과 Operation간 disconnection : 데이터 사이언티스트가 모델을 아티팩트로 전달하고, 엔지니어가 low latency로 프로덕션 환경에 배포. training-serving skew가 발생할 수 있다.

- Infrequent release iteration : 새 모델 버전의 배포가 뜨문뜨문 비정기적으로 발생한다.

- No CI : 변경이 많지 않으므로 CI가 고려되지 않는다. 스크립트 수행이나 노트북에서 개인적으로 테스트를 수행한다.

- No CD : 배포가 자주 없으므로 CD까지 필요하지 않다.

- Active performance monitoring의 부재 : 로그나 모델의 예측 성능 등을 모니터링하지 않는다. 모델의 성능이 저하되거나 모델이 이상동작 하는 것을 감지할 수 없다.

# MLOps level 1: ML Pipeline automation

Level 1의 목표는 ML 파이프라인을 자동화하여 모델을 지속적으로 학습시키는 것이다.

<img src="/images/mlops5.webp" />

## Level1의 특징들

- Rapid experiment : 실험을 빠르게 반복하고, 전체 파이프라인을 프로덕션으로 빠르게 배포
  개발 환경에서 쓰인 파이프라인이 운영 환경에도 그대로 쓰임. DevOps의 MLOps 통합에 있어 핵심적인 요소

- 포로덕션 모델의 CT(Continuous Training) : 새로운 데이터를 사용하여 프로덕션 모델이 자동으로 학습

- CD: 새로운 데이터로 학습되고 검증된 모델이 지속적으로 배포됨.

- Level 0에서는 학습된 모델만을 배포했다면 Level 1에서는 전체 파이프라인이 배포됨.

## CT를 위해서 필요한 것들

새로운 데이터를 통해 새로운 모델을 지속적으로 학습하므로, data validation과 model validation이 필수적이다.

## Data and Model Validation

- Data validation
  데이터 검증에서 실패하면, 신규 모델의 배포를 중지해야한다. 이 의사결정도 자동화되어야 한다.

  - Data schema skews: 예상치 못한 데이터가 생성된 경우, 예상범주를 벗어난 특성이 생성된 경우 등.

  - Data values skews: 데이터의 통계적 속성이 변화되고 있음을 감지해야 한다. 이러한 변화를 감지해 모델의 재학습을 트리거한다.

- Model Validation
  모델이 새로운 데이터로 재학습을 마치고, 운영 환경에 반영되기 전에 평가되고 검증되어야 한다.

  - 테스트 데이터셋으로 평가 메트릭을 생성한다.

  - 평가메트릭을 새로운 모델과, 현재 모델 사이에 비교한다. 새로운 모델이 기존 모델보다 더 나은 성과를 보이는지 검증한다.

  - 새로운 모델의 성능이 다양한 세그먼트에서 일관된 성과를 보이는지 검증한다.

  - 인프라 및 예측 서비스 API와 호환성 테스트를 완료한다.

## Feature store

Feature store는 학습과 서빙에 사용되는 모든 feature들을 모아둔 저장소이다. 대용량 배치 처리와 low latency의 실시간 서빙을 모두 지원할 수 있어야 한다.

- 사용 가능한 모든 feature의 저장소

- 항상 최신화된 데이터

## Metadata management

ML 파이프라인의 실행 정보, 데이터 및 아티팩트의 계보 등을 저장한다.

- 실행된 파이프라인 버전, 시작-종료 시간, 소요시간 등

- 파이프라인의 실행자, 매개변수 인수

- 이전 모델에 대한 포인터(모델의 롤백이 필요한 경우)

- 모델 평가 단계에서 생성된 모델 평가 측정 항목.

## ML pipeline trigger

- 모델을 재학습 시키는 파이프라인의 자동화

- 매일, 매주 또는 매월 등의 재학습 빈도는 데이터 패턴의 변경 빈도와 모델 재학습 비용에 따라 달라질 수 있다.

- 모델 성능 저하가 눈에 띄는 경우 모델 재학습 트리거

# MLOps level 2: CI/CD pipeline automation

## Continuous Integration

파이프라인과 구성요소는 커밋되거나 소스 레포지토리로 푸시될 때 빌드, 테스트, 패키징된다. 아래와 같은 테스트가 포함될 수 있다.

- 특성 추출 로직을 테스트

- 모델에 구현된 메소드를 단위 테스트

- 모델 학습이 수렴하는지 테스트

- 모델 학습에서 0으로 나누거나 작은 값 또는 큰 값을 조작하여 NaN 값을 생성하지 않는지 테스트

- 파이프라인의 각 구성요소가 예상된 아티팩트를 생성하는지 테스트

- 파이프라인 구성요소간 통합 테스트

## Continuous Delivery

- 모델 배포 전 모델과 대상 인프라 호환성 확인. (패키지 호환 여부/메모리/컴퓨팅 자원등)

- 서비스 API 호출 테스트

- QPS 및 지연 시간과 같은 서비스 부하 테스트

# Traditional Software System vs ML System

<img src="/images/mlops7.webp" />

