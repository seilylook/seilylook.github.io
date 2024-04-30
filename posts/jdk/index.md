# JDK Version Change


# openJDK version 여러개 사용하기

{{<admonition tip>}}
2024년 4월 기준으로 adoptopenjdk의 JDK 8 버전은 deprecated 되었다. 이를 해결하기 위해 `temurin`을 사용해 JDK 8 버전을 설치해야 한다.
{{</admonition>}}

## temurin 8 설치

```bash
brew install --cask temurin@8
```

설치하고나서 확인하면 다음과 같이 2개 버전의 자바를 djk를 볼 수 있다.

```bash
 {seilylook} 💡 /usr/libexec/java_home -V
Matching Java Virtual Machines (2):

    11.0.22 (arm64) "Homebrew" - "OpenJDK 11.0.22" /opt/homebrew/Cellar/openjdk@11/11.0.22/libexec/openjdk.jdk/Contents/Home
    1.8.0_412 (x86_64) "Eclipse Temurin" - "Eclipse Temurin 8" /Library/Java/JavaVirtualMachines/temurin-8.jdk/Contents/Home
/opt/homebrew/Cellar/openjdk@11/11.0.22/libexec/openjdk.jdk/Contents/Home
```

## ZSH script 수정

상황에 따른 버전을 설정해주기 위해 zsh script를 수정해준다.

```bash
 {seilylook} 💡 vim ~/.zshrc

export JAVA_HOME=$(/usr/libexec/java_home -v 1.8)

export PATH="/opt/homebrew/opt/openjdk@11/bin:$PATH"

export PATH="$JAVA_HOME/bin:$PATH"

export PATH="/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:/usr/local/sbin:$PATH"

alias setJava8='export JAVA_HOME=$(/usr/libexec/java_home -v 1.8); export PATH="$JAVA_HOME/bin:$PATH"'

alias setJava11='export JAVA_HOME=$(/usr/libexec/java_home -v 11); export PATH="$JAVA_HOME/bin:$PATH"'
```

## 버전 변경

```bash
{seilylook} 💡 setJava8
{seilylook} 💡 java -version
openjdk version "1.8.0_412"
OpenJDK Runtime Environment (Temurin)(build 1.8.0_412-b08)
OpenJDK 64-Bit Server VM (Temurin)(build 25.412-b08, mixed mode)

{seilylook} 💡 setJava11
{seilylook} 💡 java -version
openjdk version "11.0.22" 2024-01-16
OpenJDK Runtime Environment Homebrew (build 11.0.22+0)
OpenJDK 64-Bit Server VM Homebrew (build 11.0.22+0, mixed mode)
```

