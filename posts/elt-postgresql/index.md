# ELT PostgreSQL


# Introduction

Data Engineering 학습을 시작하고 처음 시작하는 간단한 ELT(Extract, Load, Transform) 프로세스 시연.

# Structure

```bash
├── elf_script
│   ├── Dockerfile
│   └── elf_script.py
├── source_db_init
│   └──init.sql
├── docker-compose.yaml
```

# Docker Compose configuration

## docker compose 파일 생성

```Bash
touch docker-compose.yaml
```

## docker compose script 작성

```yaml
version: "3"

services:
  source_postgres:
    # 여기때문에 계속 동작하지 않았다.
    # 처음에는 postgres:latest
    # pg_dump와 현재 버전이 안 맞다고 docker desktop를 확인하고
    # 버전을 특정 버전으로 지정해 주니 해결됐다.
    image: postgres:15.5
    ports:
      - "5433:5432"
    networks:
      - elt_network
    environment:
      POSTGRES_DB: source_db
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: secret
    volumes:
      - ./source_db_init/init.sql:/docker-entrypoint-initdb.d/init.sql

  destination_postgres:
    image: postgres:15.5
    ports:
      - "5434:5432"
    networks:
      - elt_network
    environment:
      POSTGRES_DB: destination_db
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: secret

    # 결과를 저장할 destination db는
    # 매 test마다 데이터를 저장하면 과부하가 생기기 때문에
    # volume을 지정해주지 않는다.

  elt_scripts:
    build:
      context: ./elt_script # Directory containing the Dockerfile and elt_script.py
      dockerfile: Dockerfile # Name of the Dockerfile, if it's something other than "Dockerfile", specify here
    command: ["python", "elt_script.py"]
    networks:
      - elt_network

    # 스크립트를 실행하기 전에, source, destination db를 연결해야 되기 때문에 depends로 설정.
    depends_on:
      - source_postgres
      - destination_postgres

networks:
  elt_network:
    driver: bridge
```

- `source_postgres`: 원본 데이터가 존재하는 Postgres DB

- `destination_postgres`: 가공한 데이터를 저장할 Postgres DB

# Dockerfile

docker-compose.yaml의 `elt_script`의 `depends_on`을 보면 알 수 있듯이, 앞서 두개의 데이터베이스 연결(source, destination)이 끝난 후 `elt_script` 를 실행한다.

이제 elf_script를 실행할 Dockerfile을 작성해준다.

```Docker
FROM python:3.11-slim

# Install PostgreSQL command-line tools
RUN apt-get update && apt-get install -y postgresql-client

# Copy the ELT script
COPY elt_script.py .

# Set the default command to run the ELT script
CMD ["python", "elt_script.py"]
```

# ELT Pipeline

`Dockerfile`에서 수행하도록 명령어는 적어줬으니 실질적으로 postgreSQL에 연결할 코드를 작성해준다.

```python
import subprocess
import time


def wait_for_postgres(host, max_retries=5, delay_seconds=5):
    """Wait for PostgreSQL to become available."""
    retries = 0
    while retries < max_retries:
        try:
            result = subprocess.run(
                ["pg_isready", "-h", host], check=True, capture_output=True, text=True)
            if "accepting connections" in result.stdout:
                print("Successfully connected to PostgreSQL!")
                return True
        except subprocess.CalledProcessError as e:
            print(f"Error connecting to PostgreSQL: {e}")
            retries += 1
            print(
                f"Retrying in {delay_seconds} seconds... (Attempt {retries}/{max_retries})")
            time.sleep(delay_seconds)
    print("Max retries reached. Exiting.")
    return False


# Use the function before running the ELT process
if not wait_for_postgres(host="source_postgres"):
    exit(1)

print("Starting ELT script...")

# Configuration for the source PostgreSQL database
source_config = {
    'dbname': 'source_db',
    'user': 'postgres',
    'password': 'secret',
    # Use the service name from docker-compose as the hostname
    'host': 'source_postgres'
}

# Configuration for the destination PostgreSQL database
destination_config = {
    'dbname': 'destination_db',
    'user': 'postgres',
    'password': 'secret',
    # Use the service name from docker-compose as the hostname
    'host': 'destination_postgres'
}

# Use pg_dump to dump the source database to a SQL file
dump_command = [
    'pg_dump',
    '-h', source_config['host'],
    '-U', source_config['user'],
    '-d', source_config['dbname'],
    '-f', 'data_dump.sql',
    '-w'  # Do not prompt for password
]

# Set the PGPASSWORD environment variable to avoid password prompt
subprocess_env = dict(PGPASSWORD=source_config['password'])

# Execute the dump command
subprocess.run(dump_command, env=subprocess_env, check=True)

# Use psql to load the dumped SQL file into the destination database
load_command = [
    'psql',
    '-h', destination_config['host'],
    '-U', destination_config['user'],
    '-d', destination_config['dbname'],
    '-a', '-f', 'data_dump.sql'
]

# Set the PGPASSWORD environment variable for the destination database
subprocess_env = dict(PGPASSWORD=destination_config['password'])

# Execute the load command
subprocess.run(load_command, env=subprocess_env, check=True)

print("Ending ELT script...")
```

