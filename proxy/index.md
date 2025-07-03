# Proxy


# 프록시 서버 완벽 가이드: 개념부터 실제 구현까지

## 들어가며

현대 웹 개발과 네트워크 아키텍처에서 프록시 서버는 필수적인 구성 요소가 되었습니다. 로드 밸런싱, 보안, 캐싱, 그리고 다양한 네트워크 최적화를 위해 프록시 서버를 이해하고 활용하는 것은 개발자에게 매우 중요한 역량입니다.

## 프록시 서버란?

프록시 서버(Proxy Server)는 클라이언트와 서버 사이에서 중개 역할을 하는 서버입니다. "프록시(Proxy)"라는 단어 자체가 "대리인"을 의미하는 것처럼, 클라이언트를 대신해서 다른 서버에 요청을 전달하고 응답을 받아오는 역할을 합니다.

### 기본 작동 원리

```
클라이언트 → 프록시 서버 → 대상 서버
클라이언트 ← 프록시 서버 ← 대상 서버
```

1. 클라이언트가 프록시 서버에 요청을 보냅니다
2. 프록시 서버가 클라이언트를 대신해 대상 서버에 요청을 전달합니다
3. 대상 서버가 프록시 서버에 응답을 보냅니다
4. 프록시 서버가 클라이언트에게 응답을 전달합니다

## 프록시 서버의 종류

### 1. Forward Proxy (정방향 프록시)

Forward Proxy는 클라이언트와 인터넷 사이에 위치하여 클라이언트의 요청을 대신 처리합니다.

#### 특징
- 클라이언트가 프록시 서버를 명시적으로 설정
- 대상 서버는 프록시 서버의 IP만 확인 가능
- 클라이언트의 익명성 보장
- 기업 내부 네트워크에서 인터넷 접근 제어에 주로 사용

#### 활용 사례
```javascript
// 기업 내부에서 외부 API 호출 시 Forward Proxy 사용 예제
const https = require('https');
const HttpsProxyAgent = require('https-proxy-agent');

const proxyUrl = 'http://corporate-proxy:8080';
const agent = new HttpsProxyAgent(proxyUrl);

const options = {
  hostname: 'api.external-service.com',
  port: 443,
  path: '/data',
  method: 'GET',
  agent: agent
};

const req = https.request(options, (res) => {
  console.log(`상태 코드: ${res.statusCode}`);
  res.on('data', (chunk) => {
    console.log(chunk.toString());
  });
});

req.end();
```

### 2. Reverse Proxy (역방향 프록시)

Reverse Proxy는 서버와 인터넷 사이에 위치하여 서버를 대신해 클라이언트의 요청을 처리합니다.

#### 특징
- 클라이언트는 프록시 서버의 존재를 모름
- 여러 백엔드 서버를 하나의 진입점으로 통합
- 로드 밸런싱, SSL 종료, 캐싱 등의 기능 제공
- 서버의 익명성과 보안 강화

#### Nginx를 이용한 Reverse Proxy 설정 예제

```nginx
# /etc/nginx/sites-available/reverse-proxy
upstream backend_servers {
    server 192.168.1.10:3000 weight=3;
    server 192.168.1.11:3000 weight=2;
    server 192.168.1.12:3000 weight=1;
}

server {
    listen 80;
    server_name example.com;

    location / {
        proxy_pass http://backend_servers;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # 타임아웃 설정
        proxy_connect_timeout 30s;
        proxy_send_timeout 30s;
        proxy_read_timeout 30s;
    }

    # 정적 파일 캐싱
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
        proxy_pass http://backend_servers;
        proxy_cache my_cache;
        proxy_cache_valid 200 1h;
        add_header X-Cache-Status $upstream_cache_status;
    }
}
```

## 프록시 서버의 주요 기능

### 1. 캐싱 (Caching)

프록시 서버는 자주 요청되는 리소스를 캐시하여 응답 속도를 향상시킵니다.

