# Dataclass


# Introduction

파이썬에서 데이터를 저장하기 위해 여러가지 방법을 사용한다. List, Tuple, Dictionary, Namedtuple, Set, Frozen set과 같은 내장 자료구조는 사용하기 편리하다는 장점이 있다.

반면에 클래스를 이용해서 데이터를 담아두면 캡슐화를 통해 type 안정성을 높일 수 있다. 

파이썬 3.7에서 dataclasses라는 매우 매력적인 모듈이 표준 라이브러리에 추가되었다. 이에 대한 정리글이다.

## 기존 방식의 클래스를

먼저 dataclasses 모듈에 대해서 정리하기 전에 기존에 사용하던 데이터 저장용 클래스를 알아본다.

```python
from datetime import date

class User():
    def __init__(self, id:int, name: str, birth: date, role: bool = False) -> None:
        self.id = id
        self.name = name
        self.birth = birth
        self.role = role
```

위의 코드를 보면, **id, name, birth, role** 3가지 변수를 저장하기 위해 반복된 코드를 작성해야한다.

클래스의 인스턴스들을 출력해보면, 출력결과에 필드값이 나타나지 않아 불편하다.

```bash
>>> user = User(id=1, name="Steve Jobs", birthdate=date(1955, 2, 24))
>>> user
<__min__.User Ojbect at 0x12132354>
```

`__repr__()` 메서드를 추가해 필드값이 모두 출려되도록 인스턴스의 출력 형태를 바꿔본다.

```python
from datetime import date

class User():
    def __init__(self, id:int, name: str, birth: date, role: bool = False) -> None:
        self.id = id
        self.name = name
        self.birth = birth
        self.role = role
    def __repr__(self) -> str:
        return (
            self.__class__.__qualname__ + f"(id={self.id!r}, name={self.name!r}, "
            f"birthdate={self.birth!r}, role={self.role!r})"
        )
```

```bash
>>> user1 = User(id=1, name="Steve Jobs", birthdate=date(1955, 2, 24))
>>> user1
User(id=1, name='Steve Jobs', birthdate=datetime.date(1955, 2, 24), admin=False)
```

당연한 얘기지만, 이 클래스를 사용해 생성한 두 개의 인스턴스의 동등함을 살펴보면 다르다.

```bash
>>> user1 = User(id=1, name="Steve Jobs", birthdate=date(1955, 2, 24))
>>> user2 = User(id=1, name="Steve Jobs", birthdate=date(1955, 2, 24))
>>> user1 == user2
False
```

두 개의 인스턴스 간 필드값이 같을 때, 동등한 인스턴스로 취급하고 싶다면 `__eq__()` 메서드를 사용해야 한다.

```python
from datetime import date


class User:
    def __init__(
        self, id: int, name: str, birth: date, role: bool = False
    ) -> None:
        self.id = id
        self.name = name
        self.birth = birth
        self.role = role

    def __repr__(self) -> str:
        return (
            self.__class__.__qualname__ + f"(id={self.id!r}, name={self.name!r}, "
            f"birth={self.birth!r}, role={self.role!r})"
        )

    def __eq__(self, other) -> bool:
        if other.__class__ is self.__class__:
            return (self.id, self.name, self.birth, self.role) == (
                other.id,
                other.name,
                other.birth,
                other.role,
            )
        return False
```

```bash
>>> user1 = User(id=1, name="Steve Jobs", birthdate=date(1955, 2, 24))
>>> user2 = User(id=1, name="Steve Jobs", birthdate=date(1955, 2, 24))
>>> user1 == user2
True
```

이와 같이 동작하는 클래스를 만들기 위해서는 많은 양의 코드가 필요하다는 것을 알 수 있다. 이 문제를 해결하고자 등장한 것이 바로 `dataclasses`이다.

## 데이터 클래스를

`dataclasses` 모듈은 데이터를 저장하기 위한 클랫를 매우 적은 양의 코드로 작성하게 도와준다. 위 예제 코드를 이번에는 `dataclasses` 모듈을 사용해 본다.

```python
from dataclasses import dataclass
from datetime import date

@dataclass
class User():
    id: int
    name: str
    birth: date
    role: admin = False
```

`dataclasses` 모듈에서 제공하는 `@dataclass` 데코레이터를 일반 클래스에서 선언해줌녀 해당 클래스는 **데이터 클래스**가 된다.

데이터 클래스는 `__init__()`, `__repr__()`, `__eq__()` 같은 메서드를 자동으로 생성해준다. 따라서 이 데이터 클래스는 앞서 작성한 클래스와 동일하게 동작한다.

```bash
>>> user1 = User(id=1, name="Steve Jobs", birthdate=date(1955, 2, 24))
>>> user1
User(id=1, name='Steve Jobs', birthdate=datetime.date(1955, 2, 24), admin=False)
>>> user2 = User(id=1, name="Steve Jobs", birthdate=date(1955, 2, 24))
>>> user1 == user2
True
```

## 불변 데이터

그렇다면 객체 지향의 가장 큰 특징 중 하나인 캡슐화 및 은닉화를 위한 불변 데이터 작성을 위해서는 `frozen` 옵션을 사용하면 된다.

```python
from dataclasses import dataclass
from datetime import date

@dataclass(frozen=True)
class User():
    id: int
    name: str
    birth: date
    role: admin = False
```

이제 데이터 클래스의 저장된 데이터에 대해서 변경하려고 시도하면 에러를 발생시킨다.

```bash
>>> user = User(id=1, name="Steve Jobs", birth=date(1955, 2, 24))
>>> user.role = True
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "<string>", line 4, in __setattr__
dataclasses.FrozenInstanceError: cannot assign to field 'role'
```
