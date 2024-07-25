# Linux


## 기본 명령어 정리

| 명령어 및 기능         | 설명                          |
|:----------------------:|:-----------------------------:|
| `ls`                  | 현재 디렉토리의 파일 목록 표시  |
| `ls -l`               | 상세 파일 목록 표시            |
| `ls -al`              | 숨겨진 파일을 포함한 상세 목록 |
| `cat`                 | 파일 전체 내용 출력            |
| `more`                | 파일 내용을 페이지 단위로 출력 |
| `less`                | 파일 내용을 스크롤 가능하게 출력 |
| `touch`               | 빈 파일 생성 또는 파일 시간 변경 |
| `rm`                  | 파일 삭제                     |
| `cp`                  | 파일 복사                     |
| `mv`                  | 파일 이동 또는 이름 변경       |
| `ln`                  | 심볼릭 링크 생성              |
| `file`                | 파일 형식 확인                |
| `mkdir`               | 디렉토리 생성                 |
| `rmdir`               | 빈 디렉토리 삭제              |
| `cd`                  | 디렉토리 변경                 |
| `cd -`                | 이전 디렉토리로 이동          |
| `.`                   | 현재 디렉토리                 |
| `..`                  | 상위 디렉토리                 |
| `~`                   | 홈 디렉토리                   |
| `clear`               | 터미널 화면 지우기            |
| `reboot`              | 시스템 재부팅                 |
| `poweroff`, `shutdown`| 시스템 종료                   |

### cat(concatenate)

cat [OPTION] ... [FILE] ...

파일 내용 보여주기(정확히는 input과 output을 연결(concatenate) 하기)

- cat hello.txt

- cat /etc/kubernetes/manifestss/kube-apiserver.yaml

- cat /var/log/syslog

- cat -e /etc/passwd : 줄의 맨 뒤에 $ 붙이기(히든 캐릭터 공백 등 확인)

- cat -n /etc/passwd : 줄 번호 보여주기

### more

more [OPTION] ... [FILE] ...

파일 내용 보여주기 (페이지 단위로 이동 - space | 줄 단위로 이동 - enter)

- more hello.txt

- more /etc/passwd

- more /var/log/syslog

### less

less [OPTION] ... [FILE] ...

파일 내용 보여주기 (페이지 단위로 이동 - space | 줄 단위로 이동 - enter | 방향키 - 상하좌우, 페이지 up/down)

- less hello.txt

- less /etc/passwd

- less /var/log/syslog

more 보다 향상된 기능, 그리고 몯느 파일을 메모리에 올리지 않아 more 대비 속도바 빠르다.


