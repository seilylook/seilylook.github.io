# Poetry


# Introduction

`Poetry`는 Python 개발 시 패키지의 의존성을 관리하는 라이브러리이며, 자바의 Maven이나 Gradle과 비슷한 Tool이라고 볼 수 있다. 또한 **Virtualenv**와 같이 가상 환경 설정을 지원해, 보다 포괄적인 의미의 기능도 있으며 build / publish 같은 배포까지도 가능한 범용적인 Tool로도 사용할 수 있다. pip과는 다르게 `.toml`, `.lock` 파일을 생성해 의존성을 관리한다. 

- `.toml`: 프로젝트 의존성읠 메타 데이터 저장

    - 프로젝트와 의존성들 간의 충돌을 해결해준다.

- `.lock`: 설치된 패키지들의 version, hash 저장

    - 해당 파일을 사용해 프로젝트 의존성을 다른 환경에서도 동일하게 유지할 수 있도록 해준다.

## pip와의 차이점

pip의 가장 큰 단점은 패키지를 설치하면 전역적으로 설치가 된다는 점과 자신이 어떤 패키지를 설치했는지 확인하기 위해 `$ pip list`, `$ pip freeze` 명령어를 입력하면 **설치한 패키지 + 해당 패키지에 필요한 패키지(의존된 패키지)**들이 같이 나오게 된다. 이 문제는 `$ pip freeze > requirements.txt` 명령어를 통해 requirements.txt 파일을 생성할 때 더욱 귀찮다. `Poetry`는 이런 단점을 극복할 수 있는 라이브러리이다.

## Install

```bash
 brew install poetry

 {seilylook} 💎 poetry --version

 Poetry (version 1.8.5)
```

## New Project

설치를 마친 후 새 프로젝트를 생성해본다.

Project Name: **poetry-deom**

```bash
poetry new poetry-demo
```

위의 명령어를 입력하면 아래와 같이 프로젝트가 생성된 것을 확인할 수 있다.

```
poetry-demo
├── pyproject.toml
├── README.md
├── poetry_demo
│   └── __init__.py
└── tests
    └── __init__.py
```

`pyproject.toml`이 가장 중요하다. 이 파일은 프로젝트의 의존성들을 조직화해준다. 다음과 같은 형태로 보여진다.

```toml
[project]
name = "poetry-demo"
version = "0.1.0"
description = ""
authors = [
    {name = "Sébastien Eustace", email = "sebastien@eustace.io"}
]
readme = "README.md"
requires-python = ">=3.9"
dependencies = [
]

[build-system]
requires = ["poetry-core>=2.0.0,<3.0.0"]
build-backend = "poetry.core.masonry.api"
```

## Initializing a pre-existing project

새로운 프로젝트를 만드는 대신, Poetry는 `initialise`를 사용해 기존 프로젝트 Poetry를 적용할 수 있다. 

```bash
cd pre-existing-project
poetry init
```

## Add specifying dependencies

```bash
poetry add pyspark

poetry add pytest

poetry add black --dev

poetry add isort --dev
```
