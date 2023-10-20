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

## Chapter 2

### 2.1 Address & Mapping

#### Address

Ethereum 블록체인은 은행 계좌와 같은 계정들로 이루어져 있다. 계정은 Ethereum 블록체인상의 통화인 이더의 잔액을 가진다. 은행 계좌에서 다른 계좌로 돈을 송금할 수 있듯이, 계정을 통해 다른 계정과 이더를 주고 받을 수 있다.

각 계정은 은행 계좌 번호와 같은 `address`를 가지고 있다. `address`는 특정 계정을 가리키는 고유 식별자로, 다음과 같이 표현된다.

`0x0cE446255506E92DF41614C46F1d6df9Cc969183`

#### Mapping

간단히 정의 하면 `hash` 자료 구조이다.

```sol
mapping (address => uint) public accountBalance;
// 금융 앱용으로, 유저의 계좌 잔액을 보유하는 uint를 저장한다:

mapping (uint => string) userIdToName;
// 혹은 userID로 유저 이름을 저장/검색하는 데 매핑을 쓸 수도 있다
```

`mapping`은 기본적으로 `key-value` 저장소로, 데이터를 저장하고 검색하는 데 이용된다. 첫번째 예시에서 키는 address이고 값은 uint이다. 두번째 예시에서 키는 uint이고 값은 string이다.

### 2.2 Msg.sender

Solidity에는 모든 함수에서 이용 가능한 특정 전역 변수들이 있다. 그 중의 하나가 현재 함수를 호출한 사람(혹은 Smart Contract)의 주소를 가리키는 `msg.sender`이다.

{{<admonition tip>}}
Solidity에서 함수 실행은 항상 외부 호출자가 시작한다. Contract는 누군가의 Contract의 함수를 호출할 때까지 블록체인 상에서 아무것도 안하고 있는다. 그러니 항상 `msg.sender`가 있어야 한다.
{{</admonition>}}

```sol
mapping (address => uint) favoriteNumber;

function setMyNumber(uint _myNumber) public {
  // `msg.sender`에 대해 `_myNumber`가 저장되도록 `favoriteNumber` 매핑을 업데이트한다 `
  favoriteNumber[msg.sender] = _myNumber;
  // ^ 데이터를 저장하는 구문은 배열로 데이터를 저장할 떄와 동일하다
}

function whatIsMyNumber() public view returns (uint) {
  // sender의 주소에 저장된 값을 불러온다
  // sender가 `setMyNumber`을 아직 호출하지 않았다면 반환값은 `0`이 될 것이다
  return favoriteNumber[msg.sender];
}
```

### 2.3 Require

유저가 생성 함수를 무제한으로 호출하지 못하도록 막아주어야 한다. 처음 한번만 수행하도록 수정해준다.

이를 위해 `require`를 사용할 수 있다. `require`를 활용하면 특정 조건이 참이 아닐 때 함수가 에러 메세지를 발생하고 실행을 멈춘다.

```solidity
function sayHiToVitalik(string _name) public returns (string) {
  // _name이 "Vitalik"인지 비교한다. 참이 아닐 경우 에러 메시지를 발생하고 함수를 벗어난다
  // (참고: 솔리디티는 고유의 스트링 비교 기능을 가지고 있지 않기 때문에
  // 스트링의 keccak256 해시값을 비교하여 스트링 값이 같은지 판단한다)
  require(keccak256(_name) == keccak256("Vitalik"));
  // 참이면 함수 실행을 진행한다:
  return "Hi!";
}
```

{{<admonition warning>}}
솔리디티는 고유의 스트링 비교 기능을 가지고 있지 않기 때문에
스트링의 keccak256 해시값을 비교하여 스트링 값이 같은지 판단한다
{{</admonition>}}

`sayHiToVitalik("Vitalik")`로 이 함수를 실행하면, Hi!가 반환된다. Vitalik이 아닌 다른 값으로 이 함수를 호출할 경우, 에러 메세지가 뜨고 함수가 실행되지 않는다.

즉 `require`는 함수를 실행하기 전에 참이어야 하는 특정 조건을 확인하는 데 있어서 유용하다.

### 2.4 상속

```sol
contract Doge {
  function catchphrase() public returns (string) {
    return "So Wow CryptoDoge";
  }
}

contract BabyDoge is Doge {
  function anotherCatchphrase() public returns (string) {
    return "Such Moon BabyDoge";
  }
}
```

`BabyDoge` Contract는 `Doge` Contract를 상속한다. 즉 BabaDoge Contract를 컴파일해서 구축할 때, BabyDoge Contract가 `catchphrase()` 함수와 `anotherCatchphrase()` 함수에 모두 접근할 수 있다는 뜻이다.

### 2.5 Import

상속할 Contract들을 파일 기반으로 나누어 정리한다.

```sol
import "./someothercontract.sol";

