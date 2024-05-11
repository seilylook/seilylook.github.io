# Spark QA Note


# Test 1

## Question

Which of the following options describes the responsibility of the executors in Spark?

## Answer

> The executors accept tasks from the driver, execute those tasks, and return results to the driver.

## 6

{{<admonition question>}}
Which of the following is the deepest level in Spark's execution hierarchy ?
{{</admonition>}}

{{<admonition success>}}
Task
{{</admonition>}}

{{<admonition info "Description" true>}}
The hierarchy is, from top to bottom: **Job, State, Task**.

Executors and slots facilitate the execution of tasks, but they are not directly part of the hierarchy. Executors are launched by the driver on worker nodes for the purpose of running a specific Spark application. Slots help Spark parallelize work. An executor can have multiple slots which enable it to process multiple tasks in parallel.
{{</admonition>}}

## 7

{{<admonition question>}}
Which of the following satement about garbage collection in Spark is incorrect?
{{</admonition>}}

{{<admonition success>}}
Manually persisting RDDs in Spark prevents them from being garbage collected.
{{</admonition>}}

# 9

{{<admonition question>}}
Which of the following describes the difference between client and cluster execution modes?
{{</admonition>}}

{{<admonition success>}}
In cluster mode, the driver runs on the worker nodes, while the client mode runs the driver on the client machine
{{</admonition>}}

{{<admonition info "Description" true>}}
**In cluster mode, the driver runs on the master node, while in client mode, the driver runs on a virtual machine in the cloud**

This is wrong, since execution modes do not specify whether workloads are run in the cloud or on-premise.
{{</admonition>}}

## 15

{{<admonition question>}}
Which of the following is a viable way to improve Spark's perfomance when dealing with large amounts of data, given that ehrer is only a single application running on the cluster?
{{</admonition>}}

{{<admonition success>}}
Increase values for the properties `spark.default.parallelism` and `spark.sql.shuffle.partitions`
{{</admonition>}}

## 21

{{<admonition question>}}
Which of the following code blocks can be used to save DataFrame `transactionsDf` to memory only, recalculating partitions that do not fit in memory when they are needed?
{{</admonition>}}

{{<admonition success>}}

```python
from pyspark import StorageLevel

transactionDf.persist(StorageLevel.MEMORY_ONLY)
```

{{</admonition>}}

{{<admonition info "Description" true>}}
**transactionsDf.cache()**

This is
{{</admonition>}}

{{<admonition question>}}
Which of the following code blocks saves DataFrame `transactionDf` in location `/FileStore/transactions.csv` as a CSV file and throws an error if a file already exists in the location?
{{</admonition>}}

{{<admonition success>}}

```python
trnsactionsDf.write.format("csv").mode("error").save("/FileStore/transactions.csv")
```

{{</admonition>}}

# 41

{{<admonition question>}}
Which of the following blocks createds a new DataFrame with two columns `season` and `wind_speed_ms` where column `season` is of date type `string` and colum `wind_speed_ms` is of data type `double`?
{{</admonition>}}

{{<admonition success>}}

```python
spark.createDataFrame([("summer", 4.5), ("winter", 7.5)], ["season", "wind_speed_ms"])
```

{{</admonition>}}

## 49

{{<admonition question>}}
Which of the following code blocks returns about 150 randomly selected rows from the 1000-row DataFrame `transactionsDf`, assuming that any row can appear more than once in the returned DataFrame?
{{</admonition>}}

{{<admonition success>}}

```python
transactionsDf.sample(True, 0.15, 8261)
```

{{</admonition>}}

{{<admonition info "Description" true>}}
`DataFrame.sample(withReplacement=None, fraction=None, seed=None)`
{{</admonition>}}