## 라이브러리 가져오기

```python
import subprocess
import time
```

- subprocess: 이 모듈은 추가적인 프로세스와 작업하는 더 높은 수준의 인터페이스를 제공합니다. 새로운 프로세스를 생성하고, 그들의 입력/출력/오류 파이프에 연결하고, 반환 코드를 얻을 수 있습니다. 이것은 Python 스크립트에서 쉘 명령을 직접 실행하는 강력한 도구입니다.

- time: 이 모듈은 시간 관련 함수를 제공합니다. 이 스크립트에서는 주로 sleep 함수를 사용하여 지연을 도입하는 데 사용됩니다.

## wait_for_postgres 함수

```python
def wait_for_postgres(host, max_retries=5, delay_seconds=5):
    ...
```

이 함수의 목적은 PostgreSQL 인스턴스가 연결을 수용할 준비가 될 때까지 반복적으로 확인하는 것입니다.

- host: PostgreSQL 서버의 호스트 이름 또는 IP 주소입니다.

- max_retries: 함수가 데이터베이스가 사용 가능하지 않을 경우 무한 루프를 방지하기 위해 몇 번이나 데이터베이스에 연결을 시도할지를 제한합니다.

- delay_seconds: 각 실패한 시도 후 함수가 다시 시도하기 전에 기다리는 시간(초)입니다.

함수 내부:

- pg_isready: PostgreSQL과 함께 제공되는 명령 줄 유틸리티입니다. PostgreSQL 데이터베이스 인스턴스의 연결 상태를 확인합니다. 함수는 이 유틸리티를 사용하여 데이터베이스가 준비되었는지 확인합니다.

- ubprocess.run(): 이 메서드는 pg_isready 명령을 실행하는 데 사용됩니다. 명령이 실패하면(즉, 데이터베이스가 준비되지 않은 경우), 함수는 이를 처리하고 대기하고 다시 시도합니다.

## ELT 프로세스 초기화

```python
if not wait_for_postgres(host="source_postgres"):
    exit(1)
```

주요 ELT 프로세스가 시작되기 전에 스크립트는 소스 PostgreSQL 데이터베이스가 작동하는지 확인합니다. 지정된 재시도 횟수 후에 데이터베이스가 준비되지 않은 경우, 스크립트는 오류 코드(exit(1))로 종료됩니다.

## 데이터베이스 구성

```python
source_config = {...}
destination_config = {...}
```

이 딕셔너리들은 소스와 대상 PostgreSQL 데이터베이스에 대한 필요한 구성을 저장합니다:

- dbname: 데이터베이스의 이름입니다.

- user: 연결할 사용자 이름입니다.

- password: 인증에 사용되는 비밀번호입니다.

- host: 서버의 호스트 이름 또는 IP 주소입니다. Docker Compose의 컨텍스트에서는 호스트 이름으로 서비스 이름을 사용할 수 있습니다.

## 소스 데이터베이스에서 데이터 덤프하기

```python
dump_command = [...]
```

이 섹션에서는 PostgreSQL 데이터베이스를 백업하는 유틸리티인 **pg_dump**를 사용하는 명령을 구성합니다. 명령의 매개변수는 다음과 같습니다:

