# Spark_connection


# Introduction

**Docker Compose** 환경에서 **Spark & MongoDB**를 연결해서 데이터를 저장해보는 실습을 수행해본다. 4일간의 삽질을 기록해본다.

## Docker Compose

```yaml
version: '3'
services:
  spark-master:
    image: bitnami/spark:latest
    container_name: spark-master
    ports:
      - 4040:8080
      - 7077:7077
    environment:
      - SPARK_MODE=master
      - SPARK_RPC_AUTHENTICATION_ENABLED=no
      - SPARK_RPC_ENCRYPTION_ENABLED=no
      - SPARK_LOCAL_STORAGE_ENCRYPTION_ENABLED=no
      - SPARK_SSL_ENABLED=no
    networks:
      - mongodb_network

  spark-worker-a:
    image: bitnami/spark:latest
    container_name: spark-worker-a
    ports:
      - 4041:8081
    environment:
      - SPARK_MODE=worker
      - SPARK_MASTER_URL=spark://spark-master:7077
      - SPARK_WORKER_MEMORY=2g
      - SPARK_WORKER_CORES=2
      - SPARK_RPC_AUTHENTICATION_ENABLED=no
      - SPARK_RPC_ENCRYPTION_ENABLED=no
      - SPARK_LOCAL_STORAGE_ENCRYPTION_ENABLED=no
      - SPARK_SSL_ENABLED=no
    depends_on:
      - spark-master
    networks:
      - mongodb_network

  spark-worker-b:
    image: bitnami/spark:latest
    container_name: spark-worker-b
    ports:
      - 4042:8081
    environment:
      - SPARK_MODE=worker
      - SPARK_MASTER_URL=spark://spark-master:7077
      - SPARK_WORKER_MEMORY=2g
      - SPARK_WORKER_CORES=2
      - SPARK_RPC_AUTHENTICATION_ENABLED=no
      - SPARK_RPC_ENCRYPTION_ENABLED=no
      - SPARK_LOCAL_STORAGE_ENCRYPTION_ENABLED=no
      - SPARK_SSL_ENABLED=no
    depends_on:
      - spark-master
    networks:
      - mongodb_network

  mongodb:
    image: mongo
    container_name: mongodb
    ports:
      - 27017:27017
    volumes:
      - data:/data/db
    environment:
      - MONGO_INITDB_ROOT_USERNAME=rootuser
      - MONGO_INITDB_ROOT_PASSWORD=rootpass
    networks:
      - mongodb_network

  jupyterlab:
    image: jupyter/pyspark-notebook:latest
    container_name: jupyterlab
    ports:
      - "8888:8888"
    volumes:
      - ./jupyterlab:/home/jovyan/work
    environment:
      - JUPYTER_ENABLE_LAB=yes
      - GRANT_SUDO=yes
      - PYSPARK_DRIVER_PYTHON=jupyter
      - PYSPARK_DRIVER_PYTHON_OPTS='notebook --ip=0.0.0.0 --port=8888 --no-browser --allow-root'
      - SPARK_MASTER_HOST=spark-master
    command: start-notebook.sh --NotebookApp.token="sehyeonkim"
    depends_on:
      - spark-master
    user: "1000"
    networks:
      - mongodb_network

volumes:
  data: {}

networks:
  mongodb_network:
    name: mongodb_network
```

- **spark-master**: 

## Mongosh User Auth

```bash
 {seilylook} 🔑 docker exec -i -t mongodb /bin/bash
root@82cfeefce409:/# mongosh -u rootuser -p rootpass
Current Mongosh Log ID: 6773a732d7b3046553fc0420
Connecting to:          mongodb://<credentials>@127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+2.3.4
Using MongoDB:          8.0.4
Using Mongosh:          2.3.4

For mongosh info see: https://www.mongodb.com/docs/mongodb-shell/

------
   The server generated these startup warnings when booting
   2024-12-31T08:05:07.127+00:00: Using the XFS filesystem is strongly recommended with the WiredTiger storage engine. See http://dochub.mongodb.org/core/prodnotes-filesystem
   2024-12-31T08:05:07.636+00:00: For customers running the current memory allocator, we suggest changing the contents of the following sysfsFile
   2024-12-31T08:05:07.636+00:00: We suggest setting the contents of sysfsFile to 0.
   2024-12-31T08:05:07.636+00:00: Your system has glibc support for rseq built in, which is not yet supported by tcmalloc-google and has critical performance implications. Please set the environment variable GLIBC_TUNABLES=glibc.pthread.rseq=0
   2024-12-31T08:05:07.636+00:00: vm.max_map_count is too low
   2024-12-31T08:05:07.636+00:00: We suggest setting swappiness to 0 or 1, as swapping can cause performance problems.
------

test> show users
[
  {
    _id: 'test.testuser',
    userId: UUID('bac43b1e-7917-4284-8414-ea9b6d73c0de'),
    user: 'testuser',
    db: 'test',
    roles: [ { role: 'readWrite', db: 'test' } ],
    mechanisms: [ 'SCRAM-SHA-1', 'SCRAM-SHA-256' ]
  }
]
test> use admin
switched to db admin
admin> show users
[
  {
    _id: 'admin.rootuser',
    userId: UUID('46d2f916-e9c8-4dba-82c1-316d9a87b0e9'),
    user: 'rootuser',
    db: 'admin',
    roles: [ { role: 'root', db: 'admin' } ],
    mechanisms: [ 'SCRAM-SHA-1', 'SCRAM-SHA-256' ]
  }
]
```

## Jupyter Notebook

```python
from pyspark.sql import SparkSession

CONN_URI = "mongodb://testuser:testpass@mongodb:27017/test.students?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+2.3.4"

spark = SparkSession.builder\
    .appName("Spark_MongoDB_Connection")\
    .config("spark.mongodb.read.connection.uri", CONN_URI) \
    .config("spark.mongodb.write.connection.uri", CONN_URI) \
    .config("spark.jars.packages", "org.mongodb.spark:mongo-spark-connector_2.12:10.4.0") \
    .getOrCreate()

df = spark.createDataFrame([
    ("Bilbo Baggins", 50),
    ("Gandalf", 1000),
    ("Thorin", 195),
    ("Balin", 178),
    ("Kili", 77),
    ("Dwalin", 169),
    ("Oin", 167),
    ("Gloin", 158),
    ("Fili", 82),
    ("Bombur", None)
], ["name", "age"])

df.write.format("mongodb")\
    .mode("append")\
    .option("database", "test")\
    .option("collection", "students")\
    .save()

```
