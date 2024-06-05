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
