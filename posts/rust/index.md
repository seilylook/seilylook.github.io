# Rust


`Rust`: Rust는 시스템 프로그래밍 언어로서, 안전성, 속도, 병행성(Concurrency)을 중요한 목표로 개발된 언어입니다. Mozilla에서 개발한 Rust는 C와 C++과 같은 언어의 잠재적인 문제를 극복하고자 설계되었습니다. Rust는 메모리 안전성을 강조하며, 코드의 버그와 런타임 에러를 최소화하고 안전한 병행성을 제공하기 위한 다양한 기능을 제공합니다.

# Rust

> https://www.rust-lang.org/

## 1. 시작

### 1.1 설치하기

Rust는 rustup이라고 하는 러스트 버전 및 관련 도구들을 관리하기 위한 커맨드 라인 도구를 통해 러스트를 다운받을 수 있다.

#### Linux && MacOS에서 Rustup 설치

```shell
$ curl https://sh.rustup.rs -sSf | sh
```

올바로 설치됐다면

```
Rust is installed now. Great!
```

이 명령어는 스크립트를 다운로드하고 rustup 도구의 설치를 시작하는데, 이 도구는 가장 최신 버전의 러스트 안정화 버전을 설치해준다.

#### Window에서 Rustup 설치

윈도우는 다음 링크로 이동해서 설명대로 설치하면 된다.

> https://www.rust-lang.org/en-US/install.html

### 1.2 Hello world

#### 프로젝트 생성

```shell
mkdir rust
cd rust

mkdir hello_world
cd hello_world
```

#### Rust 프로그램을 작성하고 실행

다음으로, main.rs라 불리는 새로운 소스 파일을 만들어준다. 러스트 파일들은 언제나 .rs 확장자로 끝난다.

방금 만든 main.rs를 열고 다음 코드를 넣어준다.

Filenamee: main.rs

```code
fn main() {
    println!('Hello world');
}
```

{{<admonition note 주의>}}
다른 언어와 다르게 println + '!'
느낌표를 꼭 넣어줘야 한다.
{{</admonition>}}

##### Hello world 출력

파일을 저장하고, VS code의 터미널을 켜서 다음 명령어를 입력한다.

```shell
rustrc main.rs

./main

=> Hello, world!
```

#### Rust 프로그램 해부하기

코드의 결과값을 확인했으니, 어떻게 동작이 수행되었는지 확인해 보아야 한다.

```
fn main() {

}
```

이 라인들은 러스트의 `함수(function)`를 정의한다. main 함수는 특별하다. 이것은 모든 실행가능한 러스트 프로그램 내에서 첫번째로 실행되는 코드이다. 첫번째 라인은 파라미터가 없고 아무것도 반환하지 않는 main이라는 이름의 함수를 정의한다. 만일 파라미터가 있었ㄷ다면, 파라미터들이 `()` 내에 존재했을 것이다.

`println!`은 러스트 매크로라고 불린다. 만일 대신에 함수라고 불리려면, (! 없이) println으로 입력되어야 할 것이다.

#### 컴파일과 실행은 개별적인 단계이다.

이제 막 새로 만든 프로그램을 실행했으므로, 이 과정의 각 단계를 검토할 필요가 있다.

러스트 프로그램을 실행하기 전에, 우리는 아래와 같이 rustc 커맨드를 입력하고 여기에 우리의 소스코드를 넘기는 식으로 러스트 컴파일러를 사용해 컴파일해야 한다.

```shell
rustc main.rs
```

이러 동작방식은 C, C++ 과 비슷하다. 명령어를 수행하고 나면 다음의 결과가 나타난다.

```shell
ls

=> main main.rs
```

루비, 파이썬, 자바스크립트와 같은 동적 언어에 더 친숙하다면, 아마도 프로그램의 컴파일과 실행을 개별적인 단계로 이용하지 않았을 수도 있다.

러스트는 `ahead-of-time compiled` 언어인데, 이는 프로그램을 컴파일하고, 그 실행파일을 다른 사람에게 주면, 그들은 러스트를 설치하지 않고도 이를 실행할 수 있다는 의미이다.

기존 동적 언어들은 py, js 파일을 전달할 때, 받는 사람이 해당 구현체가 설치되어 있어야 한다. 물론 설치만 되어있다면 하나의 커맨드로 프로그램을 컴파일하고 실행할 수 있다.

### 1.3 Hello, Cargo

Cargo는 러스트의 빌드 시스템 및 패키지 매니저이다. 기존에 많이 사용하던 npm, pnpm과 같다고 할 수 있다.