- h: 서버의 호스트 이름을 지정합니다.

- U: 연결할 사용자 이름을 지정합니다.

- d: 연결할 데이터베이스의 이름을 지정합니다.

- f: 덤프를 작성할 파일 이름을 지정합니다.

- w: **pg_dump**가 비밀번호를 묻지 않도록 합니다.

## 대상 데이터베이스로 데이터 로드하기

```python
load_command = [...]
```

이 섹션에서는 PostgreSQL에 대한 터미널 기반 프론트엔드인 **psql**을 사용하는 명령을 구성합니다. 명령의 매개변수는 다음과 같습니다:

- h: 서버의 호스트 이름을 지정합니다.

- U: 연결할 사용자 이름을 지정합니다.

- d: 연결할 데이터베이스의 이름을 지정합니다.

- a: 스크립트에서 모든 입력을 표준 출력으로 복사합니다.

- f: 실행할 명령을 포함한 파일 이름을 지정합니다.

## 인증을 위한 환경 변수

```python
subprocess_env = dict(PGPASSWORD=source_config['password'])
```

**pg_dump**와 **psql**을 실행할 때 비밀번호를 묻지 않기 위해 스크립트는 PGPASSWORD 환경 변수를 설정합니다. 이 변수에는 지정된 PostgreSQL 사용자의 비밀번호가 포함됩니다.

## 명령 실행

```python
subprocess.run(dump_command, env=subprocess_env, check=True)
```

subprocess.run() 메서드는 구성된 명령을 실행하는 데 사용됩니다. env 매개변수는 명령에 환경 변수를 전달하는 데 사용됩니다. check=True 매개변수는 명령이 오류로 인해 실패하면 CalledProcessError 예외가 발생하도록 합니다.

# DBT

## Common Table Expression(CTEs)

CTE, 또는 공통 테이블 표현식(Common Table Expression),은 SQL에서 임시 결과 집합으로, SELECT, INSERT, UPDATE 또는 DELETE 문 내에서 참조할 수 있습니다. WITH 키워드로 도입됩니다.
CTE는 복잡한 SQL 쿼리를 간단한 부분으로 분해하여 쿼리를 더 읽기 쉽고 유지 관리 가능하게 만드는 데 사용됩니다.
CTE는 파생 테이블이나 하위 쿼리와 유사하지만 더 나은 가독성을 제공하며 주 쿼리에서 여러 번 참조될 수 있습니다.
CTE의 범위는 정의된 쿼리로 제한됩니다. 데이터베이스에 객체로 저장되지 않으며 쿼리 실행 이후에도 지속되지 않습니다.

```python
WITH cte_name AS (
    SELECT column1, column2
    FROM table_name
    WHERE condition
)
SELECT column1, column2
FROM cte_name;
```

## DBT 모델 작성을 위한 전제 조건

- 초기화

  모델을 작성하기 전에 dbt init 명령을 사용하여 dbt 프로젝트를 초기화해야 합니다. 이는 dbt에 필요한 디렉토리 구조와 설정 파일을 설정합니다.

- 구성

  profiles.yml 파일을 데이터베이스에 대한 연결 세부 정보로 설정해야 합니다. 이 파일은 dbt가 데이터 웨어하우스나 데이터베이스에 연결하는 방법을 알려줍니다.

- 디렉토리 구조

  dbt 모델은 dbt 프로젝트의 models 디렉토리에 배치되어야 합니다. 이 디렉토리는 dbt 프로젝트를 초기화할 때 생성됩니다.

- 의존성

  모델이 ref() 함수를 사용하여 다른 모델을 참조하는 경우, 참조된 모델은 이미 dbt 프로젝트에 존재해야 합니다.

- 패키지(선택사항)

  dbt 패키지를 사용하는 경우(이는 dbt 모델, 매크로, 테스트 등의 세트로, dbt 프로젝트에 가져올 수 있습니다), 모델을 실행하기 전에 dbt deps 명령을 사용하여 패키지를 설치해야 합니다.

- 테스트(선택사항)

  dbt 모델에 테스트를 추가하려는 경우, tests 디렉토리에 테스트를 설정하고 dbt test 명령을 사용하여 실행해야 합니다.

