# AQE


{{<admonition info>}}
Partition은 RDDs나 Dataset를 구성하고 있는 최소 단위 객체입니다. 각 Partition은 서로 다른 노드에서 분산 처리됩니다. Spark에서는 하나의 최소 연산을 **Task**라고 표현하는데, 이 하나의 Task에서 하나의 **Partition**이 처리됩니다. 또한, 하나의 Task는 하나의 **Core**가 연산 처리합니다.

즉, 1 Core = 1 Task = 1 Partition입니다.

설정된 Partition 수에 따라 각 Partition의 크기가 결정됩니다. 그리고 이 Partition의 크기가 결국 Core 당 필요한 메모리 크기를 결정하게 됩니다.

◼️ Partition 수 → Core 수

◼️ Partition 크기 → 메모리 크기

따라서, Partition의 크기와 수가 Spark 성능에 큰 영향을 미치는데, 통상적으로는 Partition의 크기가 클수록 메모리가 더 필요하고, Partition의 수가 많을수록 Core가 더 필요합니다.

◼️ 적은 수의 Partition = 크기가 큰 Partition

◼️ 많은 수의 Partition = 크기가 작은 Partition
{{</admonition>}}

# AQE란?

AQE(Adaptive Query Execution) 최적화는 이름 그대로 shuffle이 끝난 다음 partition을 coalesce(병합)를 해주는 기능입니다. 너무 많은 partition은 많은 task가 필요하거나 I/O를 많이 유발할 수 있기 때문에 적절한 수가 필요한데, AQE 기능이 적절한 partition의 수를 정해 줍니다.

AQE 기능은, 설정에서 spark.sql.adaptive.enabled와 spark.sql.adaptive.coalescePartitions.enabled가 true 일 때 작동합니다. Spark 3.2 버전부터는 default 값이 true이므로 자동으로 적용이 됩니다.

그리고 AQE 기능은 기본적으로 coalesce를 실행하므로 충분히 많은 수의 partition을 설정해야 합니다. AQE의 Partition 수는 spark.sql.adaptive.coalescePartitions.initialPartitionNum으로 설정할 수 있습니다. 이 값이 설정되어 있지 않으면 spark.sql.shuffle.partitions 값을 따라가게 됩니다.

## AQE와 Query Stages

AQE의 구현에 있어 중요한 결정 요소는 언제 재-최적화를 수행할 것인가에 대한 것 입니다. 스파크 오퍼레이터는 주로 파이프라인 형태로 병렬 프로세스로 실행되게 됩니다. 그러나 셔플 또는 브로드캐스트 exchange는 이러한 파이프라인을 끊습니다. 이 부분은 materialization points라고 불리며 Query states라는 용어로 불립니다.

```sql
SELECT x, AVG(y)
FROM t
GROUP BY x
ORDER BY avg(Y)
```

예를 들어, 위와 같은 쿼리는 아래와 같은 쿼리 계획과 materialization point(Pipeline Breadk Point) 그리고 Query state를 가집니다:

<img src="/images/spark/spark-aqe-1.png"/>

각 Query state는 중간 결과물을 materialize하고 이후의 stage는 반드시 해당 query state의 모든 병렬 처리가 materialize 된 이후에만 진행이 가능합니다. 모든 파티션에 대한 통계치가 존재하고 이후의 연산은 아직 시작되지 않은 시점이기에 이 materialization point는 자연적으로 매우 좋은 재-최적화 지점이 됩니다.

쿼리 수행이 시작되면 AQE는 처음에는 모든 Leaf stages를 시작한다. 이러한 stages들이 materialization을 끝내면, 물리적 쿼리 계획에서 종료된 것으로 표시하고, 완료된 stages로부터 얻은 통계치를 가지고 이후의 논리적 계획을 업데이트 합니다. 또한 이러한 새로운 통계치에 기반해서 프레임워크는 옵티마이저, 물리적 플래너, 물리적 최적화 룰(일반적인 물리적 룰과 AQE의 여러 룰을 포함-아래)을 수행하게 됩니다.

## Dynamically coalescing shuffle partitions

셔플 파티션 숫자와 사이즈는 쿼리 성능에 매우 직결됩니다. 파티션의 크기가 너무 크거나, 작으면 아래와 같은 문제가 발생할 수 있습니다:

