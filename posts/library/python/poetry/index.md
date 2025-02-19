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
name = ""
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
Python:         3.12.8
Implementation: CPython
Path:           /Users/seilylook/Development/Book/Data_Engineering_with_Python/app/.venv
Executable:     /Users/seilylook/Development/Book/Data_Engineering_with_Python/app/.venv/bin/python
Valid:          True

Base
Platform:   darwin
OS:         posix
Python:     3.12.8
Path:       /Users/seilylook/.pyenv/versions/3.12.8
Executable: /Users/seilylook/.pyenv/versions/3.12.8/bin/python3.12
```

### Custom version 

```bash
 {seilylook} 🚀 poetry env info                          

Virtualenv
Python:         3.12.8
Implementation: CPython
Path:           /Users/seilylook/Development/Book/Data_Engineering_with_Python/app/.venv
Executable:     /Users/seilylook/Development/Book/Data_Engineering_with_Python/app/.venv/bin/python
Valid:          True

Base
Platform:   darwin
OS:         posix
Python:     3.12.8
Path:       /Users/seilylook/.pyenv/versions/3.12.8
Executable: /Users/seilylook/.pyenv/versions/3.12.8/bin/python3.12
```

{{<admonition info>}}
Apache Airflow의 최신 버전인 2.10.5는 파이썬 최소 | 최대 버전을 설정해 주어야 한다. 이를 위해선 `poetry add apache-airflow`가 아닌 특정 version을 포함해서 설치해 주도록 `pyproject.toml`에 **version**을 직접 설정해준다.

이어서 `poetry update` 명령어를 통해 custom version의 package를 설치할 수 있다.
{{</admonition>}}

```toml
[tool.poetry]
name = "app"
version = "0.1.0"
description = ""
authors = ["seilylook <seilylook@naver.com>"]
readme = "README.md"

[tool.poetry.dependencies]
python = "^3.12"
apache-airflow = {version = "^2.10.5", python = ">=3.8.1,<3.13"}

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
```

```bash
 {seilylook} 🚀 poetry update  
Updating dependencies
Resolving dependencies... (18.0s)

