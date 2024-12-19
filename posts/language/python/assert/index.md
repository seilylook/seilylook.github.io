# Assert


# Assert(가정 설정문)

assert는 뒤의 조건이 True가 아니면 `AssertError`를 발생시킨다.

```python
a = 3
assert a == 2

#결과
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AssertionError
```

## 왜 assert가 필요할까?

어떤 함수는 성능을 높이기 위해 반드시 정수만을 입력받아 처리하도록 만들 수 있다. 이런 함수를 만들기 위해서는 반드시 함수에 정수만 들어오는지 확인할 필요가 있다. 이를 위해 if문을 사용할 수도 있고 에외 처리를 사용할 수도 있지만 `가정 설정문`을 사용하는 방법도 있다.

아래 코드는 함수 인자가 정수인지 확인하는 코드이다.

```python
lists = [1, 3, 6, 3, 8, 7, 13, 23, 13, 2, 3.14, 2, 3, 7]

def test(t):
    assert type(t) is int, '정수 아닌 값이 있네'

for i in lists:
    test(i)
#결과
AssertionError: 정수 아닌 값이 있네
```

list에 실수가 하나 있으므로 AssertError가 발생했다. assert문은 다음 형식으로 작동한다.

`assert 조건, "메세지"`

`"메세지"는 생략할 수 있다`

assert는 개발자가 원하는 조건의 변수 값을 보증받을 때까지 assert로 테스트할 수 있다. 

이는 단순히 에러를 찾는 것일 아니라 값을 보증하기 위함이다. 

예를 들어 함수의 입력 값이 어떤 조건의 참임을 보증하기 위해서 사용할 수 있고 함수의 반환 값이 어떤 조건에 만족하도록 만들 수 있다. 혹은 변수 값이 변하는 과정에서 특정 부분은 반드시 어떤 영역에 속하는 것을 보증하기 위해 가정 설정문을 통해 확인할 수 있다.
