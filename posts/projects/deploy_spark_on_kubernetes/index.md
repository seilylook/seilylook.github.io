# Deploy Spark on Kubernetes


# Introduction

Spark를 Local Kubernetes 환경에 띄우는 프로젝트

## Docker Image

docker/spark/Dockerfile

```docker

# builder step used to download and configure spark environment
FROM openjdk:11.0.11-jre-slim-buster as builder

# Add Dependencies for PySpark
RUN apt-get update && apt-get install -y curl vim wget software-properties-common ssh net-tools ca-certificates python3 python3-pip python3-numpy python3-matplotlib python3-scipy python3-pandas python3-simpy

RUN update-alternatives --install "/usr/bin/python" "python" "$(which python3)" 1

ENV SPARK_VERSION=3.4.0 \
HADOOP_VERSION=3 \
SPARK_HOME=/opt/spark \
PYTHONHASHSEED=1

# Download and uncompress spark from the apache archive
RUN wget --no-verbose -O apache-spark.tgz "https://archive.apache.org/dist/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}.tgz" \
&& mkdir -p /opt/spark \
&& tar -xf apache-spark.tgz -C /opt/spark --strip-components=1 \
&& rm apache-spark.tgz


# Apache spark environment
FROM builder as apache-spark

WORKDIR /opt/spark

ENV SPARK_MASTER_PORT=7077 \
SPARK_MASTER_WEBUI_PORT=8080 \
SPARK_LOG_DIR=/opt/spark/logs \
SPARK_MASTER_LOG=/opt/spark/logs/spark-master.out \
SPARK_WORKER_LOG=/opt/spark/logs/spark-worker.out \
SPARK_WORKER_WEBUI_PORT=8080 \
SPARK_WORKER_PORT=8081 \
SPARK_MASTER="spark://spark-master:7077" \
SPARK_WORKLOAD="master"

EXPOSE 8080 7077 6066

RUN mkdir -p $SPARK_LOG_DIR && \
touch $SPARK_MASTER_LOG && \
touch $SPARK_WORKER_LOG && \
ln -sf /dev/stdout $SPARK_MASTER_LOG && \
ln -sf /dev/stdout $SPARK_WORKER_LOG

COPY start-spark.sh /

CMD ["/bin/bash", "/start-spark.sh"]
```

## Docker compose - Container

```yaml
version: "3.3"
services:
  spark-master:
    image: my-own-spark:3.4.0
    ports:
      - "32766:8080"
      - "32765:7077"
    volumes:
       - ./apps:/opt/spark-apps
       - ./data:/opt/spark-data
    environment:
      - SPARK_LOCAL_IP=spark-master
      - SPARK_WORKLOAD=master

  spark-worker-a:
    image: my-own-spark:3.4.0
    ports:
      - "32764:8080"
      - "32763:8081"
    depends_on:
      - spark-master
    environment:
      - SPARK_MASTER=spark://spark-master:7077
      - SPARK_WORKER_CORES=1
      - SPARK_WORKER_MEMORY=1G
      - SPARK_DRIVER_MEMORY=1G
      - SPARK_EXECUTOR_MEMORY=1G
      - SPARK_WORKLOAD=worker
      - SPARK_LOCAL_IP=spark-worker-a
    volumes:
       - ./apps:/opt/spark-apps
       - ./data:/opt/spark-data

  spark-worker-b:
    image: my-own-spark:3.4.0
    ports:
      - "32762:8080"
      - "32761:8081"
    depends_on:
      - spark-master
    environment:
      - SPARK_MASTER=spark://spark-master:7077
      - SPARK_WORKER_CORES=1
      - SPARK_WORKER_MEMORY=1G
      - SPARK_DRIVER_MEMORY=1G
      - SPARK_EXECUTOR_MEMORY=1G
      - SPARK_WORKLOAD=worker
      - SPARK_LOCAL_IP=spark-worker-b
    volumes:
        - ./apps:/opt/spark-apps
        - ./data:/opt/spark-data
```

{{<admonition warning>}}
에러:

Error response from daemon: Ports are not available: exposing port TCP 0.0.0.0:7000 -> 0.0.0.0:0: listen tcp 0.0.0.0:7000: bind: address already in use

해결:

```
lsof -i :7000

kill -9 PID
```

하지만 port를 사용중인 서비스를 kill 했는데도, 없어지지 않고 다른 PID로 서비스가 계속 7000 PORT를 사용중이었다. 원인을 찾던 중에 발견한 것은 Macbook의 Airdrop 서비스가 사용하는 PORT 번호가 7000인 것을 확인했다. 이를 해결하기 위해 기존 docker service의 port 번호를 변경해서 해결했다.
{{</admonition>}}

### spark-master

