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

`OpenZeppelin`은 우리의 DApp에서 사용할 수 있는, 안전하고 커뮤니티에서 검증받은 Smart Contract의 라이브러리이다.

```sol
/**
 * @title Ownable
 * @dev The Ownable contract has an owner address, and provides basic authorization control
 * functions, this simplifies the implementation of "user permissions".
 */
contract Ownable {
  address public owner;
  event OwnershipTransferred(address indexed previousOwner, address indexed newOwner);

  /**
   * @dev The Ownable constructor sets the original `owner` of the contract to the sender
   * account.
   */
  function Ownable() public {
    owner = msg.sender;
  }

  /**
   * @dev Throws if called by any account other than the owner.
   */
  modifier onlyOwner() {
    require(msg.sender == owner);
    _;
  }

  /**
   * @dev Allows the current owner to transfer control of the contract to a newOwner.
   * @param newOwner The address to transfer ownership to.
   */
  function transferOwnership(address newOwner) public onlyOwner {
    require(newOwner != address(0));
    OwnershipTransferred(owner, newOwner);
    owner = newOwner;
  }
}
```

- 생성자: `function Ownable()`는 생성자이다. Contract와 동일한 이름을 가진, 생략할 수 있는 특별한 함수이다. 이 함수는 Contract가 생성될 떄 딱 한번만 실행된다.

- 함수 제어자: `modifier onlyOwner()` 제어자는 다른 함수들에 대한 접근을 제어하기 위해 사용되는 일종의 유사함수이다. 보통 함수 실행 전의 요구사항 충족 여부를 확인하는 데에 사용한다. `onlyOwner`의 경우에는 접근을 제한해서 오직 Contract의 소유자만 해당 함수를 실행할 수 있도록 하기 위해 사용할 수 있다.

즉, `Ownable` Contract는 기본적으로 다음과 같은 것들을 한다.

1. Contract가 생성되면 Contract 생성자가 `Owner`에 `msg.sender`(Contract를 배포한 사람)을 대입한다.

2. 특정한 함수들에 대해서 오직 `소유자: Ownable`만 접근할 수 있도록 제한 가능한 `onlyOwner` 제어자를 추가한다.

3. 새로운 `소유자`에게 해당 Contract의 소유권을 옮길 수 있도록 한다.

`onlyOwner`는 Contract에서 흔히 쓰는 것 중 하나라, 대부분의 Solidity DApp들은 `Ownable`Contract를 복사/붙여넣기 해서 시작한다. 그리고 첫 Contract는 이 Contract를 상속해서 만든다.

### 3.4 함수 제어자

함수 제어자는 함수처럼 보이지만, `function` 키워드 대신 `modifier`키워드를 사용한다. 그리고 함수를 호출하듯이 직접 호출할 수는 없다. 대신에 함수 정의부 끝에 해당 함수의 작동 방식을 바꾸도록 제어자의 이름을 붙일 수 있다.

이에 대한 예시코드는 다음과 같다.

```sol
/**
 * @dev Throws if called by any account other than the owner.
 */
modifier onlyOwner() {
  require(msg.sender == owner);
  _;
}
```

```sol
contract MyContract is Ownable {
  event LaughManiacally(string laughter);

  // 아래 `onlyOwner`의 사용 방법을 잘 보게:
  function likeABoss() external onlyOwner {
    LaughManiacally("Muahahahaha");
  }
}
```

`likeABoss`함수의 `onlyOwner` 제어자 부분을 잘 보면, 우리가 `likeABoss` 함수를 호출하면, `onlyOwner`의 코드가 먼저 실행된다. 그리고 `onlyOwner`의 `_;` 부분을 `likeABoss` 함수로 되돌아가 해당 코드를 실행하게 된다.

우리가 제어자를 사용할 수 있는 다양한 방법이 있지만, 가장 일반적으로 쓰는 예시 중 하나는 함수 실행 전에 `require` 체크를 넣는 것이다.

`onlyOwner`의 경우에는, 함수에 이 제어자를 추가하면 오직 Contract의 소유자만이 해당 함수를 호출할 수 있다.

{{<admonition tip>}}
참고: 이렇게 소유자가 컨트랙트에 특별한 권한을 갖도록 하는 것은 자주 필요하지만, 이게 악용될 수도 있다네. 예를 들어, 소유자가 다른 사람의 좀비를 뺏어올 수 있도록 하는 백도어 함수를 추가할 수도 있지!

그러니 잘 기억하게. 이더리움에서 돌아가는 DApp이라고 해서 그것만으로 분산화되어 있다고 할 수는 없네. 반드시 전체 소스 코드를 읽어보고, 자네가 잠재적으로 걱정할 만한, 소유자에 의한 특별한 제어가 불가능한 상태인지 확인하게. 개발자로서는 자네가 잠재적인 버그를 수정하고 DApp을 안정적으로 유지하도록 하는 것과, 사용자들이 그들의 데이터를 믿고 저장할 수 있는 소유자가 없는 플랫폼을 만드는 것 사이에서 균형을 잘 잡는 것이 중요하네.
{{</admonition>}}

### 3.5 Gas

지금부터는 Solidity와 다른 프로그래밍 언어의 차이점을 살펴본다.

#### Gas - Ethereum DApp이 사용하는 연료

Solidity에서는 사용자들이 우리가 만든 DApp의 함수를 실행할 때마다 `Gas`라고 불리는 화폐를 지불해야 한다. 사용자는 이더(`ETH`, 이더리움 화폐)를 이용해서 가스를 사기 때문에, 우리의 DApp 함수를 실행하려면 사용자들은 ETH를 소모해야만 한다.

함수를 실행하는 데에 얼마나 많은 가스가 필요한지는 그 함수의 로직(논리 구조)이 얼마나 복잡한지에 따라 달라진다. 각각의 연산은 소모되는 `가스 비용(gas cost)`이 있고, 그 연산을 수행하는 데에 소모되는 컴퓨팅 자원의 양이 이 비용을 결정한다.

예를 들어, storage에 값을 쓰는 것은 두 개의 정수를 더하는 것보다 훨씬 비용이 높다. 우리 함수의 전체 `가스 비용`은 그 함수를 구성하는 개별 연산들의 가스 비용을 모두 합친 것과 같다.

함수를 실행하는 것은 사용자들에게 실제 돈을 쓰게 하기 때문에, 이더리움에서 코드 최적화는 다른 프로그래밍 언어들에 비해 훨씬 더 중요하다. 만약 코드가 엉망이라면, 사용자들은 함수를 실행하기 위해 일종의 할증료를 더 내야 한다. 그리고 수천 명의 사용자가 이런 불필요한 비용을 낸다면 할증료가 수십 억 원까지 쌓일 수 있다.

#### 가스는 왜 필요한가?

Ethereum은 크고 느린, 하지만 굉장히 안전한 컴퓨터와 같다고 할 수 있다. 어떤 함수를 실행할 때, 네트워크 상의 모든 개별 노드가 함수의 출력값을 검증하기 위해 그 함수를 실행해야 한다. 모든 함수의 실행을 검증하는 수천 개의 노드가 바로 Ethereum을 분산화하고, 데이터를 보전하면 누군가 검열할 수 없도록 하는 요소이다.

Ethereum을 만든 사람들은 누군가가 무한 반복문을 써서 네트워크를 방해하거나, 자원 소모가 큰 연산을 써서 네트워크 자원을 모두 사용하지 못하도록 만들길 원한다. 그래서 그들은 연산 처리에 비용이 들도록 만들었고, 사용자들은 저장 공간 뿐만 아니라 연산 사용 시간에 따라서도 비용을 지불해야 한다.

