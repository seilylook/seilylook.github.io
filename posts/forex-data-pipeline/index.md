# Forex Data Pipeline


# Description

이 프로젝트는 Airflow를 학습하며 실제 Data Pipeline을 구성해본다.

<br />

## Docker Configuration

### Shell

`File path: ./start.sh`

```shell
# /!\ WARNING: RESET EVERYTHING!
# Remove all containers/networks/volumes/images and data in db
docker-compose down
docker system prune -f
docker volume prune -f
docker network prune -f
rm -rf ./mnt/postgres/*
docker rmi -f $(docker images -a -q)
```

### docker-compose

```yaml
version: "2.1"
services:
  ######################################################
  # DATABASE SERVICE
  ######################################################
  postgres:
    build: "./docker/postgres"
    restart: always
    container_name: postgres
    logging:
      driver: "json-file"
      options:
        max-file: "5"
        max-size: "10m"
    ports:
      - "32769:5432"
    #volumes:
    #- ./mnt/postgres:/var/lib/postgresql/data/pgdata
    environment:
      - POSTGRES_USER=airflow
      - POSTGRES_PASSWORD=airflow
      - POSTGRES_DB=airflow_db
      #- PGDATA=/var/lib/postgresql/data/pgdata
    healthcheck:
      test: ["CMD", "pg_isready", "-q", "-d", "airflow_db", "-U", "airflow"]
      timeout: 45s
      interval: 10s
      retries: 10

  adminer:
    image: wodby/adminer:latest
    restart: always
    container_name: adminer
    logging:
      driver: "json-file"
      options:
        max-file: "5"
        max-size: "10m"
    ports:
      - "32767:9000"
    environment:
      - ADMINER_DEFAULT_DB_DRIVER=psql
      - ADMINER_DEFAULT_DB_HOST=postgres
      - ADMINER_DEFAULT_DB_NAME=airflow_db
    healthcheck:
      test: ["CMD", "nc", "-z", "adminer", "9000"]
      timeout: 45s
      interval: 10s
      retries: 10

  ######################################################
  # HADOOP SERVICES
  ######################################################
  namenode:
    build: ./docker/hadoop/hadoop-namenode
    restart: always
    container_name: namenode
    logging:
      driver: "json-file"
      options:
        max-file: "5"
        max-size: "10m"
    ports:
      - "32763:9870"
    volumes:
      - ./mnt/hadoop/namenode:/hadoop/dfs/name
    environment:
      - CLUSTER_NAME=hadoop_cluster
    healthcheck:
      test: ["CMD", "nc", "-z", "namenode", "9870"]
      timeout: 45s
      interval: 10s
      retries: 10

  datanode:
    build: ./docker/hadoop/hadoop-datanode
    restart: always
    container_name: datanode
    logging:
      driver: "json-file"
      options:
        max-file: "5"
        max-size: "10m"
    depends_on:
      - namenode
    volumes:
      - ./mnt/hadoop/datanode:/hadoop/dfs/data
    environment:
      - SERVICE_PRECONDITION=namenode:9870
    healthcheck:
      test: ["CMD", "nc", "-z", "datanode", "9864"]
      timeout: 45s
      interval: 10s
      retries: 10

  hive-metastore:
    build: ./docker/hive/hive-metastore
    restart: always
    container_name: hive-metastore
    logging:
      driver: "json-file"
      options:
        max-file: "5"
        max-size: "10m"
    depends_on:
      - namenode
      - datanode
      - postgres
    environment:
      - SERVICE_PRECONDITION=namenode:9870 datanode:9864 postgres:5432
    ports:
      - "32761:9083"
    healthcheck:
      test: ["CMD", "nc", "-z", "hive-metastore", "9083"]
      timeout: 45s
      interval: 10s
      retries: 10

  hive-server:
    build: ./docker/hive/hive-server
    restart: always
    container_name: hive-server
    logging:
      driver: "json-file"
      options:
        max-file: "5"
        max-size: "10m"
    depends_on:
      - hive-metastore
    environment:
      - SERVICE_PRECONDITION=hive-metastore:9083
    ports:
      - "32760:10000"
      - "32759:10002"
    healthcheck:
      test: ["CMD", "nc", "-z", "hive-server", "10002"]
      timeout: 45s
      interval: 10s
      retries: 10

  hive-webhcat:
    build: ./docker/hive/hive-webhcat
    restart: always
    container_name: hive-webhcat
    logging:
      driver: "json-file"
      options:
        max-file: "5"
        max-size: "10m"
    depends_on:
      - hive-server
    environment:
      - SERVICE_PRECONDITION=hive-server:10000
    healthcheck:
      test: ["CMD", "nc", "-z", "hive-webhcat", "50111"]
      timeout: 45s
      interval: 10s
      retries: 10

  hue:
    build: ./docker/hue
    restart: always
    container_name: hue
    logging:
      driver: "json-file"
      options:
        max-file: "5"
        max-size: "10m"
    depends_on:
      - hive-server
      - postgres
    ports:
      - "32762:8888"
    volumes:
      - ./mnt/hue/hue.ini:/usr/share/hue/desktop/conf/z-hue.ini
    environment:
      - SERVICE_PRECONDITION=hive-server:10000 postgres:5432
    healthcheck:
      test: ["CMD", "nc", "-z", "hue", "8888"]
      timeout: 45s
      interval: 10s
      retries: 10

  ######################################################
  # SPARK SERVICES
  ######################################################
  spark-master:
    build: ./docker/spark/spark-master
    restart: always
    container_name: spark-master
    logging:
      driver: "json-file"
      options:
        max-file: "5"
        max-size: "10m"
    ports:
      - "32766:8082"
      - "32765:7077"
    volumes:
      - ./mnt/spark/apps:/opt/spark-apps
      - ./mnt/spark/data:/opt/spark-data
    healthcheck:
      test: ["CMD", "nc", "-z", "spark-master", "8082"]
      timeout: 45s
      interval: 10s
      retries: 10

  spark-worker:
    build: ./docker/spark/spark-worker
    logging:
      driver: "json-file"
      options:
        max-file: "5"
        max-size: "10m"
    depends_on:
      - spark-master
    ports:
      - "32764:8081"
    volumes:
      - ./mnt/spark/apps:/opt/spark-apps
      - ./mnt/spark/data:/opt/spark-data
    healthcheck:
      test: ["CMD", "nc", "-z", "spark-worker", "8081"]
      timeout: 45s
      interval: 10s
      retries: 10

  livy:
    build: ./docker/livy
    restart: always
    container_name: livy
    logging:
      driver: "json-file"
      options:
        max-file: "5"
        max-size: "10m"
    depends_on:
      - spark-worker
    ports:
      - "32758:8998"
    environment:
      - SPARK_MASTER_ENDPOINT=spark-master
      - SPARK_MASTER_PORT=7077
      - DEPLOY_MODE=client
    healthcheck:
      test: ["CMD", "nc", "-z", "livy", "8998"]
      timeout: 45s
      interval: 10s
      retries: 10

  ######################################################
  # AIRFLOW
  ######################################################

  airflow:
    build: ./docker/airflow
    restart: always
    container_name: airflow
    volumes:
      - ./mnt/airflow/airflow.cfg:/opt/airflow/airflow.cfg
      - ./mnt/airflow/dags:/opt/airflow/dags
    ports:
      - 8080:8080
    healthcheck:
      test: ["CMD", "nc", "-z", "airflow", "8080"]
      timeout: 45s
      interval: 10s
      retries: 10

######################################################
# NETWORK
######################################################

# Change name of default network otherwise URI invalid for HIVE
# because of the _ contained by default network
networks:
  default:
    name: airflow-network
```

