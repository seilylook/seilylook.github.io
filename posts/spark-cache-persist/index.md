# Spark Cache Persist


# Introduction

Spark **Cache** and **Persist** are optimization techniques for iterative and interactive Spark applications to improve the performances of the jobs or applications. In

# Key Point

- **RDD.cache() cashes the RDD with the default storage level `MEMORY_ONLY`**

- **DataFrame.cache() caches the DataFrame with the default storage level `MEMORY_AND_DISK`**

- **The persist() method is used to store it to the `user-defined storage level`**

- On Spark UI, the Storage tab shows where partitions exist in memory or disk across the cluster.

- **DataFrame `cache()` is an alias for `persist(StorageLevel.MEMORY_AND_DISK)`.**

- Caching of Spark DataFrame or DataSet is a lazy operation, meaing a DataFrame will not be cached until you trigger an action.

## Spark Cache VS Persist

Usring `cache()` and `persist()` methods, Spark provides an optimization mechanism to store the intermediate computation of an RDD, DataFrame, and Dataset so they can be reused in subsequent actions(reusing the RDD, Dataframe, and Dataset computation results).

Both caching and persisting are used to save the Spark RDD, Dataframe, and Datasets. But, the difference is,

**RDD cache() method default saves it to memory `(MEMORY_ONLY)`** and,

**DataFrame cache() method default saves it to memory `(MEMORY_AND_DISK)`**,

**whereas persist() method is used to store it to the `user-defined storage level`**.

When you persist a dataset, each node stores its partitioned data in memory and reuses them in other actions on that dataset. And Spark’s persisted data on nodes are fault-tolerant meaning if any partition of a Dataset is lost, it will automatically be recomputed using the original transformations that created it.

## Persist() storage levels

All different storage level Spark supports are available at org.apache.spark.storage.StorageLevel class. The storage level specifies how and where to persist or cache a Spark DataFrame and Dataset.

`MEMORY_ONLY` – This is the default behavior of the RDD cache() method and stores the RDD or DataFrame as deserialized objects to JVM memory. When there is no enough memory available it will not save DataFrame of some partitions and these will be re-computed as and when required. This takes more memory. but unlike RDD, this would be slower than MEMORY_AND_DISK level as it recomputes the unsaved partitions and recomputing the in-memory columnar representation of the underlying table is expensive

`MEMORY_ONLY_SER` – This is the same as MEMORY_ONLY but the difference being it stores RDD as serialized objects to JVM memory. It takes lesser memory (space-efficient) then MEMORY_ONLY as it saves objects as serialized and takes an additional few more CPU cycles in order to deserialize.

`MEMORY_ONLY_2` – Same as MEMORY_ONLY storage level but replicate each partition to two cluster nodes.

`MEMORY_ONLY_SER_2` – Same as MEMORY_ONLY_SER storage level but replicate each partition to two cluster nodes.

`MEMORY_AND_DISK` – This is the default behavior of the DataFrame or Dataset. In this Storage Level, The DataFrame will be stored in JVM memory as a deserialized object. When required storage is greater than available memory, it stores some of the excess partitions into the disk and reads the data from the disk when required. It is slower as there is I/O involved.

`MEMORY_AND_DISK_SER` – This is the same as MEMORY_AND_DISK storage level difference being it serializes the DataFrame objects in memory and on disk when space is not available.

`MEMORY_AND_DISK_2` – Same as MEMORY_AND_DISK storage level but replicate each partition to two cluster nodes.

`MEMORY_AND_DISK_SER_2` – Same as MEMORY_AND_DISK_SER storage level but replicate each partition to two cluster nodes.

`DISK_ONLY` – In this storage level, DataFrame is stored only on disk and the CPU computation time is high as I/O is involved.

`DISK_ONLY_2` – Same as DISK_ONLY storage level but replicate each partition to two cluster nodes.

## Conclusion

- Spark automatically monitors every `persist()` and `cache()` calls you make and it checks usage on each node and drops persisted data if not used or using least-recently-used (LRU) algorithm. You can also manually remove using `unpersist()` method.

- Spark caching and persistance is just one of the optimization techniques to improve the performance of Spark jobs.

