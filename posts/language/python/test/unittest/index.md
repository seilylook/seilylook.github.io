# Unittest


# Introduction

어떤 언어로 코딩을 하던 단위 테스트는 신뢰할 수 있는 애플리케이션을 개발하기 위해서 필수적으로 습득해야 하는 기술이다. 파이썬에서는 내장 모듈인 `unittest`를 통해서 다른 라이브러리 없이 비교적 간단하게 단위 테스트를 수행할 수 있다.

## unittest 모듈

`unittest` 모듈은 Java의 JUnit, Javascript의 Jest 또는 Mocha와 같은 단위 테스트 프레임워크이다. 다만 다른 언어와 달리 기본적으로 언어에 내장되어 있기에 파이써만 설치가 되어 있다면 바로 모듈을 불러와 사용할 수 있다.

## TestCase 클래스 

`unittest` 모듈의 `TestCase` 클래스는 단위 테스트에 필요한 다양한 유틸리티 메소드를 제공한다. 따라서 새로운 테스트를 작성할 때는 `TestCase` 클래스를 상속하는 클래스를 먼저 작성해야 한다. 그리고 그 클래스 안에 테스트를 수행하는 로직을 메소드로 추가해주면 된다.

**파일 이름: test_unittest.py**

```python
from unittest import TestCase

class UnitTestExample(TestCase):
    def test_add_numbers(self):
        self.assertEqual(1+2, 3)
```

{{<admonition warning>}}
테스트 메소드 이름은 반드시 `test`로 시작해야 한다. 기왕이면 파일 이름도 test로 시작하도록 지정한다.

Ex) spark/python/pyspark/sql/test/test_dataframe.py
{{</admonition>}}

### 테스트 실행

아래와 같은 명령어를 통해 테스트를 실행할 수 있다.

```bash
python3 -m unittest test_unittest.py
.
--------------------------------------
Ran 1 test in 0.000s

OK
```

### 테스트 실패

실패하는 테스트를 확인해본다. 

```python
from unittest import TestCase

class UnitTestExample(TestCase):
    def test_add_numbers(self):
        self.assertEqual(1+2, 10)
```

```bash
python3 -m unittest test_unittest.py

--------------------------------------
FAIL: test_add_numbers (test_unittest.UnitTestExample)

--------------------------------------
Traceback (most recent call last):
    File "/Users/Desktop/temp/test_unittest.py", line 6, in test_add_numbers
      self.assertEqual(1+2, 10)
AssertError: 3 != 10

--------------------------------------
Ran 1 test in 0.000s

FAILED (failures=1)
```

## assertion Method

`unittest` 모듈의 `TestCase` 클래스는 `assertEqual` 외 다른 많은 메소드를 제공한다.

```python
from unittest import TestCase

class UnitTestExample(TestCase):
    def test_add_numbers(self):
        self.assertEqual(1+2, 10)

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)
```

`UnitTestExample` 클래스는 `TestCase` 클래스를 상속하기 때문에 부모 클래스인 `TestCase`가 제공하는 모든 메소드를 `self`를 통해 접근해 호출할 수 있다.

```bash
python3 -m unittest test_unittest.py
....
------------------------------------
Ran 4 tests in 0.001s

OK
```

작성한 테스트를 실행해보면 이번에는 4개의 메소드가 통과했기 때문에 (.)이 4개가 찍히는 것을 확인할 수 있다. 

좀더 자세한 결과를 확인하고 싶다면 `-v` 옵션을 붙여 테스트를 실행하면 된다.

```bash
python3 -m unittest -v test_unittest.py

test_add_numbers (__main__.TestStringMethods.test_add_numbers) ... ok
test_isupper (__main__.TestStringMethods.test_isupper) ... ok
test_split (__main__.TestStringMethods.test_split) ... ok
test_upper (__main__.TestStringMethods.test_upper) ... ok

----------------------------------------------------------------------
Ran 4 tests in 0.001s

OK
```
