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