카고는 코드 빌드, 라이브러리 다운로드, 라이브러리 빌드 등 많은 작업을 편리하게 자동으로 수행해준다.

#### Cargo를 사용해 프로젝트 생성

```shell
cargo new hello_cargo --bin

cd hello_cargo
```

첫번째 커맨드는 hello_cargo라는 새로운 실행 가능한 바이너리를 생성한다. cargo new에게 넘겨지는 --bin 인자가 라이브러리가 아닌 실행 가능한 애플리케이션으로 만들어준다.

hello_cargo 디렉토리로 가서 파일 리스트를 보면, 다음과 같다.

```
src / main.rs

Cargo.toml
```

Filename: Cargo.toml

```
[package]
name = "hello_cargo"
version = "0.1.0"
edition = "2021"

# See more keys and their definitions at https://doc.rust-lang.org/cargo/reference/manifest.html

[dependencies]

```

Filename: src/main.rs

```
fn main() {
    println!("Hello, world!");
}
```

Cargo는 우리가 작성했던 것과 똑같이 우리를 위해 `Hello, world!` 프로그램을 작성해주었다. 여기까지 우리의 이전 프로젝트와 카고가 만든 프로젝트의 차이점은
카고가 코드를 src 디렉토리 안에 위치시킨다는 점이다. 그리고 최상위 디렉토리에 Cargo.toml 환경 설정 파일을 추가한 점이다.

Cargo는 우리의 소스 파일들이 src 디렉토리 안에 있을 것이라 예상한다. 최상위 프로젝트 디렉토리는 그저 README.md 파일, 라이센스 정보, 환경 파일들(env 파일)이 있다.

#### Cargo 프로젝트를 빌드하고 실행

이제 Cargo로 만든 `Hello, world!` 프로젝트를 빌드하고 실행할 때의 차이점을 살펴보자. 다음 명령어를 입력해준다.

```shell
cargo build
```

이 커맨드는 현재 디렉토리 대신 target/debug/hello_cargo에 실행파일을 생성한다. 아래 커맨드를 통해 실행 파일을 실행시킬 수 있다.

```shell
./target/debug/hello_cargo # or .\target\debug\hello_cargo.exe on Windows

=> Hello, world!
```

모든 것이 잘 진행됐다면, 터미널에 hello, world!가 출력된다. 처음 실행한 `cargo build` 를 통해 Cargo.lock가 생성된다.

우리는 그저 `cargo build`로 프로젝트를 빌드하고 `./taget/debug/hello_cargo` 로 이를 실행했지만,

`cargo run` 커맨드를 통해 단 한번으로 컴파일한 다음 결과 실행 파일을 샐행할 수 있다.

```shell
cargo run

    Finished dev [unoptimized + debuginfo] target(s) in 0.01s
     Running `target/debug/hello_cargo`

Hello, world!
```

{{<admonition note 주의>}}
이번에는 Cargo가 hello_cargo를 컴파일하는 중이었다는 것을 나타내는 출력을 볼 수 없음을 주목해야 한다. Cargo는 파일들이 변경된 적이 없다는 것을 알아채고, 해당 바이너리를 그저 실행만 한다.
{{</admonition>}}

Cargo는 또한 `cargo check` 라는 커맨드를 제공한다. 이 커맨드는 코드가 컴파일되는지를 빠르게 확인해주지만 실행 파일을 생성하지는 않는다.

```shell
cargo check
    Checking hello_cargo v0.1.0 (/Users/seilylook/Development/study/Rust/hello_cargo)
    Finished dev [unoptimized + debuginfo] target(s) in 0.72s
```

코드를 작성하는 동안 계속해서 작업물을 검사하고 싶다면, `cargo check` 를 사용해 속도를 높일 수 있다.

지금까지 배운 것을 정리하자면,

- [x] 우리는 `cargo build` 나 `cargo check` 를 사용해 프로젝트를 빌드할 수 있다.
- [x] 우리는 `cargo run` 을 사용해 단숨에 프로젝트를 빌드하고 실행할 수 있다.
- [x] 우리 코드가 있는 동일한 디렉토리에 빌드의 결과물이 저장되는 대신, Cargo는 이를 target/debug 디렉토리에 저장한다.

Cargo를 사용하면 생기는 추가적인 이점은 어떠한 운영체제로 작업을 하든 상관 없이 커맨드들이 동일한 것이다.

#### 배포

