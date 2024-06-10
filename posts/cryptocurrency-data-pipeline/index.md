# Cryptocurrency Data Pipeline


# Description

`CoinMarketCap` API를 사용해 최상위 10개의 가상 화폐 가격 데이터를 가져오는 데이터 파이프라인을 구축해본다.

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
version: '2.1'
services:
  # PostgreSQL services
  postgres:
    build: './docker/postgres'
    restart: always
    container_name: postgres
    logging:
      driver: "json-file"
      options:
        max-file: "5"
        max-size: "10m"
    ports:
      - "32769:5432"
    environment:
      - POSTGRES_USER=airflow
      - POSTGRES_PASSWORD=airflow
      - POSTGRES_DB=airflow_db
    healthcheck:
      test: [ "CMD", "pg_isready", "-q", "-d", "airflow_db", "-U", "airflow" ]
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
      test: [ "CMD", "nc", "-z", "adminer", "9000" ]
      timeout: 45s
      interval: 10s
      retries: 10

  # Hadoop services
  namenode:
    build: ./docker/hadoop/hadoop-namenode
    restart: always
    container_name: namenodelog
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
      test: [ "CMD", "nc", "-z", "namenode", "9870" ]
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
      test: [ "CMD", "nc", "-z", "datanode", "9864" ]
      timeout: 45s
      interval: 10s
      retries: 10

  # Hive services
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
      test: [ "CMD", "nc", "-z", "hive-metastore", "9083" ]
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
      test: [ "CMD", "nc", "-z", "hive-server", "10002" ]
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
      test: [ "CMD", "nc", "-z", "hive-webhcat", "50111" ]
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
      test: [ "CMD", "nc", "-z", "hue", "8888" ]
      timeout: 45s
      interval: 10s
      retries: 10

  # Spark services
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
      test: [ "CMD", "nc", "-z", "spark-master", "8082" ]
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
      test: [ "CMD", "nc", "-z", "spark-worker", "8081" ]
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
      test: [ "CMD", "nc", "-z", "livy", "8998" ]
      timeout: 45s
      interval: 10s
      retries: 10

  # Airflow services
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
      test: [ "CMD", "nc", "-z", "airflow", "8080" ]
      timeout: 45s
      interval: 10s
      retries: 10

# Network 
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

## Airflow admins

- Variables

    PUBLIC_KEY=$COINMARKETCAP KEY&

- Connections

    1. crypto_api

        Conn Id: crypto_api

        Conn Type: HTTP

        Host: https://sandbox-api.coinmarketcap.com/

    2. hive_conn

        Conn Id: hive_conn

        Conn Type: Hive Server 2 Thrift

        Login: hive

        Port: 10000

    3. spark_conn

        Conn Id: spark_conn

        Conn Type: Spark

        Host: spark://spark-master

        Port: 7077

## 1. Http connection task - SimpleHttpOperator

### DAG

```python
from airflow.operators.http_operator import SimpleHttpOperator

    is_crypto_value_available = SimpleHttpOperator(
        task_id="is_crypto_value_available",
        method="GET",
        http_conn_id="crypto_api",
        endpoint="v1/cryptocurrency/listings/latest",
        data=params,
        headers=headers,
        do_xcom_push=True,  # Enable XCom push to share data between tasks
    )
```

### Tasks test

```bash
airflow@cd9277581b5f:/$ airflow tasks test crypto_data_pipeline is_crypto_value_available 2024-01-01
```

### 결과 확인

```bash
[2024-06-07 02:59:53,612] {taskinstance.py:1219} INFO - Marking task as SUCCESS. dag_id=crypto_data_pipeline, task_id=get_crypto_data, execution_date=20240101T000000, start_date=20240607T022537, end_date=20240607T025953
```

## 2. File save - PythonOperator

### DAG

```python
from airflow.operators.python import PythonOperator

def _get_crypto_data():
    session = Session()
    session.headers.update(headers)
    try:
        for crypto in CRYPTO_LIST:
            response = session.get(URL + crypto)
            response.raise_for_status()
            data = response.json()

            filename = f"{crypto}_data.json"
            filepath = os.path.join(OUTPUT_DIR, filename)

            with open(filepath, "w") as f:
                json.dump(data, f, indent=2)

            print(f"Data for {crypto} saved to {filepath}")

    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)
    except Exception as e:
        print(f"Unexpected error: {e}")


    get_crypto_data = PythonOperator(
        task_id="get_crypto_data",
        python_callable=_get_crypto_data,
    )
```

### Tasks test

```bash
airflow@cd9277581b5f:/$ airflow tasks test crypto_data_pipeline get_crypto_data 2024-01-01
```

### 결과 확인

```bash
Data for BTC saved to /opt/airflow/dags/files/BTC_data.json
Data for ETH saved to /opt/airflow/dags/files/ETH_data.json
Data for USDT saved to /opt/airflow/dags/files/USDT_data.json
Data for BNB saved to /opt/airflow/dags/files/BNB_data.json
Data for SOL saved to /opt/airflow/dags/files/SOL_data.json
Data for USDC saved to /opt/airflow/dags/files/USDC_data.json
Data for XRP saved to /opt/airflow/dags/files/XRP_data.json
Data for DOGE saved to /opt/airflow/dags/files/DOGE_data.json
Data for TON saved to /opt/airflow/dags/files/TON_data.json
Data for ADA saved to /opt/airflow/dags/files/ADA_data.json
[2024-06-07 03:21:18,576] {python.py:151} INFO - Done. Returned value was: None
[2024-06-07 03:21:18,585] {taskinstance.py:1219} INFO - Marking task as SUCCESS. dag_id=crypto_data_pipeline, task_id=get_crypto_data, execution_date=20240101T000000, start_date=20240607T022537, end_date=20240607T032118
```