```python
# Python Flask를 이용한 간단한 캐싱 프록시 구현
from flask import Flask, request, Response
import requests
import hashlib
import time

app = Flask(__name__)
cache = {}
CACHE_DURATION = 300  # 5분

def get_cache_key(url, headers):
    content = f"{url}:{str(sorted(headers.items()))}"
    return hashlib.md5(content.encode()).hexdigest()

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def proxy(path):
    target_url = f"http://target-server.com/{path}"
    cache_key = get_cache_key(target_url, dict(request.headers))
    
    # 캐시 확인
    if cache_key in cache:
        cached_response, timestamp = cache[cache_key]
        if time.time() - timestamp < CACHE_DURATION:
            return Response(
                cached_response['content'],
                status=cached_response['status'],
                headers=cached_response['headers']
            )
    
    # 실제 요청 수행
    response = requests.get(target_url, headers=dict(request.headers))
    
    # 캐시 저장
    cache[cache_key] = ({
        'content': response.content,
        'status': response.status_code,
        'headers': dict(response.headers)
    }, time.time())
    
    return Response(
        response.content,
        status=response.status_code,
        headers=dict(response.headers)
    )

if __name__ == '__main__':
    app.run(port=8080)
```

### 2. 로드 밸런싱 (Load Balancing)

여러 서버 간의 트래픽을 분산하여 시스템의 가용성과 성능을 향상시킵니다.

```javascript
// Node.js를 이용한 라운드 로빈 로드 밸런서
const http = require('http');
const httpProxy = require('http-proxy');

const servers = [
  'http://server1:3000',
  'http://server2:3000',
  'http://server3:3000'
];

let currentIndex = 0;

const proxy = httpProxy.createProxyServer({});

// 헬스 체크를 위한 서버 상태 관리
const serverHealth = servers.map(() => true);

function getNextServer() {
  // 건강한 서버만 선택
  const healthyServers = servers.filter((_, index) => serverHealth[index]);
  
  if (healthyServers.length === 0) {
    throw new Error('모든 서버가 다운되었습니다');
  }
  
  const server = healthyServers[currentIndex % healthyServers.length];
  currentIndex++;
  return server;
}

// 헬스 체크 함수
function healthCheck() {
  servers.forEach((server, index) => {
    http.get(`${server}/health`, (res) => {
      serverHealth[index] = res.statusCode === 200;
    }).on('error', () => {
      serverHealth[index] = false;
    });
  });
}

// 5초마다 헬스 체크 수행
setInterval(healthCheck, 5000);

const server = http.createServer((req, res) => {
  try {
    const target = getNextServer();
    console.log(`요청을 ${target}로 전달`);
    
    proxy.web(req, res, {
      target: target,
      changeOrigin: true
    });
  } catch (error) {
    res.writeHead(503, { 'Content-Type': 'text/plain' });
    res.end('서비스를 사용할 수 없습니다');
  }
});

server.listen(8080, () => {
  console.log('로드 밸런서가 8080 포트에서 실행 중입니다');
});
```

### 3. SSL 종료 (SSL Termination)

프록시 서버에서 SSL/TLS 암호화를 처리하여 백엔드 서버의 부하를 줄입니다.

```yaml
# Docker Compose를 이용한 SSL 종료 프록시 설정
version: '3.8'

services:
  nginx-proxy:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - app1
      - app2

  app1:
    image: node:alpine
    command: node server.js
    expose:
      - "3000"

  app2:
    image: node:alpine
    command: node server.js
    expose:
      - "3000"
```

## 프록시 서버의 장점

### 1. 성능 향상
- **캐싱**: 자주 요청되는 리소스를 캐시하여 응답 시간 단축
- **압축**: 데이터 압축을 통한 대역폭 절약
- **연결 풀링**: 백엔드 서버와의 연결을 재사용하여 오버헤드 감소

### 2. 보안 강화
- **방화벽 역할**: 악성 요청 필터링
- **IP 은닉**: 실제 서버의 IP 주소 숨김
- **DDoS 방어**: 트래픽 분산을 통한 공격 완화

### 3. 확장성
- **로드 밸런싱**: 여러 서버로 트래픽 분산
- **수평 확장**: 새로운 서버 추가가 용이
- **단일 진입점**: 클라이언트에게 일관된 인터페이스 제공

