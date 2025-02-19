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
 {seilylook} 💎 brew install poetry

 {seilylook} 💎 poetry --version

 Poetry (version 1.8.5)
```

## New Project

설치를 마친 후 새 프로젝트를 생성해본다.

Project Name: **poetry-deom**

```bash
 {seilylook} 💎 poetry new poetry-demo
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
 {seilylook} 💎 cd pre-existing-project
 {seilylook} 💎 poetry init
```

## Add specifying dependencies

```bash
 {seilylook} 💎 poetry add pyspark

 {seilylook} 💎 poetry add pytest

 {seilylook} 💎 poetry add black --dev

 {seilylook} 💎 poetry add isort --dev
```

## Setup Project

### Install Python 3.12

```bash
 {seilylook} 💎 pyenv install 3.12
python-build: use openssl@3 from homebrew
python-build: use readline from homebrew
Downloading Python-3.12.4.tar.xz...
-> https://www.python.org/ftp/python/3.12.4/Python-3.12.4.tar.xz
Installing Python-3.12.4...
python-build: use readline from homebrew
python-build: use ncurses from homebrew
python-build: use zlib from xcode sdk

Installed Python-3.12.4 to /Users/minwook/.pyenv/versions/3.12.4

 {seilylook} 💎 pyenv local 3.12 # notify python version to pyenv
 {seilylook} 💎 pyenv global 3.12 # Set Python version globally
```

### Create poetry project

```bash
 {seilylook} 💎 poetry init

This command will guide you through creating your pyproject.toml config.

Package name [storyline]:  
Version [0.1.0]:  
Description []:  
Author [seilylook <seilylook@naver.com>, n to skip]:  
License []:  
Compatible Python versions [^3.12]:  ^3.12

Would you like to define your main dependencies interactively? (yes/no) [yes] 
You can specify a package in the following forms:
  - A single name (requests): this will search for matches on PyPI
  - A name and a constraint (requests@^2.23.0)
  - A git url (git+https://github.com/python-poetry/poetry.git)
  - A git url with a revision (git+https://github.com/python-poetry/poetry.git#develop)
  - A file path (../my-package/my-package.whl)
  - A directory (../my-package/)
  - A url (https://example.com/packages/my-package-0.1.0.tar.gz)

Package to add or search for (leave blank to skip): 

Would you like to define your development dependencies interactively? (yes/no) [yes] 
Package to add or search for (leave blank to skip): 

Generated file

[tool.poetry]
name = "storyline"
version = "0.1.0"
description = ""
authors = ["seilylook <seilylook@naver.com>"]
readme = "README.md"

[tool.poetry.dependencies]
python = "^3.12"


[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"


Do you confirm generation? (yes/no) [yes]
```

### Set virtualenv

```bash
 {seilylook} 💎 poetry env use $(pyenv which python) # set poetry env python version
 {seilylook} 💎 poetry config virtualenvs.in-project true # set virtualenv location in the current project
 {seilylook} 💎 poetry install # create virtualenv and install dependencies
 {seilylook} 💎 poetry env info

Virtualenv
Python:         3.12.4
Implementation: CPython
Path:           /Users/minwook/codes/work/playtag/src/storyline/.venv
Executable:     /Users/minwook/codes/work/playtag/src/storyline/.venv/bin/python
Valid:          True
```