{{<admonition tip>}}
참고: 사이드체인에서는 반드시 이렇지는 않다네. 크립토좀비를 만든 사람들이 Loom Network에서 만들고 있는 것들이 좋은 예시가 되겠군. 이더리움 메인넷에서 월드 오브 워크래프트 같은 게임을 직접적으로 돌리는 것은 절대 말이 되지 않을 걸세. 가스 비용이 엄청나게 높을 것이기 때문이지. 하지만 다른 합의 알고리즘을 가진 사이드체인에서는 가능할 수 있지. 우린 다음에 나올 레슨에서 DApp을 사이드체인에 올릴지, 이더리움 메인넷에 올릴지 판단하는 방법들에 대해 더 얘기할 걸세.
{{</admonition>}}

#### 가스를 아끼기 위한 구조체 압축

우리는 `uint`에 다른 타입들이 있다는 것을 배웠다. `uint8`, `uint126`, `uint32`, 등

기본적으로 이런 하위 타입들을 쓰는 것은 아무런 이득이 없다. 왜냐하면 Solidity에서는 `uint`의 크기에 상관없이 256비트의 저장 공간을 미리 잡아놓기 때문이다. 예를들어, `uint(uint256)` 대신에 `uint8`을 쓰는 것은 가스 소모를 줄이는 데에 아무 영향이 없다.

가스 소모를 위해서는 `struct`의 안에서 줄여야 한다.

만약 구조체 안에 여러 개의 `uint`를 만든다면, 가능한 더 작은 크기의 `uint`를 쓰자. Solidity에서 그 변수들을 더 적은 공간을 차지하도록 압축할 것이다. 예를 들면 다음과 같다.

```sol
struct NormalStruct {
  uint a;
  uint b;
  uint c;
}

struct MiniMe {
  uint32 a;
  uint32 b;
  uint c;
}

// `mini`는 구조체 압축을 했기 때문에 `normal`보다 가스를 조금 사용할 것이네.
NormalStruct normal = NormalStruct(10, 20, 30);
MiniMe mini = MiniMe(10, 20, 30);
```

구조체 안에서는 가능한 작은 크기의 정수 타입을 쓰는 것이 좋다.

또한 동일한 데이터 타입은 하나로 묶어놓는 것이 좋다. 즉, 구조체에서 서로 옆에 있도록 선언하면 Solidity에서 사용하는 저장 공간을 최소화한다. 예를 들면, `uint c; uint32 a; uint32 b;`라는 필드로 구성된 구조체가 `uint32 a; uint c; uint32 b`필드로 구성된 구조체보다 가스를 덜 소모한다. `uint32` 필드가 묶여있기 때문이다.

### 3.6 시간 단위(Time units)

Solidity는 시간을 다룰 수 있는 단위계를 기본적으로 제공한다.

`now`변수를 쓰면 현재의 유닉스 타임스탬프 값을 얻을 수 있다.

Solidity는 또한 `seconds, minutes, hours, days, weeks, years`같은 시간 단위 또한 포함하고 있다. 이들은 그에 해당하는 길이 만큼의 초 단위 `uint` 숫자로 변환된다. 즉 `1 minutes는 60, 1 hours는 3600(60초 x 60 분), 1 days는 86400`로 변환된다. 이 시간 단위들이 유용하게 사용될 수 있는 예시는 다음과 같다.

```sol
uint lastUpdated;

// `lastUpdated`를 `now`로 설정
function updateTimestamp() public {
  lastUpdated = now;
}

// 마지막으로 `updateTimestamp`가 호출된 뒤 5분이 지났으면 `true`를, 5분이 아직 지나지 않았으면 `false`를 반환
function fiveMinutesHavePassed() public view returns (bool) {
  return (now >= (lastUpdated + 5 minutes));
}
```

### 3.7 구조체를 인수로 전달하기

`private` 또는 `internal` 함수에 인수로서 구조체의 storage 포인터를 전달할 수 있다. 이건 예를 들어 함수들 간에 구조체를 전달할 때 유용하다.

```sol
function _doStuff(Zombie storage _zombie) internal {
  // _zombie로 할 수 있는 것들을 처리
}
```

이런 방식으로 우리는 함수에 좀비 ID를 전달하고 좀비를 찾는 대신, 좀비에 대한 참조를 전달해 시간을 줄일 수 있다.

### 3.8 Public 함수 & 보안

보안을 점검하는 좋은 방법은 모든 `public`과 `external` 함수를 검사하고, 사용자들이 그 함수들을 남용할 수 있는 방법을 생각해 보는 것이다. 기억하자 - 이 함수들이 `onlyOwner` 같은 제어자를 갖지 않는 이상, 어떤 사용자든 이 함수들을 호출하고 자신들이 원하는 모든 데이터를 함수에 전달할 수 있다.

사용자들은 이 함수를 직접적으로 호출할 수 있고 그들이 원하는 아무 `_targetDna`나 `_species`를 전달할 수 있다. 이러한 남용을 막기 위해서는 함수를 `internal`로 만드는 것이다.

### 3.9 함수 제어자의 또 다른 특징

#### 인수를 가지는 함수 제어자

이전에는 `onlyOwner`라는 간단한 예시를 살펴보았다. 하지만 함수 제어자는 사실 인수 또한 받을 수 있다. 예를 들어

```sol
// 사용자의 나이를 저장하기 위한 매핑
mapping (uint => uint) public age;

// 사용자가 특정 나이 이상인지 확인하는 제어자
modifier olderThan(uint _age, uint _userId) {
  require (age[_userId] >= _age);
  _;
}

// 차를 운전하기 위햐서는 16살 이상이어야 하네(적어도 미국에서는).
// `olderThan` 제어자를 인수와 함께 호출하려면 이렇게 하면 되네:
function driveCar(uint _userId) public olderThan(16, _userId) {
  // 필요한 함수 내용들
}
```

여기서 `olderThan` 제어자가 함수와 비슷하게 인수를 받는 것을 확인할 수 있다. 그리고 `driveCar` 함수는 받은 인수를 제어자로 전달하고 있다.

### 3.10 View 함수를 사용해 가스 절약하기

`view` 함수는 사용자에 의해 외부에서 호출되었을 때 가스를 전혀 소모하지 않는다.

이건 `view` 함수가 블록체인 상에서 실제로 어떤 것도 수정하지 않기 때문이다. 데이터를 읽기만 한다. 그러니 함수에 `view` 표시를 하는 것은 `web3.js`에 이렇게 말하는 것과 같다. "이 함수는 실행할 때 로컬 Ethereum 노드에 질의만 날리면 되고, 블록체인에 어떤 트랙잭션도 만들지 않는다"(트랜잭션은 모든 개별 노드에서 실행되어야 하고, 가스를 소모한다.)

{{<admonition tip>}}
참고: 만약 view 함수가 동일 컨트랙트 내에 있는, view 함수가 아닌 다른 함수에서 내부적으로 호출될 경우, 여전히 가스를 소모할 것이네. 이것은 다른 함수가 이더리움에 트랜잭션을 생성하고, 이는 모든 개별 노드에서 검증되어야 하기 때문이네. 그러니 view 함수는 외부에서 호출됐을 때에만 무료라네.
{{</admonition>}}

### 3.11 Storage는 비싸다.

Solidity에서 더 비싼 연산 중 하나는 바로 `storage`를 쓰는 것이다 - 그 중에서도 쓰기 연산이다.

