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

<img src="/images/spark2.png" />

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

# RDD

Resilient Distributed Datasets(RDDs)

- distrubuted collections of objects that can be cached in memory across cluster

- manipulated through pararrel operators

- automatically recomputed on failure

- immutable(read-only)

## RDD 연산

RDD 연산은 트랜스포메이션과 액션이 있습니다. 트랜스포메이션은 RDD를 이용해서 새로운 RDD를 생성하고, 액션은 RDD를 이용해서 작업을 처리하여 결과를 드라이버에 반환하거나, 파일시스템에 결과를 쓰는 연산입니다. 스파크는 트랜스포메이션을 호출할 때는 작업을 구성하고, 액션이 호출 될 때 실제 계산을 실행합니다.

다음의 예제에서 csv파일의 데이터를 읽어서 lines라는 RDD 객체를 생성하고, 각 라인의 글자의 개수를 세는 `map` 트랜스포메이션 함수를 호출하고, 글자 수의 총합을 구하는 `reduce` 액션 함수를 호출합니다. `map` 함수를 호출할 때는 작업이 진행되지 않고, `reduce` 함수를 호출할 때 클러스터에서 작업이 진행되는 것을 확인 할 수 있습니다.

```Scala
// RDD 객체 생성
scala> val lines = sc.textFile("/user/cctv_utf8.csv")
lines: org.apache.spark.rdd.RDD[String] = /user/shs/cctv_utf8.csv MapPartitionsRDD[7] at textFile at <console>:24

// map() 액션 호출시에는 반응 없음
scala> val lineLengths = lines.map(s => s.length)
lineLengths: org.apache.spark.rdd.RDD[Int] = MapPartitionsRDD[8] at map at <console>:26

// reduce 호출시 작업 처리
scala> val totalLength = lineLengths.reduce((a, b) => a + b)
[Stage 1:> (0 + 0) / 2]
totalLength: Int = 18531244
```

### Transformations

트랜스포메이션은 RDD를 이용하여 데이터를 변환하고 RDD를 반환하는 작업입니다. 주요함수는 다음과 같습니다.

| 함수                                    | 설명                                                                 |
| --------------------------------------- | -------------------------------------------------------------------- |
| map(func)                               | *func*로 처리된 새로운 데이터 셋 변환                                |
| filter(func)                            | *func*에서 true를 반환한 값으로 필터링                               |
| flatMap(func)                           | *func*는 배열(혹은 Seq)을 반환하고, 이 배열들을 하나의 배열로 반환   |
| distinct([numPartitions])               | 데이터셋의 중복을 제거                                               |
| groupByKey([numPartitions])             | 키를 기준으로 그룹핑 처리. (K, V) 쌍을 처리하여 (K, Iterable)로 반환 |
| reduceByKey(func, [numPartitions])      | 키를 기준으로 주어진 *func*로 처리된 작업 결과를 (K, V)로 반환       |
| sortByKey([ascending], [numPartitions]) | 키를 기준으로 정렬                                                   |

트랜스포메이션은 다음처럼 사용할 수 있습니다. cctvRDD를 이용하여 처리한 트랜스포메이션은 결과값으로 RDD를 반환합니다. take 액션이 호출되기 전에는 실제 작업을 진행하지 않습니다.

```Scala
// RDD 생성
scala> val cctvRDD = sc.textFile("/user/cctv_utf8.csv")
cctvRDD: org.apache.spark.rdd.RDD[String] = /user/cctv_utf8.csv MapPartitionsRDD[1] at textFile at <console>:24

// 라인을 탭단위로 분리하여 첫번째 아이템 반환
scala> val magRDD = cctvRDD.map(line => line.split("\t")(0))
magRDD: org.apache.spark.rdd.RDD[String] = MapPartitionsRDD[3] at map at <console>:26

// 중복 제거
scala> val distRDD = magRDD.distinct()
distRDD: org.apache.spark.rdd.RDD[String] = MapPartitionsRDD[9] at distinct at <console>:28

// 중복 제거한 데이터를 10개만 출력
scala> distRDD.take(10).foreach(println)
성남둔치공영주차장
울산 동구청
```

### Actions

액션은 RDD를 이용하여 작업을 처리한 결과를 반환하는 작업입니다. 주요 함수는 다음과 같습니다.

| 함수                 | 설명                                                                                      |
| -------------------- | ----------------------------------------------------------------------------------------- |
| reduce(func)         | *func*를 이용해 데이터를 집계(두 개의 인수를 받아서 하나를 반환). 병렬 처리가 가능해야 함 |
| collect()            | 처리 결과를 배열로 반환. 필터링 등 작은 데이터 집합을 반환하는데 유용                     |
| count()              | 데이터의 개수 반환                                                                        |
| first()              | 데이터셋의 첫번째 아이템 반환(take(1)과 유사)                                             |
| take(n)              | 데이터셋의 첫번째부터 n개의 배열을 반환                                                   |
| saveAsTextFile(path) | 데이터셋을 텍스트 파일로 지정한 위치에 저장                                               |
| countByKey()         | 키를 기준으로 카운트 반환                                                                 |
| foreach(func)        | 데이터셋의 각 엘리먼트를 func로 처리. 보통 Accumulator와 함께 사용                        |

