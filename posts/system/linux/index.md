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

### rm

rm [OPTION] ... [FILE] ...

- rm hello.txt

- rm test1 test2 test3

- rm /etc/passwd(실패)

### mkdir / rmdir

mkdir [OPTION] ... [DIRECTORY] ...

- mkdir dir1

- mkdir dir2 dir3

- mkdir -p dir2/sub1 (parents)

rmdir [OPTION] ... [DIRECTORY] ...

- rmdir dir1

- rmdir dir2 dir3

- rm -r dir1 (recursive)

### cd(change directory)

- cd dir1 

- cd .. (부모 디렉토리 이동)

- cd dir1/sub1

- cd .

- cd ../..

- cd ~/ (홈 디렉토리)

- cd - (이전 디렉토리)

- 디렉토리 구조

  - . : 나 자신

  - .. : 부모 디렉토리

  - ~ : 홈 디렉토리

  - *-* : 이전 디렉토리

### cp - copy | mv - move

cp [OPTION] ... [원본][타겟]

- touch hello.txt test1 test2

- mkdir dir1

- cp hello.txt hellow2.txt : 파일 복사

- cp test1 dir1 : 파일 디렉토리 안으로 복사

- cp test2 dir1 : 파일 디렉토리 안으로 복사

- cp -r dir1 dir2 : 디렉토리 복사

- rm -r dir1 dir2 : 삭제

### ln - link

ln [OPTION] ... [TARGET][LINKNAME]

파일에 하드 링크/소프트링크 만들기

- touch hello.txt

- ln -s hello.txt hellosymlink

- ln hello.txt hellolink

- ls -ali

<img src="/images/linux/hardlink-softlink.webp" />

### file 

file [OPTION] ... [FILE] ...

- file hello

- file /etc/passwd

- file dir

- file /usr/bin/file

- file hellosymlink

### reboot, poweroff, shutdown

- reboot

- poweroff 

- showdown [OPTIONS][TIME]

  - shutdown -P now : 바로 종료

  - shutdown -r now : 바로 재시작

### vi | vim | nano

- vi hello.txt

- vi /etc/passwd

- nano hello.txt

- nano /etc/passwd

## Bash Shell



