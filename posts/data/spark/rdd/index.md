# Rdd


# RDD

Resilient Distributed Datasets(RDDs)

- distrubuted collections of objects that can be cached in memory across cluster

- manipulated through pararrel operators

- automatically recomputed on failure

- immutable(read-only)

<img src="/images/data/data/spark/spark-rdd.png"/>

## RDD 연산

RDD 연산은 트랜스포메이션과 액션이 있습니다. 트랜스포메이션은 RDD를 이용해서 새로운 RDD를 생성하고, 액션은 RDD를 이용해서 작업을 처리하여 결과를 드라이버에 반환하거나, 파일시스템에 결과를 쓰는 연산입니다. 스파크는 트랜스포메이션을 호출할 때는 작업을 구성하고, 액션이 호출 될 때 실제 계산을 실행합니다.

다음의 예제에서 csv파일의 데이터를 읽어서 lines라는 RDD 객체를 생성하고, 각 라인의 글자의 개수를 세는 `map` 트랜스포메이션 함수를 호출하고, 글자 수의 총합을 구하는 `reduce` 액션 함수를 호출합니다. `map` 함수를 호출할 때는 작업이 진행되지 않고, `reduce` 함수를 호출할 때 클러스터에서 작업이 진행되는 것을 확인 할 수 있습니다.

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

### 함수 전달

RDD 연산을 처리할 때 매번 작업을 구현하지 않고, 함수로 구현하여 작업을 처리할 수도 있습니다.

함수를 전달 할 때는 외부의 변수를 이용하지 않는 순수 함수를 이용하는 것이 좋습니다. 클러스터 환경에서 외부 변수의 사용은 잘 못된 결과를 생성할 가능성이 높기 때문입니다.

### 캐쉬 이용

RDD는 처리 결과를 메모리나 디스크에 저장하고 다음 계산에 이용할 수 있습니다. 반복작업의 경우 이 캐쉬를 이용해서 처리 속도를 높일 수 있습니다. 하지만 단일작업의 경우 데이터 복사를 위한 오버헤드가 발생하여 처리시간이 더 느려질 수 있습니다. 따라서 작업의 종류와 영향을 파악한 후에 캐슁을 이용하는 것이 좋습니다.

RDD는 `persist()`, `cache()` 메소드를 이용하여 캐슁을 지원합니다. 캐슁한 데이터에 문제가 생기면 자동으로 복구합니다. 또한 저장 방법을 설정할 수 있어서, 메모리나 디스크에 저장 할 수도 있습니다.

| 설정            | 설명                                                                                     |
| --------------- | ---------------------------------------------------------------------------------------- |
| MEMORY_ONLY     | RDD를 메모리상에 저장. 메모리보다 용량이 크면 일부만 저장하고 필요할 때마다 계산. 기본값 |
| MEMORY_AND_DISK | RDD를 메모리상에 저장. 메모리보다 용량이 크면 일부는 메모리, 일부는 디스크에 저장        |
| DISK_ONLY       | RDD를 디스크에 저장                                                                      |

### Key, Value를 이용한 처리

스파크는 MapReduce처럼 (key, value)쌍을 이용한 처리도 가능합니다. 기본적으로 제공하는 `flatMap`, `reduceByKey`, `groupByKey`, `mapValues`, `sortByKey`를 이용해서 좀 더 편리한 처리가 가능합니다.

다음의 워드 카운트는 키, 밸류를 이용한 처리를 확인할 수 있습니다. 파일의 데이터를 읽어서 `flatMap`를 이용하여 단어별로 분리하고, `map`을 이용하여 단어의 개수를 세어줍니다. `reduceByKey`를 이용하여 단어별로 그룹화 하여 단어가 나타난 개수를 세어줍니다.

### Accumulator

스파크는 PC에서 단독으로 처리되는 것이 아니라 클러스터에서 처리하기 때문에 클로져1를 이용하면 결과가 달라질 수 있습니다.

다음의 예제와 같이 `foreach()` 반복문에 외부에 선언된 `sumValue` 변수에 모든 값을 더하는 함수를 실행하면 실행 모드(local vs cluster)에 따라 결과가 달라 질 수 있습니다. 로컬 모드에서는 원하는 결과가 나오지만, 클러스터 모드에서는 각 노드에서 로컬의 `sumValue` 변수의 값을 이용하여 작업을 처리하기 때문에 결과가 달라집니다.

### Broadcast

브로드 캐스트는 맵리듀스의 디스트리뷰트 캐쉬(distribute cache)와 유사한 역활을 하는 모든 노드에서 공유되는 읽기 전용 값입니다. broadcast() 이용하여 사용할 수 있습니다. 조인에 이용되는 값들을 선언하여 이용할 수 있습니다.

다음의 예제에서 broadcastVar 변수는 클러스터의 모든 노드에서 사용할 수 있는 값이 됩니다.

### Shuffle

스파크에서 조인, 정렬 작업은 셔플(Shuffle) 작업을 실행합니다. 셔플은 파티션간에 그룹화된 데이터를 배포하는 메커니즘입니다. 셔플은 임시 파일의 복사, 이동이 있기 대문에 많은 비용이 들게 됩니다.

### Lazy Evaluation

Lazy Evaluation means when calling a transformation on an RDD(map), the operation is not immmediately performed.

Spark internally records metadata to indicate that this operation is requested. It is best to think of each RDD as consisting of instructions on how to compute the data of transformations.

### 정리

- Transformations mean `setting` functions.

- Actions mean `performing` the functions.



