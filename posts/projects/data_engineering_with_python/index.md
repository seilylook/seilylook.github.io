# Data_engineering_with_python


# Data Engineering with Python

## Chapter 2. Building Infrastructure

### Make build (docker build python image & docker compose up)

책에서는 Airflow, NiFi, PostgreSQL, Elasticsearch, Kibana 등 모조리 다 로컬 환경에서 설치해서 실습한다. 하지만 이는 내가 아주 싫어하는 상황이므로 당연하게 Docker를 활용해서 환경을 구축했다.

```bash
app-py3.12 ✘ {seilylook} 🍀 make build
==============================================
Exporting Python dependencies to requirements.txt...
==============================================
poetry export -f requirements.txt --output requirements.txt --without-hashes --with dev
Warning: poetry-plugin-export will not be installed by default in a future version of Poetry.
In order to avoid a breaking change and make your automation forward-compatible, please install poetry-plugin-export explicitly. See https://python-poetry.org/docs/plugins/#using-plugins for details on how to install a plugin.
To disable this warning run 'poetry config warnings.export false'.


==============================================
Building Docker image python-app:latest...
==============================================
docker build -t python-app:latest .
[+] Building 1.7s (20/20) FINISHED                                                                                               docker:desktop-linux
 => [internal] load build definition from Dockerfile                                                                                             0.0s
 => => transferring dockerfile: 1.14kB                                                                                                           0.0s
 => [internal] load metadata for docker.io/library/python:3.12-slim                                                                              1.5s
 => [auth] library/python:pull token for registry-1.docker.io                                                                                    0.0s
 => [internal] load .dockerignore                                                                                                                0.0s
 => => transferring context: 2B                                                                                                                  0.0s
 => [internal] load build context                                                                                                                0.0s
 => => transferring context: 33.38kB                                                                                                             0.0s
 => [builder 1/5] FROM docker.io/library/python:3.12-slim@sha256:aaa3f8cb64dd64e5f8cb6e58346bdcfa410a108324b0f28f1a7cc5964355b211                0.0s
 => CACHED [stage-1  2/10] RUN apt-get update &&     apt-get install -y --no-install-recommends     default-jdk     procps     wget     libpq5   0.0s
 => CACHED [stage-1  3/10] WORKDIR /app                                                                                                          0.0s
 => CACHED [builder 2/5] WORKDIR /app                                                                                                            0.0s
 => CACHED [builder 3/5] RUN apt-get update &&     apt-get install -y --no-install-recommends     build-essential     libpq-dev     python3-dev  0.0s
 => CACHED [builder 4/5] COPY requirements.txt .                                                                                                 0.0s
 => CACHED [builder 5/5] RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt                                      0.0s
 => CACHED [stage-1  4/10] COPY --from=builder /app/wheels /wheels                                                                               0.0s
 => CACHED [stage-1  5/10] COPY --from=builder /app/requirements.txt .                                                                           0.0s
 => CACHED [stage-1  6/10] RUN pip install --no-cache /wheels/*                                                                                  0.0s
 => [stage-1  7/10] COPY src/ src/                                                                                                               0.0s
 => [stage-1  8/10] COPY tests/ tests/                                                                                                           0.0s
 => [stage-1  9/10] COPY data/ data/                                                                                                             0.0s
 => [stage-1 10/10] COPY conf/ conf/                                                                                                             0.0s
 => exporting to image                                                                                                                           0.0s
 => => exporting layers                                                                                                                          0.0s
 => => writing image sha256:a7003da4b1bb9a04c9d98b7a386e9c28c84efe83df2ae20e99abc16cedf9e3fb                                                     0.0s
 => => naming to docker.io/library/python-app:latest                                                                                             0.0s

View build details: docker-desktop://dashboard/build/desktop-linux/desktop-linux/4go6dhhdb6ahlu1m1xmndgsou

What's next:
    View a summary of image vulnerabilities and recommendations → docker scout quickview 


==============================================
Constructing Docker Containers...
==============================================
docker compose up -d
WARN[0000] The "AIRFLOW_UID" variable is not set. Defaulting to a blank string. 
WARN[0000] The "AIRFLOW_UID" variable is not set. Defaulting to a blank string. 
WARN[0000] /Users/seilylook/Development/Book/Data_Engineering_with_Python/docker-compose.yml: the attribute `version` is obsolete, it will be ignored, please remove it to avoid potential confusion 
[+] Running 10/10
 ✔ Container postgres           Healthy                                                                                                          4.3s 
 ✔ Container elasticsearch      Healthy                                                                                                          3.6s 
 ✔ Container redis              Healthy                                                                                                          4.3s 
 ✔ Container kibana             Running                                                                                                          0.0s 
 ✔ Container airflow-init       Exited                                                                                                           7.8s 
 ✔ Container python-app         Started                                                                                                          3.8s 
 ✔ Container airflow-triggerer  Running                                                                                                          0.0s 
 ✔ Container airflow-webserver  Running                                                                                                          0.0s 
 ✔ Container airflow-scheduler  Running                                                                                                          0.0s 
 ✔ Container airflow-worker     Running                                                                                                          0.0s 


==============================================
Waiting for PostgreSQL to start...
==============================================
=====================================
Initializing PostgreSQL...
=====================================
chmod +x ./scripts/init_postgresql.sh
./scripts/init_postgresql.sh
dataengineering 데이터베이스 생성 중...
ERROR:  database "dataengineering" already exists
Successfully copied 2.05kB to postgres:/tmp/create_tables.sql
테이블 생성 중...
psql:/tmp/create_tables.sql:10: NOTICE:  relation "users" already exists, skipping
CREATE TABLE
        List of relations
 Schema | Name  | Type  |  Owner  
--------+-------+-------+---------
 public | users | table | airflow
(1 row)

                                    Table "public.users"
 Column |          Type          | Collation | Nullable |              Default              
--------+------------------------+-----------+----------+-----------------------------------
 id     | integer                |           | not null | nextval('users_id_seq'::regclass)
 name   | character varying(100) |           | not null | 
 street | character varying(200) |           |          | 
 city   | character varying(100) |           |          | 
 zip    | character varying(10)  |           |          | 
 lng    | numeric(10,6)          |           |          | 
 lat    | numeric(10,6)          |           |          | 
Indexes:
    "users_pkey" PRIMARY KEY, btree (id)

권한 부여 중...
GRANT
데이터베이스와 테이블이 성공적으로 생성되었습니다.
데이터베이스 연결 테스트 중...
/var/run/postgresql:5432 - accepting connections
데이터베이스가 정상적으로 응답합니다.




==============================================
Waiting for Elasticsearch to start...
==============================================
=====================================
Initializing Elasticsearch...
=====================================
chmod +x ./scripts/init_elasticsearch.sh
./scripts/init_elasticsearch.sh
Elasticsearch가 준비될 때까지 대기 중...
Elasticsearch가 준비되었습니다.
users 인덱스 생성 중...
{"error":{"root_cause":[{"type":"resource_already_exists_exception","reason":"index [users/AW57UPmxTYyW3G-GdL6lHw] already exists","index_uuid":"AW57UPmxTYyW3G-GdL6lHw","index":"users"}],"type":"resource_already_exists_exception","reason":"index [users/AW57UPmxTYyW3G-GdL6lHw] already exists","index_uuid":"AW57UPmxTYyW3G-GdL6lHw","index":"users"},"status":400}users 인덱스가 성공적으로 생성되었습니다.
인덱스 목록 확인:
health status index                                                              uuid                   pri rep docs.count docs.deleted store.size pri.store.size dataset.size
green  open   .internal.alerts-transform.health.alerts-default-000001            MSc-VAFyQHG9tGk2TxwbGg   1   0          0            0       249b           249b         249b
green  open   .internal.alerts-observability.logs.alerts-default-000001          Bief08evQ_SX_3UrwZOzwQ   1   0          0            0       249b           249b         249b
green  open   .internal.alerts-observability.uptime.alerts-default-000001        N-ptFAoNTYeF7OHGtOqZFw   1   0          0            0       249b           249b         249b
green  open   .internal.alerts-ml.anomaly-detection.alerts-default-000001        JL9JINenTS-XMJClxKXrYA   1   0          0            0       249b           249b         249b
green  open   .internal.alerts-observability.slo.alerts-default-000001           rFwL_h62QZmQx8kkXFZIyA   1   0          0            0       249b           249b         249b
green  open   .internal.alerts-default.alerts-default-000001                     6xFM1NqvTc--9BJ7MlhCpA   1   0          0            0       249b           249b         249b
green  open   .internal.alerts-observability.apm.alerts-default-000001           D1xM5G2DTPeF25kkR6_KWQ   1   0          0            0       249b           249b         249b
green  open   users                                                              AW57UPmxTYyW3G-GdL6lHw   1   0       1000            0    229.1kb        229.1kb      229.1kb
green  open   .internal.alerts-observability.metrics.alerts-default-000001       IO4Li-8sS6-AH8aSsvEqLg   1   0          0            0       249b           249b         249b
green  open   .internal.alerts-ml.anomaly-detection-health.alerts-default-000001 95sA140IQ2qCyErtmHKTEg   1   0          0            0       249b           249b         249b
green  open   .internal.alerts-observability.threshold.alerts-default-000001     TV3IWC9fQUuYWQO-56_5sA   1   0          0            0       249b           249b         249b
green  open   .internal.alerts-security.alerts-default-000001                    VE-qcLiURZy7h_i1hb96Lw   1   0          0            0       249b           249b         249b
green  open   .internal.alerts-stack.alerts-default-000001                       _PEhTLb4TJ2bYAwiv6kz8w   1   0          0            0       249b           249b         249b
```

