# Getattr


# Introduction

일반적으로 클래스 혹은 패키지 안의 함수를 사용하려면 다음과 같이 사용할 수 있다.

```python
import numpy as np

arr = np.array([1]) # numpy 페키지 안의 array() 함수 호출
```

`getattr(object, "NAME")`이라는 함수는 **object 내부의 name이라는 멤버를 반환한다**. numpy 패키지에서 array라는 이름의 함수를 사용하고 싶다면 패키지 이름 뒤에 `.`을 사용해서 함수를 호출할 수 있다. getattr()는 이와 완전히 동일하게 동작한다. 

즉,`getattr(np, "array")([1])` == `np.array([1])`.

## getattr() 활용

두개가 동일하다면 왜 굳이 사용하는 것일까? `.`과의 유일한 차이점은 getattr의 두번째 parameter가 STR이라는 것이다.

위의 예제를 다시보면, getattr(np, "array")([1]) == np.array([1])인데 분명히 String으로 넘겨준 "array"가 array 함수를 찾는다. 함수 뿐만 아니라 멤버 변수나 클래스에서도 동일하게 적용된다. 

이렇게 **String을 Attribute화** 시킬 수 있는 장점은 상황에 따라 패키지 내 다른 멤버를 사용해야 할 때 빛을 발한다. 아래 예시를 확인해본다.

```python
import my_models as M

def get_network_name(model_name):
    if model_name == 'googlenet':
        model = M.googlenet(args)
    elif model_name == 'vgg':
        model = M.vgg(args)
    elif model_name == 'resnet':
        model = M.resnet(args)
    
    return model
```

위와 같이 과도한 if 문은 피곤한 코딩 습관이다. 이때 코드의 가독성을 올려주는 것이 `getattr()`이다.

```python
import my_modesl as M

def get_network_name(model_name):
    return getattr(M, model_name)
```
