# Spark Architecture


# Introduction

## Terms

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

| Cluter deploy mode                                                        | Client deploy mode                                                       |
| ------------------------------------------------------------------------- | ------------------------------------------------------------------------ |
| <center><img src="/images/spark/spark-cluster-deploy-mode.png"/></center> | <center><img src="/images/spark/spark-client-deploy-mode.png"/></center> |