프로젝트가 마침내 배포를 위한 준비가 됐다면, `cargo build --release` 를 사용해 최적화와 함께 이를 커파일 할 수 있다. 이 커맨드는 taget/debug 대신 target/release에 실행파일을 생성한다.

최적화는 러스트 코드를 더 빠르게 만들어주지만, 최적화를 켜는 것은 프로그램을 컴파일하는덷 드는 시간을 길게 할 수 있다.

이것이 바로 두 개의 서로 다른 프로파일이 있는 이유이다. 하나는 빠르게 그리고 자주 다시 빌드하기를 원하는 개발용, 다른 하나는 반복적으로 다시 빌드를 할 필요 없고 가능한 빠르게 실행되어 사용자들에게 제공할 최종 프포그램을 빌드하기 위한 용도이다.

## 2. 개념

### 2.1 변수와 가변성

기본 변수는 불변성이다. 이것은 Rust가 제공하는 안전성과 손쉬운 동시성이라는 장점을 취할 수 있도록 코드를 작성하게끔 강제하는 요소 중 하나이다.

변수가 불변성일 경우, 일단 값이 이름에 bound 되면 해당 값을 변경할 수 없다. 시험 삼아 `cargo new --bin variables`를 실행해서 새 프로젝트를 생성해본다. 그런 다음 VScode를 열어 다음과 같이 수정해준다.

```
fn main() {
    let x = 5;
    println!("The value of x is: {}", x);
    x = 6;
    println!("The value of x is: {}", x);
}
```

저장하고 `cargo run`명령을 통해 실행시켜 보면, 다음과 같은 에러가 발생할 것이다.

```shell
error[E0384]: re-assignment of immutable variable `x`
 --> src/main.rs:4:5
  |
2 |     let x = 5;
  |         - first assignment to `x`
3 |     println!("The value of x is: {}", x);
4 |     x = 6;
  |     ^^^^^ re-assignment of immutable variable

```

이 에러가 발생하는 이유는 `불변성 변수에 재할당`이고, 원인은 변수 `x`에 값을 새로 정의했기 때문이다.

이전에 불변성으로 선언한 것의 값을 변경하고자 하는 시도를 하면 컴파일 타임의 에러를 얻게 되고 이로 인해 버그가 발생할 수 있기 때문에 중요하다. 만약 우리 코드의 일부는 값이 변경되지 않는다는 것을 가정하는데 다른 코드는 이와 다르게 값을 변경한다면, 전자에 해당하는 코드는 우리가 의도한 대로 수행되지 않을 수 있다.

Rust에서는 컴파일러가 변경되지 않은 값에 대한 보증을 해주고, 실제로 이는 바뀌지 않는다. 이것이 의미하는 바는 코드를 작성하거나 분석할 시에 변수의 값이 어떻게 변경되는지 추적할 필요가 없이 때문에 코드의 안정성을 높여준다.

하지만 때로는 변해야 되는 변수를 사용해야 될 때도 있기 때문에 `mut`을 추가하는 것을 통해 가변성 변수를 선언할 수 있다. 다음과 같이 사용할 수 있다.

```
fn main() {
    let mut x = 5;
    println!("The value of x is: {}", x);
    x = 6;
    println!("The value of x is: {}", x);
}
```

위의 코드로 바꾸면 다음의 결과를 확인할 수 있다.

```shell
$ cargo run
   Compiling variables v0.1.0 (file:///projects/variables)
    Finished dev [unoptimized + debuginfo] target(s) in 0.30 secs
     Running `target/debug/variables`
The value of x is: 5
The value of x is: 6
```

가변성 변수를 사용할 좋은 경우는 다음과 같다. 예를 들어, 대규모 데이터 구조체를 다루는 경우 가변한 인스턴스를 사용하는 것이 새로 인스턴스를 할당하고 반한하는 것보다 빠를 수 있다.

이는 반대로 데이터 규모가 작다면 새 인스턴스를 생성하고 함수적 프로그래밍 스타일로 작성하는 것이 더 합리적이라 할 수 있다.

#### 변수와 상수 간의 차이점들

변수의 값을 변경할 수 없는 사항이 다른 언어가 가진 프로그래밍 개념을 떠오르게 한다. `상수` 불변성 변수와 마찬가지로 상수 또한 이름으로 bound 된 후에는 값의 변경이 허용되지 않지만, 상수와 변수는 조금 다르다.

첫째, 상수에 대해서는 `mut`을 사용하는 것이 허용되지 않는다. 상수는 기본 설정이 불변성이 아니라 불변성 그 자체이다.

