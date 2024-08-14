# Ui


# Introduction

- Jobs: 스파크 애플리케이션의 모든 job에 대한 요약 정보

- Stages: 모든 jobs의 모든 stages의 현재 상태 요약 정보

- Storage: persisted RDD와 DataFrame 정보 제공

- Environment: 다양한 환경 변수 값

- Executors: 애플리케이션을 위해 생성된 Executer 정보 제공. 메모리와 디스크 사용량과 task, shuffle 정보 등

- SQL: 애플리케이션이 Spark SQL 쿼리 실행 시 정보 제공

- Streaming: Streaming jobs 실행 시 정보 제공

## 애플리케이션 실행

```python
df = spark.read.format("csv") \
     .option("inferSchema", "true") \
     .option("sep", "\t") \
     .option("header", "true") \
     .load("FILE_PATH")
```

데이터 프레임 구조는 다음과 같다.

| prev_id | curr_id |  n  |   prev_title    |  curr_title  | type  |
| :-----: | :-----: | :-: | :-------------: | :----------: | :---: |
|  null   | 3632887 | 121 |  other-google   |      !!      | other |
|  null   | 3632887 | 93  | other-wikipedia |      !!      | other |
|  64486  | 3666952 | 19  |  Louden_Up_Now  | !!!\_(album) | link  |

이후 `repartition`과 `groupBy`, `count`, `sort`을 실행해준다.

```python
df.repartition(30) \
  .groupBy("curr_title") \
  .count()
  .sort(F.col("count").desc()
)
.show(100)
```

|   curr_title   | count |
| :------------: | :---: |
|   Main_Page    | 88425 |
| United_States  | 4301  |
| United_kingdom | 2081  |
|     India      | 2002  |

## Job 탭

스파크의 애플리케이션의 action은 하나 이상의 Job을 생성하고 실행한다. Job 탭의 랜딩 페이지에서는 그러한 Job들의 1) 기본 정보 2) 이벤트 타임라인 3)실행되거나 완료된 Job 정보를 보여준다.

<img src="/images/data/spark/spark-ui-1.png"/>

1. 기본 정보

   - User: 현재 스파크 애플리케이션 사용자

   - Total Uptime: 스파크 애플리케이션이 첫 시작 이후의 시간

   - Completed Jobs: 완료된 Jobs의 개수

2. 이벤트 타임라인: 시간 순으로 Executors와 Jobs의 상태를 그래픽으로 보여준다. 2)의 상단에는 한 개의 상자가 하나의 Executor, 하단에서는 하나의 상자가 하나의 Job에 해당되는 것을 볼 수 있다. 샘플 코드를 실행하면 2)의 오른쪽 하단의 11:15 이후의 3개의 Job이 생성된 것을 확인할 수 있다.

3. Completed Jobs: 완료된 Job들을 Description, 제출 시간, 소용 시간, Stage 개수, Task 개수와 같이 나열해준다. 실행되고 있는 Job이 있다면 이 부분 위에 Active Jobs에서 동일한 형태로 보여준다. 3)의 파랑색 링크를 클릭해 각 Job의 Detail 페이지로 이동할 수 있다.

## Job Detail 탭

<img src="/images/data/spark/spark-ui-2.png"/>

1. Job 기본 정보에서는 아래와 같은 사항을 확인할 수 있다.

- Status: Job의 상태

- Submitted: Job 제출 일시

- Duration: Job 수행 시간

- Associated SQL Query: 연관 SQL Query 번호

- Job Group: 하나의 액션은 하나 이상의 Job을 생성한다.

- Completed Stages: 완료 스테이지 수

- Skipped Stages: 생략된 스테이지 수. 캐시에 데이터를 사용할 수 있는 등의 이유로 재실행이 필요 없어 생략된 경우.

2. 이벤트 타임라인 에서는 이번에는 Stage 별로 표시되게 된다.

<img src="/images/data/spark/spark-ui-3.png"/>

3. DAG 시각화: Job에 포함된 Stages들의 DAG(Directed Acyclic Graph)를 시각적으로 확인할 수 있다. 위에서는 16, 17 Stage가 Skipped 되고, 18 Stage만 실행된 것을 볼 수 있다. 각 Stage의 요소를 살펴보며 대략적인 작업흐름을 확인할 수 있다.