이건 우리가 데이터의 일부를 쓰거나 바꿀 때마다, 블록체인에 영구적으로 기록되기 때문이다. 영원히! 지구 상의 수천개의 노드들이 그들의 하드 드라이브에 그 데이터를 저장해야 하고, 블록체인이 커져가면서 이 데이터의 양 또한 같이 커져간다. 그러니 이 연산에는 비용이 든다.

비용을 최소화하기 위해서, 진짜 필요한 경우가 아니면 `storage`에 데이터를 쓰지 않는 것이 좋다. 이를 위해 때로는 겉보기에 비효율적으로 보이는 프로그래밍 구성을 할 필요가 있다 - 어떤 배열에서 내용을 빠르게 찾기 위해, 단순히 변수에 저장하는 것 대신 함수가 호출될 때마다 배열을 `memory`에 다시 만드는 것처럼 말이다.

대부분의 프로그래밍 언어에서는, 큰 데이터 집합의 개별 데이터에 모두 접근하는 것은 비용이 비싸다. 하지만 Solidity에서는 그 접근이 `external view` 함수라면 `storage`를 사용하는 것보다 더 저렴한 방법이다. `view` 함수는 사용자들의 가스를 소모하지 않기 때문이다.

#### 메모리에 배열 선언하기

Storage에 아무것도 쓰지 않고도 함수 안에 새로운 배열을 만들려면 `memory` 키워드를 쓰면 된다. 이 배열은 함수가 끝날 때까지만 존재할 것이고, 이는 `storage`의 배열을 직접 업데이트하는 것보다 가스 소모 측면에서 훨씬 저렴하다. 외부에서 호출되는 `view` 함수라면 무료이다.

메모리에 배열을 선언하는 방법은 다음과 같다.

```sol
function getArray() external pure returns(uint[]) {
  // 메모리에 길이 3의 새로운 배열을 생성한다.
  uint[] memory values = new uint[](3);
  // 여기에 특정한 값들을 넣는다.
  values.push(1);
  values.push(2);
  values.push(3);
  // 해당 배열을 반환한다.
  return values;
}
```

{{<admonition tip>}}
참고: 메모리 배열은 반드시 길이 인수와 함께 생성되어야 하네(이 예시에서는, 3). 메모리 배열은 현재로서는 storage 배열처럼 array.push()로 크기가 조절되지는 않네. 이후 버전의 솔리디티에서는 변경될 수도 있겠지만 말이야.
{{</admonition>}}

### 정리

```sol
// zombieFactory.sol

pragma solidity ^0.4.19;

import "./ownable.sol";

contract ZombieFactory is Ownable {

    event NewZombie(uint zombieId, string name, uint dna);

    uint dnaDigits = 16;
    uint dnaModulus = 10 ** dnaDigits;
    uint cooldownTime = 1 days;

    struct Zombie {
      string name;
      uint dna;
      uint32 level;
      uint32 readyTime;
    }

    Zombie[] public zombies;

    mapping (uint => address) public zombieToOwner;
    mapping (address => uint) ownerZombieCount;

    function _createZombie(string _name, uint _dna) internal {
        uint id = zombies.push(Zombie(_name, _dna, 1, uint32(now + cooldownTime))) - 1;
        zombieToOwner[id] = msg.sender;
        ownerZombieCount[msg.sender]++;
        NewZombie(id, _name, _dna);
    }

    function _generateRandomDna(string _str) private view returns (uint) {
        uint rand = uint(keccak256(_str));
        return rand % dnaModulus;
    }

    function createRandomZombie(string _name) public {
        require(ownerZombieCount[msg.sender] == 0);
        uint randDna = _generateRandomDna(_name);
        randDna = randDna - randDna % 100;
        _createZombie(_name, randDna);
    }

}
```

```sol
// zombiefeeding.sol

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

  KittyInterface kittyContract;

  function setKittyContractAddress(address _address) external onlyOwner {
    kittyContract = KittyInterface(_address);
  }

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

```sol
// ownalbe.sol

/**
 * @title Ownable
 * @dev The Ownable contract has an owner address, and provides basic authorization control
 * functions, this simplifies the implementation of "user permissions".
 */
contract Ownable {
  address public owner;

  event OwnershipTransferred(address indexed previousOwner, address indexed newOwner);

  /**
   * @dev The Ownable constructor sets the original `owner` of the contract to the sender
   * account.
   */
  function Ownable() public {
    owner = msg.sender;
  }


  /**
   * @dev Throws if called by any account other than the owner.
   */
  modifier onlyOwner() {
    require(msg.sender == owner);
    _;
  }


  /**
   * @dev Allows the current owner to transfer control of the contract to a newOwner.
   * @param newOwner The address to transfer ownership to.
   */
  function transferOwnership(address newOwner) public onlyOwner {
    require(newOwner != address(0));
    OwnershipTransferred(owner, newOwner);
    owner = newOwner;
  }

}
```

```sol
// zombiehelper.sol

pragma solidity ^0.4.19;

import "./zombiefeeding.sol";