## 3. Files upload to HDFS - BashOperator, PythonOperator

### DAG

```python
from airflow.operators.bash import BashOperator

def _generate_hdfs_commands():
    files = os.listdir(OUTPUT_DIR)
    # print(files)

    commands = []
    for filename in files:
        if filename.endswith(".json"):
            commands.append(
                f"hdfs dfs -put -f {os.path.join(OUTPUT_DIR, filename)} /crypto"
            )

    return commands


def _save_files_to_hdfs():
    commands = _generate_hdfs_commands()
    for command in commands:
        os.system(command)
        print(f"Executed: {command}")

    make_directory_to_hdfs = BashOperator(
        task_id="make_directory_to_hdfs",
        bash_command="hdfs dfs -mkdir -p /crypto",
    )

    save_files_to_hdfs = PythonOperator(
        task_id="save_files_to_hdfs",
        python_callable=_save_files_to_hdfs,
    )

    make_directory_to_hdfs >> save_files_to_hdfs
```

### Tasks test

```bash
airflow@cd9277581b5f:/$ airflow tasks test crypto_data_pipeline save_files_to_hdfs 2024-01-01
```

### 결과 확인

```bash
[2024-06-07 05:35:08,255] {taskinstance.py:1219} INFO - Marking task as SUCCESS. dag_id=crypto_data_pipeline, task_id=save_files_to_hdfs, execution_date=20240101T000000, start_date=20240607T050427, end_date=20240607T053508
airflow@cd9277581b5f:/$ hdfs dfs -ls /crypto
2024-06-07 05:35:22,232 WARN util.NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
Found 10 items
-rw-r--r--   3 airflow supergroup       1551 2024-06-07 05:35 /crypto/ADA_data.json
-rw-r--r--   3 airflow supergroup       1549 2024-06-07 05:35 /crypto/BNB_data.json
-rw-r--r--   3 airflow supergroup       1553 2024-06-07 05:35 /crypto/BTC_data.json
-rw-r--r--   3 airflow supergroup       1552 2024-06-07 05:35 /crypto/DOGE_data.json
-rw-r--r--   3 airflow supergroup       1548 2024-06-07 05:35 /crypto/ETH_data.json
-rw-r--r--   3 airflow supergroup       1549 2024-06-07 05:35 /crypto/SOL_data.json
-rw-r--r--   3 airflow supergroup       1553 2024-06-07 05:35 /crypto/TON_data.json
-rw-r--r--   3 airflow supergroup       1552 2024-06-07 05:35 /crypto/USDC_data.json
-rw-r--r--   3 airflow supergroup       1554 2024-06-07 05:35 /crypto/USDT_data.json
-rw-r--r--   3 airflow supergroup       1554 2024-06-07 05:35 /crypto/XRP_data.json
```

## 4. Make table in Hive - HiveOperator

### DAG

```python
from airflow.providers.apache.hive.operators.hive import HiveOperator

    create_crypto_data_table = HiveOperator(
        task_id="create_crypto_data_table",
        hive_cli_conn_id="hive_conn",
        hql="""
            CREATE EXTERNAL TABLE IF NOT EXISTS crypto_data(
                symbol STRING,
                id BIGINT,
                price DOUBLE,
                volume_24h DOUBLE,
                volume_change_24h DOUBLE,
                percent_change_1h DOUBLE,
                percent_change_24h DOUBLE,
                percent_change_7d DOUBLE,
                percent_change_30d DOUBLE
            )
            ROW FORMAT DELIMITED
            FIELDS TERMINATED BY ','
            STORED AS TEXTFILE
        """,
    )
```

### Tasks test

```bash
airflow@cd9277581b5f:/$ airflow tasks test crypto_data_pipeline create_crypto_data_table 2024-01-01
```

### 결과 확인

```bash
[2024-06-07 06:13:56,490] {hive.py:259} INFO - Hive Session ID = d4db24e6-cde2-4c32-9a5d-cee0b94589c9
[2024-06-07 06:13:56,507] {hive.py:259} INFO - 
[2024-06-07 06:13:56,507] {hive.py:259} INFO - Logging initialized using configuration in jar:file:/opt/hive/lib/hive-common-3.1.2.jar!/hive-log4j2.properties Async: true
[2024-06-07 06:13:57,392] {hive.py:259} INFO - Hive Session ID = 12d1142b-79fe-4b47-9553-184044201a7d
[2024-06-07 06:13:57,674] {hive.py:259} INFO - OK
[2024-06-07 06:13:57,674] {hive.py:259} INFO - Time taken: 0.261 seconds
[2024-06-07 06:13:57,880] {hive.py:259} INFO - OK
[2024-06-07 06:13:57,880] {hive.py:259} INFO - Time taken: 0.205 seconds
[2024-06-07 06:13:58,003] {taskinstance.py:1219} INFO - Marking task as SUCCESS. dag_id=crypto_data_pipeline, task_id=create_crypto_data_table
```
