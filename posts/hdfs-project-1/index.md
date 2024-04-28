# HDFS Project 1


# Install Hadoop

```bash
# https://hadoop.apache.org/release/2.7.6.html
# 접속해서 hadoop-2.7.6.tar.gz 다운로드

# 압축 해제
tar -xvf hadoop-2.7.6.tar.gz

# 링크 연결
ln -s hadoop-2.7.6 hadoop

# 환경 세팅
(venv)  {seilylook} 👑 vim hadoop/etc/hadoop/*
```

{{<admonition info>}}
리눅스 명령어 -ln

리눅스에서 ln 명령어를 사용하면 리눅스 파일 시스템에서 링크 파일을 생성할 수 있다.

1.  심볼릭 링크
    단순히 원본 파일을 가리키도록 링크만 걸어둔 것으로 MS의 윈도우 시스템에서 흔히 사용하는 '바로가기' 같은 것이며, 원본 파일을 가리키고만 있으므로 원본 파일의 크기와는 무관하다. 원본파일이 삭제되어 존재하지 않을 경우 링크 파일은 깜빡거리면서 링크 파일의 원본이 없어진 것을 알려준다.

    명령어: ln -s TARGET(원본) LINK_NAME(링크이름)

2.  하드 링크
    원본 파일과 다른 이름으로 존재하는 동일한 파일이며, 원본 파일과 동일한 내용의 다른 파일이라고 할 수 있다. 그리고 하드 링크에서는 원본 파일과 링크 파일 두개가 서로 다른 파일이기 때문에 둘 중 하나를 삭제하더라도 나머지 하나는 그대로 남아있다.

        명령어: ln TARGET(원본) LINK_NAME(링크이름)

    {{</admonition>}}

```bash
(venv)  {seilylook} 👑 ll

hadoop -> hadoop-2.7.6
hadoop-2.7.6
venv
```

# Passphraseless SSH

아래를 입력했을 때 비밀번호를 입력하라고 뜨면, 비밀번호를 계속 입력하지 않도록 설정해주어야 한다.

```bash
$ ssh localhost
```

```bash
(venv)  {seilylook} 👑 ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa

Generating public/private rsa key pair.
Your identification has been saved in /Users/seilylook/.ssh/id_rsa
Your public key has been saved in /Users/seilylook/.ssh/id_rsa.pub
The key fingerprint is:
SHA256:/x2uTFGZeRvZ+WADOC4ouw4D25H56UyJVnTDxrTTjps seilylook@gimsehyeon-ui-MacBookPro.local
The key's randomart image is:
+---[RSA 3072]----+
|      .    ..    |
|     + o  o  . ++|
|    . O... .  O+o|
|   +.o.=. .  o ++|
|. + .o. S.  .  ..|
| + =.o o .   .   |
|. * =.E   . . .  |
| . *.      + o . |
|   .+       +.o  |
+----[SHA256]-----+

(venv)  {seilylook} 👑 cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys

(venv)  {seilylook} 👑 chmod 0600 ~/.ssh/authorized_keys
```

```bash
 {seilylook} 😎 ssh localhost
Last login: Sun Apr 28 17:10:23 2024 from ::1
```

