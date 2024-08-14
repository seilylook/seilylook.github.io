# Architecture


# Terms

|      Term       |                                                                                                                                Meainig                                                                                                                                 |
| :-------------: | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------: |
|   Application   |                                                                                        User program built on Spark. Consists of a driver program and executors on the cluster.                                                                                         |
| Application jar | A jar containing the user's Spark application. In some cases users will want to create an "uber jar" containing their application along with its dependencies. The user's jar should never include Hadoop or Spark libraries, however, these will be added at runtime. |
| Driver program  |                                                                                        The process running the main() function of the application and creating the SparkContext                                                                                        |
| Cluster manager |                                                                             An external service for acquiring resources on the cluster (e.g. standalone manager, Mesos, YARN, Kubernetes)                                                                              |
|   Deploy mode   |                                Distinguishes where the driver process runs. In **cluster** mode, the framework launches the driver inside of the cluster. In **client** mode, the submitter launches the driver outside of the cluster.                                |
|   Worker node   |                                                                                                         Any node that can run application code in the cluster                                                                                                          |
|    Executor     |                                                 A process launched for an application on a worker node, that runs tasks and keeps data in memory or disk storage across them. Each application has its own executors.                                                  |
|      Task       |                                                                                                            A unit of work that will be sent to one executor                                                                                                            |
|       Job       |                                                                        A parallel computation consisting of multiple tasks that gets spawned in response to a Spark action (e.g. save, collect)                                                                        |
|      Stage      |                                                              Each job gets divided into smaller sets of tasks called stages that depend on each other (similar to the map and reduce stages in MapReduce)                                                              |

# Spark Architecture

Spark는 master / slave 구조로 **1개의 Driver(중앙 조정자)와 N개의 Executor(분산 작업 노드)로 구성되어있다.** Cluster에서 분산 모드로 실행된다면 하나의 spark application은 cluter manager(Standalone, YARN, Kubernetes)라고 불리는 외부 서비스를 사용해서 여러 개의 머신에서 실행된다.

## Cluster manager

**Cluster manager는 여러 서버로 구성된 클러스터 환경에서 애플리케이션들이 잘 동작할 수 있도록 자원을 관리한다.** cluster manager 종류에는 크게 standalone, YARN, Kubernetes가 있다.

# Spark runtime components

|                            Cluter deploy mode                             |                            Client deploy mode                            |
| :-----------------------------------------------------------------------: | :----------------------------------------------------------------------: |
| <center><img src="/images/data/data/spark/spark_cluster_mode.webp"/></center> | <center><img src="/images/data/spark/spark_client_mode.webp"/></center> |
|                                 Figure 1                                  |                                 Figure 2                                 |

**Figure 1**: Spark runtime components in `Cluster deploy mode`. Elements of a spark application are in blue boxes and an application's tasks running inside task slots are labeled with a "T". Unoccupied task of slots are in white boxes.

**Figure 2**: Spark runtime compoents in `Client deploy mode`. The driver is running inside the client's JVM process.

The physical placement of executor and driver processes depends on the cluster type and its configuration. For example, some of these processes could share a single physical machine, or they could run on different ones. Figure 1 shows only the logical components in cluster deploy mode.

## Responsibilities of the `client process` compoent

The client process starts the driver program. For example, the client process can be a spark-submit script for running applications, a spark-shell script, or a custom application using Spark API. The client process prepares the classpath and all configuration options for the Spark application. It also passes application arguments, if any, to the application running inside the driver.

## Responsibilities of the `driver` component

The driver orchestrates and monitors execution of a Spark application. There's always one driver per Spark application. You can think of the driver as a wrapper around the application.
The driver and its subcomponents - the Spark context and scheduler - are responsible for:

- requesting memory and CPU resources from cluster managers

- breaking application logic into stages and tasks

- sending tasks to executors

- collecting the results

### Two basic ways the driver program can be run are:

- **Cluster mode: the driver process runs as a seperate JVM process inside a cluster, and the cluster manages its resources(mostly JVM heap memory)**.

- **Client mode: the driver's running inside the client's JVM process and communicates with the executors managed by the cluster**.

## Responsibilities of the `executors`

The executors, which JVM processes, accept tasks from the driver, execute those tasks, and return the results to driver.

Each executor has several task slots (or CPU cores) for running tasks in parallel. The executors in the figures have six tasks slots each. Those slots in white boxes are vacant. You can set the number of task slots to a value two or three times the number of CPU cores. Although these task slots are often referred to as CPU cores in Spark, they’re implemented as threads and don’t need to correspond to the number of physical CPU cores on the machine.

## Creation of the `Spark Context`

Once the driver is started, it configures an instance of SparkContext. When running a Spark REPL shell, the shell is the driver program. Your Spark context is already preconfigured and available as a sc variable. When running running a standalone Spark applicaion by submitting a jar file, or by using Spark API from another program, yout Spark application starts and configures the Spark context.

There can be only on Spark context per JVM.

A Spark context comes with many useful methods for creating RDDs, loading data, and is the main interface for accessing Spark runtime.

# Local mode VS Deploy mode

local mode와 deploy mode를 선택하는 기준은 **cluster를 사용 여부**다. 즉, cluster를 사용해서 분산 모드로 애플리케이션을 실행한다면 deploy mode, 그렇지 않다면 local mode다.

cluster를 사용한다면 **cluster manager 종류와 배포 방식**을 선택할 수 있다. cluster manager는 standalone, YARN, Mesos 등 중에 선택할 수 있다. **배포 방식에는 client, cluster가 있고 어떤 방식을 사용하느냐에 따라 driver 실행 위치가 달라진다.**

즉, 우리는 spark 애플리케이션을 실행할때 local mode, client mode, cluster mode 총 3가지 방식으로 실행할 수 있다.

## Local mode

local mode는 **local client JVM에 Driver 1개와 Executor 1개를 생성하는 형태**로, 클러스터를 사용하지 않고 로컬 단일 머신에서 애플리케이션을 실행한다.

## Client mode

**Client mode는 Driver가 Cluster 외부인 Client JVM에서 실행된다.** Client 프로세스에 Driver program과 그 안에 Spark application, Spark Context가 있기 때문에 Client 프로세스를 중지시키면 수행 중이던 모든 스파크 Job도 종료된다.

## Cluster mode

**Cluster mode는 Driver가 Cluster 내부의 Worker node 중 하나에서 실행된다.** 애플리케이션은 Cluster 내부에서 독립적인 프로세스로 실행되고 Cluster manager에 의해 조정되기 때문에 해당 모드에서 Client는 애플리케이션 제출 후 개입하지 않는다.

