# Dependency


# Introduction

Transformations are operations on RDDs, Dataframes, or Dataset, that produce new RDDs, Dataframes, or Datasets. Transformations are **lazy evaluated**, which means they are not executed until an action is called.

Spark uses transformation to build a DAG(Directed Acyclic Graph) of computation that represents the sequence of steps required to compute the final result. Transformations can be categorized as either `Narrow` or `Wide` based on whether their dependency on input data partitions.

<img src="/images/data/spark/spark-dependency.webp"/>

## Narrow dependency(transformation)

A narrow transformation is a transformation that need to operate only on a single parition of input data to produce one partition of output data. These transformations do not require shuffling of data between partitions. They can be executed on a single partition without needing to exchange data with other partitions.

<img src="/images/data/spark/narrow-dependency.webp"/>

Here, are some examples are narrow dependencies:

1. Map transformation: In this transformation, each input element of the parent Dataframe is transformed to a single output element of the child Dataframe. Since each output element depends on only one input element, it is a narrow dependency.

2. Filter transformation: In this transformation, each partition of the parent Dataframe is filtered based on a predicate function, resulting in a child Dataframe with only the elements that satisfy the predicate. Since each partition of the child Dataframe depends on only one partition of the parent Dataframe, it is a narrow dependency.

3. Union transformation: In this transformation, two Dataframes are combined to form a single Dataframe, with each partition of the child Dataframe depending on only one partition of each parent Dataframe. Since each partition of the child Dataframe depends on only one partition of each parent Dataframe, it is a narrow dependency.

<center>
    <img src="/images/data/spark/narrow-dependency-2.webp"/>
</center>

## Wide dependency(transformation)

Wide dependency transformations are those where each partition of the output DataFrame depends on multiple partitions of the input DataFrame. This means that the transformation requires shuffling data across the network, which can be resource-intensive.

<center>
    <img src="/images/data/spark/wide-dependency.webp"/>
</center>

Here are some examples of wide dependency transformations:

1. groupByKey() - This transformation groups the elements of a DataFrame by key, producing a new DataFrame with one row per distinct key. Since the output partitions depend on all the input partitions with matching keys, groupByKey() is a wide dependency transformation.

2. reduceByKey() - This transformation groups the elements of a DataFrame by key, and then applies a reduce function to each group to produce a new DataFrame. Since the output partitions depend on all the input partitions with matching keys, reduceByKey() is a wide dependency transformation.

A join can be wide or narrow depending on the paritioning of the input. If the input tables are already paritioned on the join key, then each parition in the output of the join depends only on a partition in the input data and it will be a narrow dependency transformation. But if the input tables are not paritined on the join key, then there is need to shuffle the data and it will be wide dependency transformaiton.

