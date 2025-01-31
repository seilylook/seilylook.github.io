# Unittest.Mock


# Introduction

단위 테스트를 작성하다보면 데이터베이스 또는 외부 API에 의존하는 코드를 테스트해야 할 일이 생긴다. 운영 환경 대비 제약이 많은 테스트 환경에서는 실제 데이터베이스와 연동하거나 실제 외부 API를 호출하기가 불가능한 경우가 많다. 가령 가능하더라도, 이렇게 외부 서비스에 의존하는 테스는 해당 서비스에 문제가 생길 경우 실패할 수 있으며 실행 속도도 당연히 느리다. 

따라서 단위 테스트를 작성할 때 외부에 의존하는 부분을 임의의 가짜로 대체하는 기법이 자주 사용되는데 이를 `Mocking`이라고 한다. 즉, `Mocking`은 외부 서비스에 의존하지 않고 독립적으로 실행이 가능한 단위 테스트를 작성하기 위해서 사용되는 테스팅 기법이다.

## unittest.mock 모듈

`unittest.mock` 모듈은 파이썬 3.3부터 언어에 기본 내장되어 있는 모킹 라이브러리이다. 따라서 별도의 외부 라이브러리 설치 없이 파이썬 인터프리터에서 다음과 같이 임포트해서 바로 사용할 수 있다. 이 모듈을 이용하면 단위 테스트를 작성할 때 코드의 특정 부분을 `mock` 객체로 대체할 수 있으며, 해당 `mock` 객체가 어떻게 사용되 었는지 검증할 수 있다.

```python
from unittest.mock import Mock, MagicMock, call
```

## Mock 객체 설정

mocking은 소위 mock이라고 불리는 가짜 객체를 생성하는 것부터 시작한다. 우리는 이 mock 객체가 어떻게 작동을 할지르 지정해 줄 수 있으며, 이 mock 객체는 자신을 상대로 어떤 작업이 일어났는지를 기억한다.

먼저 호출되었을 때 특정 값을 리턴하는 mock객체는 `return_value` 옵션을 이용해서 생성할 수 있다.

```python
from unittest.mock import Mock
mock = Mock(return_value='Hello, Mock!')
mock()
'Hello, Mock!'
```

호출되었을 때 예외가 발생하는 mock 객체는 `side_effect` 옵션을 사용해서 생성할 수 있다.

```python
mock = Mock(side_effect=Exception('Oops!'))
mock()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/Users/dale/.pyenv/versions/3.7.6/lib/python3.7/unittest/mock.py", line 1011, in __call__
    return _mock_self._mock_call(*args, **kwargs)
  File "/Users/dale/.pyenv/versions/3.7.6/lib/python3.7/unittest/mock.py", line 1071, in _mock_call
    raise effect
Exception: Oops!
```

`side_effect` 옵션에 리스트를 넘기면 mock 객체가 호출될 때마다 매번 다른 값을 리턴할 수도 있다.

```python
mock = Mock(side_effect=[1, 2, 3])
mock()
1
mock()
2
mock()
3
mock()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "/Users/dale/.pyenv/versions/3.7.6/lib/python3.7/unittest/mock.py", line 1011, in __call__
    return _mock_self._mock_call(*args, **kwargs)
  File "/Users/dale/.pyenv/versions/3.7.6/lib/python3.7/unittest/mock.py", line 1073, in _mock_call
    result = next(effect)
StopIteration
```

mock은 객체처럼 속성을 가질 수 있는데 각 속성은 새로운 mock이 된다. 따라서 다음과 같이 특정 속성에 값을 할당할 수도 있고, 특정 메서드의 리턴 값을 지정해 줄 수도 있다.

```python
mock = Mock()
mock.attribute = 'ATTRIBUTE'
mock.attribute
'ATTRIBUTE'
mock.method.return_value = 'METHOD RETURN VALUE'
mock.method()
'METHOD RETURN VALUE'
```

## MagicMock

파이썬에는 **Magic method**라는 개념이 있는데, 모든 객체에는 언어 레벨에서 특수한 목적으로 쓰이는 메서드들을 정의할 수 있다. 대표적으로 `__str__`의 경우, 객체를 읽기 좋은 형태의 문자열로 출력하기 위해 사용되는 매직 메서드이다.

기본적으로 `Mock` 클래스를 사용하면 이러한 매직 메서드가 자동으로 모킹되지 않는다.

```python
from unittest.mock import Mock
mock = Mock()
mock.__str__.return_value

Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: 'method-wrapper' object has no attribute 'return_value'
```

따라서, 매직 메서드를 모킹하려면 다른 속성이나 메서드와 달리 다음과 같이 새로운 mock 객체를 직접 생성해서 할당을 해줘야 한다.

```python
mock.__str__ = Mock(return_value = "I'm a mock.")
str(mock)

"I'm a mock."
```

하지만 `Mock` 클래스의 확장 버전인 `MagicMock` 클래스를 사용하면 이러한 매직 메서드를 미리 알아서 모킹 해놓기 때문에 편리하다.

```python
from unittest.mock import MagicMock
mock = MagicMock()
mock.__str__.return_value
"<MagicMock id='4556752144'>"

mock.__str__.return_value = "I'm a magic mock."
str(mock)
"I'm a magic mock."
```
