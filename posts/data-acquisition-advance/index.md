# Data Acquisition Advance


# Crawling > Recursive way

## Recursive Way Crawling

1. analyze a html file

2. extract links in the html

3. downloads the links if they are a file

4. if the file is a html file, go back to the first task

python 공식 문서의 데이터들 가져오기.

# Selenium Advanced

LinkedIn 접속 -> 로그인 -> 특정 조건 검색 -> 지원

# Web API

Client(Http Request) -> Server(Http Response) -> Client

- Client == Customer

- Server == Kitchen

- API == Waiter

## Features == Side Effect

- Crawling 표적이 될 수 있다.

- Web API는 변하거나 없어질 수 있다.

# Crontab Scheduling

Cron is the name of program that enables unix users to `execute commands or scripts(groups of commands) automatically at a specified time/date`.

It is normally used for sys admin commands, for `running a backup script`, but can be used for anything. A common use for it it today is `conecting to the internet and downloading your email`.

## What is crontab?

Crontab(CRON Table) is a `file` which `contains the schedule of cron entries` to be run and at specified times, File location varies by OS, See Crontab file location at hte end of this document.

## What is a cron job or cron schedule?

Cron job or cron schedule is a specific set of `execution instructions specifying day, time` and command to execute. Crontab can have `multiple execution statements`.

## Crontab Restriction

You can execute crontab if your name appears in the file /usr/lib/cron/cron.allow. If that file does not exist, you can use crontab if your name does not appear in the file `/usr/lib/cron/cron.deny`.

If only cron.deny exists and is empty, all users can use crontab. If neigher file exists, only the root user can use crontab. The allow/deny files consists of one user name per line.

## 주기 결정 예시

```shell
*　　　　　　 *　　　　　　  *　　　　　　 *　　　　　　  *
분(0-59)　　시간(0-23)　　일(1-31)　　월(1-12)　　　요일(0-7)
```

### 주기별 예제

#### 매분 실행

```shell
# 매분 test.sh 실행
* * * * * /home/script/test.sh
```

#### 특정 시간 실행

```shell
# 매주 금요일 오전 5시 45분에 test.sh 를 실행
45 5 * * 5 /home/script/test.sh
```

#### 반복 실행

```shell
# 매일 매시간 0분, 20분, 40분에 test.sh 를 실행
0,20,40 * * * * /home/script/test.sh
```

#### 범위 실행

```shell
# 매일 1시 0분부터 30분까지 매분 tesh.sh 를 실행
0-30 1 * * * /home/script/test.sh
```

#### 간격 실행

```shell
# 매 10분마다 test.sh 를 실행
*/10 * * * * /home/script/test.sh
```

#### 복잡하게 실행

```shell
# 5일에서 6일까지 2시,3시,4시에 매 10분마다 test.sh 를 실행
*/10 2,3,4 5-6 * * /home/script/test.sh
```

# Proxy Server

Server에서 특정 Target 서비스에 크롤링을 위해 많은 요청을 보내거나 오랫동안 요청시, 해당 서비스는 요청을 감지하고 해당 접근을 막아버린다.

`upcoming issue`: Too many requests 429 error or NoSuchElement, e.g., find_element()

## Role like 중개인

1. Client에서 Proxy Server로 전달할 `Request`를 보낸다.

2. Proxy Server는 Client로부터 전달 받은 `Request`를 Server에 요청한다.

3. Server는 `Request`에 대한 `Response`를 Proxy Server롤 전달한다.

4. Proxy Server는 해당 `Response`를 Client에 전달한다.

## Features

1. 보안: 다른 익명의 사용자는 Server의 위치 또는 IP를 알기

2. 캐시: 이전 요청들을 Proxy Server에 저장(Cache) 하여, 다음 번에 재요청시 본 Server를 거치지 않고 데이터를 빠르게 주고 받을 수 있다.

3. 우회: 1번 보안처럼 IP 주소를 감출 수 있으므로 어느 곳에서 Client가 접속한지 모른다.

## Type

### Forwarded Proxy

Client에서 Server로 요청 시 직접 요청이 아닌 Proxy Server를 거쳐, Forward Proxy라 지칭

<img src="/images/forward-proxy.png" />

### Reverse Proxy

Forward와 반대로 Server에서 Client로 직접 데이터를 전달하지 않고 Proxy Server를 거치는 방식

<img src="/images/reverse-proxy.png" />