contract ZombieHelper is ZombieFeeding {

  modifier aboveLevel(uint _level, uint _zombieId) {
    require(zombies[_zombieId].level >= _level);
    _;
  }

  function changeName(uint _zombieId, string _newName) external aboveLevel(2, _zombieId) {
    require(msg.sender == zombieToOwner[_zombieId]);
    zombies[_zombieId].name = _newName;
  }

  function changeDna(uint _zombieId, uint _newDna) external aboveLevel(20, _zombieId) {
    require(msg.sender == zombieToOwner[_zombieId]);
    zombies[_zombieId].dna = _newDna;
  }

  function getZombiesByOwner(address _owner) external view returns(uint[]) {
    uint[] memory result = new uint[](ownerZombieCount[_owner]);
    // 여기서 시작하게
        uint counter = 0;
    for (uint i = 0; i < zombies.length; i++) {
      if (zombieToOwner[i] == _owner) {
        result[counter] = i;
        counter++;
      }
    }
    return result;
  }

}
```

{{<admonition info>}}

1. 함수 제어자

- `private`: Contract 내부의 다른 함수들에서만 호출될 수 있다.

- `internal`: 해당 Contract를 상속하는 Contract에서도 호출될 수 있다.

- `external`: 오직 Contract 외부에서만 호출될 수 있다.

- `public`: 내외부 모두에서, 어디서든 호출될 수 있다.

2. 상태 제어자

- `view`: 해당 함수를 실행해도 어떤 데이터도 저장/변경되지 않음을 알려준다.

- `pure`: 해당 함수가 어떤 데이터도 블록체인에 저장하지 않을 뿐만 아니라, 블록체인으로부터 어떤 데이터도 읽지 않음을 알려준다.

  이들 모두 Contract 외부에서 불렸을 때 가스를 전혀 소모하지 않는다.(하지만 다른 함수에 의해 내부적으로 호출됐을 경우에는 가스를 소모한다.)

3. 사용자 정의 제어자

예를 들어 `onlyOwner`, `aboveLevel` 같은 것이다. 이런 제어자를 사용해 함수에 이 제어자들이 어떻게 영향을 줄지를 결정하는 논리를 구성할 수 있다.

```sol
function test() external view onlyOwner anotherModifier { /* ... */ }
```

{{</admonition>}}

## Chapter 4

### 4.1 Payable 제어자

`payable` 함수는 Solidity와 Ethereum을 아주 멋지게 만드는 것 중 하나다. 이는 이더를 받을 수 있는 특별한 함수 유형이다.

일반적인 웹 서버에서 API 함수를 실행할 때에는, 함수 호출을 통해서 US 달러를 보낼 수 없다 - 비트코인도 마찬가지로 보낼 수 없다.

하지만 Ethereum에서는 돈(이더), 데이터(transaction payload), 그리고 Contract 코드 자체 모두 Ethereum 위에 존재하기 때문에, 함수를 실행하는 동시에 Contract에 돈을 지불하는 것이 가능하다.

이를 통해 흥미로운 구성을 만들 수 있다. 함수를 실행하기 위해 Contract에 일정 금액을 지불하게 하는 것과 같이 말이다.

예시를 보면 다음과 같다.

```sol
contract OnlineStore {
  function buySomething() external payable {
    // 함수 실행에 0.001이더가 보내졌는지 확실히 하기 위해 확인:
    require(msg.value == 0.001 ether);
    // 보내졌다면, 함수를 호출한 자에게 디지털 아이템을 전달하기 위한 내용 구성:
    transferThing(msg.sender);
  }
}
```

여기서, `msg.sender`는 Contract로 이더가 얼마나 보내졌는지 확인하는 방법이고, `ether`는 기본적으로 포함된 단위이다.

여기서 일어나는 일은 누군가 web3.js(DApp의 자바스크립트 프론트엔드)에서 다음과 같이 함수를 실행할 때 발생한다.

```JS
// `OnlineStore`는 자네의 이더리움 상의 컨트랙트를 가리킨다고 가정하네:
OnlineStore.buySomething({
  from: web3.eth.defaultAccount,
  value: web3.utils.toWei(0.001),
});
```

`value` 필드를 자세히 보면, 자바스크립트 함수 호출에서 이 필드를 통해 `ether`를 얼마나 보낼지 결정한다(여기서는 0.001). Transaction을 봉투로 생각하고, 함수 호출에 전달하는 매개 변수를 편지 내용이라 생각한다면, `value`는 봉투 안에 현금을 넣는 것과 같다.

{{<admonition warning>}}
참고: 만약 함수가 payable로 표시되지 않았는데 자네가 위에서 본 것처럼 이더를 보내려 한다면, 함수에서 자네의 트랜잭션을 거부할 것이네.
{{</admonition>}}

### 4.2 출금

Contract로 이더를 보내면, 해당 Contract의 Ethereum 계좌에 이더가 저장되고 거기에 갇히게 된다.

다음과 같이 Contract에서 이더를 인출하는 함수를 작성할 수 있다.

```sol
contract GetPaid is Ownable {
  function withdraw() external onlyOwner {
    owner.transfer(this.balance);
  }
}
```

`Ownable` Contract를 import 했다고 가정하고 `owner`와 `onlyOwner`를 사용하고 있다.

`transfer` 함수를 사용해서 특정한 Ethereum 주소에 돈을 보낼 수 있다. 예를 들어, 만약 누군가 한 아이템에 대해 초과 지불을 했다면, 이더를 `msg.sender`로 되돌려주는 함수를 만들 수도 있다.

```sol
uint itemFee = 0.001 ether;
msg.sender.transfer(msg.value - itemFee);
```

혹은 구매자와 판매자가 존재하는 Contract에서, 판매자의 주소를 storage에 저장하고, 누군가 판매자의 아이템을 구매하면 구매자로부터 받은 요금을 그에게 전달할 수도 있다: `seller.transfer(msg.sender)`

### 4.3 난수

모든 좋은 게임들은 일정 수준의 무작위성을 필요로한다.

#### keccak256을 통한 난수 생성

Solidity에서 난수를 만들기에 가장 좋은 방법은 `keccak256` 해시 함수를 쓰는 것이다.

다음과 같이 사용할 수 있닫.

```sol
// Generate a random number between 1 and 100:
uint randNonce = 0;
uint random = uint(keccak256(now, msg.sender, randNonce)) % 100;
randNonce++;
uint random2 = uint(keccak256(now, msg.sender, randNonce)) % 100;
```

위의 예시에서는 `now`의 타임스탬프 값, `msg.sender`, 증가하는 `noncee`(딱 한 번만 사용되는 숫자, 즉 똑같은 입력으로 두 번 이상 동일한 해시 함수를 실행할 수 없게 함)를 받고 있다.

그리고서 `keccak`을 사용해서 이 입력들을 임의의 해시 값으로 변환하고, 변환환 해시 값을 `uint`로 바꾼 후, `% 100`을 써서 마지막 2자리 숫자만 받도록 한ㄷ다. 이를 통해 0과 99 사이의 완전한 난수를 얻을 수 있다.

#### 이 메소드는 정직하지 않은 노드의 공격에 취약하다.

Ethereum에서는 Contract의 함수를 실행하면 Transaction으로서 네트워크의 노드 하나 혹은 여러 노드에 실행을 알리게 된다. 그 후 네트워크의 노드들은 여러 개의 transaction을 모으고, "직업 증명"으로 알려진 계산이 매우 복잡한 수학적 문제를 먼저 풀기 위한 시도를 한다. 그리고서 해당 transaction 그룹을 그들의 직업증명(PoW)와 함께 블록으로 네트워크에 배포한다.

한 노드가 어떤 PoW를 풀면, 다른 노드들은 그 PoW를 풀려는 시도를 멈추고 해당 노드가 보낸 transaction 목록이 유효한 것인지 검증한다. 유효하다면 해당 블록을 받아들이고 다음 블록을 풀기 시작한다.

이것이 난수 함수를 취약하게 만든다.

우리가 동전 던지기 Contract를 사용한다고 가정해보자 - 앞면이 나오면 돈이 두 배가 되고, 뒷면이 나오면 모두 잃는 것이다. 앞뒤면을 결정할 때 위에서 본 난수 함수를 사용한다고 가정해보자.(`random >= 50`은 앞면, `random < 50`은 뒷면이다)

내가 만약 노드를 실행하고 있다면, 나는 오직 나의 노드에만 transaction을 알리고 이것을 공유하지 않을 수 있다. 그 후 내가 이기는지 확인하기 위해 동전 던지기 함수를 실행할 수 있다 - 그리고 만약 내가 진다면, 내가 풀고 있는 다음 블록에 해당 transaction을 포함하지 않는 것을 선택한다. 난 이것을 내가 결국 동전 던지기에서 이기고 다음 블록을 풀 때까지 무한대로 반복할 수 있고, 이득을 볼 수 있다.

#### 그럼 Ethereum에서는 어떻게 난수를 안전하게 만들어 낼 수 있을까?

블록체인의 전체 내용은 모든 참여자에게 공개되므로, 이건 풀기 어려운 문제이다. 하나의 방법은 Ethereum 블록체인 외북의 난수 함수에 접근할 수 있도록 `Oracle`을 사용하는 것이다.

### 정리

```sol
// zombieAttack.sol

import "./zombiehelper.sol";

contract ZombieBattle is ZombieHelper {
  uint randNonce = 0;
  uint attackVictoryProbability = 70;

  function randMod(uint _modulus) internal returns(uint) {
    randNonce++;
    return uint(keccak256(now, msg.sender, randNonce)) % _modulus;
  }

  function attack(uint _zombieId, uint _targetId) external ownerOf(_zombieId) {
    Zombie storage myZombie = zombies[_zombieId];
    Zombie storage enemyZombie = zombies[_targetId];
    uint rand = randMod(100);
    if (rand <= attackVictoryProbability) {
      myZombie.winCount++;
      myZombie.level++;
      enemyZombie.lossCount++;
      feedAndMultiply(_zombieId, enemyZombie.dna, "zombie");
    } else {
      myZombie.lossCount++;
      enemyZombie.winCount++;
    }
    _triggerCooldown(myZombie);
  }
}
```

```sol
// zombie.helper.sol

