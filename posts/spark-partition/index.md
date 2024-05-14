# Spark Partition


# What is Partition?

Partition은 RDDs나 Dataset을 구성하고 있는 최소 단위 객체이다. 각 Partition은 서로 다른 노드에서 분산 처리된다.

Spark에서는 하나의 최소 연산을 `Task`라고 표현하는데, 이 하나의 Task에서 하나의 Partition이 처리된다. 또한, 하나의 Task는 하나의 `Core`가 연산 처리한다.

즉, **1 Core = 1 Task = 1 Partition**이다.

예를 들어, 다음과 같다면 전체 Core 수를 300개로 세팅한 상태이고, 이 300개가 현재 실행 중인 Task 수이자, 현재 처리 중인 Partition 수에 해당한다. 또한, 전체 Partition 수는 1800개로 세팅했으며, 이는 전체 Task 수이기도 하다.

<img src="/images/spark/spark-partition-1.png"/>

이처럼 설정된 Partition 수에 따라 각 Partition의 크기가 결정된다. 그리고 이 Partition의 크기가 결국 Core 당 필요한 메모리 크기를 결정한다.

**Partion 수 -> Core 수**

**Partition 크기 -> 메모리 크기**

따라서, Partition의 크기와 수가 Spark 성능에 큰 영향을 미치는데, 통상적으로는 Partition 크기가 클수록 메모리가 더 필요하고, Partition의 수가 많을 수록 Core가 더 필요하다.

**적은 수의 Partition = 크기가 큰 Partition**

**많은 수의 Partition = 크기가 작은 Partition**

즉, Partition의 수를 늘리는 것은 Task 당 필요한 메모미를 줄이고 병렬화의 정도를 늘린다.

# Spark Partition 종류

동일한 Partition이지만, 쓰이는 때에 따라 다음의 3가지로 구분할 수 있다.

**Input Partition**

**Output Partition**

**Shuffle Partition**

이 중, Spark의 주요 연산이 Shuffle인 만큼, Shuffle Partition이 가장 중요하다.

## Input Partition

관련 설정: spark.sql.files.maxpartitionBytes

Input Partition은 처음 파일을 읽을 때 생성하는 Partition이다. 관련 설정값은 spark.sql.files.maxPartitionBytes로, Input Partition 크기를 설정할 수 있고, 기본값은 134217728(128MB)이다.

파일(HDFS 상의 마지막 경로에 존재하는 파일)의 크기가 128MB보다 크다면, Spark에서 128MB만큼 쪼개면서 파일을 읽는다. 파일의 크기가 128MB보다 작다면 그대로 읽어 들여, 파일 하나당 Partition 하나가 된다.

대부분의 경우, 필요한 칼럼만 골라서 뽑아 쓰기 때문에 128MB보다 작다. 가끔씩 큰 파일을 다룰 경우에는 이 설정값을 조절해야 한다.

<img src="/images/spark/spark-partition-2.png"/>

## Output Partition

관련 설정: df.repartition(cnt), df.coalesce(cnt)

Output Partition은 파일을 저장할 때 생성하는 Partition이다. 이 Partition의 수가 HDFS 상의 마지막 경로의 파일 수를 지정한다.

기본적으로, HDFS는 큰 파일을 다루도록 설계되어 있어, 크기가 큰 파일로 저장하는 것이 좋다.

보통 HDFS Blocksize에 맞게 설정하면 되는데, 카카오 Hadoop 클러스터의 HDFS Blocksize는 268435456 (256MB)로 설정되어 있어서, 통상적으로 파일 하나의 크기를 256MB에 맞도록 Partition의 수를 설정하면 된다.

Partition의 수는 df.repartition(cnt), df.coalesce(cnt)를 통해 설정한다. 이 repartition과 coalesce를 이용해 Partition 수를 줄일 수 있다.

아래의 예시는, 파일 수를 줄여 50개로 저장하는 모습이다.

<img src="/images/spark/spark-partition-3.png" />

Use Case

- 보통 groupBy 집계 후 저장할 때 데이터의 크기가 작아집니다. 그런 다음 spark.sql.shuffle.partitions 설정에 따라 파일 수가 지정되는데, 이때 파일의 크기를 늘리기 위해 repartition와 coalesce을 사용해 Partition 수를 줄일 수 있다.

- df.where()를 통해 필터링을 하고 나서 그대로 저장한다면 파편화가 생깁니다. 그래서 repartition(cnt)을 한 후 저장한다.