우리가 상수를 사용하고자 한다면 let 키워드 대신 const 키워드를 사용해야 하고, 값의 유형을 선언해야 한다.

상수는 전체 영역을 포함해 어떤 영역에서도 선언될 수 있다. 이는 코드의 많은 부분에서 사용될 필요가 있는 값을 다루는데 유용하다. `ex) PUBLIC_BASE_URL=https://example.com`

#### shadowing

이전에 선언한 변수와 같은 이름의 새 변수를 선언할 수 있고, 새 변수는 이전 변수를 `shadows`하게 된다. 해당 변수명은 두 번째 변수의 값을 갖게 된다는 뜻이다. let 키워드를 사용해 다음처럼 반복해 같은 변수명으로 shadow 할 수 있다.

```
fn main() {
    let x = 5;

    let x = x + 1;

    let x = x * 2;

    println!("The value of x is: {}", x);
}
```

이 프로그램은 처음 `x`에 값 5를 bind 한다. 이후 반복된 `let x = `구문으로 `x`를 shadow하고 원본 값에 `1`을 더해 `x`의 값은 `6`이 된다. 세번째 `let`문으로 또 `x`를 shadow하고, 이전 값에 `2`를 곱해 `x`의 최종값은 `12`가 된다. 프로그램을 실행하면 결과값이 다음과 같다.

```
$ cargo run
   Compiling variables v0.1.0 (file:///projects/variables)
    Finished dev [unoptimized + debuginfo] target(s) in 0.31 secs
     Running `target/debug/variables`
The value of x is: 12
```

이와 같은 사용은 변수를 `mut`으로 선언하는 것과는 차이가 있다. 왜냐면 `let` 키워드를 사용하지 않고 변수에 새로 값을 대입하려고 하면 컴파일-시에 에러를 얻게 되기 때문이다. 우리가 몇 번 값을 변경할 수 있지만 그 이후에 변수는 불변성을 갖게 된다.

또 다른 `mut`과 `shadowing`의 차이는 `let` 키워드를 다시 사용해 효과적으로 새 변수를 선언하고, 값의 유형을 변경할 수 있으면서도 동일 이름을 사용할 수 있다는 점 이다. 예를 들어, 공백 문자들을 입력받아 공백 문자의 길이를 보여주고자 할 때, 실제로 저장하고자 하는 것은 공백의 개수이다.

```
let spaces = "   ";
let spaces = spaces.len();
```

이런 구조가 허용되는 이유는 첫 `spaces` 변수가 문자열 유형이고 두번째 `spaces` 변수는 첫 번째 것과 동일한 이름을 가진 새롭게 정의된 숫자 유형의 변수이기 때문이다.

`Shadowing`은 `space_str`이나 `space_num`과 같이 대체된 이름을 사용하는 대신 간단히 `spaces` 이름을 사용할 수 있게 해준다.

그러나 `mut`를 사용하려고 한다면

```
let mut spaces = "   ";
spaces = spaces.len();
```

다음과 같은 에러가 발생한다.

```shell
error[E0308]: mismatched types
 --> src/main.rs:3:14
  |
3 |     spaces = spaces.len();
  |              ^^^^^^^^^^^^ expected &str, found usize
  |
  = note: expected type `&str`
             found type `usize`

```

### 2.2 데이터 타입들

Rust에서 사용되는 모든 값들은 어떤 타입을 갖습니다. 그러니 어떤 형태의 데이터인지 명시하여 Rust에게 알려줘서 이를 통해 데이터를 어떻게 다룰지 알 수 있도록 해야 합니다.

이번 장의 전체에 걸쳐 주지해야 할 점은 Rust는 타입이 고정된 언어라는 점 입니다. 이게 의미하는 바는 모든 변수의 타입이 컴파일 시에 반드시 정해져 있어야 한다는 겁니다. 보통 컴파일러는 우리가 값을 사용하는 지에 따라 타입을 추측할 수 있습니다. 2장에서 `String`을 `parse`를 사용하여 숫자로 변환했던 경우처럼 타입의 선택 폭이 넓은 경우는 반드시 타입의 명시를 첨가해야 합니다. 다음처럼:

```
let guess: u32 = "42".parse().expect("Not a number!");
```

여기에 타입 명시를 첨가하지 않은 경우, Rust는 다음과 같은 에러를 발생시킵니다.

```
error[E0282]: type annotations needed
 --> src/main.rs:2:9
  |
2 |     let guess = "42".parse().expect("Not a number!");
  |         ^^^^^
  |         cannot infer type for `_`
  |         consider giving `guess` a type
```