pragma solidity ^0.4.19;

import "./zombiefeeding.sol";

contract ZombieHelper is ZombieFeeding {

  uint levelUpFee = 0.001 ether;

  modifier aboveLevel(uint _level, uint _zombieId) {
    require(zombies[_zombieId].level >= _level);
    _;
  }

  function withdraw() external onlyOwner {
    owner.transfer(this.balance);
  }

  function setLevelUpFee(uint _fee) external onlyOwner {
    levelUpFee = _fee;
  }

  function changeName(uint _zombieId, string _newName) external aboveLevel(2, _zombieId) ownerOf(_zombieId) {
    zombies[_zombieId].name = _newName;
  }

  function changeDna(uint _zombieId, uint _newDna) external aboveLevel(20, _zombieId) ownerOf(_zombieId) {
    zombies[_zombieId].dna = _newDna;
  }

  function getZombiesByOwner(address _owner) external view returns(uint[]) {
    uint[] memory result = new uint[](ownerZombieCount[_owner]);
    uint counter = 0;
    for (uint i = 0; i < zombies.length; i++) {
      if (zombieToOwner[i] == _owner) {
        result[counter] = i;
        counter++;
      }
    }
    return result;
  }

}

```

```sol
// zombiefeeding.sol

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

  KittyInterface kittyContract;

  modifier ownerOf(uint _zombieId) {
    require(msg.sender == zombieToOwner[_zombieId]);
    _;
  }

  function setKittyContractAddress(address _address) external onlyOwner {
    kittyContract = KittyInterface(_address);
  }

  function _triggerCooldown(Zombie storage _zombie) internal {
    _zombie.readyTime = uint32(now + cooldownTime);
  }

  function _isReady(Zombie storage _zombie) internal view returns (bool) {
      return (_zombie.readyTime <= now);
  }

  function feedAndMultiply(uint _zombieId, uint _targetDna, string _species) internal ownerOf(_zombieId) {
    Zombie storage myZombie = zombies[_zombieId];
    require(_isReady(myZombie));
    _targetDna = _targetDna % dnaModulus;
    uint newDna = (myZombie.dna + _targetDna) / 2;
    if (keccak256(_species) == keccak256("kitty")) {
      newDna = newDna - newDna % 100 + 99;
    }
    _createZombie("NoName", newDna);
    _triggerCooldown(myZombie);
  }

  function feedOnKitty(uint _zombieId, uint _kittyId) public {
    uint kittyDna;
    (,,,,,,,,,kittyDna) = kittyContract.getKitty(_kittyId);
    feedAndMultiply(_zombieId, kittyDna, "kitty");
  }
}
```

```sol
// zombiefactory.sol

pragma solidity ^0.4.19;

import "./ownable.sol";

contract ZombieFactory is Ownable {

    event NewZombie(uint zombieId, string name, uint dna);

    uint dnaDigits = 16;
    uint dnaModulus = 10 ** dnaDigits;
    uint cooldownTime = 1 days;

    struct Zombie {
      string name;
      uint dna;
      uint32 level;
      uint32 readyTime;
      uint16 winCount;
      uint16 lossCount;
    }

    Zombie[] public zombies;

    mapping (uint => address) public zombieToOwner;
    mapping (address => uint) ownerZombieCount;

    function _createZombie(string _name, uint _dna) internal {
        uint id = zombies.push(Zombie(_name, _dna, 1, uint32(now + cooldownTime), 0, 0)) - 1;
        zombieToOwner[id] = msg.sender;
        ownerZombieCount[msg.sender]++;
        NewZombie(id, _name, _dna);
    }

    function _generateRandomDna(string _str) private view returns (uint) {
        uint rand = uint(keccak256(_str));
        return rand % dnaModulus;
    }

    function createRandomZombie(string _name) public {
        require(ownerZombieCount[msg.sender] == 0);
        uint randDna = _generateRandomDna(_name);
        randDna = randDna - randDna % 100;
        _createZombie(_name, randDna);
    }

}
```

## Chapter 5

### 5.1 Token

Ethereum에서 `Token`은 기본적으로 그저 몇몇 공통 규약을 따르는 Smart Contract이다. 즉 다른 모든 Token Contract가 사용하는 표준 함수 집합을 구현하는 것이다. 예를 들어 `transfer(address _to, uint256 _value)`나 `balanceOf(address _owner)`같은 함수들이 있다.

내부적으로 Smart Contract는 보통 `mapping(address => uint256) balances`와 같은 mapping을 가지고 있다. 각각의 주소에 잔액이 얼마나 있는지 기록하는 것이다.

즉 기본적으로 Token은 그저 하나의 Contract이다. 그 안에서 누가 얼마나 많은 Token을 가지고 있는지 기록하고, 몇몇 함수를 가지고 사용자들이 그들의 Token을 다른 주소로 전송할 수 있게 해주는 것이다.

#### 이렇게 하는 이유?

모든 ERC20 토큰들이 똑같은 이름의 동일한 함수 집합을 공유하기 때문에, 이 Tokeen들에 똑같은 방식으로 상호작용이 가능하다.

즉 하나의 ERC20 Token과 상호작용할 수 있는 애플리케이션 하나를 만들면, 이 앱이 다른 어떤 ERC20 Token과도 상호작용이 가능하다. 이런 방식으로 앱에 더 많은 Token을 추가할 수 있다. 커스텀 코드를 추가하지 않고도 말이다. 우리는 그저 새로운 Token의 Contract 주소만 끼워넣으면 된다. 그러고 나면, 앱에서 사용할 수 있는 또 다른 Token이 생긴다.

이런 방식의 예시로는 거래소가 있다. 한 거래소에서 새로운 ERC20 Token을 상장할 때, 실제로는 이 거래소에서 통신이 가능한 또 하나의 Smart Contract를 추가하는 것이다. 사용자들은 이 Contract에 거래소의 지갑 주소에 Token을 보내라고 할 수 있고, 거래소에서는 이 Contract에 사용자들이 출금을 신청하면 Token을 다시 돌려보내라고 할 수 있게 만드는 것이다.

거래소에서는 이 진송 로직을 한 번만 구현하면 된다. 그리고서 새로운 ERC20 Token을 추가하고 싶으면, 데이터베이스에 단순히 새 Contract 주소를 추가하기만 하면 된다.

#### 다른 Token 표준

ERC721 Token은 교체가 불가하다. 각각의 Token이 유일하고 분할이 불가하기 때문이다. 이 Token을 하나의 전체 단위로만 거래할 수 있고, 각각의 Token은 유일한 ID를 가지고 있다.

### 5.2 ERC721 표준

먼저 ERC721 표준은 다음과 같다.

```sol
contract ERC721 {
  event Transfer(address indexed _from, address indexed _to, uint256 _tokenId);
  event Approval(address indexed _owner, address indexed _approved, uint256 _tokenId);

  function balanceOf(address _owner) public view returns (uint256 _balance);
  function ownerOf(uint256 _tokenId) public view returns (address _owner);
  function transfer(address _to, uint256 _tokenId) public;
  function approve(address _to, uint256 _tokenId) public;
  function takeOwnership(uint256 _tokenId) public;
}
```

#### balanceOf

이 함수는 단순히 `address`를 받아, 해당 `address`가 Token을 얼마나 가지고 있는지 반환한다.

#### ownerOf

이 함수에서는 Token ID를 받아, 이를 소유하고 있는 사람의 `address`를 반환한다.

### 5.3 Overflow 막기

#### Contract 보안 강화: Overflow와 Underflow

Overflow란 무엇인가?

우리가 8비트 데이터를 저장할 수 있는 `uint8` 하나를 가지고 있다고 해보자. 이 말인즉 우리가 저장할 수 있는 가장 큰 수는 이진수로 `11111111`(또는 십진수로 2^8-1 = 255)가 된다.

다음 예시를 보면, 마지막 `number`의 값은 무엇이 될까?

```sol
uint8 number = 255;
number++;
```

위의 예시에서, 우리는 이 변수에 Overflow를 만들었다 - 즉 `number`가 직관과는 다르게 0이 된다. 우리가 증가를 시켰음에도 말이다. 우리가 이진수 `11111111`에 1을 더하면, 이 수는 `00000000`로 돌아간다.

Underflow는 이와 유사하게 우리가 `0` 값을 가진 `uint8`에서 `1`을 빼면, `255`와 같아지는 것을 말한다(`uint`에 부호가 없어, 음수가 될 수 없기 때문이다).

우리가 여기서 `uint8`을 쓰지는 않고, `1`씩 증가시킨다고 `uint256`에 Overflow가 발생하지는 않을 것 같지만, 미래에 우리의 DApp에 예상치 못한 문제가 발생하지 않도록 여전히 Contract에 보호 장치를 두는 것이 좋다.

#### SafeMath 사용하기

Library는 Solidity에서 특별한 종류의 Contract이다. 이게 유용하게 사용되는 경우 중 하나는 기본(native) 데이터 타입에 함수를 붙일 때이다.

예를 들어, SafeMath 라이브러리를 쓸 때는 `using SafeMath for uint256`이라는 구문을 사용한다. SafeMath 라이브러리는 4개의 함수를 가지고 있다 - `add`, `sub`, `mul`, `div`.

```sol
using SafeMath for uint256;