#### Make test

```bash
app-py3.12 {seilylook} 🍀 make test 
=======================
Running tests with pytest...
=======================
mkdir -p target
docker run --rm -v /Users/seilylook/Development/Book/Data_Engineering_with_Python/app/target:/app/target python-app:latest /bin/bash -c \
                'for test_file in $(find tests -name "*.py" ! -name "__init__.py"); do \
                        base_name=$(basename $test_file .py); \
                        pytest $test_file --junitxml=target/$base_name.xml; \
                done'
============================= test session starts ==============================
platform linux -- Python 3.12.9, pytest-8.3.4, pluggy-1.5.0
rootdir: /app
plugins: Faker-36.1.1, time-machine-2.16.0, anyio-4.8.0
collected 7 items

tests/test_progress_bar.py .......                                       [100%]

------------ generated xml file: /app/target/test_progress_bar.xml -------------
============================== 7 passed in 0.06s ===============================
============================= test session starts ==============================
platform linux -- Python 3.12.9, pytest-8.3.4, pluggy-1.5.0
rootdir: /app
plugins: Faker-36.1.1, time-machine-2.16.0, anyio-4.8.0
collected 9 items

tests/test_data_generator.py .........                                   [100%]

----------- generated xml file: /app/target/test_data_generator.xml ------------
============================== 9 passed in 0.03s ===============================
============================= test session starts ==============================
platform linux -- Python 3.12.9, pytest-8.3.4, pluggy-1.5.0
rootdir: /app
plugins: Faker-36.1.1, time-machine-2.16.0, anyio-4.8.0
collected 0 items

----------------- generated xml file: /app/target/conftest.xml -----------------
============================ no tests ran in 0.00s =============================
============================= test session starts ==============================
platform linux -- Python 3.12.9, pytest-8.3.4, pluggy-1.5.0
rootdir: /app
plugins: Faker-36.1.1, time-machine-2.16.0, anyio-4.8.0
collected 7 items

tests/test_postgres_connector.py .......                                 [100%]

--------- generated xml file: /app/target/test_postgres_connector.xml ----------
============================== 7 passed in 0.20s ===============================
============================= test session starts ==============================
platform linux -- Python 3.12.9, pytest-8.3.4, pluggy-1.5.0
rootdir: /app
plugins: Faker-36.1.1, time-machine-2.16.0, anyio-4.8.0
collected 9 items

tests/test_database_config.py .........                                  [100%]

----------- generated xml file: /app/target/test_database_config.xml -----------
============================== 9 passed in 0.02s ===============================
============================= test session starts ==============================
platform linux -- Python 3.12.9, pytest-8.3.4, pluggy-1.5.0
rootdir: /app
plugins: Faker-36.1.1, time-machine-2.16.0, anyio-4.8.0
collected 14 items

tests/test_database_pytest.py ..............                             [100%]

----------- generated xml file: /app/target/test_database_pytest.xml -----------
============================== 14 passed in 0.19s ==============================
============================= test session starts ==============================
platform linux -- Python 3.12.9, pytest-8.3.4, pluggy-1.5.0
rootdir: /app
plugins: Faker-36.1.1, time-machine-2.16.0, anyio-4.8.0
collected 8 items

tests/test_elasticsearch_connector.py ........                           [100%]

------- generated xml file: /app/target/test_elasticsearch_connector.xml -------
============================== 8 passed in 0.18s ===============================
```