contract newContract is SomeOtherContract {

}
```

### 2.6 Storage VS Memory

Solidity에는 변수를 저장할 수 있는 공간으로 `storage`와 `memory` 두 가지가 있다.

`Storage`: 블록체인 상에 영구적으로 저장되는 변수를 의미한다.

`Memeoy`: 임시적으로 저장되는 변수로, Contract 함수에 대한 외부 호출들이 일어나는 사이에 지워진다.

두 변수는 각각 컴퓨터 하드 디스크와 RAM과 같다.

대부분의 경우에 우리는 이런 키워드들을 이용할 필요 없이 Solidity가 알아서 처리해준다. 상태변수는 초기 설정 상 `storage`로 선언되어 블록체인에 영구적으로 저장되는 반면, 함수 내에 선언된 변수는 `memory`로 자동 선언되어 함수 호출이 끝나면 사라진다. -> Garbase collection

하지만 이 키워드들을 사용해야 하는 때가 있다. 바로 함수 내의 `구조체`와 `배열`을 처리할 때다.

```sol
contract SandwichFactory {
  struct Sandwich {
    string name;
    string status;
  }

  Sandwich[] sandwiches;

  function eatSandwich(uint _index) public {
    // Sandwich mySandwich = sandwiches[_index];

    // ^ 꽤 간단해 보이나, 솔리디티는 여기서
    // `storage`나 `memory`를 명시적으로 선언해야 한다는 경고 메시지를 발생한다.
    // 그러므로 `storage` 키워드를 활용하여 다음과 같이 선언해야 한다:
    Sandwich storage mySandwich = sandwiches[_index];
    // ...이 경우, `mySandwich`는 저장된 `sandwiches[_index]`를 가리키는 포인터이다.

    // 그리고
    mySandwich.status = "Eaten!";
    // ...이 코드는 블록체인 상에서 `sandwiches[_index]`을 영구적으로 변경한다.

    // 단순히 복사를 하고자 한다면 `memory`를 이용하면 된다:
    Sandwich memory anotherSandwich = sandwiches[_index + 1];
    // ...이 경우, `anotherSandwich`는 단순히 메모리에 데이터를 복사하는 것이 된다.

    // 그리고
    anotherSandwich.status = "Eaten!";
    // ...이 코드는 임시 변수인 `anotherSandwich`를 변경하는 것으로
    // `sandwiches[_index + 1]`에는 아무런 영향을 끼치지 않는다.

    그러나 다음과 같이 코드를 작성할 수 있다:
    sandwiches[_index + 1] = anotherSandwich;
    // ...이는 임시 변경한 내용을 블록체인 저장소에 저장하고자 하는 경우이다.
  }
}
```

예시를 코드를 보면,

`storage` 키워드를 통해 `얕은 복사`(원본에 영향)

`memory` 키워드를 통해 `깊은 복사`(원본에 영향 끼치지 않음)

### 2.7 접근 제어자

#### Internal

`internal`은 함수가 정의된 Contract를 상속하는 Contract 내에서도 접근이 가능하다는 점을 제외하면 `private`와 동일하다.

`external`은 함수가 Contract 바깥에서만 호출될 수 있고 Contract 내의 다른 함수에 의해 호출 될 수 없다는 점을 제외하면 `public`과 동일하다.

```sol
contract Sandwich {
  uint private sandwichesEaten = 0;

  function eat() internal {
    sandwichesEaten++;
  }
}

contract BLT is Sandwich {
  uint private baconSandwichesEaten = 0;

  function eatWithBacon() public returns (string) {
    baconSandwichesEaten++;
    // eat 함수가 internal로 선언되었기 때문에 여기서 호출이 가능하다
    eat();
  }
}
```

### 2.8 Interface

블록체인 상에 있으면서 우리가 소유하지 않은 Contract와 우리 Contract가 상호작용 하려면 우선 `interface`를 정의해야 한다.

```sol
contract LuckyNumber {
  mapping(address => uint) numbers;

  function setNum(uint _num) public {
    numbers[msg.sender] = _num;
  }

  function getNum(address _myAddress) public view returns (uint) {
    return numbers[_myAddress];
  }
}
```

위의 Contract는 아무나 자신의 행운의 수를 저장할 수 있는 Contract이고, 각자의 이더리움 주소와 연관이 있을 것이다. 이 주소를 이용해서 누구나 그 사람의 행운의 수를 찾아볼 수 있다.

이제 `getNum` 함수를 이용해 이 Contract에 있는 데치터를 읽고자 하는 `external` 함수가 있다고 가정해본다.

먼저, `LuckyNumber` Contract의 `interface`를 정의할 필요가 있다.

```sol
contract NumberInterface {
  function getNum(address _myAddress) public view returns (uint);
}
```

약간 다르지만, interface를 정의하는 것이 Contract를 정의하는 것과 유사하다는 걸 참고하자. 먼저, 다른 Contract와 상호작용하고자 하는 함수만을 선언할 뿐(이 경우, getNum이 바로 그러한 함수이지) 다른 함수나 상태 변수를 언급하지 않는다.

다음으로, 함수 몸체를 정의하지 않는다. 중괄호 `{}`쓰지 않고 함수 선언을 `;`으로 간단하게 끝낸다.

정리하자면, interface는 뼈대라고 할 수 있다.

우리의 dapp 코드에 이런 인터페이스를 포함하면 Contract는 다른 Contract에 정의된 함수의 특성, 호출 방법, 예상되는 응답 내용에 대해 알 수 있게 된다.

### 2.9 다수의 반환값 처리하기

함수가 다수의 반환값을 가질 떄, 이를 다루는 방법에 대해서 알아본다.

```sol
function multipleReturns() internal returns(uint a, uint b, uint c) {
  return (1, 2, 3);
}

