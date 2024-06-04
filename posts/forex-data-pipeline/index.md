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

## Section 1

Http Connection task 실행하기

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
(venv) venv {seilylook} 😎 docker exec -it afc31a3f3254 /bin/bash

[2024-06-04 05:59:17,459] {http.py:101} INFO - Poking: marclamberti/f45f872dea4dfd3eaa015a4a1af4b39b
[2024-06-04 05:59:17,460] {base.py:79} INFO - Using connection to: id: forex_api. Host: https://gist.github.com/, Port: None, Schema: , Login: , Password: None, extra: {}
[2024-06-04 05:59:17,461] {http.py:140} INFO - Sending 'GET' to url: https://gist.github.com/marclamberti/f45f872dea4dfd3eaa015a4a1af4b39b
[2024-06-04 05:59:17,866] {base.py:248} INFO - Success criteria met. Exiting.
[2024-06-04 05:59:17,868] {taskinstance.py:1219} INFO - Marking task as SUCCESS. dag_id=forex_data_pipeline, task_id=is_forex_rates_available, execution_date=20240101T000000, start_date=20240604T055917, end_date=20240604T055917
```

## Section 2

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
(venv) venv {seilylook} 😎  main ±  docker exec -it afc31a3f3254 /bin/bash

airflow@afc31a3f3254:/$ cd opt/airflow/dags/files/

airflow@afc31a3f3254:~/dags/files$ airflow tasks test forex_data_pipeline is_forex_currencies_file_available 2024-01-01

[2024-06-04 09:19:12,326] {base.py:248} INFO - Success criteria met. Exiting.

[2024-06-04 09:19:12,328] {taskinstance.py:1219} INFO - Marking task as SUCCESS. dag_id=forex_data_pipeline, task_id=is_forex_currencies_file_available, execution_date=20240101T000000, start_date=20240604T091912, end_date=20240604T091912
```

## Section 3

### DAG

### Tasks test

