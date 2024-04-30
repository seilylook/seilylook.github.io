# HDFS Project 1


# Install Hadoop

강의대로 2.7.6으로 하려했는데, 도저히 에러가 잡히지 않아, 3.3.2로 진행.

```bash
# https://hadoop.apache.org/release/3.3.2.html
# 접속해서 hadoop-3.3.2.tar.gz 다운로드

# 압축 해제
tar -xvf hadoop-3.3.2.tar.gz

# 링크 연결
ln -s hadoop-3.3.2 hadoop

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

hadoop -> hadoop-3.3.2
hadoop-3.3.2
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

# Hadoop Configuration

## JDK & Hadoop path 지정

```bash
{seilylook} 💡 ~/Development/DataEngineering/Data_HDFS/hadoop-3.3.2 cd etc/hadoop

{seilylook} 💡 ~/Development/DataEngineering/Data_HDFS/hadoop-3.3.2/etc/hadoop vim hadoop-env.sh
```

### hadoop-env.sh

파일 가장 아래에 다음과 같이 JAVA_HOME 설정을 해준다.

```shell
export JAVA_HOME=/Library/Java/JavaVirtualMachines/temurin-8.jdk/Contents/Home
```

## core site 설정

```bash
{seilylook} 💡   ~/Development/DataEngineering/Data_HDFS/hadoop-3.3.2/etc/hadoop  vim core-site.xml
```

### core-site.xml

```xml
<configuration>
  <property>
    <name>fs.defaultFS</name>
    <value>hdfs://localhost:9000</value>
  </property>
</configuration>
```

## hdfs site 설정

```bash
{seilylook} 💡   ~/Development/DataEngineering/Data_HDFS/hadoop-3.3.2/etc/hadoop  vim hdfs-site.xml
```

### hdfs-site.xml

```xml
<configuration>
    <property>
        <name>dfs.replication</name>
        <value>1</value>
    </property>

    <property>
        <name>dfs.block.size</name>
        <value>268435456</value>
    </property>
</configuration>
```

이제 로컬에서 `MapReduce`를 실행해 볼 수 있지만,

YARN으로 맵리듀스 및 리소스매니저와 노드매니저 `daemon`을 실행해보기 위해 추가적으로 더 환경 변수를 수정해준다.

## mapred site 설정

```bash
{seilylook} 💡   ~/Development/DataEngineering/Data_HDFS/hadoop-3.3.2/etc/hadoop  vim mapred-site.xml
```

### mapred-site.xml

```xml
<configuration>
  <property>
    <name>mapreduce.framework.name</name>
    <value>yarn</value>
  </property>
  <property>
    <name>mapreduce.application.classpath</name>
    <value
      >$HADOOP_MAPRED_HOME/share/hadoop/mapreduce/*:$HADOOP_MAPRED_HOME/share/hadoop/mapreduce/lib/*</value
    >
  </property>
</configuration>
```

## yarn site 설정

```bash
{seilylook} 💡   ~/Development/DataEngineering/Data_HDFS/hadoop-3.3.2/etc/hadoop  vim yarn-site.xml
```

### yarn-site.xml

```xml
<configuration>
  <property>
    <name>yarn.nodemanager.aux-services</name>
    <value>mapreduce_shuffle</value>
  </property>
  <property>
    <name>yarn.nodemanager.env-whitelist</name>
    <value
      >JAVA_HOME,HADOOP_COMMON_HOME,HADOOP_HDFS_HOME,HADOOP_CONF_DIR,CLASSPATH_PREPEND_DISTCACHE,HADOOP_YARN_HOME,HADOOP_HOME,PATH,LANG,TZ,HADOOP_MAPRED_HOME</value
    >
  </property>
</configuration>
```

## Execution, Namemode front

```bash
{seilylook} 💡 ~/Development/DataEngineering/Data_HDFS/hadoop-3.3.2/etc/hadoop cd ../../

{seilylook} 💡 ~/Development/DataEngineering/Data_HDFS/hadoop-3.3.2 bin/hadoop namenode -format
```

## Execution

### Hadoop 실행

```bash
{seilylook} 💡 ~/Development/DataEngineering/Data_HDFS/hadoop-3.3.2 cd sbin

./start-all.sh
# 또는 로컬에서 맵리듀스 실행
./start-dfs.sh
# 또는 yarn에서 맵리듀스 실행
./start-yarn.sh
```

위 명령어를 입력해주면 실행된다.

또한 `MapReduce` 실행을 위해서 HDFS 디렉터리가 필요하므로 만들어둔다.

```bash
# 경로는 하둡 최상위 경로에서 실행
# cd /opt/homebrew/Cellar/hadoop/3.3.2
bin/hdfs dfs -mkdir /user
bin/hdfs dfs -mkdir /user/<username>
```

### 실행 확인

```bash
jps
```

jps를 터미널에 입력하면, 하둡이 정상 설치 및 실행되고 있음을 보여준다.

```bash
{seilylook} 🇰 ~/Development/DataEngineering/Data_HDFS/hadoop-3.3.2/sbin jps

52304 DataNode
52448 SecondaryNameNode
52198 NameNode
52554 Jps
```

그럼 이제 localhost 로 접속해서 확인해보자

Cluster status : http://localhost:8088

HDFS status : http://localhost:9870

Secondary NameNode status : http://localhost:9868

### 실행 종료

```bash
## 만약 경로가 하둡 최상단 경로가 아니라면 다시 들어가준다.
## 하지만 해당 경로에서 ./start-all.sh 로 실행 해 줬기 때문에
## 그냥 아래 ./stop-all.sh만 실행해주면 된다.

./stop-all.sh
# 또는
./stop-dfs.sh
# 또는
./stop-yarn.sh
```

