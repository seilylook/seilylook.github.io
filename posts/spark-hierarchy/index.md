# Spark Hierarchy


# Hardware Hierarchy

<img src="/images/spark/spark-hierarchy-1.webp"/>

## Cluster

### Driver

### Executor

- Cores / Slots: Each executor can be considered as servers and they have cores. A core can be considered a slot that can be used to put workload into. Each core can take one piece of work.

## Memory

Each server also has memory. But not all of it is given for Spark. On average 90% of this memory is given for Spark.

At a high level, this memory is divided into Storage and Working Memory.

> Storage memory is where data is cached or persisted.

> Working memory is where Spark does all in-memory computations

### Storage Memory

- to store persisted objects

- Default configured limit - 50% of total storage

### Working Memory

- will be utilized by spark workloads

- 50% of total storage will be used for spark workloads

### Disks

Each server also has locally attached/mounted storage.

- RAM/SSD/NFS Drivers

- Better disks would ensure fast shuffling of data

These disks are extremely important because - a lot of time, Spark does **Shuffle**(Data compared between partitions). In the intermediate stages, when data is moved around, that data goes to Disk. Faster the disk, Faster the shuffle.

---

# Software Hierarchy

<img src="/images/spark/spark-hierarchy-2.webp"/>

## Transformation(lazy)

- **Narrow**(all the data needed for the transformation is available to CPU at the same time)

- **Wide**(data needs to be moved around nodes, require shuffle)

|   DataFrame APIs   |
| :----------------: |
|     `select()`     |
|     `filter()`     |
|    `groupBy()`     |
|      `agg()`       |
|    `orderBy()`     |
|      `join()`      |
| `dropDuplicates()` |
|   `withColumn()`   |
|     `limit()`      |
|      `drop()`      |

## Action

When we call an action, we start all the transformations that spark has staged. Action launches 1 or many jobs depending on the transformations.

- **Jobs**

  - 1 Job can have many stages

- **Stages**

  - It is a section of work taht is going to be done

  - 1 Stage can have many tasks

- Jobs and Stages are part of the orchestration

- **Tasks**(interact with hardware directly)

- Every task inside a stage does the same thing, only on another segment of the data

- If a task is required to do something different, it is required to be in the inside of another stage

- One Task is done by 1 core and on one partition

| DataFrame APIs  |
| :-------------: |
|    `show()`     |
|    `count()`    |
|   `collect()`   |
| `saveAsTable()` |
|    `write()`    |
|   `foreach()`   |

# Shuffle

Shuffle happends whenever Spark can't perform tasks on individual partitions or it needs data from other partitions for computation.

<img src="/images/spark/spark-shuffle-1.webp"/>

In the above picture, we have 3 names in 3 partitions and we are trying to get the number of names for each first character. Getting the first character in each name can be done independently.

But the `groupBy` task required all A's in a single partition and hence th Shuffle. Shuffle gathers all A's into a single partition and then takes count of individual names for each first character.

<img src="/images/spark/spark-shuffle-2.webp"/>

During shuffle, data from each partitions is written into disks based on the Hash keys. In this case, Stage 1 writes data to disk based on the first character. Stage 2 pulls data from disks and gets the count.