| 파티션이 너무 작을 때 |   파티션이 너무 클 때   |
| :-------------------: | :---------------------: |
|    비효율적인 I/O     | Garbage Collection 부하 |
|  스케줄러의 오버헤드  |      Disk Spilling      |
|  Task 셋업 오버헤드   |

**Dynamically coalescing shuffle partitions** 기능은 동적으로 셔플 파티션 수를 줄일 수 있도록 하여, 기존의 정적 파티션 숫자 설정 기능에서 발생하는 것과 같이 너무 크거나 작은 파티션 사이즈의 문제를 피하며 성능을 개선합니다. 최초의 파티션 숫자는 큰 데이터 사이즈를 감당할 수 있도록 크게 설정하고, 쿼리 state에서 필요하다면 자동적으로 파티션 수를 줄이게 됩니다.

<img src="/images/spark/spark-aqe-2.png"/>

기존의 정적 파티션 숫자 설정은 아래와 같이 초기에 설정된 파티션 숫자를 끝까지 사용하기에 작은 파티션 사이즈가 존재하게 됩니다:

<img src="/images/spark/spark-aqe-3.png"/>

하지만, AQE가 적용된 경우에는 Coalescing이 자동적으로 수행되어 파티션 숫자가 동적으로 설정되어 낮아지며 작은 파티션 사이즈의 문제를 피할 수 있게 됩니다.

<img src="/images/spark/spark-aqe-4.png"/>

## Dynamically switching join strategies

스파크는 join의 대상인 2개의 데이터 중 하나 이상이 메모리에 로드되기에 충분히 작다면 Broadcast Hash Join을 선택합니다. 하지만, 수행 초기 시점에 행한 데이터 크기에 대한 예측이 틀릴 수 있으며 이는 Broadcast Hash Join로 수행될 수 있는 기회를 놓치게 만듭니다. 그러한 틀린 예측은 아래와 가은 이유로 발생하게 됩니다:

- Cardinality 또는 Selectivity 예측을 위한 통계가 부정확할 수 있음

- 대상 데이터가 여러 오퍼레이터의 복잡한 서브 트리일 수 있음

- UDFs와 같이 블랙박스 predicates이여서 초기 기점에 통계치 계산이 불가능할 수 있음

AQE의 Dynamically switching join strateges 기능은 **런타임 시의 정보를 바탕으로 join 전략을 다시 계획**할 수 있도록 합니다.

<img src="/images/spark/spark-aqe-5.png"/>

위와 같이 초기의 Sort Merge Join 전략이, 런타임 시 정보가 업데이트 되어 특정 데이터 대상이 충분히 작다는 사실을 인지하게 되고 Broadcast Hash Join로 변경되게 됩니다.

## Dynamically optimizing skew joins

AQE의 3번째 기능은 동적으로 skew가 존재하는 join을 최적화하는 기능입니다. 데이터 skew는 셔플 시에 특정 키에 값이 치우쳐져서 많이 존재하고 셔플 시에는 해당 셔플의 병렬 처리가 모두 종료되고 나서 다음 단계의 처리르 수행할 수 있기에 모든 병렬 처리가 빨리 끝나도 다음 단계로 넘어가기 위해서 가장 늦은 처리를 기다릴 수 밖에 없게 만듭니다. 그리고 이 부분은 성능을 매우 저하시키게 됩니다.

AQE의 Dynamically optimizing skew joins 기능은 런타임 통계치를 사용해

1. 파티션 사이즈로부터 skew를 디렉팅하고

2. skew 파티션을 더 작은 서브 파티션들로 나눕니다.

<img src="/images/spark/spark-aqe-6.png"/>

위와 같은 join 시에, 오른쪽과 같이 skew reader가 skew 파티션의 존재 여부를 파악하고 존재한다면 서브 파티션을 생성하게 됩니다.

파티션의 사이즈를 중점적으로 살펴보면, 일반적인 경우 A0 파티션에 더욱 상대적으로 많은 데이터가 존재하고, A1, A2, A3 파티션의 처리가 모두 끝나도 다음 단계의 수행을 위해서 A0 처리 종료를 기다리게 됩니다.

<img src="/images/spark/spark-aqe-7.png"/>

AQE가 적용되게 되면 아래와 같이 동적으로 skew 파티션을 쪼개 병렬처리하게 되면서, 더욱 빠르게 셔플 단계의 처리가 수행되게 됩니다.

<img src="/images/spark/spark-aqe-8.png"/>

