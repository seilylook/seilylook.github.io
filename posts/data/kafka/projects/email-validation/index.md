# Email Validation


## Configurations

### Docker Image

We use official Airflow image. We have to install the necessary libraries and packages into the Airflow container. For that, we have to create a Dockerfile

```docker
FROM apache/airflow:2.10.2

USER airflow

COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
```

```text
confluent-kafka
cassandra-driver
pymongo
```

This Dockerfile will be used to install **airflow:2.10.2**. Then, it will install all necessary libraries in the **requirements.txt**. We will use this Dockerfile to build a container named **install-requirements**.

### Docker compose - Container

After creating the Dockerfile, we can follow the instructions that [Official Airflow Run Airflow on Docker](https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html#fetching-docker-compose-yaml). 

```bash
curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.10.2/docker-compose.yaml'
```

After completing all the instructions, we will have a **docker-compose.yaml** file locally.

After obtaining the docker-compose file, we are going to modify that before starting the services. The first thing we have to do is add the following under the service section.

```yaml
# docker-compose.yaml

install-requirements:
    <<: *airflow-common
    container_name: install-requirements
    build:
      context: .
    volumes:
      - ./requirements.txt:/requirements.txt
    depends_on:
      - postgres
      - redis
    networks:
      - cassandra-kafka
```

This will be the container that will install all the necessary dependencies inside airflow container. After adding that under the services section, we should add the below parameters under the **x-airflow-common** section.

```yaml
# docker-compose.yaml

x-airflow-common:
  &airflow-common
  # In order to add custom dependencies or upgrade provider packages you can use your extended image.
  # Comment the image line, place your Dockerfile in the directory where you placed the docker-compose.yaml
  # and uncomment the "build" line below, Then run `docker-compose build` to build the images.
  image: ${AIRFLOW_IMAGE_NAME:-apache/airflow:2.10.2}
  # build: .
  environment:
    &airflow-common-env
    AIRFLOW__CORE__EXECUTOR: CeleryExecutor
    AIRFLOW__DATABASE__SQL_ALCHEMY_CONN: postgresql+psycopg2://airflow:airflow@postgres/airflow
    AIRFLOW__CELERY__RESULT_BACKEND: db+postgresql://airflow:airflow@postgres/airflow
    AIRFLOW__CELERY__BROKER_URL: redis://:@redis:6379/0
    AIRFLOW__CORE__FERNET_KEY: ''
    AIRFLOW__CORE__DAGS_ARE_PAUSED_AT_CREATION: 'true'
    AIRFLOW__CORE__LOAD_EXAMPLES: 'true'
    AIRFLOW__API__AUTH_BACKENDS: 'airflow.api.auth.backend.basic_auth,airflow.api.auth.backend.session'
    # yamllint disable rule:line-length
    # Use simple http server on scheduler for health checks
    # See https://airflow.apache.org/docs/apache-airflow/stable/administration-and-deployment/logging-monitoring/check-health.html#scheduler-health-check-server
    # yamllint enable rule:line-length
    AIRFLOW__SCHEDULER__ENABLE_HEALTH_CHECK: 'true'
    # WARNING: Use _PIP_ADDITIONAL_REQUIREMENTS option ONLY for a quick checks
    # for other purpose (development, test and especially production usage) build/extend Airflow image.
    _PIP_ADDITIONAL_REQUIREMENTS: ${_PIP_ADDITIONAL_REQUIREMENTS:-}
    AIRFLOW__SCHEDULER__DAG_DIR_LIST_INTERVAL: 30
    AIRFLOW__SMTP__SMTP_HOST: 'smtp.gmail.com' 
    AIRFLOW__SMTP__SMTP_MAIL_FROM: 'sample_email@my_email.com' 
    AIRFLOW__SMTP__SMTP_USER: 'sample_email@my_email.com' 
    AIRFLOW__SMTP__SMTP_PASSWORD: 'your_password' 
    AIRFLOW__SMTP__SMTP_PORT: '587'
```

We can add the additional services to our **docker-compose.yaml** file. Having a single docker-compose file will make things easier and we can start all the services with only one command.

```yaml
# docker-comose.yaml

zoo1:
    image: confluentinc/cp-zookeeper:7.3.2
    container_name: zookeeper
    ports:
      - "2181:2181"
    environment:
      ZOOKEEPER_CLIENT_PORT: 2181
      ZOOKEEPER_SERVER_ID: 1
      ZOOKEEPER_SERVERS: zoo1:2888:3888
    networks:
      - kafka-network
      - cassandra-kafka

  kafka1:
    image: confluentinc/cp-kafka:7.3.2
    container_name: kafka1
    ports:
      - "9092:9092"
      - "29092:29092"
    environment:
      KAFKA_ADVERTISED_LISTENERS: INTERNAL://kafka1:19092,EXTERNAL://${DOCKER_HOST_IP:-127.0.0.1}:9092,DOCKER://host.docker.internal:29092
      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: INTERNAL:PLAINTEXT,EXTERNAL:PLAINTEXT,DOCKER:PLAINTEXT
      KAFKA_INTER_BROKER_LISTENER_NAME: INTERNAL
      KAFKA_ZOOKEEPER_CONNECT: "zoo1:2181"
      KAFKA_BROKER_ID: 1
      KAFKA_LOG4J_LOGGERS: "kafka.controller=INFO,kafka.producer.async.DefaultEventHandler=INFO,state.change.logger=INFO"
      KAFKA_AUTHORIZER_CLASS_NAME: kafka.security.authorizer.AclAuthorizer
      KAFKA_ALLOW_EVERYONE_IF_NO_ACL_FOUND: "true"
    networks:
      - kafka-network
      - cassandra-kafka

  kafka2:
    image: confluentinc/cp-kafka:7.3.2
    container_name: kafka2
    ports:
      - "9093:9093"
      - "29093:29093"
    environment:
      KAFKA_ADVERTISED_LISTENERS: INTERNAL://kafka2:19093,EXTERNAL://${DOCKER_HOST_IP:-127.0.0.1}:9093,DOCKER://host.docker.internal:29093
      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: INTERNAL:PLAINTEXT,EXTERNAL:PLAINTEXT,DOCKER:PLAINTEXT
      KAFKA_INTER_BROKER_LISTENER_NAME: INTERNAL
      KAFKA_ZOOKEEPER_CONNECT: "zoo1:2181"
      KAFKA_BROKER_ID: 2
      KAFKA_LOG4J_LOGGERS: "kafka.controller=INFO,kafka.producer.async.DefaultEventHandler=INFO,state.change.logger=INFO"
      KAFKA_AUTHORIZER_CLASS_NAME: kafka.security.authorizer.AclAuthorizer
      KAFKA_ALLOW_EVERYONE_IF_NO_ACL_FOUND: "true"
    networks:
      - kafka-network
      - cassandra-kafka

  kafka3:
    image: confluentinc/cp-kafka:7.3.2
    container_name: kafka3
    ports:
      - "9094:9094"
      - "29094:29094"
    environment:
      KAFKA_ADVERTISED_LISTENERS: INTERNAL://kafka3:19094,EXTERNAL://${DOCKER_HOST_IP:-127.0.0.1}:9094,DOCKER://host.docker.internal:29094
      KAFKA_LISTENER_SECURITY_PROTOCOL_MAP: INTERNAL:PLAINTEXT,EXTERNAL:PLAINTEXT,DOCKER:PLAINTEXT
      KAFKA_INTER_BROKER_LISTENER_NAME: INTERNAL
      KAFKA_ZOOKEEPER_CONNECT: "zoo1:2181"
      KAFKA_BROKER_ID: 3
      KAFKA_LOG4J_LOGGERS: "kafka.controller=INFO,kafka.producer.async.DefaultEventHandler=INFO,state.change.logger=INFO"
      KAFKA_AUTHORIZER_CLASS_NAME: kafka.security.authorizer.AclAuthorizer
      KAFKA_ALLOW_EVERYONE_IF_NO_ACL_FOUND: "true"
    networks:
      - kafka-network
      - cassandra-kafka

  kafka-connect:
    image: confluentinc/cp-kafka-connect:7.3.2
    container_name: kafka-connect
    ports:
      - "8083:8083"
    environment:
      CONNECT_BOOTSTRAP_SERVERS: kafka1:19092,kafka2:19093,kafka3:19094
      CONNECT_REST_PORT: 8083
      CONNECT_GROUP_ID: compose-connect-group
      CONNECT_CONFIG_STORAGE_TOPIC: compose-connect-configs
      CONNECT_OFFSET_STORAGE_TOPIC: compose-connect-offsets
      CONNECT_STATUS_STORAGE_TOPIC: compose-connect-status
      CONNECT_KEY_CONVERTER: org.apache.kafka.connect.storage.StringConverter
      CONNECT_VALUE_CONVERTER: org.apache.kafka.connect.storage.StringConverter
      CONNECT_INTERNAL_KEY_CONVERTER: "org.apache.kafka.connect.json.JsonConverter"
      CONNECT_INTERNAL_VALUE_CONVERTER: "org.apache.kafka.connect.json.JsonConverter"
      CONNECT_REST_ADVERTISED_HOST_NAME: 'kafka-connect'
      CONNECT_LOG4J_ROOT_LOGLEVEL: 'INFO'
      CONNECT_LOG4J_LOGGERS: 'org.apache.kafka.connect.runtime.rest=WARN,org.reflections=ERROR'
      CONNECT_PLUGIN_PATH: '/usr/share/java,/usr/share/confluent-hub-components'
    networks:
      - kafka-network
      - cassandra-kafka

  schema-registry:
    image: confluentinc/cp-schema-registry:7.3.2
    container_name: schema-registry
    ports:
      - "8081:8081"
    environment:
      SCHEMA_REGISTRY_KAFKASTORE_BOOTSTRAP_SERVERS: kafka1:19092,kafka2:19093,kafka3:19094
      SCHEMA_REGISTRY_HOST_NAME: schema-registry
      SCHEMA_REGISTRY_LISTENERS: http://0.0.0.0:8081
    networks:
      - kafka-network
      - cassandra-kafka

  kafka-ui:
    container_name: kafka-ui
    image: provectuslabs/kafka-ui:latest
    ports:
      - 8888:8080
    depends_on:
      - kafka1
      - kafka2
      - kafka3
      - schema-registry
      - kafka-connect
    environment:
      KAFKA_CLUSTERS_0_NAME: local
      KAFKA_CLUSTERS_0_BOOTSTRAPSERVERS: PLAINTEXT://kafka1:19092,PLAINTEXT_HOST://kafka1:19092
      KAFKA_CLUSTERS_0_SCHEMAREGISTRY: http://schema-registry:8081
      KAFKA_CLUSTERS_0_KAFKACONNECT_0_NAME: connect
      KAFKA_CLUSTERS_0_KAFKACONNECT_0_ADDRESS: http://kafka-connect:8083
      DYNAMIC_CONFIG_ENABLED: 'true'
    networks:
      - kafka-network
      - cassandra-kafka
  
  cassandra:
    image: cassandra:latest
    container_name: cassandra
    hostname: cassandra
    ports:
      - 9042:9042
    environment:
      - MAX_HEAP_SIZE=512M
      - HEAP_NEWSIZE=100M
      - CASSANDRA_USERNAME=cassandra
      - CASSANDRA_PASSWORD=cassandra
    volumes:
      - ./:/home
      - cassandra-data:/var/lib/cassandra
    networks:
      - cassandra-kafka
  
  mongo:
    image: mongo
    container_name: mongo
    restart: always
    environment:
      MONGO_INITDB_ROOT_USERNAME: root
      MONGO_INITDB_ROOT_PASSWORD: root
    networks:
      - cassandra-kafka

  mongo-express:
    image: mongo-express
    container_name: mongo-express
    restart: always
    ports:
      - 8082:8081
    environment:
      ME_CONFIG_MONGODB_ADMINUSERNAME: root
      ME_CONFIG_MONGODB_ADMINPASSWORD: root
      ME_CONFIG_MONGODB_URL: mongodb://root:root@mongo:27017/
    networks:
      - cassandra-kafka

volumes:
  cassandra-data:
  postgres-db-volume:

networks:
  kafka-network:
    driver: bridge
  cassandra-kafka:
    external: true
```

{{<admonition info>}}
We must add the external network for **cassandra-kafka**. 

```bash
docker network create cassandra-kafka
```
{{</admonition>}}

Create the init airflow container

```bash
docker compose up airflow-init
```

This command will initiate Airflow first, Then, we will run the below command to run all the services.

```bash
docker compose up -d --build
```

This command will build the container upon the Dockerfile and start all other services. After wait for docker operations, we will see the folder **dags** which includes the DAG script. 

## Create Kafka Topic