uint256 a = 5;
uint256 b = a.add(3); // 5 + 3 = 8
uint256 c = a.mul(2); // 5 * 2 = 10
```

SafeMath 내부의 코드는 다음과 같다.

```sol
library SafeMath {

  function mul(uint256 a, uint256 b) internal pure returns (uint256) {
    if (a == 0) {
      return 0;
    }
    uint256 c = a * b;
    assert(c / a == b);
    return c;
  }

  function div(uint256 a, uint256 b) internal pure returns (uint256) {
    // assert(b > 0); // Solidity automatically throws when dividing by 0
    uint256 c = a / b;
    // assert(a == b * c + a % b); // There is no case in which this doesn't hold
    return c;
  }

  function sub(uint256 a, uint256 b) internal pure returns (uint256) {
    assert(b <= a);
    return a - b;
  }

  function add(uint256 a, uint256 b) internal pure returns (uint256) {
    uint256 c = a + b;
    assert(c >= a);
    return c;
  }
}
```

먼저 `library` 키워드를 살펴본다 - Library는 Contract와 비슷하지만 조금 다른 점이 있다. Library는 우리가 `using` 키워드를 사용할 수 있게 해준다. 이를 통해 Library의 메소드들을 다른 데이터 타입에 적용할 수 있다.

```sol
using SafeMath for uint;
// 우리는 이제 이 메소드들을 아무 uint에서나 쓸 수 있네.
uint test = 2;
test = test.mul(3); // test는 이제 6이 되네
test = test.add(5); // test는 이제 11이 되네
```

`mul`과 `add` 함수는 각각 2개의 인수를 필요로 한다. 하지만 우리가 `using SafeMath for uint`를 선언할 때, 우리가 함수를 적용하는 `uint(test)`는 첫 번째 인수로 자동으로 전달된다.

SafeMath가 어떤 것을 하는 지 보기 위해 `add` 함수를 살펴본다.

```sol
function add(uint256 a, uint256 b) internal pure returns (uint256) {
  uint256 c = a + b;
  assert(c >= a);
  return c;
}
```

기본적으로 `add`는 그저 2개의 `uint`를 `+`처럼 더한다. 하지만 그 안에 `assert` 구문을 써서 그 합이 `a`보다 크도록 보장한다. 이것이 `Overflow`를 막아준다.

`assert`는 조건을 만족하지 않으면 에러를 발생시킨다는 점에서 `require`와 비슷하다. `assert`와 `require`의 차이점은, `require`는 함수 실행이 실패하면 남은 가스를 사용자에게 되돌려 주지만, `assert`는 그렇지 않다. 즉 대부분 코드에 `require`를 쓰고싶다. `assert`는 일반적으로 코드가 심각하게 잘못 실행될 때 사용한다.

정리하자면, SafeMath의 add, sub, mul, div는 4개의 수학 연산을 수행하는 함수이지만, Overflow나 Underflow가 발생하면 에러를 발생시키는 것이다.

### 정리

```sol
// zombieownership.sol

pragma solidity ^0.4.19;

import "./zombieattack.sol";
import "./erc721.sol";
import "./safemath.sol";

/// TODO: natspec에 맞도록 이 부분을 바꾸게.
contract ZombieOwnership is ZombieAttack, ERC721 {

  using SafeMath for uint256;

  mapping (uint => address) zombieApprovals;

  function balanceOf(address _owner) public view returns (uint256 _balance) {
    return ownerZombieCount[_owner];
  }

  function ownerOf(uint256 _tokenId) public view returns (address _owner) {
    return zombieToOwner[_tokenId];
  }

  function _transfer(address _from, address _to, uint256 _tokenId) private {
    ownerZombieCount[_to] = ownerZombieCount[_to].add(1);
    ownerZombieCount[msg.sender] = ownerZombieCount[msg.sender].sub(1);
    zombieToOwner[_tokenId] = _to;
    Transfer(_from, _to, _tokenId);
  }

  function transfer(address _to, uint256 _tokenId) public onlyOwnerOf(_tokenId) {
    _transfer(msg.sender, _to, _tokenId);
  }

  function approve(address _to, uint256 _tokenId) public onlyOwnerOf(_tokenId) {
    zombieApprovals[_tokenId] = _to;
    Approval(msg.sender, _to, _tokenId);
  }

  function takeOwnership(uint256 _tokenId) public {
    require(zombieApprovals[_tokenId] == msg.sender);
    address owner = ownerOf(_tokenId);
    _transfer(owner, msg.sender, _tokenId);
  }
}
```

```sol
// zombieattack.sol

pragma solidity ^0.4.19;

import "./zombiehelper.sol";

contract ZombieAttack is ZombieHelper {
  uint randNonce = 0;
  uint attackVictoryProbability = 70;

  function randMod(uint _modulus) internal returns(uint) {
    randNonce++;
    return uint(keccak256(now, msg.sender, randNonce)) % _modulus;
  }

  function attack(uint _zombieId, uint _targetId) external onlyOwnerOf(_zombieId) {
    Zombie storage myZombie = zombies[_zombieId];
    Zombie storage enemyZombie = zombies[_targetId];
    uint rand = randMod(100);
    if (rand <= attackVictoryProbability) {
      myZombie.winCount++;
      myZombie.level++;
      enemyZombie.lossCount++;
      feedAndMultiply(_zombieId, enemyZombie.dna, "zombie");
    } else {
      myZombie.lossCount++;
      enemyZombie.winCount++;
      _triggerCooldown(myZombie);
    }
  }
}
```

```sol
// zombiehelper.sol

pragma solidity ^0.4.19;

import "./zombiefeeding.sol";

