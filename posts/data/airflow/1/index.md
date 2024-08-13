# Airflow


# Why Airflow 

## Organization

**Apache Airflow** helps you:

- Set the order of your tasks

- Make sure each task starts only when the provious ones are done

- Control the timing of your entire data process

ex) You need to collect data from a database, clean it, perform some calculations, and then generate a report. 

Airflow helps you define this sequence and **makes sure each step happens in the correct order**, even if some tasks take loger than others

## Visibility

Visibility helps you:

- Monitor the progress of your workflows

- Quickly identify and troubleshoot issuses

- Understand dependencies between tasks

ex) If you're running multiple workflows for different projects, Airflow provides a dashboard where you can see the status of each pipeline at a glance. 

If one task fails, you can **easily spot it and take action**, rather than discovering the problem hours later when your report doesn't arrive.

## Flexibility and Scalability

Flexibility allows you to:

- Connect to many data sources and tools

- Start small and grow as your projects get bigger

- Customize your work to fit your exact needs

ex) You might start by using Airflow to plan simple database queries

As your needs grow, **you can add more complex tasks** like training AI models, checking data quility, or even starting outside programs - all using the same Airflow system you know

</br>

# What is Airflow

Apache Airflow is an open source platform to **programmatically author**, **schedule** and **monitor** workflows

Airflow is a tool that helps you create, organize and keep track of your data tasks automatically. 

It's like a very smart to-do list for your data work that runs itself.

## Benefit 1: Dynamic

Airflow can adapt and change based on what's happening

- Dynamic tasks: Generate tasks based on dynamic inputs

- Dynamic workflows: Generatet workflows based on static inputs

- Branching: Execute a different set of tasks based on a condition or result

## Benefit 2: Scalability

Airflow can handle both small and larget amounts of work.

- Different execution modes

- Depend on your infrastructure and budget

## Benefit 3: Fully functional User Interface

Airflow has a visual dashboard where you can see and control your tasks and workflows.

- Monitor and troubleshoot your workflows

- Highlight relationships between workflows and tasks

- Identify bottleneck with performance metrics

- Manage users and roles of your Airflow instance

## Benefit 4: Extensibility

Add new features or connect Airflow to other tools easily

- Many provides: package with functions to intreact with a tool or service

- Customizable user interface

- Possibility to custom existing functions

# Core components

## Component 1: The web server

The web server provides the user interface you see when you use Airflow.

It allows you to view, manage, and monitor your workflows through a web browser.

## Component 2: The scheduler

The scheduler is reponsible for determining when tasks should run.

It ensures your tasks run at the right time and in the correct order.

## Component 3: The Meta database

This is a database that stores information about your tasks and their status.

It keeps track of all the important details about your workflows.

## Component 4: The Triggerer

The triggerer is reponsible for managing deferrable tasks - tasks that wait for external events.

It allows Airflow to efficiently handle tasks taht depend on external factors without blocking other progresses.

## Component 5: The Executor

The executor detemines how your tasks will be run

It manages the execution of your tasks, deciding whether to run them in sequence or in parallel and on which system

## Component 6: The Queue

The Queue is a list of tasks waiting to be executed.

It helps manage the order of task execution, especially when there are many tasks to run.

## Component 7: The Woker

Workers are the processes that actually perform the tasks.

They do the actual work defined in your details.

# Core Concepts

## DAG(Directed Acyclic Graph)


