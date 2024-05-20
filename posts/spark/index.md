# Spark


# Apache Spark란 무엇입니까?

Apache Spark는 빅 데이터 워크로드에 사용되는 오픈 소스 분산 처리 시스템입니다. Apache Spark는 인 메모리 캐시 및 최적화된 쿼리 실행을 활용하여 모든 크기의 데이터에 대해 빠른 분석 쿼리를 실행합니다. Java, Scala, Python 및 R로 개발 API를 제공하고 일괄 처리, 대화형 쿼리, 실시간 분석, 기계 학습, 그래프 처리 등 여러 워크로드에서 코드 재사용을 지원합니다. FINRA, Yelp, Zillow, DataXu, Urban Institute 및 CrowdStrike를 포함한 모든 업계의 조직에서 사용됩니다.

# Apache Spark는 어떻게 작동하나요?

Hadoop MapReduce는 병렬 분산 알고리즘을 사용하여 빅 데이터 세트를 처리하기 위한 프로그래밍 모델입니다. 개발자는 작업 배포 및 내결함성에 대해 걱정할 필요 없이 대규모 병렬 연산자를 작성할 수 있습니다. 그러나 MapReduce의 과제는 작업을 실행하는 데 필요한 순차적인 다단계 프로세스입니다. 각 단계에서 MapReduce는 클러스터에서 데이터를 읽고, 작업을 수행하고, 결과를 HDFS에 다시 씁니다. 각 단계에는 디스크 읽기 및 쓰기가 필요하므로 MapReduce 작업은 디스크 I/O 지연 시간으로 인해 속도가 느려집니다.

Spark는 인 메모리 처리를 수행하고, 작업의 단계 수를 줄이고, 여러 병렬 작업에서 데이터를 재사용하여 MapReduce의 한계를 해결하기 위해 만들어졌습니다. Spark를 사용하면 데이터를 메모리로 읽어 들이고, 작업을 수행하고, 결과를 다시 쓰는 과정에서 단 한 단계만 필요하므로 실행 속도가 훨씬 빨라집니다. 또한 Spark는 인 메모리 캐시를 사용하여 데이터를 재사용하여 동일한 데이터 세트에서 함수를 반복적으로 호출하는 기계 학습 알고리즘의 속도를 크게 높입니다. 데이터 재사용은 메모리에 캐시되고 여러 Spark 작업에서 재사용되는 객체 모음인 Resilient Distributed Dataset(RDD)에 대한 추상화인 DataFrames 생성을 통해 수행됩니다. 이는 특히 기계 학습 및 대화형 분석을 수행할 때 Spark가 MapReduce보다 몇 배 더 빨라지도록 지연 시간을 크게 줄여줍니다.

# 주요 차이점: Apache Spark와 Apache Hadoop

Spark와 Hadoop MapReduce 설계의 차이점 외에도 많은 조직에서는 이러한 빅 데이터 프레임워크를 무료로 사용하여 더 광범위한 비즈니스 문제를 해결하는 데 사용하고 있습니다.

Hadoop은 Hadoop 분산 파일 시스템(HDFS)을 스토리지로, YARN을 다양한 애플리케이션에서 사용하는 컴퓨팅 리소스를 관리하는 방법으로, MapReduce 프로그래밍 모델을 실행 엔진으로 구현하는 오픈 소스 프레임워크입니다. 일반적인 Hadoop 구현에서는 Spark, Tez 및 Presto와 같은 다양한 실행 엔진도 배포됩니다.

Spark는 대화형 쿼리, 기계 학습 및 실시간 워크로드에 초점을 맞춘 오픈 소스 프레임워크입니다. 자체 스토리지 시스템은 없지만 HDFS와 같은 다른 스토리지 시스템이나 Amazon Redshift, Amazon S3, Couchbase, Cassandra 등과 같은 기타 인기 스토어에서 분석을 실행합니다. Spark on Hadoop은 YARN을 활용하여 다른 Hadoop 엔진과 마찬가지로 공통 클러스터 및 데이터 세트를 공유하여 일관된 서비스 수준과 응답을 보장합니다.

# Apache Spark의 이점은 무엇인가요?

Apache Spark를 Hadoop 에코시스템에서 가장 활발한 프로젝트 중 하나로 만드는 데에는 많은 이점이 있습니다. 여기에는 다음이 포함됩니다.

신속함

인 메모리 캐시 및 최적화된 쿼리 실행을 통해 Spark는 모든 크기의 데이터에 대해 빠른 분석 쿼리를 실행할 수 있습니다.

개발자 친화적

Apache Spark는 기본적으로 Java, Scala, R 및 Python을 지원하므로, 애플리케이션을 구축할 수 있도록 다양한 언어를 제공합니다. 이러한 API를 사용하면 필요한 코드 양을 크게 줄이는 간단한 고급 연산자 뒤에 분산 처리의 복잡성이 숨겨지기 때문에 개발자가 작업을 쉽게 수행할 수 있습니다.

다중 워크로드

Apache Spark는 대화형 쿼리, 실시간 분석, 기계 학습, 그래프 처리 등 여러 워크로드를 실행할 수 있는 기능을 제공합니다. 하나의 애플리케이션으로 여러 워크로드를 원활하게 결합할 수 있습니다.

# Apache Spark 워크로드란 무엇인가요?

Spark 프레임워크에는 다음이 포함됩니다.

- 플랫폼의 기반인 Spark Core

- 대화형 쿼리를 위한 Spark SQL

- 실시간 분석을 위한 Spark Streaming

- 기계 학습을 위한 Spark MLlib