### Docker files

```css
docker/
├── airflow/
│   ├── Dockerfile
│   └── start-airflow.sh
├── hadoop/
│   ├── hadoop-base
│   ├── hadoop-datanode
│   ├── hadoop-historyserver
│   ├── hadoop-namenode
│   ├── hadoop-nodemanager
│   └── hadoop-resourcemanager
├── hive/
│   ├── hive-base
│   ├── hive-metastore
│   ├── hive-server
│   ├── hive-webhcat
├── hue/
│   ├── Dockerfile
│   └── entrypoint.sh
├── livy/
│   ├── Dockerfile
├── postgres/
│   ├── Dockerfile
│   └── init-hive-db.sh
├── spark/
│   ├── spark-base
│   ├── spark-master
│   ├── spark-submit
│   └── spark-worker
```

## Airflow admin connections

1. forex_api

  Conn Id: forex_api

  Conn Type: HTTP

  Host: https://gist.github.com/

2. forex_path

  Conn Id: forex_path

  Conn Type: File(path)

  Extra: {"path":"/opt/airflow/dags/files"}

3. hive_conn

  Conn Id: hive_conn

  Conn Type: Hive Server 2 Thrift

  Host: hive-server

  Login: hive

  port: 10000

4. spark_conn

  Conn Id: spark_conn

  Conn Type: Spark

  Host: spark://spark-master

  Port: 7077


