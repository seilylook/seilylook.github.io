# Spark Architecture


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

# Spark runtime components

|                            Cluter deploy mode                             |                            Client deploy mode                            |
| :-----------------------------------------------------------------------: | :----------------------------------------------------------------------: |
| <center><img src="/images/spark/spark-cluster-deploy-mode.png"/></center> | <center><img src="/images/spark/spark-client-deploy-mode.png"/></center> |
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

- **In this mode, the driver process runs as a seperate JVM process inside a cluster, and the cluster manages its resources(mostly JVM heap memory)**.

- **In this mode, the driver's running inside the client's JVM process and communicates with the executors managed by the cluster**.

## Responsibilities of the `executors`

The executors, which JVM processes, accept tasks from the driver, execute those tasks, and return the results to driver.

Each executor has several task slots (or CPU cores) for running tasks in parallel. The executors in the figures have six tasks slots each. Those slots in white boxes are vacant. You can set the number of task slots to a value two or three times the number of CPU cores. Although these task slots are often referred to as CPU cores in Spark, they’re implemented as threads and don’t need to correspond to the number of physical CPU cores on the machine.

## Creation of the `Spark Context`

Once the driver is started, it configures an instance of SparkContext. When running a Spark REPL shell, the shell is the driver program. Your Spark context is already preconfigured and available as a sc variable. When running running a standalone Spark applicaion by submitting a jar file, or by using Spark API from another program, yout Spark application starts and configures the Spark context.

There can be only on Spark context per JVM.

A Spark context comes with many useful methods for creating RDDs, loading data, and is the main interface for accessing Spark runtime.

# Spark cluster types

## Spark standalone cluster

A Spark standalone cluster is a Spark-specific cluster. Because a standalone cluter's built specifically for Spark applications, it doesn't support communication with an HDFS secured with Kerberos authentication protocol.

## YARN cluster

The resource manager in Hadoop 3.

Running Spark on YARN has several advantages:

- YARN lets you run different types of Java applications, not only Spark, and you can mix legacy Hadoop and Spark applications with ease.

- YARN also provides methods for isolating and prioritizing applications among users and organizations, a functionality the standalone cluster doesn’t have.

