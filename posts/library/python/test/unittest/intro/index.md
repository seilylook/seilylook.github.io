# Unittest


# Introduction

`unittest` 모듈은 Java의 **JUnit**, JS의 **Jest** 같은 단위 테스트 프레임워크이다. 다만 다른 언어와 달리 기본적으로 내장되어 있기에 파이썬만 설치된다면 바로 모듈을 불러와서 사용할 수 있다.

## TestCase 클래스

`unittest` 모듈의 `TestCase` 클래스는 단위 테스트에 필요한 다양한 유틸리티 메소드를 제공한다. 따라서 새로운 테스트를 작성할 때는 `TestCase` 클래스를 상속하는 클래스를 먼저 작성해야 한다. 해당 클래스 안에 테스트를 수행하는 로직을 메서드로 추가해주면 된다.

예를 들어 1과 2을 더해서, 3을 return 하는 테스트는 다음과 같이 작성할 수 있다.

- my_tests.py

```python
from unittest import TestCase

class MyTests(TestCase):
    def test_one_plus_two(self):
        self.assertEqual(1+2, 3)
```

{{<admonition warning>}}
테스트를 실행하기 위해서는 반드시 메서드의 이름을 `test`로 시작해야 한다.
{{</admonition>}}

## 테스트 실행

작성한 테스트는 터미널에서 쉽게 실행할 수 있다.

```bash
python -m unittest my_tests.py
```

## 테스트 실패

테스트를 성공하는 것보다 실패에 대한 연구가 훨씬 더 중요하다. 1+2의 결과 값으로 5를 넘겨본다.

```python
from unittest import TestCase

class MyTests(TestCase):
    def test_one_plus_two(self):
        self.assertEqual(1+2, 5)
```

다시 테스트를 실행해보면 실패한 Log를 확인할 수 있다.

```bash
$ python -m unittest my_tests.py
F
======================================================================
FAIL: test_one_plus_two (my_tests.MyTests)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/Users/seilylook/Development/python-unittest-testcase/my_tests.py", line 6, in test_one_plus_two
    self.assertEqual(1 + 2, 5)
AssertionError: 3 != 5

----------------------------------------------------------------------
Ran 1 test in 0.000s

FAILED (failures=1)
```

## 다양한 메서드

### assert 메서드

`unittest` 모듈의 `TestCase` 클래스는 `assert`로 시작하는 많은 메서드를 제공한다. 

```python
from unittest import TestCase


class MyTests(TestCase):
    def test_one_plus_two(self):
        self.assertEqual(1 + 2, 3)

    def test_other_assertions(self):
        self.assertTrue(1 == 1)
        self.assertFalse(1 == 2)
        self.assertGreater(2, 1)
        self.assertLess(1, 2)
        self.assertIn(1, [1, 2])
        self.assertIsInstance(1, int)
```

`MyTests` 클래스는 `TestCase` 클래스를 상속하고 있기 때문에 부모 클래스인 `TestCase`가 제공하는 모든 메서드를 `self`를 통해 접근하고 사용할 수 있다.

작성한 테스트를 실행하면 이번에는 두개의 테스트를 통과했기 때문에 점(.)이 2개가 찍히는 것을 볼 수 있다. 

```bash
$ python -m unittest my_tests.py
..
----------------------------------------------------------------------
Ran 2 tests in 0.000s

OK
```

점(.) 대신 좀 더 자세한 피드백을 확인하고 싶다면 `-v` 옵션을 추가해주면 된다.

```bash
$ python -m unittest -v my_tests.py
test_one_plus_two (my_tests.MyTests) ... ok
test_other_assertions (my_tests.MyTests) ... ok

----------------------------------------------------------------------
Ran 2 tests in 0.000s

OK
```

### assert 예외 검증

예외가 발생하는지를 검증해야 할 때는 `assertRaises(exception)` 메서드를 사용한다. **Context manager**를 Return 하기 때문에 사용법이 약간 생소할 수 있다.

`with self.assertRaises(예상 예외):` 식으로 발생해야하는 예외를 먼저 명시하고, 실제로 그 예외를 일으키는 로직을 `with` 절 안에 들여쓰기 해주면 된다.

```python
class MyTests(TestCase):
    def test_exceptions(self):
        with self.assertRaises(ZeroDivisionError):
            1 / 0
        with self.assertRaises(TypeError):
            1 + '2'
```
