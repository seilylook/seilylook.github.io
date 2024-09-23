# Email Validation


## Docker Image

```docker
FROM apache/airflow:2.10.2

USER airflow

RUN curl -O 'https://bootstrap.pypa.io/get-pip.py' && \
    python3 get-pip.py --user

COPY requirements.txt /requirements.txt
RUN pip install --user -r /requirements.txt
```

```text
confluent-kafka
cassandra-driver
pymongo
```

We will use this **Dockerfile** to build an image which is install airflow, requirements.txt. 

In **docker-compose.yaml**, we build the container **install-requirements**. 

After creating the Dockerfile, we can follow the instructions that [Official Airflow Run Airflow on Docker](https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html#fetching-docker-compose-yaml)

```bash
curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.10.2/docker-compose.yaml'
```

After obtaining the docker-compose file, we are going to modify that before starting the services. The first thing we have to do is add the following container under the **services** section.
