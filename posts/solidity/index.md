# Solidity


# Introduction

`Solidity` 언어 학습 기록.

## Chapter 1

### 1.1 Contract

Solidity 언어는 Contract 안에 쌓여 있다. Contract는 Ethereum 애플리케이션의 기본적인 구성 요소로, 모든 변수와 함수는 어느 한 Contract 에 속하게 되어 있다.

즉 모든 프로젝트의 시작점이다.

#### Version Pragma

모든 Solidity 소스 코드는 `version pragma`로 시작해야 한다. 이는 해당 코드가 사용해야 하는 Solidity 버전을 선언하는 것이다. 이를 통해 이후에 새로운 컴파일러 버전이 나와도 기존 코드가 깨지지 않도록 예방하는 것이다.

{{<admonition info>}}
npm을 사용한 프로젝트를 개발할 때마다 version 관리 때문에 에러 처리한 경험이 많은데, 위의 기능은 편리하다고 생각된다.
{{</admonition>}}

선언은 다음과 같이한다: `pragma solidity ^0.4.19;`

```Sol
pragma solidity ^0.4.19;

contract HelloWorld {

}
```

### 1.2 Variables

상태 변수는 Contract 저장소에 영구적으로 저장된다. 즉, Ethereum 블록체인에 기록되는 것이다. 데이터베이스에 데이터를 저장하는 것과 동일하다.

#### uint: 부호 없는 정수

uint 자료형은 부호 없는 정수로, 값이 음수가 아니어야 한다.

부호 있는 정수를 위해서는 int를 사용해야 한다.

{{<admonition tip>}}
솔리디티에서 uint는 실제로 uint256, 즉 256비트 부호 없는 정수의 다른 표현이지. uint8, uint16, uint32 등과 같이 uint를 더 적은 비트로 선언할 수도 있네.
{{</admonition>}}

### 1.3 구조체

```Sol
struct Person {
  uint age;
  string name;
}
```

### 1.4 배열

대부분의 언어와 마찬가지로 Solidity에는 정적 배열, 동적 배열 두가지가 존재한다.

```sol
// 2개의 원소를 담을 수 있는 고정 길이의 배열:
uint[2] fixedArray;
// 또다른 고정 배열으로 5개의 스트링을 담을 수 있다:
string[5] stringArray;
// 동적 배열은 고정된 크기가 없으며 계속 크기가 커질 수 있다:
uint[] dynamicArray;
```

앞서 배운 구조체 배열도 생성할 수 있다.

```sol
Person[] people; // 이는 동적 배열로, 원소를 계속 추가할 수 있다.
```

### 1.5 함수

```sol
function eatHamburgers(string _name, uint _amount) {

}
```

### 1.6 구조체 배열 활용

앞서 말한 `Person` 형식을 가진 people 구조체 배열을 만들어 데이터를 넣는다.

```sol
struct Person {
  uint age;
  string name;
}

Person[] public people;

// 새로운 사람을 생성한다:
Person satoshi = Person(172, "Satoshi");

// 이 사람을 배열에 추가한다:
people.push(satoshi);

// 데이터를 직접 넣어줄 수 있다.
people.push(Person(16, "Vitalik"));
```

### 1.7 Private / Public 함수

Solidity에서 함수는 기본적으로 `public`으로 선언된다. 즉, 누구나 Contract의 함수를 호출하고 코드를 실행할 수 있다.

이는 바람직한 건 아닐 뿐더러, 자네 Contract를 공격에 취약하게 만들 수 있다. 그러니 Java와 마찬가지로 기본적으로 `private`으로 선언하는 것이 옳다.

```sol
uint[] numbers;

function _addToArray(uint _number) private {
  numbers.push(_number);
}
```

`private`는 Contract 내의 다른 함수들만이 이 함수를 호출해 numbers 배열로 무언가를 추가할 수 있다.

위의 예시에서 볼 수 있듯이 `private` 키워드는 함수명 다음에 적는다. 함수 인자명과 마찬가지로 `private` 함수명도 언더바(`_`)로 시작하는 것이 관례이다.

### 1.8 함수 제어자

```sol
string greeting = "What's up dog";

function sayHello() public returns (string) {
  return greeting;
}
```

위의 함수 `sayHello()`는 상태를 변화시키지 않는다.

이 경우에는 함수를 `view` 함수로 선언한다. 이는 함수가 데이터를 보기만 하고 변경하지 않는다는 뜻이다.

```sol
function sayHello() public view returns (string) {
}
```

Solidity는 `pure` 함수도 가지고 있는데, 이는 함수가 앱에서 어떤 데이터도 접근하지 않는 것을 의미한다.

```sol
function _multiply(uint a, uint b) private pure returns (uint) {
  return a * b;
}
```

{{<admonition tip>}}
참고: 함수를 pure나 view로 언제 표시할지 기억하기 어려울 수 있지. 운 좋게도 솔리디티 컴파일러는 어떤 제어자를 써야 하는지 경고 메시지를 통해 잘 알려주네.
{{</admonition>}}

### 1.9 Keccak256

Ethereum은 SHA3의 한 버전인 `keccak256`를 내장 해시 함수로 가지고 있다. 해시 함수는 기본적으로 입력 스트링을 랜덤 256비트 16진수로 매핑한다. 스트링에 약간의 변화라도 있으면 해시 값은 크게 달란진다.

해시 함수는 Ethereum에서 여러 용도로 활용된다.

```sol
keccak256("aaaab");
//6e91ec6b618bb462a4a6ee5aa2cb0e9cf30f7a052bb467b0ba58b8748c00d2e5

keccak256("aaaac");
//b1f078126895a1424524de5321b339ab00408010b7cf0e6ed451514981e58aa9
```

### 1.10 Event

`event`는 Contract가 블록체인 상에서 앱의 사용자 단에서 무언가 액션이 발생했을 때 의사소통하는 방법이다. Contract는 특정 이벤트가 일어나는 지 듣고 그 이벤트가 발생하면 행동을 취한다.

```sol
// 이벤트를 선언한다
event IntegersAdded(uint x, uint y, uint result);

function add(uint _x, uint _y) public {
  uint result = _x + _y;
  // 이벤트를 실행하여 앱에게 add 함수가 실행되었음을 알린다:
  IntegersAdded(_x, _y, result);
  return result;
}
```

### 정리

```sol
pragma solidity ^0.4.19;

contract ZombieFactory {

    event NewZombie(uint zombieId, string name, uint dna);

    uint dnaDigits = 16;
    uint dnaModulus = 10 ** dnaDigits;

    struct Zombie {
        string name;
        uint dna;
    }

    Zombie[] public zombies;

    function _createZombie(string _name, uint _dna) private {
        uint id = zombies.push(Zombie(_name, _dna)) - 1;
        NewZombie(id, _name, _dna);
    }

    function _generateRandomDna(string _str) private view returns (uint) {
        uint rand = uint(keccak256(_str));
        return rand % dnaModulus;
    }

    function createRandomZombie(string _name) public {
        uint randDna = _generateRandomDna(_name);
        _createZombie(_name, randDna);
    }

}
```