#### Make start

```bash
app-py3.12 {seilylook} 🍀 make start
=========================
Starting the application...
=========================
python -m src.main
2025-02-28 17:34:59,269 - root - INFO - 데이터 생성 및 저장 프로세스 시작
2025-02-28 17:34:59,269 - root - INFO - 데이터셋이 이미 존재합니다: data/raw/test_data.csv
2025-02-28 17:34:59,285 - src.utils.connection - INFO - PostgreSQL 연결 성공!
2025-02-28 17:34:59,286 - src.utils.connection - INFO - Elasticsearch 클라이언트 생성 완료
2025-02-28 17:34:59,290 - elastic_transport.transport - INFO - GET http://localhost:9200/ [status:200 duration:0.004s]
2025-02-28 17:34:59,290 - src.utils.connection - INFO - Elasticsearch 연결 성공! 버전: 8.17.2
2025-02-28 17:34:59,290 - root - INFO - Postgresql 상태: 연결됨
2025-02-28 17:34:59,290 - root - INFO - Elasticsearch 상태: 연결됨
2025-02-28 17:34:59,295 - root - INFO - PostgreSQL: 1000개 레코드를 data/raw/test_data.csv에서 읽었습니다
2025-02-28 17:34:59,330 - src.database.repository - INFO - Bulk inserted 1000 users
2025-02-28 17:34:59,331 - root - INFO - PostgreSQL에 1000개 레코드 저장 완료
2025-02-28 17:34:59,331 - root - INFO - PostgreSQL에 1000개 레코드 저장됨
2025-02-28 17:34:59,333 - root - INFO - Elasticsearch: 1000개 레코드를 data/raw/test_data.csv에서 읽었습니다
2025-02-28 17:34:59,335 - src.utils.connection - INFO - Elasticsearch 클라이언트 생성 완료
2025-02-28 17:34:59,408 - elastic_transport.transport - INFO - PUT http://localhost:9200/_bulk?refresh=true [status:200 duration:0.068s]
2025-02-28 17:34:59,410 - src.database.repository - INFO - Elasticsearch에 1000개 문서 벌크 저장 완료
2025-02-28 17:34:59,410 - root - INFO - Elasticsearch에 1000개 레코드 저장 완료
2025-02-28 17:34:59,410 - root - INFO - Elasticsearch에 1000개 레코드 저장됨
2025-02-28 17:34:59,414 - root - INFO - PostgreSQL에서 5개 레코드 조회 완료
2025-02-28 17:34:59,414 - root - INFO - PostgreSQL 데이터 확인 (샘플 5개):
2025-02-28 17:34:59,414 - root - INFO -   레코드 1: {'id': 1, 'name': 'Whitney Olson', 'street': '1791 Pittman Overpass', 'city': 'Lake Jason', 'zip': '48870', 'lng': Decimal('114.735089'), 'lat': Decimal('45.235433')}
2025-02-28 17:34:59,414 - root - INFO -   레코드 2: {'id': 2, 'name': 'David Smith', 'street': '0474 Julian Station', 'city': 'West Sophia', 'zip': '72976', 'lng': Decimal('94.204753'), 'lat': Decimal('-88.761862')}
2025-02-28 17:34:59,414 - root - INFO -   레코드 3: {'id': 3, 'name': 'Mr. Jason Hughes MD', 'street': '7351 Robinson Underpass', 'city': 'Stephaniebury', 'zip': '8702', 'lng': Decimal('-87.282108'), 'lat': Decimal('12.763472')}
2025-02-28 17:34:59,414 - root - INFO -   레코드 4: {'id': 4, 'name': 'John Johnson', 'street': '8304 Cooper Mews', 'city': 'Candicefort', 'zip': '87821', 'lng': Decimal('-169.562279'), 'lat': Decimal('-53.845951')}
2025-02-28 17:34:59,414 - root - INFO -   레코드 5: {'id': 5, 'name': 'Gregory Harrison', 'street': '0866 Lee Expressway Suite 888', 'city': 'Dianaport', 'zip': '14219', 'lng': Decimal('-30.874919'), 'lat': Decimal('84.261251')}
2025-02-28 17:34:59,414 - src.utils.connection - INFO - Elasticsearch 클라이언트 생성 완료
2025-02-28 17:34:59,419 - elastic_transport.transport - INFO - POST http://localhost:9200/users/_search [status:200 duration:0.005s]
2025-02-28 17:34:59,420 - root - INFO - Elasticsearch에서 5개 레코드 조회 완료
2025-02-28 17:34:59,420 - root - INFO - Elasticsearch 데이터 확인 (샘플 5개):
2025-02-28 17:34:59,420 - root - INFO -   레코드 1: {'name': 'Whitney Olson', 'age': 26, 'street': '1791 Pittman Overpass', 'city': 'Lake Jason', 'state': 'Idaho', 'zip': 48870, 'lng': 114.735089, 'lat': 45.2354325}
2025-02-28 17:34:59,420 - root - INFO -   레코드 2: {'name': 'David Smith', 'age': 28, 'street': '0474 Julian Station', 'city': 'West Sophia', 'state': 'Arizona', 'zip': 72976, 'lng': 94.204753, 'lat': -88.761862}
2025-02-28 17:34:59,420 - root - INFO -   레코드 3: {'name': 'Mr. Jason Hughes MD', 'age': 70, 'street': '7351 Robinson Underpass', 'city': 'Stephaniebury', 'state': 'Mississippi', 'zip': 8702, 'lng': -87.282108, 'lat': 12.763472}
2025-02-28 17:34:59,420 - root - INFO -   레코드 4: {'name': 'John Johnson', 'age': 41, 'street': '8304 Cooper Mews', 'city': 'Candicefort', 'state': 'Rhode Island', 'zip': 87821, 'lng': -169.562279, 'lat': -53.845951}
2025-02-28 17:34:59,420 - root - INFO -   레코드 5: {'name': 'Gregory Harrison', 'age': 24, 'street': '0866 Lee Expressway Suite 888', 'city': 'Dianaport', 'state': 'New Jersey', 'zip': 14219, 'lng': -30.874919, 'lat': 84.261251}
2025-02-28 17:34:59,420 - root - INFO - 데이터 생성 및 저장 프로세스 완료
```