## 1. Http connection task - HttpSensor

### DAG

`File path: /min/airflow/dags/forex_data_pipeline.py`

```python
from airflow import DAG
from airflow.providers.http.sensors.http import HttpSensor
from datetime import datetime, timedelta

default_args = {
    "owner": "airflow",
    "email_on_failure": False,
    "email_on_retry": False,
    "email": "admin@localhost.com",
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    'forex_data_pipeline',
    start_date=datetime(2024, 1, 1),
    schedule_interval="@daily",
    default_args=default_args,
    catchup=False,
) as dag:

    is_forex_rates_available = HttpSensor(
        task_id="is_forex_rates_available",
        http_conn_id="forex_api",
        endpoint="marclamberti/f45f872dea4dfd3eaa015a4a1af4b39b",
        response_check=lambda response: "rates" in response.text,
        poke_interval=5,
        timeout=20,
    )
```

### Tasks test

```bash
(venv) {seilylook} 😎 docker exec -it afc31a3f3254 /bin/bash

airflow@afc31a3f3254:/$ airflow tasks test forex_data_pipeline is_forex_rates_available 2024-01-01
```

### 결과 확인

```bash
[2024-06-04 05:59:17,459] {http.py:101} INFO - Poking: marclamberti/f45f872dea4dfd3eaa015a4a1af4b39b

[2024-06-04 05:59:17,460] {base.py:79} INFO - Using connection to: id: forex_api. Host: https://gist.github.com/, Port: None, Schema: , Login: , Password: None, extra: {}

[2024-06-04 05:59:17,461] {http.py:140} INFO - Sending 'GET' to url: https://gist.github.com/marclamberti/f45f872dea4dfd3eaa015a4a1af4b39b
[2024-06-04 05:59:17,866] {base.py:248} INFO - Success criteria met. Exiting.

[2024-06-04 05:59:17,868] {taskinstance.py:1219} INFO - Marking task as SUCCESS. dag_id=forex_data_pipeline, task_id=is_forex_rates_available, execution_date=20240101T000000, start_date=20240604T055917, end_date=20240604T055917
```

## 2. File upload task - FileSensor

### DAG

```python
    is_forex_currencies_file_available = FileSensor(
        task_id="is_forex_currencies_file_available",
        fs_conn_id="forex_path",
        filepath="forex_currencies.csv",
        poke_interval=5,
        timeout=20,
    )
```

### Tasks test

```bash
(venv) {seilylook} 😎  main ±  docker exec -it afc31a3f3254 /bin/bash

airflow@afc31a3f3254:/$ cd opt/airflow/dags/files/

airflow@afc31a3f3254:~/dags/files$ airflow tasks test forex_data_pipeline is_forex_currencies_file_available 2024-01-01
```

### 결과 확인