function processMultipleReturns() external {
  uint a;
  uint b;
  uint c;
  // 다음과 같이 다수 값을 할당한다:
  (a, b, c) = multipleReturns();
}

// 혹은 단 하나의 값에만 관심이 있을 경우:
function getLastReturnValue() external {
  uint c;
  // 다른 필드는 빈칸으로 놓기만 하면 된다:
  (,,c) = multipleReturns();
}
```

### 정리

```sol
pragma solidity ^0.4.19;
import "./zombiefactory.sol";

contract KittyInterface {
  function getKitty(uint256 _id) external view returns (
    bool isGestating,
    bool isReady,
    uint256 cooldownIndex,
    uint256 nextActionAt,
    uint256 siringWithId,
    uint256 birthTime,
    uint256 matronId,
    uint256 sireId,
    uint256 generation,
    uint256 genes
  );
}

contract ZombieFeeding is ZombieFactory {

  address ckAddress = 0x06012c8cf97BEaD5deAe237070F9587f8E7A266d;
  KittyInterface kittyContract = KittyInterface(ckAddress);

  function feedAndMultiply(uint _zombieId, uint _targetDna, string _species) public {
    require(msg.sender == zombieToOwner[_zombieId]);

    Zombie storage myZombie = zombies[_zombieId];
    _targetDna = _targetDna % dnaModulus;
    uint newDna = (myZombie.dna + _targetDna) / 2;

    if (keccak256(_species) == keccak256("kitty")) {
      newDna = newDna - newDna % 100 + 99;
    }
    _createZombie("NoName", newDna);
  }

  function feedOnKitty(uint _zombieId, uint _kittyId) public {
    uint kittyDna;
    (,,,,,,,,,kittyDna) = kittyContract.getKitty(_kittyId);
    feedAndMultiply(_zombieId, kittyDna, "kitty");
  }

}
```

## Chapter 3

### 3.1 Contract의 불변성

지금까지 본 것만으로는, Solidity는 자바스크립트 같은 다른 언어와 꽤 비슷해보인다. 하지만 Ethereum DApp에는 일반적인 애플리케이션과는 다른 여러가지 특징이 있다.

첫째, Ethereum에 Contract를 배포하고 나면, Contract는 변하지 않는다 (`Immutable`). 다시 말하자면 Contract를 수정하거나 업데이트할 수 없다.

Contract로 배포한 최초의 코드는 항상, 블록체인에 영구적으로 존재한다. 이것이 바로 Solidity에 있어서 보안이 굉장히 큰 이슈인 이유다. 만약 Contract 코드에 결점이 잇다면, 그것을 이후에 고칠 수 있는 방법이 전혀 없다. 사용자들엑게 결점을 보완한 다른 Smart Contract를 사용해달라고 부탁할 수 밖에 없다.

#### 외부 의존성

어떤 Contract에 버그가 발생했다면 어떡해야 하나?

수정해야 될 때를 대비해 DApp의 중요한 일부를 수정할 수 있도록 하는 함수를 만들어 놓는것이 합리적이다.

### 3.2 소유 가능한 Contract

우리는 우리 Contract에서 이 주소를 바꿀 수 있게끔 하고 싶지만, 그렇다고 모든 사람이 주소를 업데이트할 수 있기를 원하지는 않는다.

이런 경우에 대처하기 위해서, 최근에 주로 쓰는 하나의 방법은 Contract를 `소유 가능`하게 만드는 것이다. Contract를 대상으로 특별한 권리를 가지는 소유자가 있음을 의미하는 것이다.

### 3.3 OpenZeppelin의 `Ownalbe` Contract

