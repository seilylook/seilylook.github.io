# CCTV Quality Monitor


# CCTV 영상 데이터 품질 모니터링 시스템

## 프로젝트 개요

CCTV 영상 데이터 품질 모니터링 시스템은 국가교통정보센터에서 제공하는 실시간 도로 CCTV 영상의 품질을 자동으로 모니터링하고 분석하는 시스템입니다. 이 시스템은 영상의 해상도, 프레임 손실, 밝기, 대비, 선명도 등 다양한 품질 지표를 실시간으로 측정하고, 문제가 있는 CCTV를 신속하게 식별하여 품질 관리를 효율화합니다.

|Kibana Dashboard|
|:-----------------|
| {{< image src="/images/projects/cctv-quality-monitor/1.png" caption="Dashboard 1: 실시간 상태 확인" >}} |
| {{< image src="/images/projects/cctv-quality-monitor/2.png" caption="Dashboard 2: 품질 추세 시각화" >}} |

## 주요 기능

- **실시간 CCTV 데이터 수집**: 국가교통정보센터 API를 통해 실시간으로 CCTV 메타데이터 및 스트림 URL 수집
- **영상 품질 분석**: OpenCV를 활용한 영상 품질 분석 (밝기, 대비, 블러, 프레임 손실율 등)
- **실시간 데이터 스트리밍**: Kafka를 통한 실시간 품질 데이터 스트리밍
- **데이터 저장 및 시각화**: Elasticsearch에 품질 데이터를 저장하고 Kibana를 통해 시각화
- **워크플로우 자동화**: Airflow를 사용한 품질 점검 작업 자동화
- **알림 시스템**: 품질 문제 발생 시 알림 기능

### 백엔드

- **Python 3.9+**: 주요 개발 언어
- **OpenCV**: 영상 데이터 품질 분석
- **Apache Kafka**: 실시간 데이터 스트리밍
- **Elasticsearch**: 품질 데이터 저장 및 검색
- **Apache Airflow**: 워크플로우 자동화

### 인프라 및 배포

- **Docker & Docker Compose**: 컨테이너화 및 서비스 오케스트레이션
- **Makefile**: 프로젝트 명령어 관리
- **Poetry**: Python 의존성 관리

### 시각화 및 모니터링

- **Kibana**: 대시보드 및 데이터 시각화
- **Kafka UI**: Kafka 클러스터 모니터링

---

## 시스템 아키텍처

시스템은 다음과 같은 주요 컴포넌트로 구성됩니다:

1. **데이터 수집 모듈**: 국가교통정보센터 API에서 CCTV 정보를 수집하고 Kafka에 전송
2. **품질 분석 모듈**: OpenCV를 사용하여 CCTV 스트림 품질을 분석
3. **데이터 저장 모듈**: 분석된 품질 데이터를 Elasticsearch에 저장
4. **워크플로우 관리**: Airflow로 전체 데이터 파이프라인 관리
5. **시각화 모듈**: Kibana 대시보드를 통한 품질 데이터 시각화

---

## 구현 세부 사항

### 품질 측정 지표

- **밝기(Brightness)**: 영상의 평균 밝기 수준
- **대비(Contrast)**: 영상의 명암 대비
- **선명도(Sharpness)**: 영상의 선명도 지표 (라플라시안 분산)
- **프레임 손실율**: 정지된 프레임 감지를 통한 프레임 손실률
- **프레임 레이트(FPS)**: 초당 프레임 수
- **해상도**: 영상의 해상도 측정

### 데이터 파이프라인

```
API 수집 → Kafka Producer → Kafka Topic → Kafka Consumer → 품질 분석 → Elasticsearch → Kibana 시각화
```

### 대시보드 구성

- **실시간 상태 대시보드**: 전체 CCTV 시스템의 현재 상태 표시
- **품질 추세 대시보드**: 시간에 따른 품질 지표 변화 추세
- **위치 기반 대시보드**: 지도 위에 CCTV 위치 및 상태 표시
- **문제 감지 대시보드**: 품질 문제가 있는 CCTV 강조 표시

## 설치 및 실행 방법

### 사전 요구사항

- Docker 및 Docker Compose
- Python 3.9 이상
- Poetry (Python 패키지 관리)
- 최소 8GB RAM 권장

### 설치 과정

1. 저장소 클론
```bash
git clone https://github.com/seilylook/CCTV_Quality_Monitor.git
cd cctv-quality-monitoring
```

