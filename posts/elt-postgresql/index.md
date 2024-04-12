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

# elf_script.py

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

{{<admonition tip>}}
`pg_dump`는 PostgreSQL 데이터베이스의 데이터를 백업하는 데 사용되는 유틸리티입니다. 이 도구는 PostgreSQL 서버에서 데이터베이스를 백업하고 그것을 복원하는 데 도움이 됩니다.

pg_dump는 SQL 스크립트 형식으로 데이터베이스 구조(schema) 및 데이터를 추출하여 저장할 수 있습니다. 이것은 데이터베이스를 다른 서버로 이전하거나, 예기치 않은 데이터 손실을 방지하기 위해 주기적으로 백업하는 데 유용합니다. 이 백업 파일을 사용하여 데이터를 다시 복원할 수 있습니다.
{{</admonition>}}

# Docker Container 실행

```
 ✘ {seilylook} ~/Development/DataEngineering/elt main ± docker compose up
[+] Running 16/16
 ✔ source_postgres 14 layers [⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿]      0B/0B      Pulled                                         22.0s
   ✔ 25d3892798f8 Pull complete                                                                               5.8s
   ✔ 77c2305dd978 Pull complete                                                                               2.0s
   ✔ 54c99c28f11f Pull complete                                                                               1.8s
   ✔ 5feeada49781 Pull complete                                                                               2.8s
   ✔ 6baaea6e6673 Pull complete                                                                               4.5s
   ✔ c1dcdf0cbea0 Pull complete                                                                               4.3s
   ✔ 3bb7d395f8d0 Pull complete                                                                               5.5s
   ✔ 6047577c3718 Pull complete                                                                               5.2s
   ✔ a2ecdbb9172a Pull complete                                                                              16.1s
   ✔ 258c83b0abc3 Pull complete                                                                               6.2s
   ✔ 5af381ce9c20 Pull complete                                                                               6.6s
   ✔ e43fd3818d7d Pull complete                                                                               8.0s
   ✔ 48dab18ebdde Pull complete                                                                               8.6s
   ✔ 5bd2657647e7 Pull complete                                                                               8.8s
 ✔ destination_postgres Pulled                                                                               22.0s
[+] Building 9.6s (9/9) FINISHED                                                              docker:desktop-linux
 => [elt_scripts internal] load .dockerignore                                                                 0.0s
 => => transferring context: 2B                                                                               0.0s
 => [elt_scripts internal] load build definition from Dockerfile                                              0.0s
 => => transferring dockerfile: 287B                                                                          0.0s
 => [elt_scripts internal] load metadata for docker.io/library/python:3.11-slim                               2.7s
 => [elt_scripts auth] library/python:pull token for registry-1.docker.io                                     0.0s
 => [elt_scripts 1/3] FROM docker.io/library/python:3.11-slim@sha256:dad770592ab3582ab2dabcf0e18a863df9d86bd  2.3s
 => => resolve docker.io/library/python:3.11-slim@sha256:dad770592ab3582ab2dabcf0e18a863df9d86bd9d23efcfa614  0.0s
 => => sha256:dad770592ab3582ab2dabcf0e18a863df9d86bd9d23efcfa614110ce49ac20e4 1.65kB / 1.65kB                0.0s
 => => sha256:521521eaabcbd63c13e6d99c58a16c1e229c8a3fc5f951193d75684bcf23f4ed 1.37kB / 1.37kB                0.0s
 => => sha256:f8e98f0336d5bb3c8a1e3430ad91f3579d5ce98624c02045d480f8905229c8c8 6.93kB / 6.93kB                0.0s
 => => sha256:5aa60d344ce833ecc2c54477647f85648d7b36158bcaba859d607398ea2b5f9b 12.84MB / 12.84MB              1.8s
 => => sha256:7ae832c8db1427050a19bf0bacd9c4a41556a5184f98fb65d4f38c10d597d0a9 241B / 241B                    0.2s
 => => sha256:f98a62eb7798aead5a082b12b4f03c8a27d45d3f9085d46ff15b7403ab6d4de2 3.41MB / 3.41MB                1.1s
 => => extracting sha256:5aa60d344ce833ecc2c54477647f85648d7b36158bcaba859d607398ea2b5f9b                     0.3s
 => => extracting sha256:7ae832c8db1427050a19bf0bacd9c4a41556a5184f98fb65d4f38c10d597d0a9                     0.0s
 => => extracting sha256:f98a62eb7798aead5a082b12b4f03c8a27d45d3f9085d46ff15b7403ab6d4de2                     0.1s
 => [elt_scripts internal] load build context                                                                 0.0s
 => => transferring context: 72B                                                                              0.0s
 => [elt_scripts 2/3] RUN apt-get update && apt-get install -y postgresql-client                              4.4s
 => [elt_scripts 3/3] COPY elt_script.py .                                                                    0.0s
 => [elt_scripts] exporting to image                                                                          0.2s
 => => exporting layers                                                                                       0.2s
 => => writing image sha256:d9e7fd37e79aee91e6c50209c5cc16248b035d17fe433dba0e363f311846c470                  0.0s
 => => naming to docker.io/library/elt-elt_scripts                                                            0.0s
[+] Running 4/4
 ✔ Network elt_elt_network               Created                                                              0.0s
 ✔ Container elt-destination_postgres-1  Created                                                              0.0s
 ✔ Container elt-source_postgres-1       Created                                                              0.0s
 ✔ Container elt-elt_scripts-1           Created                                                              0.1s
Attaching to destination_postgres-1, elt_scripts-1, source_postgres-1
destination_postgres-1  | The files belonging to this database system will be owned by user "postgres".
destination_postgres-1  | This user must also own the server process.
source_postgres-1       | The files belonging to this database system will be owned by user "postgres".
destination_postgres-1  |
source_postgres-1       | This user must also own the server process.
source_postgres-1       |
source_postgres-1       | The database cluster will be initialized with locale "en_US.utf8".
destination_postgres-1  | The database cluster will be initialized with locale "en_US.utf8".
destination_postgres-1  | The default database encoding has accordingly been set to "UTF8".
destination_postgres-1  | The default text search configuration will be set to "english".
destination_postgres-1  |
destination_postgres-1  | Data page checksums are disabled.
source_postgres-1       | The default database encoding has accordingly been set to "UTF8".
destination_postgres-1  |
source_postgres-1       | The default text search configuration will be set to "english".
destination_postgres-1  | fixing permissions on existing directory /var/lib/postgresql/data ... ok
source_postgres-1       |
source_postgres-1       | Data page checksums are disabled.
destination_postgres-1  | creating subdirectories ... ok
source_postgres-1       |
source_postgres-1       | fixing permissions on existing directory /var/lib/postgresql/data ... ok
destination_postgres-1  | selecting dynamic shared memory implementation ... posix
source_postgres-1       | creating subdirectories ... ok
source_postgres-1       | selecting dynamic shared memory implementation ... posix
source_postgres-1       | selecting default max_connections ... 100
destination_postgres-1  | selecting default max_connections ... 100
source_postgres-1       | selecting default shared_buffers ... 128MB
destination_postgres-1  | selecting default shared_buffers ... 128MB
destination_postgres-1  | selecting default time zone ... Etc/UTC
destination_postgres-1  | creating configuration files ... ok
source_postgres-1       | selecting default time zone ... Etc/UTC
source_postgres-1       | creating configuration files ... ok
destination_postgres-1  | running bootstrap script ... ok
source_postgres-1       | running bootstrap script ... ok
source_postgres-1       | performing post-bootstrap initialization ... ok
destination_postgres-1  | performing post-bootstrap initialization ... ok
destination_postgres-1  | syncing data to disk ... ok
destination_postgres-1  |
destination_postgres-1  |
destination_postgres-1  | Success. You can now start the database server using:
destination_postgres-1  |
destination_postgres-1  |     pg_ctl -D /var/lib/postgresql/data -l logfile start
destination_postgres-1  |
source_postgres-1       | syncing data to disk ... ok
destination_postgres-1  | initdb: warning: enabling "trust" authentication for local connections
source_postgres-1       |
source_postgres-1       |
source_postgres-1       | Success. You can now start the database server using:
source_postgres-1       |
source_postgres-1       |     pg_ctl -D /var/lib/postgresql/data -l logfile start
destination_postgres-1  | initdb: hint: You can change this by editing pg_hba.conf or using the option -A, or --auth-local and --auth-host, the next time you run initdb.
source_postgres-1       |
source_postgres-1       | initdb: warning: enabling "trust" authentication for local connections
source_postgres-1       | initdb: hint: You can change this by editing pg_hba.conf or using the option -A, or --auth-local and --auth-host, the next time you run initdb.
destination_postgres-1  | waiting for server to start....2024-04-10 08:22:48.668 UTC [48] LOG:  starting PostgreSQL 15.5 (Debian 15.5-1.pgdg120+1) on aarch64-unknown-linux-gnu, compiled by gcc (Debian 12.2.0-14) 12.2.0, 64-bit
source_postgres-1       | waiting for server to start....2024-04-10 08:22:48.668 UTC [48] LOG:  starting PostgreSQL 15.5 (Debian 15.5-1.pgdg120+1) on aarch64-unknown-linux-gnu, compiled by gcc (Debian 12.2.0-14) 12.2.0, 64-bit
destination_postgres-1  | 2024-04-10 08:22:48.668 UTC [48] LOG:  listening on Unix socket "/var/run/postgresql/.s.PGSQL.5432"
source_postgres-1       | 2024-04-10 08:22:48.668 UTC [48] LOG:  listening on Unix socket "/var/run/postgresql/.s.PGSQL.5432"
destination_postgres-1  | 2024-04-10 08:22:48.671 UTC [51] LOG:  database system was shut down at 2024-04-10 08:22:48 UTC
source_postgres-1       | 2024-04-10 08:22:48.671 UTC [51] LOG:  database system was shut down at 2024-04-10 08:22:48 UTC
destination_postgres-1  | 2024-04-10 08:22:48.673 UTC [48] LOG:  database system is ready to accept connections
source_postgres-1       | 2024-04-10 08:22:48.673 UTC [48] LOG:  database system is ready to accept connections
destination_postgres-1  |  done
destination_postgres-1  | server started
source_postgres-1       |  done
source_postgres-1       | server started
source_postgres-1       | CREATE DATABASE
destination_postgres-1  | CREATE DATABASE
destination_postgres-1  |
source_postgres-1       |
source_postgres-1       |
source_postgres-1       | /usr/local/bin/docker-entrypoint.sh: running /docker-entrypoint-initdb.d/init.sql
destination_postgres-1  |
destination_postgres-1  | /usr/local/bin/docker-entrypoint.sh: ignoring /docker-entrypoint-initdb.d/*
destination_postgres-1  |
destination_postgres-1  | waiting for server to shut down...2024-04-10 08:22:48.807 UTC [48] LOG:  received fast shutdown request
destination_postgres-1  | .2024-04-10 08:22:48.808 UTC [48] LOG:  aborting any active transactions
destination_postgres-1  | 2024-04-10 08:22:48.809 UTC [48] LOG:  background worker "logical replication launcher" (PID 54) exited with exit code 1
destination_postgres-1  | 2024-04-10 08:22:48.809 UTC [49] LOG:  shutting down
destination_postgres-1  | 2024-04-10 08:22:48.810 UTC [49] LOG:  checkpoint starting: shutdown immediate
source_postgres-1       | CREATE TABLE
source_postgres-1       | INSERT 0 14
source_postgres-1       | CREATE TABLE
source_postgres-1       | INSERT 0 20
source_postgres-1       | CREATE TABLE
destination_postgres-1  | 2024-04-10 08:22:48.832 UTC [49] LOG:  checkpoint complete: wrote 918 buffers (5.6%); 0 WAL file(s) added, 0 removed, 0 recycled; write=0.007 s, sync=0.015 s, total=0.024 s; sync files=301, longest=0.005 s, average=0.001 s; distance=4223 kB, estimate=4223 kB
source_postgres-1       | INSERT 0 39
source_postgres-1       | CREATE TABLE
source_postgres-1       | CREATE TABLE
source_postgres-1       | INSERT 0 20
destination_postgres-1  | 2024-04-10 08:22:48.836 UTC [48] LOG:  database system is shut down
source_postgres-1       | INSERT 0 20
source_postgres-1       |
source_postgres-1       |
source_postgres-1       | 2024-04-10 08:22:48.837 UTC [48] LOG:  received fast shutdown request
source_postgres-1       | waiting for server to shut down....2024-04-10 08:22:48.837 UTC [48] LOG:  aborting any active transactions
source_postgres-1       | 2024-04-10 08:22:48.838 UTC [48] LOG:  background worker "logical replication launcher" (PID 54) exited with exit code 1
source_postgres-1       | 2024-04-10 08:22:48.838 UTC [49] LOG:  shutting down
source_postgres-1       | 2024-04-10 08:22:48.839 UTC [49] LOG:  checkpoint starting: shutdown immediate
source_postgres-1       | 2024-04-10 08:22:48.861 UTC [49] LOG:  checkpoint complete: wrote 950 buffers (5.8%); 0 WAL file(s) added, 0 removed, 0 recycled; write=0.008 s, sync=0.013 s, total=0.023 s; sync files=315, longest=0.004 s, average=0.001 s; distance=4325 kB, estimate=4325 kB
source_postgres-1       | 2024-04-10 08:22:48.864 UTC [48] LOG:  database system is shut down
destination_postgres-1  |  done
destination_postgres-1  | server stopped
destination_postgres-1  |
destination_postgres-1  | PostgreSQL init process complete; ready for start up.
destination_postgres-1  |
destination_postgres-1  | 2024-04-10 08:22:48.921 UTC [1] LOG:  starting PostgreSQL 15.5 (Debian 15.5-1.pgdg120+1) on aarch64-unknown-linux-gnu, compiled by gcc (Debian 12.2.0-14) 12.2.0, 64-bit
destination_postgres-1  | 2024-04-10 08:22:48.921 UTC [1] LOG:  listening on IPv4 address "0.0.0.0", port 5432
destination_postgres-1  | 2024-04-10 08:22:48.921 UTC [1] LOG:  listening on IPv6 address "::", port 5432
destination_postgres-1  | 2024-04-10 08:22:48.922 UTC [1] LOG:  listening on Unix socket "/var/run/postgresql/.s.PGSQL.5432"
destination_postgres-1  | 2024-04-10 08:22:48.924 UTC [64] LOG:  database system was shut down at 2024-04-10 08:22:48 UTC
destination_postgres-1  | 2024-04-10 08:22:48.926 UTC [1] LOG:  database system is ready to accept connections
source_postgres-1       |  done
source_postgres-1       | server stopped
source_postgres-1       |
source_postgres-1       | PostgreSQL init process complete; ready for start up.
source_postgres-1       |
source_postgres-1       | 2024-04-10 08:22:48.948 UTC [1] LOG:  starting PostgreSQL 15.5 (Debian 15.5-1.pgdg120+1) on aarch64-unknown-linux-gnu, compiled by gcc (Debian 12.2.0-14) 12.2.0, 64-bit
source_postgres-1       | 2024-04-10 08:22:48.948 UTC [1] LOG:  listening on IPv4 address "0.0.0.0", port 5432
source_postgres-1       | 2024-04-10 08:22:48.948 UTC [1] LOG:  listening on IPv6 address "::", port 5432
source_postgres-1       | 2024-04-10 08:22:48.949 UTC [1] LOG:  listening on Unix socket "/var/run/postgresql/.s.PGSQL.5432"
source_postgres-1       | 2024-04-10 08:22:48.951 UTC [66] LOG:  database system was shut down at 2024-04-10 08:22:48 UTC
source_postgres-1       | 2024-04-10 08:22:48.953 UTC [1] LOG:  database system is ready to accept connections
source_postgres-1       | 2024-04-10 08:22:53.497 UTC [70] FATAL:  password authentication failed for user "root"
source_postgres-1       | 2024-04-10 08:22:53.497 UTC [70] DETAIL:  Role "root" does not exist.
source_postgres-1       |       Connection matched pg_hba.conf line 100: "host all all all scram-sha-256"
elt_scripts-1           | --
elt_scripts-1           | -- PostgreSQL database dump
elt_scripts-1           | --
elt_scripts-1           | -- Dumped from database version 15.5 (Debian 15.5-1.pgdg120+1)
elt_scripts-1           | -- Dumped by pg_dump version 15.6 (Debian 15.6-0+deb12u1)
elt_scripts-1           | SET statement_timeout = 0;
elt_scripts-1           | SET
elt_scripts-1           | SET lock_timeout = 0;
elt_scripts-1           | SET
elt_scripts-1           | SET idle_in_transaction_session_timeout = 0;
elt_scripts-1           | SET
elt_scripts-1           | SET client_encoding = 'UTF8';
elt_scripts-1           | SET
elt_scripts-1           | SET standard_conforming_strings = on;
elt_scripts-1           | SET
elt_scripts-1           | SELECT pg_catalog.set_config('search_path', '', false);
elt_scripts-1           |  set_config
elt_scripts-1           | ------------
elt_scripts-1           |
elt_scripts-1           | (1 row)
elt_scripts-1           |
elt_scripts-1           | SET check_function_bodies = false;
elt_scripts-1           | SET
elt_scripts-1           | SET xmloption = content;
elt_scripts-1           | SET
elt_scripts-1           | SET client_min_messages = warning;
elt_scripts-1           | SET
elt_scripts-1           | SET row_security = off;
elt_scripts-1           | SET
elt_scripts-1           | SET default_tablespace = '';
elt_scripts-1           | SET
elt_scripts-1           | SET default_table_access_method = heap;
elt_scripts-1           | SET
elt_scripts-1           | --
elt_scripts-1           | -- Name: actors; Type: TABLE; Schema: public; Owner: postgres
elt_scripts-1           | --
elt_scripts-1           | CREATE TABLE public.actors (
elt_scripts-1           |     actor_id integer NOT NULL,
elt_scripts-1           |     actor_name character varying(255) NOT NULL
elt_scripts-1           | );
elt_scripts-1           | CREATE TABLE
elt_scripts-1           | ALTER TABLE public.actors OWNER TO postgres;
elt_scripts-1           | ALTER TABLE
elt_scripts-1           | --
elt_scripts-1           | -- Name: actors_actor_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
elt_scripts-1           | --
elt_scripts-1           | CREATE SEQUENCE public.actors_actor_id_seq
elt_scripts-1           |     AS integer
elt_scripts-1           |     START WITH 1
elt_scripts-1           |     INCREMENT BY 1
elt_scripts-1           |     NO MINVALUE
elt_scripts-1           |     NO MAXVALUE
elt_scripts-1           |     CACHE 1;
elt_scripts-1           | CREATE SEQUENCE
elt_scripts-1           | ALTER TABLE public.actors_actor_id_seq OWNER TO postgres;
elt_scripts-1           | ALTER TABLE
elt_scripts-1           | --
elt_scripts-1           | -- Name: actors_actor_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
elt_scripts-1           | --
elt_scripts-1           | ALTER SEQUENCE public.actors_actor_id_seq OWNED BY public.actors.actor_id;
elt_scripts-1           | ALTER SEQUENCE
elt_scripts-1           | --
elt_scripts-1           | -- Name: film_actors; Type: TABLE; Schema: public; Owner: postgres
elt_scripts-1           | --
elt_scripts-1           | CREATE TABLE public.film_actors (
elt_scripts-1           |     film_id integer NOT NULL,
elt_scripts-1           |     actor_id integer NOT NULL
elt_scripts-1           | );
elt_scripts-1           | CREATE TABLE
elt_scripts-1           | ALTER TABLE public.film_actors OWNER TO postgres;
elt_scripts-1           | ALTER TABLE
elt_scripts-1           | --
elt_scripts-1           | -- Name: film_category; Type: TABLE; Schema: public; Owner: postgres
elt_scripts-1           | --
elt_scripts-1           | CREATE TABLE public.film_category (
elt_scripts-1           |     category_id integer NOT NULL,
elt_scripts-1           |     film_id integer,
elt_scripts-1           |     category_name character varying(50) NOT NULL
elt_scripts-1           | );
elt_scripts-1           | CREATE TABLE
elt_scripts-1           | ALTER TABLE public.film_category OWNER TO postgres;
elt_scripts-1           | ALTER TABLE
elt_scripts-1           | --
elt_scripts-1           | -- Name: film_category_category_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
elt_scripts-1           | --
elt_scripts-1           | CREATE SEQUENCE public.film_category_category_id_seq
elt_scripts-1           |     AS integer
elt_scripts-1           |     START WITH 1
elt_scripts-1           |     INCREMENT BY 1
elt_scripts-1           |     NO MINVALUE
elt_scripts-1           |     NO MAXVALUE
elt_scripts-1           |     CACHE 1;
elt_scripts-1           | CREATE SEQUENCE
elt_scripts-1           | ALTER TABLE public.film_category_category_id_seq OWNER TO postgres;
elt_scripts-1           | ALTER TABLE
elt_scripts-1           | --
elt_scripts-1           | -- Name: film_category_category_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
elt_scripts-1           | --
elt_scripts-1           | ALTER SEQUENCE public.film_category_category_id_seq OWNED BY public.film_category.category_id;
elt_scripts-1           | ALTER SEQUENCE
elt_scripts-1           | --
elt_scripts-1           | -- Name: films; Type: TABLE; Schema: public; Owner: postgres
elt_scripts-1           | --
elt_scripts-1           | CREATE TABLE public.films (
elt_scripts-1           |     film_id integer NOT NULL,
elt_scripts-1           |     title character varying(255) NOT NULL,
elt_scripts-1           |     release_date date,
elt_scripts-1           |     price numeric(5,2),
elt_scripts-1           |     rating character varying(10),
elt_scripts-1           |     user_rating numeric(2,1),
elt_scripts-1           |     CONSTRAINT films_user_rating_check CHECK (((user_rating >= (1)::numeric) AND (user_rating <= (5)::numeric)))
elt_scripts-1           | );
elt_scripts-1           | CREATE TABLE
elt_scripts-1           | ALTER TABLE public.films OWNER TO postgres;
elt_scripts-1           | ALTER TABLE
elt_scripts-1           | --
elt_scripts-1           | -- Name: films_film_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
elt_scripts-1           | --
elt_scripts-1           | CREATE SEQUENCE public.films_film_id_seq
elt_scripts-1           |     AS integer
elt_scripts-1           |     START WITH 1
elt_scripts-1           |     INCREMENT BY 1
elt_scripts-1           |     NO MINVALUE
elt_scripts-1           |     NO MAXVALUE
elt_scripts-1           |     CACHE 1;
elt_scripts-1           | CREATE SEQUENCE
elt_scripts-1           | ALTER TABLE public.films_film_id_seq OWNER TO postgres;
elt_scripts-1           | ALTER TABLE
elt_scripts-1           | --
elt_scripts-1           | -- Name: films_film_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
elt_scripts-1           | --
elt_scripts-1           | ALTER SEQUENCE public.films_film_id_seq OWNED BY public.films.film_id;
elt_scripts-1           | ALTER SEQUENCE
elt_scripts-1           | --
elt_scripts-1           | -- Name: users; Type: TABLE; Schema: public; Owner: postgres
elt_scripts-1           | --
elt_scripts-1           | CREATE TABLE public.users (
elt_scripts-1           |     id integer NOT NULL,
elt_scripts-1           |     first_name character varying(50),
elt_scripts-1           |     last_name character varying(50),
elt_scripts-1           |     email character varying(100),
elt_scripts-1           |     date_of_birth date
elt_scripts-1           | );
elt_scripts-1           | CREATE TABLE
elt_scripts-1           | ALTER TABLE public.users OWNER TO postgres;
elt_scripts-1           | ALTER TABLE
elt_scripts-1           | --
elt_scripts-1           | -- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
elt_scripts-1           | --
elt_scripts-1           | CREATE SEQUENCE public.users_id_seq
elt_scripts-1           |     AS integer
elt_scripts-1           |     START WITH 1
elt_scripts-1           |     INCREMENT BY 1
elt_scripts-1           |     NO MINVALUE
elt_scripts-1           |     NO MAXVALUE
elt_scripts-1           |     CACHE 1;
elt_scripts-1           | CREATE SEQUENCE
elt_scripts-1           | ALTER TABLE public.users_id_seq OWNER TO postgres;
elt_scripts-1           | ALTER TABLE
elt_scripts-1           | --
elt_scripts-1           | -- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
elt_scripts-1           | --
elt_scripts-1           | ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;
elt_scripts-1           | ALTER SEQUENCE
elt_scripts-1           | --
elt_scripts-1           | -- Name: actors actor_id; Type: DEFAULT; Schema: public; Owner: postgres
elt_scripts-1           | --
elt_scripts-1           | ALTER TABLE ONLY public.actors ALTER COLUMN actor_id SET DEFAULT nextval('public.actors_actor_id_seq'::regclass);
elt_scripts-1           | ALTER TABLE
elt_scripts-1           | --
elt_scripts-1           | -- Name: film_category category_id; Type: DEFAULT; Schema: public; Owner: postgres
elt_scripts-1           | --
elt_scripts-1           | ALTER TABLE ONLY public.film_category ALTER COLUMN category_id SET DEFAULT nextval('public.film_category_category_id_seq'::regclass);
elt_scripts-1           | ALTER TABLE
elt_scripts-1           | --
elt_scripts-1           | -- Name: films film_id; Type: DEFAULT; Schema: public; Owner: postgres
elt_scripts-1           | --
elt_scripts-1           | ALTER TABLE ONLY public.films ALTER COLUMN film_id SET DEFAULT nextval('public.films_film_id_seq'::regclass);
elt_scripts-1           | ALTER TABLE
elt_scripts-1           | --
elt_scripts-1           | -- Name: users id; Type: DEFAULT; Schema: public; Owner: postgres
elt_scripts-1           | --
elt_scripts-1           | ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);
elt_scripts-1           | ALTER TABLE
elt_scripts-1           | --
elt_scripts-1           | -- Data for Name: actors; Type: TABLE DATA; Schema: public; Owner: postgres
elt_scripts-1           | --
elt_scripts-1           | COPY public.actors (actor_id, actor_name) FROM stdin;
elt_scripts-1           | COPY 20
elt_scripts-1           | --
elt_scripts-1           | -- Data for Name: film_actors; Type: TABLE DATA; Schema: public; Owner: postgres
elt_scripts-1           | --
elt_scripts-1           | COPY public.film_actors (film_id, actor_id) FROM stdin;
elt_scripts-1           | COPY 20
elt_scripts-1           | --
elt_scripts-1           | -- Data for Name: film_category; Type: TABLE DATA; Schema: public; Owner: postgres
elt_scripts-1           | --
elt_scripts-1           | COPY public.film_category (category_id, film_id, category_name) FROM stdin;
elt_scripts-1           | COPY 39
elt_scripts-1           | --
elt_scripts-1           | -- Data for Name: films; Type: TABLE DATA; Schema: public; Owner: postgres
elt_scripts-1           | --
elt_scripts-1           | COPY public.films (film_id, title, release_date, price, rating, user_rating) FROM stdin;
elt_scripts-1           | COPY 20
elt_scripts-1           | --
elt_scripts-1           | -- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
elt_scripts-1           | --
elt_scripts-1           | COPY public.users (id, first_name, last_name, email, date_of_birth) FROM stdin;
elt_scripts-1           | COPY 14
elt_scripts-1           | --
elt_scripts-1           | -- Name: actors_actor_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
elt_scripts-1           | --
elt_scripts-1           | SELECT pg_catalog.setval('public.actors_actor_id_seq', 20, true);
elt_scripts-1           |  setval
elt_scripts-1           | --------
elt_scripts-1           |      20
elt_scripts-1           | (1 row)
elt_scripts-1           |
elt_scripts-1           | --
elt_scripts-1           | -- Name: film_category_category_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
elt_scripts-1           | --
elt_scripts-1           | SELECT pg_catalog.setval('public.film_category_category_id_seq', 39, true);
elt_scripts-1           |  setval
elt_scripts-1           | --------
elt_scripts-1           |      39
elt_scripts-1           | (1 row)
elt_scripts-1           |
elt_scripts-1           | --
elt_scripts-1           | -- Name: films_film_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
elt_scripts-1           | --
elt_scripts-1           | SELECT pg_catalog.setval('public.films_film_id_seq', 20, true);
elt_scripts-1           |  setval
elt_scripts-1           | --------
elt_scripts-1           |      20
elt_scripts-1           | (1 row)
elt_scripts-1           |
elt_scripts-1           | --
elt_scripts-1           | -- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
elt_scripts-1           | --
elt_scripts-1           | SELECT pg_catalog.setval('public.users_id_seq', 14, true);
elt_scripts-1           |  setval
elt_scripts-1           | --------
elt_scripts-1           |      14
elt_scripts-1           | (1 row)
elt_scripts-1           |
elt_scripts-1           | --
elt_scripts-1           | -- Name: actors actors_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
elt_scripts-1           | --
elt_scripts-1           | ALTER TABLE ONLY public.actors
elt_scripts-1           |     ADD CONSTRAINT actors_pkey PRIMARY KEY (actor_id);
elt_scripts-1           | ALTER TABLE
elt_scripts-1           | --
elt_scripts-1           | -- Name: film_actors film_actors_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
elt_scripts-1           | --
elt_scripts-1           | ALTER TABLE ONLY public.film_actors
elt_scripts-1           |     ADD CONSTRAINT film_actors_pkey PRIMARY KEY (film_id, actor_id);
elt_scripts-1           | ALTER TABLE
elt_scripts-1           | --
elt_scripts-1           | -- Name: film_category film_category_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
elt_scripts-1           | --
elt_scripts-1           | ALTER TABLE ONLY public.film_category
elt_scripts-1           |     ADD CONSTRAINT film_category_pkey PRIMARY KEY (category_id);
elt_scripts-1           | ALTER TABLE
elt_scripts-1           | --
elt_scripts-1           | -- Name: films films_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
elt_scripts-1           | --
elt_scripts-1           | ALTER TABLE ONLY public.films
elt_scripts-1           |     ADD CONSTRAINT films_pkey PRIMARY KEY (film_id);
elt_scripts-1           | ALTER TABLE
elt_scripts-1           | --
elt_scripts-1           | -- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
elt_scripts-1           | --
elt_scripts-1           | ALTER TABLE ONLY public.users
elt_scripts-1           |     ADD CONSTRAINT users_pkey PRIMARY KEY (id);
elt_scripts-1           | ALTER TABLE
elt_scripts-1           | --
elt_scripts-1           | -- Name: film_actors film_actors_actor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
elt_scripts-1           | --
elt_scripts-1           | ALTER TABLE ONLY public.film_actors
elt_scripts-1           |     ADD CONSTRAINT film_actors_actor_id_fkey FOREIGN KEY (actor_id) REFERENCES public.actors(actor_id);
elt_scripts-1           | ALTER TABLE
elt_scripts-1           | --
elt_scripts-1           | -- Name: film_actors film_actors_film_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
elt_scripts-1           | --
elt_scripts-1           | ALTER TABLE ONLY public.film_actors
elt_scripts-1           |     ADD CONSTRAINT film_actors_film_id_fkey FOREIGN KEY (film_id) REFERENCES public.films(film_id);
elt_scripts-1           | ALTER TABLE
elt_scripts-1           | --
elt_scripts-1           | -- Name: film_category film_category_film_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
elt_scripts-1           | --
elt_scripts-1           | ALTER TABLE ONLY public.film_category
elt_scripts-1           |     ADD CONSTRAINT film_category_film_id_fkey FOREIGN KEY (film_id) REFERENCES public.films(film_id);
elt_scripts-1           | ALTER TABLE
elt_scripts-1           | --
elt_scripts-1           | -- PostgreSQL database dump complete
elt_scripts-1           | --
elt_scripts-1           | Error connecting to PostgreSQL: Command '['pg_isready', '-h', 'source_postgres']' returned non-zero exit status 2.
elt_scripts-1           | Retrying in 5 seconds... (Attempt 1/5)
elt_scripts-1           | Successfully connected to PostgreSQL!
elt_scripts-1           | Starting ELT script...
elt_scripts-1           | Ending ELT script...
elt_scripts-1 exited with code 0
```

앞서 작성했던 파이썬 코드에서 올바로 연결됐다면 `Ending ELT script...`을 출력하도록 했기에 올바로 연결된 것을 확인할 수 있다.