## 프록시 서버의 단점

### 1. 복잡성 증가
- 네트워크 아키텍처가 복잡해짐
- 디버깅과 모니터링이 어려워질 수 있음
- 추가적인 관리 포인트 생성

### 2. 단일 장애점 (SPOF)
- 프록시 서버에 문제가 발생하면 전체 서비스 영향
- 고가용성 구성이 필요

### 3. 지연 시간
- 추가적인 네트워크 홉으로 인한 지연
- 프록시 서버 처리 시간

## 실제 구현 시 고려사항

### 1. 모니터링 및 로깅

```python
# 프록시 서버 모니터링을 위한 메트릭 수집
import time
import logging
from collections import defaultdict

class ProxyMetrics:
    def __init__(self):
        self.request_count = defaultdict(int)
        self.response_times = defaultdict(list)
        self.error_count = defaultdict(int)
    
    def record_request(self, endpoint, response_time, status_code):
        self.request_count[endpoint] += 1
        self.response_times[endpoint].append(response_time)
        
        if status_code >= 400:
            self.error_count[endpoint] += 1
    
    def get_average_response_time(self, endpoint):
        times = self.response_times[endpoint]
        return sum(times) / len(times) if times else 0
    
    def get_error_rate(self, endpoint):
        total = self.request_count[endpoint]
        errors = self.error_count[endpoint]
        return (errors / total) * 100 if total > 0 else 0

metrics = ProxyMetrics()

# 요청 처리 시 메트릭 수집
def handle_request(endpoint):
    start_time = time.time()
    
    try:
        # 실제 요청 처리
        response = process_request(endpoint)
        status_code = response.status_code
    except Exception as e:
        logging.error(f"요청 처리 중 오류: {e}")
        status_code = 500
    
    response_time = time.time() - start_time
    metrics.record_request(endpoint, response_time, status_code)
    
    return response
```

### 2. 보안 헤더 설정

```nginx
# 보안 강화를 위한 Nginx 설정
server {
    # 보안 헤더 추가
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header Content-Security-Policy "default-src 'self'" always;
    
    # 서버 정보 숨기기
    server_tokens off;
    
    # Rate Limiting
    limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
    
    location /api/ {
        limit_req zone=api burst=20 nodelay;
        proxy_pass http://backend_servers;
    }
}
```

### 3. 오류 처리 및 Fallback

```javascript
// Express.js를 이용한 프록시 서버의 오류 처리
const express = require('express');
const { createProxyMiddleware } = require('http-proxy-middleware');

const app = express();

const proxyOptions = {
  target: 'http://backend-server',
  changeOrigin: true,
  onError: (err, req, res) => {
    console.error('프록시 오류:', err.message);
    
    // Fallback 응답
    res.status(503).json({
      error: '서비스 일시 중단',
      message: '잠시 후 다시 시도해주세요',
      timestamp: new Date().toISOString()
    });
  },
  onProxyReq: (proxyReq, req, res) => {
    // 요청 로깅
    console.log(`${req.method} ${req.url} -> ${proxyReq.path}`);
  },
  timeout: 30000,
  proxyTimeout: 30000
};

app.use('/api', createProxyMiddleware(proxyOptions));

// 헬스 체크 엔드포인트
app.get('/health', (req, res) => {
  res.json({ status: 'healthy', timestamp: new Date().toISOString() });
});

app.listen(8080, () => {
  console.log('프록시 서버가 8080 포트에서 실행 중입니다');
});
```

## 마치며

프록시 서버는 현대 웹 아키텍처에서 핵심적인 역할을 합니다. 적절한 프록시 서버 구성을 통해 성능, 보안, 확장성을 모두 향상시킬 수 있습니다. 하지만 복잡성 증가와 추가적인 관리 포인트라는 단점도 고려해야 합니다.

프록시 서버를 도입할 때는 비즈니스 요구사항과 기술적 제약사항을 충분히 고려하여 적절한 솔루션을 선택하는 것이 중요합니다. 또한 지속적인 모니터링과 성능 튜닝을 통해 최적의 성능을 유지해야 합니다.