contract ZombieHelper is ZombieFeeding {

  uint levelUpFee = 0.001 ether;

  modifier aboveLevel(uint _level, uint _zombieId) {
    require(zombies[_zombieId].level >= _level);
    _;
  }

  function withdraw() external onlyOwner {
    owner.transfer(this.balance);
  }

  function setLevelUpFee(uint _fee) external onlyOwner {
    levelUpFee = _fee;
  }

  function levelUp(uint _zombieId) external payable {
    require(msg.value == levelUpFee);
    zombies[_zombieId].level++;
  }

  function changeName(uint _zombieId, string _newName) external aboveLevel(2, _zombieId) onlyOwnerOf(_zombieId) {
    zombies[_zombieId].name = _newName;
  }

  function changeDna(uint _zombieId, uint _newDna) external aboveLevel(20, _zombieId) onlyOwnerOf(_zombieId) {
    zombies[_zombieId].dna = _newDna;
  }

  function getZombiesByOwner(address _owner) external view returns(uint[]) {
    uint[] memory result = new uint[](ownerZombieCount[_owner]);
    uint counter = 0;
    for (uint i = 0; i < zombies.length; i++) {
      if (zombieToOwner[i] == _owner) {
        result[counter] = i;
        counter++;
      }
    }
    return result;
  }

}
```

```sol
// zombiefeeding.sol

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

  KittyInterface kittyContract;

  modifier onlyOwnerOf(uint _zombieId) {
    require(msg.sender == zombieToOwner[_zombieId]);
    _;
  }

  function setKittyContractAddress(address _address) external onlyOwner {
    kittyContract = KittyInterface(_address);
  }

  function _triggerCooldown(Zombie storage _zombie) internal {
    _zombie.readyTime = uint32(now + cooldownTime);
  }

  function _isReady(Zombie storage _zombie) internal view returns (bool) {
      return (_zombie.readyTime <= now);
  }

  function feedAndMultiply(uint _zombieId, uint _targetDna, string _species) internal onlyOwnerOf(_zombieId) {
    Zombie storage myZombie = zombies[_zombieId];
    require(_isReady(myZombie));
    _targetDna = _targetDna % dnaModulus;
    uint newDna = (myZombie.dna + _targetDna) / 2;
    if (keccak256(_species) == keccak256("kitty")) {
      newDna = newDna - newDna % 100 + 99;
    }
    _createZombie("NoName", newDna);
    _triggerCooldown(myZombie);
  }

  function feedOnKitty(uint _zombieId, uint _kittyId) public {
    uint kittyDna;
    (,,,,,,,,,kittyDna) = kittyContract.getKitty(_kittyId);
    feedAndMultiply(_zombieId, kittyDna, "kitty");
  }
}
```

```sol
// zombiefactory.sol

pragma solidity ^0.4.19;

import "./ownable.sol";
import "./safemath.sol";

contract ZombieFactory is Ownable {

  using SafeMath for uint256;

  event NewZombie(uint zombieId, string name, uint dna);

  uint dnaDigits = 16;
  uint dnaModulus = 10 ** dnaDigits;
  uint cooldownTime = 1 days;

  struct Zombie {
    string name;
    uint dna;
    uint32 level;
    uint32 readyTime;
    uint16 winCount;
    uint16 lossCount;
  }

  Zombie[] public zombies;

  mapping (uint => address) public zombieToOwner;
  mapping (address => uint) ownerZombieCount;

  function _createZombie(string _name, uint _dna) internal {
    uint id = zombies.push(Zombie(_name, _dna, 1, uint32(now + cooldownTime), 0, 0)) - 1;
    zombieToOwner[id] = msg.sender;
    ownerZombieCount[msg.sender]++;
    NewZombie(id, _name, _dna);
  }

  function _generateRandomDna(string _str) private view returns (uint) {
    uint rand = uint(keccak256(_str));
    return rand % dnaModulus;
  }

  function createRandomZombie(string _name) public {
    require(ownerZombieCount[msg.sender] == 0);
    uint randDna = _generateRandomDna(_name);
    randDna = randDna - randDna % 100;
    _createZombie(_name, randDna);
  }

}
```

```sol
// safemath.sol

pragma solidity ^0.4.18;

/**
 * @title SafeMath
 * @dev Math operations with safety checks that throw on error
 */
library SafeMath {

  /**
  * @dev Multiplies two numbers, throws on overflow.
  */
  function mul(uint256 a, uint256 b) internal pure returns (uint256) {
    if (a == 0) {
      return 0;
    }
    uint256 c = a * b;
    assert(c / a == b);
    return c;
  }

  /**
  * @dev Integer division of two numbers, truncating the quotient.
  */
  function div(uint256 a, uint256 b) internal pure returns (uint256) {
    // assert(b > 0); // Solidity automatically throws when dividing by 0
    uint256 c = a / b;
    // assert(a == b * c + a % b); // There is no case in which this doesn't hold
    return c;
  }

  /**
  * @dev Subtracts two numbers, throws on overflow (i.e. if subtrahend is greater than minuend).
  */
  function sub(uint256 a, uint256 b) internal pure returns (uint256) {
    assert(b <= a);
    return a - b;
  }

  /**
  * @dev Adds two numbers, throws on overflow.
  */
  function add(uint256 a, uint256 b) internal pure returns (uint256) {
    uint256 c = a + b;
    assert(c >= a);
    return c;
  }
}
```

```sol
// erc721.sol

contract ERC721 {
  event Transfer(address indexed _from, address indexed _to, uint256 _tokenId);
  event Approval(address indexed _owner, address indexed _approved, uint256 _tokenId);

  function balanceOf(address _owner) public view returns (uint256 _balance);
  function ownerOf(uint256 _tokenId) public view returns (address _owner);
  function transfer(address _to, uint256 _tokenId) public;
  function approve(address _to, uint256 _tokenId) public;
  function takeOwnership(uint256 _tokenId) public;
}
```

## Chapter 6

### 6.1 Web3.js 소개

#### Web3.js란 무엇인가?

Ethereum 네트워크는 노드로 구성되어 있고, 각 노드는 블록체인의 복사본을 가지고 있다. Smart Contract의 함수를 실행하고자 한다면, 이 노드들 중 하나에 질의를 보내 아래 내용을 전달해야 한다.

1. Smart Contract의 주소

2. 실행하고자 하는 함수

3. 그 함수에 전달하고자 하는 변수들

Ethereum 노드들은 JSON_RPC라고 불리는 언어로만 소통할 수 있고, 이는 사람이 읽기는 불편하다. Contract의 함수를 실행하고 싶다고 질의 보내는 것은 다음과 같이 생겼다.

```sol
// 그래... 이런 방법으로 모든 함수 호출을 잘 작성할 수 있길 빌겠네!
// 오른쪽으로 스크롤하게 ==>
{"jsonrpc":"2.0","method":"eth_sendTransaction","params":[{"from":"0xb60e8dd61c5d32be8058bb8eb970870f07233155","to":"0xd46e8dd67c5d32be8058bb8eb970870f07244567","gas":"0x76c0","gasPrice":"0x9184e72a000","value":"0x9184e72a","data":"0xd46e8dd67c5d32be8d46e8dd67c5d32be8058bb8eb970870f072445675058bb8eb970870f072445675"}],"id":1}
```

이렇게 복잡하게 실행하지 않고 `Web3.js`는 쉽게 사용하도록 해준다.

```sol
CryptoZombies.methods.createRandomZombie("Vitalik Nakamoto 🤔")
  .send({ from: "0xb60e8dd61c5d32be8058bb8eb970870f07233155", gas: "3000000" })