<img src="/images/data/spark/spark-ui-4.png"/>

4. 완료 및 생략 Stages: Stage별로 축약된 정보와 함께 주요 정보들을 확인할 수 있다. 실행되는 Pool 이름, Stage로 이동할 수 있는 링크가 있는 Description, 제출 일시, 소요 시간, Tasks, 입출력 사이즈와 Shuffle Read & Write 사이즈가 그러한 정보에 포함된다. Task 레벨로 scale down 하기전에 Stage 레벨에서 특정 작업이 너무 많은 Task를 발생시키지는 않는지, Shuffle I/O가 과도하지는 않은지 확인할 수 있다.

## Stages 탭

Stages 탭의 페이지에서는 Jobs 탭과 유사하게 완료 및 실행 중인 여러 Stages에 대한 정보를 확인할 수 있다. 또한, 개별 Stage 페이지로 이동해 아래와 같이 상세 정보를 확인할 수 있다.

<img src="/images/data/spark/spark-ui-5.png"/>

특징적으로 중요한 부분은 아래와 같이 병렬의 최소 단위인 Task들의 실행 이벤트 타임라인과 다양한 개별 또는 집계 메트릭을 확인할 수 있는 부분이다. Job, Stage 레벨에서 특정 현상에 대한 전체적인 흐름을 봤다면, 아래와 같은 개별 Task를 탐색하면서 일부 이상치 또는 현상에 대해 더욱 세밀한 분석을 진행할 수 있다.

<img src="/images/data/spark/spark-ui-6.png"/>

<img src="/images/data/spark/spark-ui-7.png"/>

위와 같은 메트릭에서는 해당 Stage에 속하는 200개의 Task들에 대한 다양한 수치를 요약해서 보여주고 있다.

## Storage 탭

`cache`가 진행되면, 그러한 데이터에 대한 정보를 전달한다.

## Enviroment 탭

JVM, Spark, Resource, Hadoop, System, Classpath와 같은 설정 정보들을 한눈에 확인할 수 있는 Environment 탭이다. 스파크 운영이 기본을 넘어 다양한 것들을 시도하고자 할 때 설정을 건드린다.

스파크 옵션의 설정은 1) 설정 파일을 통해(SPARK_HOME에 위치) 2) spark-submit 시 --conf와 같은 옵션을 통해 3) Spark 애플리케이션 내의 SparkSession을 통해서 설정

## Executors 탭

스파크는 executor-cores, executor-memory와 같이 executor 단위로 자원을 할당하기에 해당 부분과 관련되어서 설정을 조정할 때 사용한다.

그렇기에 아래의 메트릭에 있어서도 메모리와 관련된 값들이 주를 이루는 것을 볼 수 있다.

<img src="/images/data/spark/spark-ui-8.png"/>

스파크 튜닝 시, shuffle의 IO와 함께 executor의 메모리가 주요 요소로 많이 다뤄지기에, 그런 상황에서도 위와 같은 수치가 어떤 부분을 나타내 주는 지 알고 있는 것은 매우 중요하다.

## SQL 탭

Spark SQL로 수행되는 작업은 아래와 같이 SQL 탭에 Query를 생성하게 된다. RDD 연산이 아니라 Spark SQL에 기반한 처리라면, Job, Stage, Task 정보를 통해 작업의 흐름을 파악하기는 조금 어렵다. 그러한 부분에서 SQL의 쿼리 플랜을 그래프로 표현하고, details 정보를 통해 각 단계의 여러 수치를 한 눈에 확인할 수 있다.

<img src="/images/data/spark/spark-ui-9.png"/>

위와 같은 Query의 Description의 링크를 통해 아래와 같은 Detail 페이지에 도달할 수 있다.

Scan에서부터, Exchange, Aggregate 등 쿼리 플랜에 따른 DAG 그래프를 보여준다. 스파크 transformation에서 narrow와 wide를 구분하는 것과 같이, Join에 따른 Shuffle의 형태는 성능에 큰 영향을 끼친다.

그러한 join을 최적화하는데 필요한 정보는 아래의 SQL 탭에서 얻을 수 있다.

<img src="/images/data/spark/spark-ui-10.png"/>