```bash
[2024-06-04 09:19:12,326] {base.py:248} INFO - Success criteria met. Exiting.

[2024-06-04 09:19:12,328] {taskinstance.py:1219} INFO - Marking task as SUCCESS. dag_id=forex_data_pipeline, task_id=is_forex_currencies_file_available, execution_date=20240101T000000, start_date=20240604T091912, end_date=20240604T091912
```

## 3. Download data task - PythonOperator

### DAG

```python
from airflow.operators.python import PythonOperator

import csv
import requests
import json

def download_rates():
    BASE_URL = "https://gist.githubusercontent.com/marclamberti/f45f872dea4dfd3eaa015a4a1af4b39b/raw/"
    ENDPOINTS = {
        "USD": "api_forex_exchange_usd.json",
        "EUR": "api_forex_exchange_eur.json",
    }
    with open("/opt/airflow/dags/files/forex_currencies.csv") as forex_currencies:
        reader = csv.DictReader(forex_currencies, delimiter=";")

        for idx, row in enumerate(reader):
            base = row["base"]
            with_pairs = row["with_pairs"].split(" ")
            indata = requests.get(f"{BASE_URL}{ENDPOINTS[base]}").json()
            outdata = {"base": base, "rates": {}, "last_update": indata["date"]}

            for pair in with_pairs:
                outdata["rates"][pair] = indata["rates"][pair]

            with open("/opt/airflow/dags/files/forex_rates.json", "a") as outfile:
                json.dump(outdata, outfile)
                outfile.write("\n")

with DAG(
    "forex_data_pipeline",
    start_date=datetime(2024, 1, 1),
    schedule_interval="@daily",
    default_args=default_args,
    catchup=False,
) as dag:

    ...

    # Download the forex rates from the API - PythonOperator
    downloading_rates = PythonOperator(
        task_id="downloading_rates",
        python_callable=download_rates,
    )

```

### Tasks test

```bash
(venv) {seilylook} 🐯 docker exec -it afc31a3f3254 /bin/bash   

airflow@afc31a3f3254:/$ airflow tasks test forex_data_pipeline downloading_rates 2024-01-01
```

### 결과 확인

```bash
[2024-06-04 10:32:56,752] {taskinstance.py:1254} INFO - Exporting the following env vars:
AIRFLOW_CTX_DAG_EMAIL=admin@localhost.com
AIRFLOW_CTX_DAG_OWNER=airflow
AIRFLOW_CTX_DAG_ID=forex_data_pipeline
AIRFLOW_CTX_TASK_ID=downloading_rates
AIRFLOW_CTX_EXECUTION_DATE=2024-01-01T00:00:00+00:00

[2024-06-04 10:32:57,549] {python.py:151} INFO - Done. Returned value was: None

[2024-06-04 10:32:57,551] {taskinstance.py:1219} INFO - Marking task as SUCCESS. dag_id=forex_data_pipeline, task_id=downloading_rates, execution_date=20240101T000000, start_date=20240604T103256, end_date=20240604T103257
```

## 4. Save the forex rates into HDFS - BashOperator

### DAG

```python
from airflow.operators.bash import BashOperator

    saving_rates = BashOperator(
        task_id="saving_rates",
        bash_command="""
            hdfs dfs -mkdir -p /forex && \
            hdfs dfs -put -f $AIRFLOW_HOME/dags/files/forex_rates.json /forex
        """,
    )
```

### Tasks test

```bash
(venv)  {seilylook} 🐯 docker exec -it 8477c6d75a95 /bin/bash            

airflow@8477c6d75a95:/$ airflow tasks test forex_data_pipeline saving_rates 2024-01-01
```

### 결과 확인