```yaml
spark-master:
  image: my-own-spark:3.4.0
  ports:
    - "32766:8080"
    - "32765:7077"
  volumes:
    - ./apps:/opt/spark-apps
    - ./data:/opt/spark-data
  environment:
    - SPARK_LOCAL_IP=spark-master
    - SPARK_WORKLOAD=master
```

- 포트

    - `32766:8080`: 호스트의 포트 32766을 컨테이너 내부의 8080 포트에 매핑합니다. 8080 포트는 Spark 마스터의 웹 UI에서 사용됩니다.

    - `32765:7077`: 호스트의 포트 32765를 컨테이너 내부의 7077 포트에 매핑합니다. 7077 포트는 Spark 마스터의 클러스터 매니저가 워커 노드와 통신하는데 사용됩니다.

- 볼륨
    - **./apps:/opt/spark-apps**: 로컬 디렉토리 ./apps를 컨테이너의 /opt/spark-apps 디렉토리에 마운트합니다.

    - **./data:/opt/spark-data**: 로컬 디렉토리 ./data를 컨테이너의 /opt/spark-data 디렉토리에 마운트합니다.

- 환경 변수
    - **SPARK_LOCAL_IP**=spark-master: Spark 마스터의 IP 주소를 spark-master로 지정합니다.

    - **SPARK_WORKLOAD**=master: Spark 작업 유형을 마스터로 설정합니다.

### spark-worker-a

```yaml
spark-worker-a:
  image: my-own-spark:3.4.0
  ports:
    - "32764:8080"
    - "32763:8081"
  depends_on:
    - spark-master
  environment:
    - SPARK_MASTER=spark://spark-master:7077
    - SPARK_WORKER_CORES=1
    - SPARK_WORKER_MEMORY=1G
    - SPARK_DRIVER_MEMORY=1G
    - SPARK_EXECUTOR_MEMORY=1G
    - SPARK_WORKLOAD=worker
    - SPARK_LOCAL_IP=spark-worker-a
  volumes:
    - ./apps:/opt/spark-apps
    - ./data:/opt/spark-data
```

- 포트
    - `32764:8080`: 호스트의 포트 32764를 컨테이너 내부의 8080 포트에 매핑합니다. 8080 포트는 이 워커 노드의 웹 UI에서 사용됩니다.
    - `32763:8081`: 호스트의 포트 32763을 컨테이너 내부의 8081 포트에 매핑합니다. 8081 포트는 워커 노드의 추가적인 관리 인터페이스로 사용될 수 있습니다.

- 의존성
    - **depends_on**: spark-master 서비스가 먼저 실행된 후 이 워커가 실행되도록 설정합니다.

- 환경 변수
    - **SPARK_MASTER**=spark://spark-master:7077: 이 워커가 연결할 마스터의 주소를 지정합니다.
    - **SPARK_WORKER_CORES**=1: 워커가 사용할 코어 수를 1로 설정합니다.
    - **SPARK_WORKER_MEMORY**=1G: 워커가 사용할 메모리를 1GB로 설정합니다.
    - **SPARK_WORKLOAD**=worker: 이 컨테이너의 역할을 워커로 설정합니다.
    - **SPARK_LOCAL_IP**=spark-worker-a: 이 워커 노드의 IP 주소를 spark-worker-a로 설정합니다.

### spark-worker-b

```yaml
spark-worker-b:
  image: my-own-spark:3.4.0
  ports:
    - "32762:8080"
    - "32761:8081"
  depends_on:
    - spark-master
  environment:
    - SPARK_MASTER=spark://spark-master:7077
    - SPARK_WORKER_CORES=1
    - SPARK_WORKER_MEMORY=1G
    - SPARK_DRIVER_MEMORY=1G
    - SPARK_EXECUTOR_MEMORY=1G
    - SPARK_WORKLOAD=worker
    - SPARK_LOCAL_IP=spark-worker-b
  volumes:
    - ./apps:/opt/spark-apps
    - ./data:/opt/spark-data
```

- 포트
    - `32762:8080`: 호스트의 포트 32762를 컨테이너 내부의 8080 포트에 매핑합니다.

    - `32761:8081`: 호스트의 포트 32761을 컨테이너 내부의 8081 포트에 매핑합니다.

### 포트 설명

- **호스트 포트와 컨테이너 포트 매핑**: 이 설정은 호스트의 특정 포트를 컨테이너의 포트에 매핑합니다. 예를 들어, 32766:8080은 호스트의 32766번 포트로 접근하면 컨테이너 내부의 8080번 포트로 요청이 전달됨을 의미합니다.

- **포트 선택**: 이 예제에서는 32761부터 32766까지의 포트를 사용하여 충돌 가능성이 낮은 고유한 포트 번호를 선택했습니다. 이는 각각의 Spark 마스터 및 워커가 서로 다른 포트를 사용하도록 하여 충돌을 방지합니다.