#### 스칼라 타입들

스칼라는 하나의 값으로 표현되는 타입입니다. Rust는 정수형, 부동소수점 숫자, boolean, 그리고 문자, 네 가지 스칼라 타입을 보유하고 있습니다.

#### 복합 타입들

복합 타입들은 다른 타입의 다양한 값들을 하나의 타입으로 묶을 수 있습니다. Rust는 두 개의 기본 타입들을 갖고 있습니다: 튜플과 배열.

##### 값들을 집합시켜서 튜플화하기

튜플은 다양한 타입의 몇 개의 숫자를 집합시켜 하나의 복합 타입으로 만드는 일반적인 방법입니다.

우리는 괄호 안에 콤마로 구분되는 값들의 목록을 작성하여 튜플을 만듭니다. 튜플에 포함되는 각 값의 타입이 동일할 필요없이 서로 달라도 됩니다. 다음의 예제에 우리는 선택 사항인 타입 명시를 추가했습니다.

Filename: src/main.rs

```
fn main() {
    let tup: (i32, f64, u8) = (500, 6.4, 1);
}
```

튜플은 단일 요소를 위한 복합계로 고려되었기에 변수 `tup`에는 튜플 전체가 bind 됩니다. 개별 값을 튜플의 밖으로 빼내오기 위해서는, 패턴 매칭을 사용하여 튜플의 값을 구조해체 시키면 됩니다. 다음을 봅시다:

Filename: src/main.rs

```
fn main() {
    let tup = (500, 6.4, 1);

    let (x, y, z) = tup;

    println!("The value of y is: {}", y);
}
```

해당 프로그램은 처음에 튜플을 만들고 변수 `tup`에 bind 시킵니다. 이후 패턴과 `let`을 통해 `tup`을 세개의 분리된 변수 `x`, `y`, 그리고 `z`에 이동시킵니다. 이것을 `구조해체`라고 부르는 이유는 하나의 튜플을 세 부분으로 나누기 때문입니다. 최종적으로 프로그램은 `y`의 값을 출력할 것이고 이는 6.4입니다.

패턴 매칭을 통한 `구조해체`에 추가로, 우리는 마침표(.) 뒤에 우리가 접근하길 원하는 값의 색인을 넣는 것을 통해 튜플의 요소에 직접적으로 접근할 수 있습니다. 예제를 봅시다:

Filename: src/main.rs

```
fn main() {
    let x: (i32, f64, u8) = (500, 6.4, 1);

    let five_hundred = x.0;

    let six_point_four = x.1;

    let one = x.2;
}
```

##### 배열

여러 값들의 집합체를 만드는 다른 방법은 배열입니다. 튜플과는 다르게, 배열의 모든 요소는 모두 같은 타입이여야 합니다. Rust의 배열이 몇 다른 언어들의 배열과 다른 점은 Rust에서는 배열은 고정된 길이를 갖는다는 점입니다: 한번 선언되면, 이들은 크기는 커지거나 작아지지 않습니다.

Rust에서는 대괄호 안에 값들을 콤마로 구분하여 나열해서 배열을 만듭니다:

```
fn main() {
    let a = [1, 2, 3, 4, 5];
}
```

배열이 유용할 때는 당신의 데이터를 heap보다 stack에 할당하는 것을 원하거나(stack 과 heap에 대해서는 4장에서 다루게 될 것입니다), 당신이 항상 고정된 숫자의 요소를 갖는다고 확신하고 싶을 때입니다. 이들은 벡터 타입처럼 가변적이지 않습니다. 벡터 타입은 유사 집합체로 표준 라이브러리에서 제공되며 확장 혹은 축소가 가능합니다. 배열이나 벡터 중에 뭘 선택해야 할지 확실하지 않은 상황이라면 벡터를 사용하도록 하세요. 8장에서 벡터에 대해 더 자세히 다룹니다.

벡터가 아닌 배열을 선택하게 되는 경우의 예로, 프로그램이 올해의 달 이름을 알고자 할 경우입니다. 프로그램이 달을 추가하거나 삭제하는 경우는 거의 없을 것이므로, 고정적으로 12개의 아이템을 가질테니 배열을 사용하면 됩니다.

배열의 접근은 다른 언어들과 마찬가지로 접근하면 된다.

```
fn main() {
    let a = [1, 2, 3, 4, 5];

    let first = a[0];
    let second = a[1];
}
```