## Chapter 3. Reading and Writing Files

### Handling files using NiFi processors

앞서 `make start`를 통해 Faker를 활용해 테스트 데이터를 생성한다. 이 데이터는 다음 디렉토리에 존재한다.

- local: /app/data/raw/test_data.csv

- NiFi container: /opt/nifi/nifi-current/data/raw/test_data.csv

```bash
# Nifi container 실행
app-py3.12 {seilylook} 🚀 docker exec -i -t nifi /bin/bash

# Container에 원본 데이터가 존재하는지 확인
nifi@e92527995ead:/opt/nifi/nifi-current$ ls data/raw/
test_data.csv

# 40세 이상 사람들 Query 하고 Name 기준으로 저장
nifi@e92527995ead:/opt/nifi/nifi-current/data/processed$ ls -al
total 84
drwxr-xr-x 12 nifi nifi  384 Mar  7 07:17  .
drwxr-xr-x  4 root root 4096 Mar  7 07:05  ..
-rw-r--r--  1 nifi nifi 5637 Mar  7 07:17 'Amber Taylor'
-rw-r--r--  1 nifi nifi 5284 Mar  7 07:17 'Charles Arnold'
-rw-r--r--  1 nifi nifi 5789 Mar  7 07:17 'Corey Hardin'
-rw-r--r--  1 nifi nifi 6580 Mar  7 07:17 'Ebony Miller'
-rw-r--r--  1 nifi nifi 6030 Mar  7 07:17 'Grant Garrison'
-rw-r--r--  1 nifi nifi 5108 Mar  7 07:17 'Kristina Parker'
-rw-r--r--  1 nifi nifi 5444 Mar  7 07:17 'Nicholas Baker MD'
-rw-r--r--  1 nifi nifi 5277 Mar  7 07:17 'Phillip Love'
-rw-r--r--  1 nifi nifi 6180 Mar  7 07:17 'Whitney Barnes'
-rw-r--r--  1 nifi nifi 5438 Mar  7 07:17 'Zachary Cohen'
```