## Shuffle Partition

관련 설정: spark.sql.shuffle.partitions

Spark 성능에 가장 큰 영향을 미치는 Partition으로, `Join`, `groupBy` 등의 연산을 수행할 때 Shuffle Partition이 쓰인다.

설정값은 spark.sql.shuffle.partitions이고, 이 설정값에 따라 Join, groupBy 수행 시 Partition의 수(또는 Task의 수)가 결정된다.

<img src="/images/spark/spark-partition-4.png" />

이 설정값은 Core 수에 맞게 설정하라고 하지만, Partition의 크기에 맞추어 설정해야 한다.

이 Partition의 크기가 크고 연산에 쓰이는 메모리가 부족하다면 Shuffle Spill(데이터를 직렬화하고 스토리지에 저장, 처리 이후에는 역직렬화하고 연산 재개함)이 발생하기 때문이다.

Shuffle Spill이 발생하면, Task가 지연되고 에러가 발생할 수 있다. 또한, Hadoop 클러스터의 사용률이 높다면, 연달아 에러가 발생하고 Spark가 강제 종료될 수 있다.

Memory Limit Over와 같이, Shuffle Spill도 메모리 부족으로 나타나는데, 보통 이에 대한 대응을 Core 당 메모리를 늘리는 것으로 해결한다. 하지만, 모든 사람이 메모리가 부족하다고 메모리 할당량을 늘린다면, 클러스터가 사용성이 더 떨어지고 작업이 더욱 실패할 것이다. 그래서 개인적으로, Partition의 크기를 결정하는 옵션인 Spark.sql.shuffle.partitions를 우선적으로 고려해 설정해야 한다.

또한, 일반적으로 하나의 Shuffle Partition 크기가 100 ~ 200MB 정도 나올 수 있도록 spark.sql.shuffle.partitions 수를 조절하는 것이 최적이다.

Use Case

- Memory Limit Over, Memory Spill 등 자원 문제가 생길 경우, Shuffle Partition 크기를 우선적으로 고려해야 한다.

# Partition 최적화

최적화의 우선 순위는 **쿼리 > Partition 수 > Core 당 메모리 증가**이다.

쿼리는 최대한 `groupBy`로 집계를 한 후 `join`을 하고 그 다음에 Partition 수를 조절한 다음, 그래도 안된다면 `Core` 당 메모리를 증가시켜야 한다.

Partition 수를 증가시킨다면 Task 수도 늘어나서 실행 시간이 증가될 수 있지만, Shuffle Spill이 일어나지 않도록 한다면 시간이 더 감소한다. 따라서 Shuffle Spill이 일어나지 않게 하는 선인 Shuffle Partition의 크기를 100 ~ 200MB로 설정하는 것이 최적이다.

단, 대부분의 데이터 처리에서 위의 설정이 적합하지만, Shuffle Size가 600GB에 가깝거나 그 이상일 경우에는 Core 당 메모리를 증가시키는 것을 권장한다. 보통 Shuffle Size가 600GB 이상이 되면 1 코어당 4GB를 고려하는 것을 권장한다.

Cartesian join(cross join) 사용으로 Row 수가 급격하게 증가한 경우에도 Shuffle Size가 커지기 때문에 메모리 증가를 고려해야 한다.

이 외에도, Spark ML을 사용하거나 Caching을 하는 경우, Spark 메모리 구조 중 Storage Memory Fraction 부분에서 캐싱을 하게 되는데, 이렇게 되면 연산(Execution)을 해야 하는 부분이 줄어들어 결국에는 메모리를 증대해야 한다.

- Storage 메모리: Spark의 Cache 데이터 저장을 위해 사용

- Execution 메모리: Shuffle, Join, Sort, Aggregation 등의 연산 과정에서 임시 데이터 저장을 위해 사용

<img src="/images/spark/spark-partition-5.png" />

# 정리

- Shuffle Spill이 일어난다면 에러가 발생해 작업이 지연될 수 있다. 그리고 Hadoop 클러스터가 busy 상태인 경우, 연달아 에러가 발생하고 강제 종료될 수 있다.

- 메모리가 부족하다면, 우선적으로 Shuffle Partition 수를 고려해야 한다.

- Shuffle Partition의 크기를 100MB~200MB 사이로 나오도록 spark.sql.Shuffle.Partitions를 설정해야 한다.