```bash
[2024-06-05 03:49:00,586] {subprocess.py:63} INFO - Running command: ['bash', '-c', '\n            hdfs dfs -mkdir -p /forex &&             hdfs dfs -put -f $AIRFLOW_HOME/dags/files/forex_rates.json /forex\n        ']
[2024-06-05 03:49:00,588] {subprocess.py:74} INFO - Output:
[2024-06-05 03:49:00,759] {subprocess.py:78} INFO - 2024-06-05 03:49:00,759 WARN util.NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
[2024-06-05 03:49:01,371] {subprocess.py:78} INFO - 2024-06-05 03:49:01,371 WARN util.NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
[2024-06-05 03:49:02,281] {subprocess.py:82} INFO - Command exited with return code 0
[2024-06-05 03:49:02,298] {taskinstance.py:1219} INFO - Marking task as SUCCESS. dag_id=forex_data_pipeline, task_id=saving_rates, execution_date=20240101T000000, start_date=20240605T034900, end_date=20240605T034902
```

## 5. Create the Hive table forex rates - HiveOperator

### DAG

```python
from airflow.providers.apache.hive.operators.hive import HiveOperator

    # Create the Hive table forex rates - HiveOperator
    creating_forex_rates_table = HiveOperator(
        task_id="creating_forex_rates_table",
        hive_cli_conn_id="hive_conn",
        hql="""
            CREATE EXTERNAL TABLE IF NOT EXISTS forex_rates(
                base STRING,
                last_update DATE,
                eur DOUBLE,
                usd DOUBLE,
                nzd DOUBLE,
                gbp DOUBLE,
                jpy DOUBLE,
                cad DOUBLE
            )
            ROW FORMAT DELIMITED
            FIELDS TERMINATED BY ','
            STORED AS TEXTFILE
        """,
    )
```

### Tasks test

```bash
(venv)  {seilylook} 🐯 docker exec -it 8477c6d75a95 /bin/bash            

airflow@8477c6d75a95:/$ airflow tasks test forex_data_pipeline creating_forex_rates_table 2024-01-01
```

### 결과 확인

```bash
[2024-06-05 05:09:04,833] {hive.py:137} INFO - Executing: 
            CREATE EXTERNAL TABLE IF NOT EXISTS forex_rates(
                base STRING,
                last_update DATE,
                eur DOUBLE,
                usd DOUBLE,
                nzd DOUBLE,
                gbp DOUBLE,
                jpy DOUBLE,
                cad DOUBLE
            )
            ROW FORMAT DELIMITED
            FIELDS TERMINATED BY ','
            STORED AS TEXTFILE
        
[2024-06-05 05:09:04,834] {base.py:79} INFO - Using connection to: id: ***_conn. Host: ***-server, Port: 10000, Schema: , Login: ***, Password: ***, extra: {}
[2024-06-05 05:09:04,835] {hive.py:155} INFO - Passing HiveConf: {'airflow.ctx.dag_email': 'admin@localhost.com', 'airflow.ctx.dag_owner': 'airflow', 'airflow.ctx.dag_id': 'forex_data_pipeline', 'airflow.ctx.task_id': 'creating_forex_rates_table', 'airflow.ctx.execution_date': '2024-01-01T00:00:00+00:00'}
[2024-06-05 05:09:04,835] {hive.py:247} INFO - *** -***conf airflow.ctx.dag_id=forex_data_pipeline -***conf airflow.ctx.task_id=creating_forex_rates_table -***conf airflow.ctx.execution_date=2024-01-01T00:00:00+00:00 -***conf airflow.ctx.dag_run_id= -***conf airflow.ctx.dag_owner=airflow -***conf airflow.ctx.dag_email=admin@localhost.com -***conf mapred.job.name=Airflow HiveOperator task for 8477c6d75a95.forex_data_pipeline.creating_forex_rates_table.2024-01-01T00:00:00+00:00 -f /tmp/airflow_***op_pnwps4j2/tmpbbxzoihf
[2024-06-05 05:09:04,997] {hive.py:259} INFO - SLF4J: Class path contains multiple SLF4J bindings.
[2024-06-05 05:09:04,997] {hive.py:259} INFO - SLF4J: Found binding in [jar:file:/opt/***/lib/log4j-slf4j-impl-2.10.0.jar!/org/slf4j/impl/StaticLoggerBinder.class]
[2024-06-05 05:09:04,997] {hive.py:259} INFO - SLF4J: Found binding in [jar:file:/opt/hadoop/share/hadoop/common/lib/slf4j-log4j12-1.7.25.jar!/org/slf4j/impl/StaticLoggerBinder.class]
[2024-06-05 05:09:04,997] {hive.py:259} INFO - SLF4J: See http://www.slf4j.org/codes.html#multiple_bindings for an explanation.
[2024-06-05 05:09:04,998] {hive.py:259} INFO - SLF4J: Actual binding is of type [org.apache.logging.slf4j.Log4jLoggerFactory]
[2024-06-05 05:09:05,847] {hive.py:259} INFO - Hive Session ID = 97eddf31-2ed2-4e5c-a9ad-14f12efddbc4
[2024-06-05 05:09:05,865] {hive.py:259} INFO - 
[2024-06-05 05:09:05,865] {hive.py:259} INFO - Logging initialized using configuration in jar:file:/opt/***/lib/***-common-3.1.2.jar!/***-log4j2.properties Async: true
[2024-06-05 05:09:06,665] {hive.py:259} INFO - Hive Session ID = 8f51bafb-4e60-41d5-bef3-79b13fb24aec
[2024-06-05 05:09:07,061] {hive.py:259} INFO - OK
[2024-06-05 05:09:07,061] {hive.py:259} INFO - Time taken: 0.374 seconds
[2024-06-05 05:09:12,304] {hive.py:259} INFO - OK
[2024-06-05 05:09:12,304] {hive.py:259} INFO - Time taken: 5.242 seconds
[2024-06-05 05:09:12,423] {taskinstance.py:1219} INFO - Marking task as SUCCESS. dag_id=forex_data_pipeline, task_id=creating_forex_rates_table, execution_date=20240101T000000, start_date=20240605T050904, end_date=20240605T050912
```