2. 환경 변수 설정
```bash
cp .env.example .env
# .env 파일을 편집하여 API 키 및 기타 설정을 구성하세요
```

3. 프로젝트 설정
```bash
make setup
```

4. 서비스 시작
```bash
make all
```

### 웹 인터페이스 접속

- **Airflow**: http://localhost:8080 (기본 계정: airflow/airflow)
- **Kibana**: http://localhost:5601
- **Kafka UI**: http://localhost:8989

---

## 프로젝트 구조

```
cctv-quality-monitoring/
├── .env.example                # 환경 변수 예시 파일
├── .gitignore                  # Git 무시 파일 목록
├── Makefile                    # 프로젝트 명령어 관리
├── README.md                   # 프로젝트 설명
├── docker-compose.yml          # 도커 컴포즈 설정
├── pyproject.toml              # Poetry 의존성 설정
├── Dockerfile                  # 애플리케이션 도커 이미지
├── Dockerfile.airflow          # Airflow 커스텀 이미지
├── airflow/
│   ├── dags/
│   │   └── cctv_quality_dag.py # Airflow DAG 정의
│   └── plugins/
│       └── operators/
│           └── cctv_operators.py
├── src/
│   ├── __init__.py
│   ├── config.py               # 설정 관리
│   ├── main.py                 # 메인 애플리케이션
│   ├── api/
│   │   ├── __init__.py
│   │   └── cctv_api.py         # CCTV API 클라이언트
│   ├── kafka/
│   │   ├── __init__.py
│   │   ├── producer.py         # Kafka 프로듀서
│   │   └── consumer.py         # Kafka 컨슈머
│   ├── quality/
│   │   ├── __init__.py
│   │   ├── analyzer.py         # 영상 품질 분석 로직
│   │   └── metrics.py          # 품질 메트릭 정의
│   └── storage/
│       ├── __init__.py
│       └── elasticsearch.py    # Elasticsearch 연동
└── tests/
    ├── __init__.py
    ├── conftest.py             # 테스트 설정
    ├── test_api.py             # API 테스트
    └── test_analyzer.py        # 분석기 테스트
```

---

## 개발 과정 및 도전 과제

### 도전 과제

1. **스트림 처리 안정성**: HLS 스트림 형식의 다양한 CCTV URL을 안정적으로 처리하기 위한 예외 처리 및 재시도 로직 구현
2. **실시간 처리 부하**: 다수 CCTV 스트림의 동시 처리로 인한 시스템 부하 관리
3. **OpenCV 호환성**: Docker 환경에서 OpenCV 라이브러리 종속성 문제 해결
4. **데이터 일관성**: Kafka와 Elasticsearch 간 데이터 일관성 유지

### 해결 방법

1. 견고한 에러 처리 및 로깅 시스템 구현
2. 컨테이너 자원 할당 최적화 및 배치 처리 도입
3. 커스텀 Docker 이미지를 통한 시스템 라이브러리 관리
4. 데이터 스키마 정의 및 검증 로직 구현

## 시스템 성능

- **처리 용량**: 시간당 최대 500개 CCTV 스트림 처리
- **응답 시간**: 품질 이슈 감지 시 평균 1분 이내 알림
- **정확도**: 영상 품질 문제 감지 정확도 95% 이상
- **가용성**: 99.9% 시스템 가동 시간

---

## 미래 개선 사항

- **딥러닝 모델 통합**: 영상 품질 분석을 위한 딥러닝 모델 도입
- **이상치 탐지 개선**: 시계열 데이터 기반 고급 이상치 탐지 알고리즘 구현
- **클라우드 환경 최적화**: AWS, Azure 또는 GCP 환경에 최적화된 배포 구성
- **모바일 알림 시스템**: 모바일 애플리케이션을 통한 실시간 알림 시스템 구현

---

## 결론

CCTV 영상 데이터 품질 모니터링 시스템은 대규모 CCTV 네트워크의 품질을 효율적으로 모니터링하고 관리할 수 있는 확장 가능한 솔루션입니다. 실시간 데이터 처리, 고급 영상 분석, 직관적인 시각화를 통해 CCTV 관리자가 품질 문제를 신속하게 식별하고 대응할 수 있습니다.

이 프로젝트는 빅데이터 처리, 영상 분석, 분산 시스템 설계 등의 기술을 실무에 적용한 사례로, 대규모 데이터 파이프라인 구축과 실시간 모니터링 시스템 개발 역량을 보여줍니다.

