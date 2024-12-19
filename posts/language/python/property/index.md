# Property


# Introduction

`Property`는 객체의 속성을 제어할 때 유용하게 사용되는 기능이며 데이터 캡슐화를 위한 방법이다.

## 직접 접근

사람의 이름, 나이, 연봉 데이터를 가진 클래스를 만들어본다. 밑의 Person 클래스는 name, age, salary 3개의 필드로 이루어져 있다.

```python
class Persion():
    def __init__(self, name, age, salary):
        self._name = name
        self._age = age
        self._salary = salary
```

Person 클래스의 인스턴스를 생성한 후, 현재 필드 값을 읽거나 새로운 필드 값을 쓰는 것은 매우 자유롭다.(하지만 이는 지양해야 한다.)

```python
person = Person("kim", 25, 5000)
person.age

25

person.age = person.age + 1
person.age

26
```

## Getter / Setter를 통한 접근

클래스 인스턴스의 내부 데이터를 보호하기 위해서 데이터의 접근용 메소드를 작성하는 것은 객체 지향 프로그래밍의 기본이다. Person 클래스의 age에 대한 `get_age()`, `set_age()` 메소드를 추가한다.

```python
class Person():
    def __init__(self, name: str, age: int, salary: int):
        self._name = name
        self._age = age
        self._salary = salary
    
    def get_age(self):
        return self._age
    
    def set_age(self, age:int):
        if age < 0:
            raise ValueError("Invalid age")
        self._age = age
```

{{<admonition tip>}}
`_`로 시작하는 변수는 외부에서 직접 접근하지 않는 파이썬의 관행에 따른다.
{{</admonition>}}

이렇게 getter/setter 메소드를 사용함녀 객체 내부 데이터에 대해 직접 접근을 통제할 수 있고, 속성을 읽거나 쓸 때 유효성 검사와 같은 추가적인 로직을 추가할 수 있다. 하지만 클래스의 인터페이스가 변경됨에 따라 기존에 해당 클래스가 사용되는 코드를 모두 수정해야 하는 단점이 있다.

## property() 함수

파이썬의 내장 함수인 `property()`를 사용하면 마치 필드명을 직접 사용하는 것처럼 깔끔하게 getter/setter 메소드가 호출되게 할 수 있다.

```python
class Person():
    def __init__(self, name: str, age: int, salary: int):
        self._name = name
        self._age = age
        self._salary = salary
    
    def get_age(self):
        return self._age
    
    def set_age(self, age:int):
        if age < 0:
            raise ValueError("Invalid age")
        self._age = age
    
    age = property(get_age, set_age)
```

`property()` 함수의 첫 번째 인자로 getter 메소드를 두 번째 인자로 setter 메소드를 넘겨주면 `age` 필드명을 이용해 데이터에 접근할 수 있다.

```python
person = Person("Lee", 30, 3000)
person.age

30

person.age += 1
person.age

31
```

이렇게 `property()` 함수를 사용하면 클래스를 사용하는 측면에서는 일반 필드에 직접 접근하는 것처럼 보이지만 내부적으로 getter/setter 메소드가 호출된다. 

## @property 데코레이터

`@property`를 사용하면 `property()`와 동일한 동작을 좀 더 간결하고 읽기 쉽게 작성할 수 있다.

```python
class Person():
    def __init__(self, name: str, age: int, salary: int):
        self._name = name
        self._age = age
        self._salary = salary
    
    @property
    def get_age(self):
        return self._age
    
    @property
    def set_age(self, age:int):
        if age < 0:
            raise ValueError("Invalid age")
        self._age = age
```

`property()` 함수나 `@property` 데코레이터를 사용했을 때 가장 큰 이점은 직접 접근처럼 사용하지만 캡슐화 정책을 지킨다는 것이다. 

## 읽기 전용 프로퍼티

클래스를 작성하다보면 다른 필드로부터 값이 유추되거나 계산되는 읽기 전용 필드가 필요할 때가 있다. Ex) `Person` 클래스에서 전체 이름을 얻고 싶다면 다음과 같이 `@property` 데코레이터를 사용해 `full_name` 필드를 추가할 수 있다.

```python
class Person():
    def __init__(self, name, age, salary):
        self._name = name
        self._age = age
        self._salary = salary
    
    @property
    def get_name_and_age(self):
        return self._name + " " + str(self._age)
```

이렇게 `@property` 데코레이터를 활용하면, 마치 해당 객체의 일반 속성을 읽듯이 사용할 수 있다.

```python
person = Person("Park", 28, 4000)
person.get_name_and_age

"Park 28"
