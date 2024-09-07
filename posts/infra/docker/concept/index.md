# Docker


# Introduction

쿠버네티스를 공부했지만 정작 Docker에 대해서는 제대로 공부한 적이 없는 것이 마음에 들지 않아, 이번 기회에 Docker를 완벽히 이해하고 내 것으로 만든다.

[공식 문서](https://docs.docker.com/guides/getting-started/)를 읽으면서 이해되지 않거나 앞으로 계속 사용해야 할 핵심 코드 위주로 정리해 놓는다.

## Docker Image 생성

```Docker
# Spark Docker

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

```bash
docker build -t <IMAGE NAME> <DOCKERFILE PATH>
```



## Docker container 생성

```yaml
spark-master:
  image: <IMAGE NAME>
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

```bash
# docker-compose.yml 디렉토리 위치에서

docker compose up
```

{{<admonition info>}}
만약, 내가 기존에 만든 Image를 기반으로 Container를 만든다면 

앞서 `docker build -t <IMAGE NAME>`으로 지정한 Image Name:Tag를 docker compose의 image에 넣으면 된다.

그게 아니라, 공식 Docker hub에 있는 이미지를 사용한다면,

Docker Hub의 이미지를 들어가서 `docker pull` 뒤에 있는 것을 복사해서 docker compose의 image에 넣으면 된다.
{{</admonition>}}

