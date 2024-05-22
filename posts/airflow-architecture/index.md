# Airflow Architecture


Airflow is a platform that lets you build and run **workflows**. A workflow is represented as a `**DAG**` (a Directed Acyclic Graph), and contains individual pieces of work called `Tasks`, arranged with dependencies and data flows taken into account.

<img src="/images/airflow/airflow-architecture-1.png"/>

A **DAG** specifies the dependencies between tasks, which defines the order in which to execute the tasks. Tasks describe what to do, be it fetching data, running analysis, triggering other systems, or more.

Airflow itself is agnostic to what you’re running - it will happily orchestrate and run anything, either with high-level support from one of our providers, or directly as a command using the shell or Python `Operators`.

# Airflow components

## Required components

### **Scheduler**

handles both triggering scheduled workflows, and submitting Tasks to the executor to run. The executor, is a configuration property of the **scheduler**, not a separate component and runs within the **scheduler** process. There are several executors available out of the box, and you can also write your own.

### **Webserver**

presents a handy user interface to inspect, trigger and debug the behaviour of **DAG**s and tasks.

### Folder of **DAG**s

read by the **scheduler** to figure out what tasks to run and when and to run them.

### Metadata database

airflow components use to store state of workflows and tasks. Setting up a metadata database is described in Set up a Database Backend and is required for Airflow to work.

---

## Optional components

Optional **worker**, which executes the tasks given to it by the **scheduler**. In the basic installation worker might be part of the **scheduler** not a separate component. It can be run as a long running process in the CeleryExecutor, or as a POD in the KubernetesExecutor.

Optional \***\*triggerer\*\***, which executes deferred tasks in an asyncio event loop. In basic installation where deferred tasks are not used, a **triggerer** is not necessary.

Optional \***\*DAG** processor**, which parses **DAG** files and serializes them into the metadata database. By default, the **dag** processor process is part of the **scheduler**, but it can be run as a separate component for scalability and security reasons. If **dag** processor is present **scheduler** does not need to read the **DAG\*\* files directly.

Optional folder of **plugins**. Plugins are a way to extend Airflow’s functionality (similar to installed packages). Plugins are read by the **scheduler**, **dag** processor, **triggerer** and **webserver**.

# Deploying Airflow components

All the components are Python applications that can be deployed using various deployment mechanisms.

They can have extra installed packages installed in their Python environment. This is useful for example to install custom operators or sensors or extend Airflow functionality with custom plugins.

While Airflow can be run in a single machine and with simple installation where only **scheduler** and **webserver** are deployed,

Airflow is designed to be scalable and secure, and is able to run in a distributed environment - where various components can run on different machines, with different security perimeters and can be scaled by running multiple instances of the components above.

The separation of components also allow for increased security, by isolating the components from each other and by allowing to perform different tasks. For example separating **dag** processor from **scheduler** allows to make sure that the **scheduler** does not have access to the **DAG** files and cannot execute code provided by **DAG** author.

- brown solid lines represent DAG files submission and synchronization

- blue solid lines represent deploying and accessing installed packages and plugins

- black dashed(점선) lines represent control flow of workers by the scheduler (via executor)

- black solid lines represent accessing the UI to manage execution of the workflows

- red dashed(점선) lines represent accessing the metadata database by all components

## Basic Airflow deployment

This is the simplest deployment of Airflow, usually operated and managed on a single machine. Such a deployment usually uses the LocalExecutor, where the **scheduler** and the **workers** are in the same Python process and the **DAG** files are read directly from the local filesystem by the **scheduler**. The **webserver** runs on the same machine as the **scheduler**. There is no **triggerer** component, which means that task deferral is not possible.

Such an installation typically does not separate user roles - deployment, configuration, operation, authoring and maintenance are all done by the same person and there are no security perimeters between the components.

<img src="/images/airflow/airflow-architecture-2.png" />

## Distributed Airflow architecture

This is the architecture of Airflow where components of Airflow are distributed among multiple machines and where various roles of users are introduced - Deployment Manager, `DAG author, Operations User`.

In the case of a distributed deployment, it is important to consider the security aspects of the components. The **webserver** does not have access to the DAG files directly. The code in the Code tab of the UI is read from the metadata database. The **webserver** cannot execute any code submitted by the `DAG author`. It can only execute code that is installed as an installed package or plugin by the `Deployment Manager`. The `Operations User` only has access to the UI and can only trigger DAGs and tasks, but cannot author DAGs.

The DAG files need to be synchronized between all the components that use them - **scheduler, triggerer and workers**. The **DAG** files can be synchronized by various mechanisms - typical ways how DAGs can be synchronized are described in Manage DAGs files ot our Helm Chart documentation. Helm chart is one of the ways how to deploy Airflow in Kubernetes cluster.

<img src="/images/airflow/airflow-architecture-3.png" />

## Seperate DAG processing architecture

In a more complex installation where security and isolation are important, you’ll also see the standalone **dag processor** component that allows to separate scheduler from accessing **DAG files**. This is suitable if the deployment focus is on isolation between parsed tasks. While Airflow does not yet support full multi-tenant features, it can be used to make sure that `DAG author` provided code is never executed in the context of the scheduler.

<img src="/images/airflow/airflow-architecture-4.png" />

# Workloads

A DAG runs through a series of Tasks, and there are three common types of task you will see:

`Operators`, predefined tasks that you can string together quickly to build most parts of your DAGs.

`Sensors`, a special subclass of Operators which are entirely about waiting for an external event to happen.

A `TaskFlow`-decorated **@task**, which is a custom Python function packaged up as a Task.

Internally, these are all actually subclasses of Airflow’s `BaseOperator`, and the concepts of Task and Operator are somewhat interchangeable, but it’s useful to think of them as separate concepts - essentially, Operators and Sensors are templates, and when you call one in a DAG file, you’re making a Task.

