# Mathematics Begin


# 벡터

## 벡터가 뭔가요?

벡터는 숫자를 원소로 가지는 `List` 혹은 `Array` 이다.

<img src="/images/math/vector/1.png" />

벡터끼리 `같은 모양을 가지면` 성분곱(Hadamard product)를 계산할 수 있다.


```python
x = [1, 7, 2] # 열 벡터

x = np.array([1, 7, 2]) # 행 벡터
```

이와 깉이 벡터의 개수에 따라 **벡터의 차원**이라고 한다.

<img src="/images/math/vector/2.png" />

벡터는 공간에서 `한 점`을 나타낸다.

<img src="/images/math/vector/3.png" />

벡터는 원점으로부터 상대적 `위치`를 표현한다.

<img src="/images/math/vector/4.png" />

벡터에 숫자를 곱해주면 `방향은 그대로이고 길이만 변한다.` 이 연산을 `스칼라 곱`이라고 부른다. 곱해주는 숫자를 a라고 정했을 때, a < 1이면 길이가 줄어들고 a > 1이면 길이가 늘어난다. 단, a < 0이 될 시 벡터는 `반대 방향`이 된다.

<img src="/images/math/vector/5.png" />

두 벡터의 덧셈은 다른 벡테로부터 `상대적 위치 이동`을 표현한다.

<img src="/images/math/vector/6.png" />

<img src="/images/math/vector/7.png" />

<img src="/images/math/vector/8.png" />

## 벡터의 노름 구해보기

벡터의 노름(norm)은 `원점에서부터의 거리`를 말한다.

L1-노름은 각 성분의 `변화량의 절대값`을 모두 더한다.

<img src="/images/math/vector/9.png" />

L2-노름은 피타고라스 정리를 이용해 `유클리드 거리`를 계산한다.

<img src="/images/math/vector/10.png" />

노름의 종류에 따라 `기하학적 성질`이 달라진다.

<img src="/images/math/vector/11.png" />

## 두 벡터 사이의 거리를 구해보자

L1, L2-노름을 이용해 `두 벡터 사이의 거리`를 계산할 수 있다.

두 벡터 사이의 거리를 계산할 때는 `벡터의 뺄셈`을 이용한다.

<img src="/images/math/vector/12.png" />

거리를 계산할 수 있으니, `제 2 cos 법칙`에 의해 두 벡터 사이의 각도를 계산할 수 있다.

<img src="/images/math/vector/13.png" />

분자를 쉽게 계산하는 방법이 `내적`이다.

<img src="/images/math/vector/14.png" />

<img src="/images/math/vector/15.png" />

## 내적은 어떻게 해석할까?

내적은 `정사영(Orthogonal Projection)`된 벡터의 길이와 관련 있다.

Proj(x)의 길이는 `코사인 법칙`에 의해 ||x|| cos 세타가 된다.

<img src="/images/math/vector/16.png" />

내적은 정사영의 길이를 `벡터 y의 길이 ||y||만큼 조정`한 값이다.

<img src="/images/math/vector/17.png" />

---

# 행렬

## 행렬은 뭔가요?

행렬은 벡터를 원소로 가지는 `2차원 배열`이다.

행렬은 `행(Row)와 열(Column)`이라는 Index를 가진다.

<img src="/images/math/matrix/1.png" />

행렬의 특정 행(열)을 고정하면 행(열) 벡터라 부른다.

<img src="/images/math/matrix/2.png" />

## 행렬을 이해하는 방법(1)

벡터가 공간에서 한 점을 의미한다면 행렬은 `여러 점들`을 나타낸다.

행렬의 행벡터 xi는 `i번째 데이터`를 의미한다.

<img src="/images/math/matrix/4.png" />

행렬의 xij는 `i번째 데이터의 j번째 변수`의 값을 말한다.

<img src="/images/math/matrix/5.png" />
