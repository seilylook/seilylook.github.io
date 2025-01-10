# Spark_connection


## Makefile

```makefile
.PHONY: build start stop test clean init_mongo

# Image configuration
IMAGE_NAME = session_2-python-app
DEFAULT_TAG = latest

# ===========================
# Export Python dependencies
# ===========================
_requirements:
	@echo "=============================================="
	@echo "Exporting Python dependencies to requirements.txt..."
	@echo "=============================================="
	poetry export -f requirements.txt --output requirements.txt --without-hashes --with dev
	@echo "\n"

# ============================
# Build Docker image
# ============================
build: _requirements
	@echo "=============================================="
	@echo "Building Docker image $(IMAGE_NAME):$(DEFAULT_TAG)..."
	@echo "=============================================="
	docker build --no-cache -t $(IMAGE_NAME):$(DEFAULT_TAG) .
	@echo "\n"

# ============================
# Start application with Docker Compose
# ============================
start: build
	@echo "========================="
	@echo "Starting the application..."
	@echo "========================="
	docker compose up -d --build
	@echo "Waiting for MongoDB to start..."
	@sleep 5
	@make init_mongo
	@echo "\n"
```

# Docker Compose

**Docker Compose** 환경에서 **Spark & MongoDB**를 연결해서 데이터를 저장해보는 실습을 수행해본다. 4일간의 삽질을 기록해본다.

## Docker Compose

```yaml
version: '3'
services:
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

volumes:
  data: {}

networks:
  mongodb_network:
    name: mongodb_network
```

## Init MongoDB Database

FILE PATH=**app/scrips/init_mongo.sh**

```shell
#!/bin/bash

# 4. MongoDB 초기화 작업 시작
echo "
====================================
Executing MongoDB Initialization
====================================
"

# MongoDB 초기화 명령어를 실행 (실행을 위해 /bin/bash 사용)
docker exec -i -t mongodb /bin/bash -c "mongosh -u rootuser -p rootpass <<EOF
use test

if (db.getUser(\"testuser\") == null) {
    db.createUser({
        \"user\": \"testuser\",
        \"pwd\": \"testpass\",
        \"roles\": [{\"role\": \"readWrite\", \"db\": \"test\"}]
    });
    print(\"User 'testuser' created successfully.\");
} else {
    print(\"User 'testuser' already exists.\");
}

if (db.getCollectionNames().indexOf(\"students\") === -1) {
    db.createCollection(\"students\");
    print(\"Collection 'students' created successfully.\");
} else {
    print(\"Collection 'students' already exists.\");
}
EOF"

# 7. MongoDB 초기화 완료 확인
if [ $? -eq 0 ]; then
    echo "
====================================
MongoDB Initialization Complete
====================================
"
else
    echo "
====================================
MongoDB Initialization Failed
====================================
"
    exit 1
fi

# 8. 이후 프로세스 실행
exec "$@"
```

## Check the MongoDB with Mongosh

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