#### Processors 설정

책 63p를 참조해서 Processors와 각 Processors들의 Properties를 설정했다. 원본 데이터는 Row가 1000개이다. SplitRecord Processor의 `Records Per Split`를 100으로 설정했기 때문에 /opt/nifi/nifi-current/data/processed 에 있는 결과 파일들을 보면 10개임을 확인할 수 있다.

#### 문제 및 해결

1. Nifi container 생성 

초기에 apache/nifi:latest 버전으로 image pull을 수행하니 version 2부터 자동으로 `https:`로 연결되도록 정의되어 있었다. 그래서 이전까지 Nifi를 빼고 나머지(postgresql, elasticsearch, airflow)만을 docker container로 만들었으나 문제를 해결하고 싶어 여러가지 시도를 하다가 마지막 수단으로 version을 1.28.0(버전을 낮출 떄 주의할 점은 OS/ARCH == linux/arm64 를 지원하는 docker image 인지 확인해야 한다. 내 MAC은 arm64이기 때문이다.) 으로 낮추니 정상적으로 `http:` port를 사용해서 접근할 수 있었다.

2. Nifi Processor

Nifi Processor를 생성하고 Properties를 설정하는 것은 책과 동일해 큰 문제가 발생하지 않았다. 그런데 계속해서 SplitRecord 부분에서 문제가 발생했는데, 원인은 `RELATIONS` 설정. 즉, 각각의 Processor는 원하는 연결 ex, success, splits, over . 40, matched 뿐만 아니라 failure, unmatched 등 예상치 못한 상황에서 대해서 **terminate** | **retry** 를 설정해주어야 한다. 쉽게 생각하면 상단의 `!(Warning)`이 하나도 없어야 한다.

## Chapter 4. Working with Databases

### Building data pipelines in Apache Airflow

### Handling databases with NiFi processorss
