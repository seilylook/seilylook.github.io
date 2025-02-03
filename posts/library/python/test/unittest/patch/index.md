# Patch


# Introduction

`unittest.mock` 모듈의 `patch()` 데코레이터를 이용하면 특정 모듈의 함수나 클래스를 가짜(mock)객체, 좀 더 엄밀히 말하면, `MagicMock` 인스턴스로 대체할 수 있다. 이 과정을 흔히 mocking 또는 patching이라고 하는데, 단위 테스트를 작성할 떄 외부 서비스에 의존하지 않고 독립적으로 실행이 가능한 단위 테스트를 작성하기 위해서 사용되는 테스팅 기법이다.

## patch 데코레이터

`unittest.mock` 모듈의 `patch()` 데코레이터는 특정 범위 내에서만 mocking이 가능하도록 해준다. 일반적으로 다음과 같이 patching이 필요한 단위 테스트 메서드에 `patch()` 데코레이터를 선언해줌으로서 해당 메서드 내에서만 patching이 이뤄지게 한다.

- test_us.py

```python
from unittest import TestCase, main
from unittest.mock import patch


def hello():
    return "Hello!"


class TestMe(TestCase):
    @patch("__main__.hello", return_value="Mock!")
    def test_hello(self, mock_hello):
        self.assertEqual(hello(), "Mock!")
        self.assertIs(hello, mock_hello)
        mock_hello.assert_called_once_with()


if __name__ == "__main__":
    main()
```

```bash
$ python test_me.py
.
----------------------------------------------------------------------
Ran 1 test in 0.000s

OK
```

위 예제에서, 원래 **Hello!**를 리턴하는 `hello()` 함수가 **Mock!**를 대신 리턴하도록 `@patch()` 데코레이터로 patching 하고 있다.

`@patch()` 데코레이터는 첫번쨰 인자로 patching 할 메서드를 `package.module.Class.method` 형태의 문자열로 받는다. 위의 예제에서는 patching할 메서드가 같은 모듈에 있기 때문에 `__main__` 모듈명을 사용한다. `@patch()` 데코레이터를 사용해서 patching을 하면 mock 객체를 테스트 메서드의 인자로 추가되는데, 바로 `mock_hello`이 이 mock 객체의 매개 변수 명으로 쓰이고 있다.

테스트 메서드에서 검증하는 내용을 보면, `hello()` 함수를 호출했을 때 원래 리턴 값인 `Hello!` 대신에 `Mock!`을 리턴하는지 검사한다. 그리고 정말로 `hello()` 함구가 `mock_hello()` 함수로 대체가 되었는지, 그리고 mock 객체에 함수 호출이 기억되었는지를 검증하고 있다.