- 그래프 처리를 위한 Spark GraphX

<img src="/images/spark/spark2.png" />

## Spark Core

Spark Core는 플랫폼의 기초입니다. 메모리 관리, 장애 복구, 스케줄링, 작업 배포 및 모니터링, 스토리지 시스템과의 상호 작용을 담당합니다. Spark Core는 Java, Scala, Python 및 R용으로 구축된 애플리케이션 프로그래밍 인터페이스(API)를 통해 노출됩니다. 이러한 API는 간단한 상위 수준 연산자 뒤에 분산 처리의 복잡성을 숨깁니다.

## MLlib

기계 학습

Spark에는 대규모 데이터에 대한 기계 학습을 수행하는 알고리즘 라이브러리인 MLlib가 포함되어 있습니다. 기계 학습 모델은 모든 Hadoop 데이터 소스에서 R 또는 Python을 사용하여 데이터 사이언티스트가 훈련하고, MLlib를 사용하여 저장하고, Java 또는 Scala 기반 파이프라인으로 가져올 수 있습니다. Spark는 메모리에서 실행되는 빠른 대화형 계산을 위해 설계되어 기계 학습을 빠르게 실행할 수 있습니다. 알고리즘에는 분류, 회귀, 클러스터링, 협업 필터링 및 패턴 마이닝을 수행하는 기능이 포함됩니다.

## Spark Streaming

실시간

Spark Streaming은 Spark Core의 빠른 스케줄링 기능을 활용하여 스트리밍 분석을 수행하는 실시간 솔루션입니다. 미니 배치로 데이터를 수집하고 배치 분석을 위해 작성된 동일한 애플리케이션 코드를 사용하여 해당 데이터에 대한 분석을 가능하게 합니다. 이렇게 하면 배치 처리 및 실시간 스트리밍 애플리케이션에 동일한 코드를 사용할 수 있으므로 개발자 생산성이 향상됩니다. Spark Streaming은 Twitter, Kafka, Flume, HDFS, ZeroMQ 및 Spark 패키지 생태계에서 발견된 기타 여러 데이터를 지원합니다.

## Spark SQL

대화형 쿼리

Spark SQL은 MapReduce보다 최대 100배 빠른 지연 시간이 짧은 대화형 쿼리를 제공하는 분산 쿼리 엔진입니다. 여기에는 수천 개의 노드로 확장하는 동시에 빠른 쿼리를 위한 비용 기반 옵티마이저, 열 기반 스토리지 및 코드 생성이 포함됩니다. 비즈니스 분석가는 데이터 쿼리를 위해 표준 SQL 또는 Hive 쿼리 언어를 사용할 수 있습니다. 개발자는 Scala, Java, Python, R로 제공되는 API를 사용할 수 있으며 JDBC, ODBC, JSON, HDFS, Hive, ORC, Parquet 등 다양한 데이터 소스를 즉시 사용할 수 있습니다. 다른 인기 스토어(Amazon Redshift, Amazon S3, Couchbase, Cassandra, MongoDB, Salesforce.com, Elasticsearch 등)를 Spark Packages 생태계에서 찾을 수 있습니다.

{{<admonition tip>}}
대화형 쿼리(Interactive Query)는 사용자가 데이터베이스나 데이터 저장소에 대해 질의하고 결과를 즉시 확인할 수 있는 방식의 쿼리 처리 방법을 말합니다. 이는 일반적으로 실시간 또는 거의 실시간으로 데이터에 대한 질의와 분석을 수행할 때 사용됩니다.

대화형 쿼리 시스템은 다음과 같은 특징을 가집니다:

실시간 또는 거의 실시간 응답: 사용자가 쿼리를 실행하면 시스템은 즉시 결과를 반환하거나 매우 빠르게 처리하여 결과를 제공합니다. 이는 대규모 데이터셋에 대한 빠른 응답성을 보장하기 위해 필요합니다.

대화형 사용자 경험: 사용자는 쿼리를 실행한 후에도 추가 질문이나 분석을 계속할 수 있어야 합니다. 대화형 쿼리 시스템은 이러한 요구사항을 충족하기 위해 사용자가 원하는 만큼 자유롭게 질의하고 결과를 탐색할 수 있는 환경을 제공합니다.

실시간 데이터 처리: 대화형 쿼리는 종종 실시간 데이터 스트림에 대한 처리를 지원하여 실시간 분석과 모니터링을 가능하게 합니다.

스케일링 가능성: 대화형 쿼리 시스템은 대량의 데이터와 동시에 많은 수의 사용자 요청을 처리할 수 있어야 합니다. 이를 위해 수평 및 수직 스케일링이 가능해야 합니다.

복잡한 분석 기능 지원: 단순한 질의뿐만 아니라 집계, 조인, 필터링 등과 같은 복잡한 분석 기능도 지원해야 합니다.
{{</admonition>}}

## GraphX

그래프 프로세싱

Spark GraphX는 Spark를 기반으로 구축된 분산 그래프 처리 프레임워크입니다. GraphX는 ETL, 탐색적 분석 및 반복적 그래프 계산을 제공하여 사용자가 대화형 방식으로 그래프 데이터 구조를 대규모로 구축하고 변환할 수 있도록 합니다. 매우 유연한 API와 다양한 분산 그래프 알고리즘이 함께 제공됩니다.

# [Spark Architecture](https://seilylook.github.io/posts/spark-architecture/)

# [Spark RDD(Resilient Distributed Dataset)](https://seilylook.github.io/posts/spark-rdd/)

# [DataFrame APIs](https://seilylook.github.io/posts/spark-dataframe-api/)