액션은 다음처럼 사용할 수 있습니다. cctvRDD를 이용하여 처리한 액션은 결과를 드라이버(스파크쉘)에 반환하거나, 파일로 저장할 수 있습니다.

```Scala
// RDD 생성
scala> val cctvRDD = sc.textFile("/user/cctv_utf8.csv")
cctvRDD: org.apache.spark.rdd.RDD[String] = /user/cctv_utf8.csv MapPartitionsRDD[1] at textFile at <console>:24

// 첫번째 라인 반환
scala> cctvRDD.first()
res0: String = 관리기관명    소재지도로명주소    소재지지번주소 설치목적구분  카메라대수   카메라화소수  촬영방면정보  보관일수    설치년월    관리기관전화번호    위도  경도  데이터기준일자 제공기관코드  제공기관명

// 10개의 라인을 출력
scala> cctvRDD.take(10).foreach(println)
관리기관명   소재지도로명주소    소재지지번주소 설치목적구분  카메라대수   카메라화소수  촬영방면정보  보관일수    설치년월    관리기관전화번호    위도  경도  데이터기준일자 제공기관코드  제공기관명
제주특별자치도 제주특별자치도 제주시 동문로9길 3 제주특별자치도 제주시 건입동 1120    생활방범    1       청은환타지아 북측 4가    30      064-710-8855    33.5132891  126.5300275 2018-04-30  6500000 제주특별자치도

// 텍스트 파일로 지정한 위치에 저장
scala> cctvRDD.saveAsTextFile("/user/cctvRDD")
[Stage 7:>                                                          (0 + 0) / 2]

// 저장한 파일을 확인
$ hadoop fs -ls /user/cctvRDD/
Found 3 items
-rw-r--r--   2 hadoop hadoop          0 2019-01-22 04:05 /user/cctvRDD/_SUCCESS
-rw-r--r--   2 hadoop hadoop   15333006 2019-01-22 04:05 /user/cctvRDD/part-00000
-rw-r--r--   2 hadoop hadoop   15332503 2019-01-22 04:05 /user/cctvRDD/part-00001
```

### 함수 전달

RDD 연산을 처리할 때 매번 작업을 구현하지 않고, 함수로 구현하여 작업을 처리할 수도 있습니다.

함수를 전달 할 때는 외부의 변수를 이용하지 않는 순수 함수를 이용하는 것이 좋습니다. 클러스터 환경에서 외부 변수의 사용은 잘 못된 결과를 생성할 가능성이 높기 때문입니다.

```Scala
// RDD에 map, reduce 함수를 람다함수로 전달
scala> cctvRDD.map(line => line.length).reduce((a, b) => a + b)
res12: Int = 18531244

// 함수 구현체
object Func {
  // line의 길이를 반환하는 함수
  def mapFunc(line: String): Int = { line.length }
  // a, b의 합을 반환하는 함수
  def reduceFunc(a:Int, b:Int): Int = { a + b }
}

// RDD에 mapFunc, reduceFunc를 전달
scala> cctvRDD.map(Func.mapFunc).reduce(Func.reduceFunc)
res11: Int = 18531244
```

### 캐쉬 이용

RDD는 처리 결과를 메모리나 디스크에 저장하고 다음 계산에 이용할 수 있습니다. 반복작업의 경우 이 캐쉬를 이용해서 처리 속도를 높일 수 있습니다. 하지만 단일작업의 경우 데이터 복사를 위한 오버헤드가 발생하여 처리시간이 더 느려질 수 있습니다. 따라서 작업의 종류와 영향을 파악한 후에 캐슁을 이용하는 것이 좋습니다.

RDD는 `persist()`, `cache()` 메소드를 이용하여 캐슁을 지원합니다. 캐슁한 데이터에 문제가 생기면 자동으로 복구합니다. 또한 저장 방법을 설정할 수 있어서, 메모리나 디스크에 저장 할 수도 있습니다.

| 설정            | 설명                                                                                     |
| --------------- | ---------------------------------------------------------------------------------------- |
| MEMORY_ONLY     | RDD를 메모리상에 저장. 메모리보다 용량이 크면 일부만 저장하고 필요할 때마다 계산. 기본값 |
| MEMORY_AND_DISK | RDD를 메모리상에 저장. 메모리보다 용량이 크면 일부는 메모리, 일부는 디스크에 저장        |
| DISK_ONLY       | RDD를 디스크에 저장                                                                      |