```

#### 시작하기

```shell
npm i web3
```

또는 github에서 간략화 된 `.js` 파일을 가져와 적용할 수 있다.

```html
<script language="javascript" type="text/javascript" src="web3.min.js"></script>
```

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <title>CryptoZombies front-end</title>
    <script
      language="javascript"
      type="text/javascript"
      src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.3.1/jquery.min.js"
    ></script>
    <!-- 여기에 web3.js를 포함하게. -->
  </head>
  <body></body>
</html>
```

### 6.2 Web3 Provider

처음 필요로 하는 것은 `Web3 Provider`이다.

Ethereum은 똑같은 데이터의 복사본을 공유하는 노드들로 구성되어 있다. Web3.js에서 Web3 Provider를 설정하는 것은 우리 코드에 읽기와 쓰기를 처리하려면 어떤 노드와 통신을 해야 하는지 설정하는 것이다. 이는 전통적인 웹 앱에서 `API` 호출을 위해 원격 웹 서버의 `URL`을 설정하는 것과 똑같다.

우리만의 Ethereum 노드를 Provider로 운영할 수 있다. 하지만 편리하게 쓸 수 있는 제 3자 서비스가 있다. DApp의 사용자들을 위해 Ethereum 노드를 운영할 필요가 없도록 하기 위해 사용할 수 있는 서비스이다 - `Infura`이다.

#### Infura

Infura는 빠른 읽기를 위한 캐시 계층을 포함하는 다수의 Ethereum 노드를 운영하는 서비스이다. 접근을 위한 API를 무료로 사용할 수 있다. Infura를 프로바이더로 사용하면, 우리만의 Ethereum을 설치하고 계속 유지할 필요 없이 Ethereum 블록체인과 메세지를 주고받을 수 있다.

다음과 같이 Web3에 Web3 Provider로 Infura를 쓰도록 설정할 수 있다.

```JS
var web3 = new Web3(new
Web3.providers.WebsocketProvider("wss://mainnet.infura.io/ws"));
```

많은 사용자들이 우리의 DApp을 사용할 것이기에 - 그리고 이 사용자들은 단순히 읽기만 하는 게 아니라 블록체인에 뭔가 쓰기도 할 것 이기에 - 우리는 이 사용자들이 그들의 개인 키로 Trasaction에 서명을 할 수 있도록 해야 한다.

{{<admonition info>}}
참고: 이더리움(그리고 일반적으로 블록체인)은 트랜잭션에 전자 서명을 하기 위해 공개/개인 키 쌍을 사용하네. 말하자면 전자 서명을 위해 엄청나게 안전한 비밀번호 같은 것이지. 이런 방식으로 내가 만약 블록체인에서 어떤 데이터를 변경하면, 나의 공개 키를 통해 내가 거기 서명을 한 사람이라고 증명할 수 있네 - 하지만 아무도 내 개인 키를 모르기 때문에, 내 트랜잭션을 누구도 위조할 수 없지.
{{</admonition>}}

이런 암호학을 실제로 구현한다는 것은 미련한 생각이다. 이런 공동/개인 키 관리를 대신 처리해주는 서비스가 바로 `Metamask`이다.

#### Metamask

Metamask는 사용자들이 Ethereum 계정과 개인 키를 안전하게 관리할 수 있게 해주는 크롬롸 파이어폭스의 브라우저 확장 프로그램이다. 그리고 해당 계정들을 써서 Web3.js를 사용하는 웹사이트들과 상호작용을 할 수 있도록 해준다.

그리고 개발자로서, 사용자들이 웹 브라우저를 써서 웹 사이트를 통해 우리의 DApp과 상호작용을 하길 원한다면, 기존에 만든 DApp을 Metamask와 호환할 수 있도록 해야 한다.

{{<admonition tip>}}
참고: 메타마스크는 내부적으로 Infura의 서버를 Web3 프로바이더로 사용하네. 위에서 우리가 했던 것처럼 말이야 - 하지만 사용자들에게 그들만의 Web3 프로바이더를 선택할 수 있는 옵션을 주기도 하지. 즉 메타마스크의 Web3 프로바이더를 사용하면, 사용자에게 선택권을 주는 것이기도 하면서 자네 앱에서 걱정할 거리를 하나 줄일 수 있지.
{{</admonition>}}

#### Metamask의 Web3 Provider 사용하기

Metamask는 `web3`라는 전역 자바스크립트 객체를 통해 브라우저에 Web3 Provider를 주입한다. 그러니 우리 앱에서는 web3가 존재하는지 확인하고, 만약 존재한다면 `web3.currentProvider`를 `Provider`로 사용하면 된다.

아래는 Metamask에서 제공하는 템플릿 코드이다. 사용자가 Metamask를 설치했는지 확인하고 설치가 안 된 경우 우리 앱을 사용하려면 설치해야 한다고 알려준다.

```sol
window.addEventListener('load', function() {

  // Web3가 브라우저에 주입되었는지 확인(Mist/MetaMask)
  if (typeof web3 !== 'undefined') {
    // Mist/MetaMask의 프로바이더 사용
    web3js = new Web3(web3.currentProvider);
  } else {
    // 사용자가 Metamask를 설치하지 않은 경우에 대해 처리
    // 사용자들에게 Metamask를 설치하라는 등의 메세지를 보여줄 것
  }

  // 이제 자네 앱을 시작하고 web3에 자유롭게 접근할 수 있네:
  startApp()

})
```

{{<admonition tip>}}
참고: 메타마스크 말고도 사용자들이 쓸 수 있는 다른 개인 키 관리 프로그램도 있네. 미스트(Mist) 웹 브라우저 같은 것들이지. 하지만, 그것들도 모두 web3 변수를 주입하는 동일한 형태를 사용하네. 그러니 사용자들이 다른 프로그램을 쓰더라도 여기서 우리가 설명하는 방식으로 사용자의 Web3 프로바이더를 인식할 수 있을 것이네.
{{</admonition>}}

### 6.3 Contract와 대화하기

이제 Metamask의 Web3 Provider로 Web3.js를 초기화했으니, 우리의 Smart Contract와 통신을 할 수 있도록 설정해준다.

Web3.js는 우리의 Smart Contract와 통신하기 위해 2가지를 필요로 한다.

1. Contract Address

2. ABI

#### Contract address

Smart Contract를 모두 작성한 후, 우리는 그걸 컴파일한 후 Ethereum에 배포할 것이다.

Contract를 배포한 후, 해당 Contract는 영원히 존재하는, Ethereum 상에서 고정된 주소를 얻는다. 예를 들어 `0x06012c8cf97BEaD5deAe237070F9587f8E7A266d`이다.

#### Contract ABI

`ABI`는 Application Binary Interface의 줄임말이다. 기본적으로 JSON 형태로 Contract의 메소드를 표현하는 것이다. 우리 Contract가 이해할 수 있도록 하려면 Web3.js가 어떤 형태로 함수 호출을 해야 하는지 알려준다.

Ethereum에 배포하기 위해 Contract를 컴파일할 때, Solidity 컴파일러가 우리에게 ABI를 줄 것이다. 그러니 Contract address 와 Contract ABI를 저장하고 사용해야 한다.

#### Web3.js Contract 인스턴스화하기

Contract의 Address와 ABI를 얻고나면, 우리는 다음과 같이 Web3에서 인스턴스화(객체화)할 수 있다.

```sol
// myContract 인스턴스화
var myContract = new web3js.eth.Contract(myABI, myContractAddress);
```