Package operations: 136 installs, 0 updates, 0 removals

  - Installing wrapt (1.17.2)
  - Installing zipp (3.21.0)
  - Installing attrs (25.1.0)
  - Installing deprecated (1.2.18)
  - Installing markupsafe (3.0.2)
  - Installing mdurl (0.1.2)
  - Installing rpds-py (0.22.3)
  - Installing importlib-metadata (8.5.0)
  - Installing typing-extensions (4.12.2)
  - Installing click (8.1.8)
  - Installing referencing (0.36.2)
  - Installing werkzeug (2.2.3)
  - Installing markdown-it-py (3.0.0)
  - Installing opentelemetry-api (1.30.0)
  - Installing packaging (24.2)
  - Installing protobuf (5.29.3)
  - Installing pygments (2.19.1)
  - Installing itsdangerous (2.2.0)
  - Installing jinja2 (3.1.5)
  - Installing babel (2.17.0)
  - Installing opentelemetry-proto (1.30.0)
  - Installing opentelemetry-semantic-conventions (0.51b0)
  - Installing dnspython (2.7.0)
  - Installing flask (2.2.5)
  - Installing frozenlist (1.5.0)
  - Installing idna (3.10)
  - Installing jsonschema-specifications (2024.10.1)
  - Installing limits (4.0.1)
  - Installing marshmallow (3.26.1)
  - Installing multidict (6.1.0)
  - Installing certifi (2025.1.31)
  - Installing charset-normalizer (3.4.1)
  - Installing ordered-set (4.1.0)
  - Installing propcache (0.2.1)
  - Installing pyjwt (2.10.1)
  - Installing pytz (2025.1)
  - Installing pyyaml (6.0.2)
  - Installing rich (13.9.4)
  - Installing six (1.17.0)
  - Installing sqlalchemy (1.4.54)
  - Installing urllib3 (2.3.0)
  - Installing wtforms (3.2.1)
  - Installing aiohappyeyeballs (2.4.6)
  - Installing apispec (6.8.1)
  - Installing colorama (0.4.6)
  - Installing email-validator (2.2.0)
  - Installing flask-babel (2.0.0)
  - Installing flask-jwt-extended (4.7.1)
  - Installing flask-limiter (3.10.1)
  - Installing flask-login (0.6.3)
  - Installing flask-sqlalchemy (2.5.1)
  - Installing flask-wtf (1.2.2)
  - Installing googleapis-common-protos (1.67.0)
  - Installing grpcio (1.70.0)
  - Installing h11 (0.14.0)
  - Installing jsonschema (4.23.0)
  - Installing marshmallow-sqlalchemy (0.28.2)
  - Installing aiosignal (1.3.2)
  - Installing more-itertools (10.6.0)
  - Installing opentelemetry-exporter-otlp-proto-common (1.30.0)
  - Installing opentelemetry-sdk (1.30.0)
  - Installing prison (0.2.1)
  - Installing pycparser (2.22)
  - Installing python-dateutil (2.9.0.post0)
  - Installing requests (2.32.3)
  - Installing sniffio (1.3.1)
  - Installing sqlalchemy-utils (0.41.2)
  - Installing sqlparse (0.5.3)
  - Installing yarl (1.18.3)
  - Installing text-unidecode (1.3)
  - Installing aiohttp (3.11.12)
  - Installing aiosqlite (0.21.0)
  - Installing anyio (4.8.0)
  - Installing apache-airflow-providers-common-compat (1.3.0)
  - Installing apache-airflow-providers-common-sql (1.21.0)
  - Installing asgiref (3.8.1)
  - Installing cachelib (0.9.0)
  - Installing cffi (1.17.1)
  - Installing clickclick (20.10.2)
  - Installing flask-appbuilder (4.5.3)
  - Installing fsspec (2025.2.0)
  - Installing google-re2 (1.1.20240702)
  - Installing httpcore (1.0.7)
  - Installing inflection (0.5.1)
  - Installing jmespath (1.0.1)
  - Installing lockfile (0.12.2)
  - Installing mako (1.3.9)
  - Installing opentelemetry-exporter-otlp-proto-grpc (1.30.0)
  - Installing opentelemetry-exporter-otlp-proto-http (1.30.0)
  - Installing python-slugify (8.0.4)
  - Installing requests-toolbelt (1.0.0)
  - Installing tzdata (2025.1)
  - Installing uc-micro-py (1.0.3)
  - Installing wirerope (1.0.0)
  - Installing alembic (1.14.1): Downloading... 70%
  - Installing apache-airflow-providers-common-io (1.5.0)
  - Installing apache-airflow-providers-fab (1.5.3)
  - Installing apache-airflow-providers-ftp (3.12.0)
  - Installing apache-airflow-providers-http (5.0.0)
  - Installing apache-airflow-providers-imap (3.8.0): Downloading... 0%
  - Installing apache-airflow-providers-smtp (1.9.0)
  - Installing apache-airflow-providers-smtp (1.9.0)
  - Installing apache-airflow-providers-imap (3.8.0): Downloading... 23%
  - Installing apache-airflow-providers-smtp (1.9.0)
  - Installing apache-airflow-providers-common-io (1.5.0)
  - Installing apache-airflow-providers-fab (1.5.3)
  - Installing apache-airflow-providers-ftp (3.12.0)
  - Installing apache-airflow-providers-http (5.0.0)
  - Installing apache-airflow-providers-imap (3.8.0): Downloading... 23%
  - Installing apache-airflow-providers-smtp (1.9.0)
  - Installing alembic (1.14.1): Downloading... 100%
  - Installing apache-airflow-providers-common-io (1.5.0)
  - Installing apache-airflow-providers-fab (1.5.3)
  - Installing apache-airflow-providers-ftp (3.12.0)
  - Installing apache-airflow-providers-http (5.0.0)
  - Installing apache-airflow-providers-imap (3.8.0): Downloading... 23%
  - Installing apache-airflow-providers-smtp (1.9.0)
  - Installing apache-airflow-providers-sqlite (4.0.0)
  - Installing argcomplete (3.5.3)
  - Installing apache-airflow-providers-smtp (1.9.0)
  - Installing apache-airflow-providers-sqlite (4.0.0)
  - Installing argcomplete (3.5.3)
  - Installing apache-airflow-providers-imap (3.8.0): Downloading... 100%
  - Installing apache-airflow-providers-smtp (1.9.0)
  - Installing apache-airflow-providers-sqlite (4.0.0)
  - Installing argcomplete (3.5.3)
  - Installing blinker (1.9.0)
  - Installing apache-airflow-providers-common-io (1.5.0)
  - Installing apache-airflow-providers-fab (1.5.3)
  - Installing apache-airflow-providers-ftp (3.12.0)
  - Installing apache-airflow-providers-http (5.0.0)
  - Installing apache-airflow-providers-imap (3.8.0): Downloading... 100%
  - Installing apache-airflow-providers-smtp (1.9.0)
  - Installing apache-airflow-providers-sqlite (4.0.0)
  - Installing argcomplete (3.5.3)
  - Installing blinker (1.9.0)
  - Installing alembic (1.14.1): Installing...
  - Installing apache-airflow-providers-common-io (1.5.0)
  - Installing apache-airflow-providers-fab (1.5.3)
  - Installing apache-airflow-providers-ftp (3.12.0)
  - Installing apache-airflow-providers-http (5.0.0)
  - Installing apache-airflow-providers-imap (3.8.0): Downloading... 100%
  - Installing apache-airflow-providers-smtp (1.9.0)
  - Installing apache-airflow-providers-sqlite (4.0.0)
  - Installing argcomplete (3.5.3)
  - Installing blinker (1.9.0)
  - Installing colorlog (6.9.0)
  - Installing apache-airflow-providers-smtp (1.9.0)
  - Installing apache-airflow-providers-sqlite (4.0.0)
  - Installing argcomplete (3.5.3)
  - Installing blinker (1.9.0)
  - Installing colorlog (6.9.0)
  - Installing apache-airflow-providers-imap (3.8.0): Installing...
  - Installing apache-airflow-providers-smtp (1.9.0)
  - Installing apache-airflow-providers-sqlite (4.0.0)
  - Installing argcomplete (3.5.3)
  - Installing blinker (1.9.0)
  - Installing colorlog (6.9.0)
  - Installing configupdater (3.2)
  - Installing connexion (2.14.2)
  - Installing apache-airflow-providers-smtp (1.9.0)
  - Installing apache-airflow-providers-sqlite (4.0.0)
  - Installing argcomplete (3.5.3)
  - Installing blinker (1.9.0)
  - Installing colorlog (6.9.0)
  - Installing configupdater (3.2)
  - Installing connexion (2.14.2)
  - Installing apache-airflow-providers-imap (3.8.0)
  - Installing apache-airflow-providers-smtp (1.9.0)
  - Installing apache-airflow-providers-sqlite (4.0.0)
  - Installing argcomplete (3.5.3)
  - Installing blinker (1.9.0)
  - Installing colorlog (6.9.0)
  - Installing configupdater (3.2)
  - Installing connexion (2.14.2)
  - Installing cron-descriptor (1.4.5): Downloading... 0%
  - Installing cron-descriptor (1.4.5): Downloading... 100%
  - Installing cron-descriptor (1.4.5): Installing...
  - Installing cron-descriptor (1.4.5)
  - Installing apache-airflow-providers-common-io (1.5.0)
  - Installing apache-airflow-providers-fab (1.5.3)
  - Installing apache-airflow-providers-ftp (3.12.0)
  - Installing apache-airflow-providers-http (5.0.0)
  - Installing apache-airflow-providers-imap (3.8.0)
  - Installing apache-airflow-providers-smtp (1.9.0)
  - Installing apache-airflow-providers-sqlite (4.0.0)
  - Installing argcomplete (3.5.3)
  - Installing blinker (1.9.0)
  - Installing colorlog (6.9.0)
  - Installing configupdater (3.2)
  - Installing connexion (2.14.2)
  - Installing cron-descriptor (1.4.5)
  - Installing alembic (1.14.1)
  - Installing apache-airflow-providers-common-io (1.5.0)
  - Installing apache-airflow-providers-fab (1.5.3)
  - Installing apache-airflow-providers-ftp (3.12.0)
  - Installing apache-airflow-providers-http (5.0.0)
  - Installing apache-airflow-providers-imap (3.8.0)
  - Installing apache-airflow-providers-smtp (1.9.0)
  - Installing apache-airflow-providers-sqlite (4.0.0)
  - Installing argcomplete (3.5.3)
  - Installing blinker (1.9.0)
  - Installing colorlog (6.9.0)
  - Installing configupdater (3.2)
  - Installing connexion (2.14.2)
  - Installing cron-descriptor (1.4.5)
  - Installing croniter (6.0.0)
  - Installing cryptography (44.0.1)
  - Installing dill (0.3.9)
  - Installing flask-caching (2.3.0)
  - Installing flask-session (0.5.0)
  - Installing gunicorn (23.0.0)
  - Installing httpx (0.28.1)
  - Installing lazy-object-proxy (1.10.0)
  - Installing linkify-it-py (2.0.3)
  - Installing marshmallow-oneofschema (3.1.1)
  - Installing mdit-py-plugins (0.4.2)
  - Installing methodtools (0.4.7)
  - Installing opentelemetry-exporter-otlp (1.30.0)
  - Installing pathspec (0.12.1)
  - Installing pendulum (3.0.0)
  - Installing pluggy (1.5.0)
  - Installing psutil (7.0.0)
  - Installing python-daemon (3.1.2)
  - Installing python-nvd3 (0.16.0)
  - Installing rfc3339-validator (0.1.4)
  - Installing rich-argparse (1.7.0)
  - Installing setproctitle (1.3.4)
  - Installing sqlalchemy-jsonfield (1.0.2)
  - Installing tabulate (0.9.0)
  - Installing tenacity (9.0.0)
  - Installing termcolor (2.5.0)
  - Installing universal-pathlib (0.2.6)
  - Installing apache-airflow (2.10.5)

Writing lock file
 {seilylook} 🚀 poetry add apache-airflow
The following packages are already present in the pyproject.toml and will be skipped:

  - apache-airflow

If you want to update it to the latest compatible version, you can use `poetry update package`.
If you prefer to upgrade it to the latest available version, you can use `poetry add package@latest`.

Nothing to add.
```