```Scala
val txts = sc.textFile("/user/sample.txt")
val pairs = txts.flatMap(line => line.split(" ")).map(word => (word, 1))

// 각 단계의 결과를 캐슁
scala> pairs.persist()
res39: pairs.type = MapPartitionsRDD[36] at map at <console>:26

val counts = pairs.reduceByKey(_ + _)
scala> counts.persist()
res38: counts.type = ShuffledRDD[37] at reduceByKey at <console>:28
```

### Key, Value를 이용한 처리

스파크는 MapReduce처럼 (key, value)쌍을 이용한 처리도 가능합니다. 기본적으로 제공하는 `flatMap`, `reduceByKey`, `groupByKey`, `mapValues`, `sortByKey`를 이용해서 좀 더 편리한 처리가 가능합니다.

다음의 워드 카운트는 키, 밸류를 이용한 처리를 확인할 수 있습니다. 파일의 데이터를 읽어서 `flatMap`를 이용하여 단어별로 분리하고, `map`을 이용하여 단어의 개수를 세어줍니다. `reduceByKey`를 이용하여 단어별로 그룹화 하여 단어가 나타난 개수를 세어줍니다.

```Scala
val txts = sc.textFile("/user/sample.txt")
val pairs = txts.flatMap(line => line.split(" ")).map(word => (word, 1))
val counts = pairs.reduceByKey(_ + _)

scala> counts.take(10).foreach(println)
(under,1)
(better.,1)
(goals,1)
(call,3)
(its,7)
(opening,1)
(extraordinary,1)
(internationalism，to,1)
(have,4)
(include,2)
```

### Accumulator

스파크는 PC에서 단독으로 처리되는 것이 아니라 클러스터에서 처리하기 때문에 클로져1를 이용하면 결과가 달라질 수 있습니다.

다음의 예제와 같이 `foreach()` 반복문에 외부에 선언된 `sumValue` 변수에 모든 값을 더하는 함수를 실행하면 실행 모드(local vs cluster)에 따라 결과가 달라 질 수 있습니다. 로컬 모드에서는 원하는 결과가 나오지만, 클러스터 모드에서는 각 노드에서 로컬의 `sumValue` 변수의 값을 이용하여 작업을 처리하기 때문에 결과가 달라집니다.

```Scala
// 모든 데이터를 sumValue에 합함
var sumValue = 0
var rdd = sc.parallelize(Array(1, 2, 3, 4, 5))
rdd.foreach(x => sumValue += x)

// 원하는 결과가 나오지 않음
scala> println("sum value: " + sumValue )
sum value: 0
```

스파크에서 맵리듀스의 카운터와 유사한 역활을 하는 Accmulator를 이용하여 모든 노드가 공유할 수 있는 변수를 선언해 주어야 합니다. Accmulator는 스파크 컨텍스트를 이용해서 생성합니다. 사용법은 다음과 같습니다.

```Scala
var sumValue = sc.longAccumulator("Sum Accumulator")
var rdd = sc.parallelize(Array(1, 2, 3, 4, 5))
rdd.foreach(x => sumValue.add(x))

// Accmulator를 이용하여 값 처리
scala> println("sum value: " + sumValue.value)
sum value: 15
```

### Broadcast

브로드 캐스트는 맵리듀스의 디스트리뷰트 캐쉬(distribute cache)와 유사한 역활을 하는 모든 노드에서 공유되는 읽기 전용 값입니다. broadcast() 이용하여 사용할 수 있습니다. 조인에 이용되는 값들을 선언하여 이용할 수 있습니다.

다음의 예제에서 broadcastVar 변수는 클러스터의 모든 노드에서 사용할 수 있는 값이 됩니다.

```Scala
scala> val broadcastVar = sc.broadcast(Array(1, 2, 3))
broadcastVar: org.apache.spark.broadcast.Broadcast[Array[Int]] = Broadcast(0)

scala> broadcastVar.value
res0: Array[Int] = Array(1, 2, 3)
```

### Shuffle

스파크에서 조인, 정렬 작업은 셔플(Shuffle) 작업을 실행합니다. 셔플은 파티션간에 그룹화된 데이터를 배포하는 메커니즘입니다. 셔플은 임시 파일의 복사, 이동이 있기 대문에 많은 비용이 들게 됩니다.

### Lazy Evaluation

Lazy Evaluation means when calling a transformation on an RDD(map), the operation is not immmediately performed.

Spark internally records metadata to indicate that this operation is requested. It is best to think of each RDD as consisting of instructions on how to compute the data of transformations.

### 정리

- Transformations mean `setting` functions.

- Actions mean `performing` the functions.

# DataFrame

DataFrame is a programming abstraction in the Spark SQL module. DataFrames resemble relational database tables or excel spreadsheets with headers: the data resides in rows and columns of different datatypes.