## 6. Process the forex rates with Spark - SparkSubmitOperator

### DAG

```python
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator

    forex_processing = SparkSubmitOperator(
        task_id="forex_processing",
        application="/opt/airflow/dags/scripts/forex_processing.py",
        conn_id="spark_conn",
        verbose=False,
    )
```

### Tasks test

```bash
(venv)  {seilylook} 🐯 docker exec -it 7537a6729498 /bin/bash    

airflow@7537a6729498:/$ airflow tasks test forex_data_pipeline forex_processing 2024-01-01
```

### 결과 확인

```bash
[2024-06-05 06:20:18,496] {taskinstance.py:1219} INFO - Marking task as SUCCESS. dag_id=forex_data_pipeline, task_id=forex_processing, execution_date=20240101T000000, start_date=20240605T055403, end_date=20240605T062018
```

## 7. Send an Email notification

### DAG

```python
from airflow.operators.email import EmailOperator

    send_email_notification = EmailOperator(
        task_id="send_email_notification",
        to="airflow_course@yopmail.com",
        subject="forex_data_pipeline",
        html_content="<h1>forex_data_pipeline</h1>",
    )
```

### Tasks test

```bash
(venv)  {seilylook} 🐯 docker exec -it 7537a6729498 /bin/bash            
airflow@7537a6729498:/$ airflow tasks test forex_data_pipeline send_email_notification 2024-01-01
```

### 결과 확인

```bash
[2024-06-05 09:12:39,676] {email.py:208} INFO - Email alerting: attempt 1
[2024-06-05 09:12:41,029] {email.py:220} INFO - Sent an alert email to ['airflow_course@yopmail.com']
[2024-06-05 09:12:42,560] {taskinstance.py:1219} INFO - Marking task as SUCCESS. dag_id=forex_data_pipeline, task_id=send_email_notification, execution_date=20240101T000000, start_date=20240605T091239, end_date=20240605T091242
airflow@7537a6729498:/$ 
```

## 8. Send a Slack notification

### DAG

### Tasks test

### 결과 확인
