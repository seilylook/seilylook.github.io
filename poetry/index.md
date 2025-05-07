# Poetry


## Poetry로 Python 프로젝트 환경 설정하기

Python 프로젝트를 만들 때 의존성 관리와 가상환경 설정이 번거로운 경우가 많습니다. `Poetry`는 이러한 작업을 깔끔하게 정리해주는 툴로, 패키지 관리와 프로젝트 배포까지 도와주는 훌륭한 도구입니다. 아래는 프로젝트에서 `Poetry`를 설정하는 방법을 정리한 내용입니다.

---

### 1. 프로젝트 초기화

Poetry를 사용해 프로젝트를 초기화하려면 아래 명령어를 입력합니다.

```bash
🔥 poetry init
```

명령어를 실행하면 `pyproject.toml` 파일을 생성하며, 의존성 등을 직접 입력하거나 생략할 수 있습니다.

---

### 2. 가상환경을 프로젝트 내부에 생성하기

Poetry는 기본적으로 프로젝트 외부에 가상환경을 생성합니다. 하지만 프로젝트 폴더 내부에 `.venv`로 가상환경을 만들고 싶다면 다음 설정을 추가합니다.

```bash
🔥 poetry config virtualenvs.in-project true
```

이 설정을 해두면, 프로젝트 루트 디렉토리에 `.venv/` 폴더가 생성됩니다.

---

### 3. pyenv와 함께 사용하는 경우: Python 버전 지정

`pyenv`를 사용 중이라면, 현재 선택된 Python 버전을 Poetry에 적용할 수 있습니다.

```bash
🔥 poetry env use $(pyenv which python)
```

이 명령어는 `pyenv`가 가리키는 Python 버전을 현재 프로젝트에 설정해줍니다.

---

### 4. 가상환경 정보 확인

현재 프로젝트에서 사용 중인 가상환경의 경로나 정보를 확인하고 싶다면 다음 명령어를 실행합니다.

```bash
🔥 poetry env info
```

---

### 5. VS Code에서 가상환경 Python 경로 설정

VS Code에서 Poetry의 가상환경을 Python 인터프리터로 설정하려면:

1. `Cmd + Shift + P` 를 눌러 **명령 팔레트**를 열고
2. `Python: 인터프리터 선택`을 검색
3. 사용자 정의 경로 입력 옵션을 선택한 후
4. 다음 경로를 입력합니다:

```
/Users/seilylook/Development/Projects/traffic-congestion-monitoring/.venv/bin/python
```

---

### 6. requirements.txt 파일로 의존성 내보내기

배포나 서버 설정 시 `requirements.txt` 파일이 필요한 경우가 많은데, Poetry에서는 플러그인을 사용해 이를 쉽게 생성할 수 있습니다.

먼저 `pyproject.toml`에 다음 설정을 추가합니다:

```toml
[tool.poetry.plugins."poetry.plugin"]
"export" = "poetry_plugin_export.plugin:ExportPlugin"
```

혹은 Poetry 1.8 이상에서는 아래처럼 명령어로 설정할 수 있습니다:

```toml
[tool.poetry.requires-plugins]
poetry-plugin-export = ">=1.8"
```

이후 아래 명령어로 `requirements.txt` 파일을 생성할 수 있습니다:

```bash
🔥 poetry export -f requirements.txt --output requirements.txt
```

---

### 7. 의존성 설치

`pyproject.toml`에 정의된 의존성들을 설치하려면 아래 명령어를 사용합니다:

```bash
🔥 poetry install
```

---

## 마무리

이제 Poetry를 활용하여 깔끔하고 안정적인 Python 개발 환경을 구축할 수 있습니다. 프로젝트마다 반복되는 설정을 자동화하고, 코드 배포나 협업 시에도 환경 차이로 인한 이슈를 줄일 수 있습니다.

