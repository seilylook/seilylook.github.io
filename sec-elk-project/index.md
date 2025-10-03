# SEC ELK Project


## 프로젝트 개요

SSH Brute Force 탐지 / 로그 수집 체계 구축

디렉토리 구조

```bash
sec-elk-project/
├─ docker-compose.yml
├─ logstash/
│  └─ config/
│     └─ logstash.yml
│  └─ pipeline/
│     └─ logstash.conf
├─ filebeat/
│  └─ filebeat.yml.sample
├─ docs/
│  └─ report.pdf
│  └─ presentation.pptx
└─ README.md
```

## 1. 환경 세팅

### Kali Linux에 docker / docker-compose 설치

```bash
kali@kali:~$ sudo apt update
kali@kali:~$
kali@kali:~$ sudo apt install -y docker.io
kali@kali:~$
kali@kali:~$ sudo systemctl enable docker --now
kali@kali:~$
kali@kali:~$ docker
kali@kali:~$
kali@kali:~$ sudo usermod -aG docker $USER
kali@kali:~$
kali@kali:~$ docker -v
Docker version 26.1.5+dfsg1, build ad a72d7cd
kali@kali:~$ docker compose
Command 'docker-compose' not found, but can be installed with:
sudo apt install docker-compose
Do you want to install it? y
Installing:
  docker-compose
```

### Kali Linux에 VScode 설치하기

```bash
kali@kali:~$ sudo apt update
kali@kali:~$
kali@kali:~$ wget -qO- https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > packages.microsoft.gpg
kali@kali:~$
kali@kali:~$ sudo install -o root -g root -m 644 packages.microsoft.gpg /etc/apt/trusted.gpg.d/
kali@kali:~$
kali@kali:~$ sudo sh -c 'echo "deb [arch=arm64 signed-by=/etc/apt/trusted.gpg.d/packages.microsoft.gpg] https://packages.microsoft.com/repos/vscode/ stable main" > /etc/apt/sources.list.d/vscode.list'
kali@kali:~$
kali@kali:~$ code .
```

{{<admonition warning>}}
마지막 명령어, sudo sh -c 부분에서 linux 종류(amd | arm)에 따라 적절하게 바꿔주어야 한다.
{{</admonition>}}

## 2. Kali Linux에서 ELK 설치 및 동작 확인

### docker-compose.yml

```yaml
version: '3.7'

services:
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:8.9.0
    container_name: elasticsearch
    environment:
      - discovery.type=single-node
      - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
      # 보안 비활성화 (개발/테스트 환경용)
      - xpack.security.enabled=false
      - xpack.security.enrollment.enabled=false
      - xpack.security.http.ssl.enabled=false
      - xpack.security.transport.ssl.enabled=false
    ulimits:
      memlock:
        soft: -1
        hard: -1
      nofile:
        soft: 65536
        hard: 65536
    volumes:
      - esdata:/usr/share/elasticsearch/data
    ports:
      - "9200:9200"
    networks:
      - elk

  logstash:
    image: docker.elastic.co/logstash/logstash:8.9.0
    container_name: logstash
    environment:
      - "LS_JAVA_OPTS=-Xms256m -Xmx256m"
    ports:
      - "5044:5044"   # beats input
      - "5000:5000"   # tcp input
      - "9600:9600"   # monitoring API
    volumes:
      - ./logstash/pipeline:/usr/share/logstash/pipeline
      - ./logstash/config/logstash.yml:/usr/share/logstash/config/logstash.yml
    networks:
      - elk
    depends_on:
      - elasticsearch

  kibana:
    image: docker.elastic.co/kibana/kibana:8.9.0
    container_name: kibana
    environment:
      - ELASTICSEARCH_HOSTS=http://elasticsearch:9200
      - ELASTICSEARCH_USERNAME=kibana_system
      - SERVER_NAME=kibana
    ports:
      - "5601:5601"
    networks:
      - elk
    depends_on:
      - elasticsearch:

networks:
  elk:
    driver: bridge

volumes:
  esdata:
    driver: local
```

### logstash/pipeline/logstash.conf

```conf
input {
    beats {
        port => 5044
    }
    tcp {
        port => 5000
        codec => json_lines
        type => "syslog"
    }
}
filter {
    if [fileset][module] == "system" {
        # System module
    }
    if [message] =~ /Failed password/ {
        mutate { add_tag => ["ssh_failed"] }
    }
    if [message] =~ /Accepted password/ {
        mutate { add_tag => ["ssh_success"] }
    }
}
output {
    elasticsearch {
        hosts => ["http://elasticsearch:9200"]
        index => "%{[@metadata][beat]-%{+YYYY.MM.dd}}"
    }
    stdout { code => rubydebug}
}
```

### logstash/config/logstash.yml

```yaml
http.host: "0.0.0.0"
xpack.monitoring.enabled: false
xpack.monitoring.elasticsearch.hosts: ["http://elasticsearch:9200"]
```

## 3. Kali에 Filebeat 설치 및 구성(로그 수집자)
