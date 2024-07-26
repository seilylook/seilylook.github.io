# Yaml


# What is YAML?

시스템 간 데이터를 교화할 때 데이터의 연동과 호환성을 위해 **포맷에 대한 규칙**이 필요해졌다. 

기존에 사용하던 XML은 사용하기 까다롭고 가독성이 매우 떨어지기 떄문에 JSON으로 변경되다가, JSON 역시 주석을 달 수 없는 등 제한이 있고 중괄호/대괄호로 인해 코드 길이가 증가하는 단점이 존재했다. 

이런 문제점을 해결하기 위해 `YAML`이 등장하게 된다.

<img src="/images/yaml/xml-yaml.png" />

YAML은 XML과 JSON 포맷과 같이 타 시스템 간에 데이터를 주고 받을 때 약속된 포맷이 정의된 파일 형식이라 할 수 있다.

## YAML 문법 정리

### 데이터 정의 

#### Key : Value

JSON 포맷과 같이 기본적으로 key: value는 **:**을 기준으로 구분된다.

단, 주의할 점은 value를 쓸 때 반드시 **콜론(:) 뒤에 띄어쓰기를 한번** 해주어야 한다.

```yaml
name: sehyeonkim
age: 22
position: data-engineer
```

#### Indent

중괄호로 계층 구조를 표현하는 JSON과 달리, YAML은 파이썬과 마찬가지로 들여쓰기로 계층 구조를 표현한다.

예를 들어, `client` 속성 안에 `name`, `age`, `position` 키를 가진 객체를 포함하게 만들면, 들여쓰기를 통해 관계를 표시해준다.

```yaml
client:
  name: sehyeonkim
  age: 22
  position: data-engineer
```

#### "따옴표"

JSON을 작성할 떄는 기본적으로 따옴표을 붙여줘야 하지만, YAML을 쓸 때는 큰 따옴표, 작은 따옴표 혹은 안 써도 자동으로 숫자 혹은 문자로 인식된다.

만약 `:`가 들어간 문자열의 경우, 무조건 따옴표로 적어줘야 인식한다.

```yaml
name: seilylook
phone1: 010
phone2: 0000
phone3: 0000
residence: "10:20:30:40"
```

##### 큰 따옴표 작은 따옴표 차이

YAML에서는 문자 데이터를 표현할 때 따옴표를 안 써도 되지만, **이스케이프 문자**를 구분할 때는 이 둘을 구분해서 사용해야 한다.

예를 들어 큰 따옴표는 escape sequence 처리를 해주고, 작은 따옴표는 주어진 그대로 문자열 처리한다.

아래와 같이 `\n` 문자를 큰 따옴표로 묶으면 **개행 문자**로 인식되고, 작은 따옴표로 묶으면 **문자 그대로 \n** 처리해준다.

```yaml
test1: "\t abc \n de"
test2: '\t abs \n de'
```

### 배열 & 리스트

#### 배열

YAML에서 배열을 표현할 때는 `-`으로 시작하는 하위 엘리먼트로 표현한다.

```yaml
command:
  - sleep
  - "4800"
```

```json
{
    command: [
        "sleep",
        "4800",
    ]
}
```

#### 객체 배열

객체 리스트를 표현할 때 `-`과 `key: value` 구조를 사용해 객체를 가지는 배열을 표현 가능하다.

이때 하나의 객체 중과호 쌍인 것을 나타내기 위해, 하나의 객체 원솜녀 `-`을 쓰지 않고 그대로 나열한다.

객체 배열을 만들 때, 앞에 들여써도 되고 들여쓰지 않아도 의미는 같다.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: multi-pod
spec:
  containers:
    - name: alpha
      image: nginx
      env:
        - name: name
          value: alpha
    - name: beta
      image: busybox
      command:
        - sleep
        - "4800"
      env: 
        - name: name
          value: beta
```

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: multi-pod
spec:
  containers:
  - name: alpha
    image: nginx
    env: 
    - name: name
      value: alpha
  - name: beta
    image: busybox
    command:
    - sleep
    - "4800"
    env:
    - name: name
      value: beta
```

```json
{
    "apiVersion": "v1",
    "kind": "Pod",
    "metadata": {
        "name": "multi-pod"
    },
    "spec": {
        "containers": [
            {
                "name": "alpha",
                "image": "nginx",
                "env": [
                    {
                        "name": "name",
                        "value": "alpha"
                    }
                ]
            },
            {
                "name": "beta",
                "image": "busybox",
                "command": [
                    "sleep",
                    "4800"
                ],
                "env": [
                    {
                        "name": "name",
                        "value": "beta"
                    }
                ]
            }
        ]
    }
}
```
