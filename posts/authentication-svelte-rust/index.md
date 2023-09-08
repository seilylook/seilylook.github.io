# Authentication Svelte Rust


# Introduction

`Svelte`와 `Rust`를 사용해서 사용자 인증 시스템을 구현한 프로젝트.

## Tech stack

- Front-end

  - `Sveltekit`

  - `Typescript`

  - `tailwindcss`

  - `vite`

  - `pnpm`

- Back-end

  - `Actix-web`: Rust 전용 웹 프레임워크

  - `tokio`: Rust 전용 비동기 프레임워크

  - `serde`: Rust 데이터 구조에 대한 직렬화, 역직렬화를 제공하는 라이브러리

  - `minijinja`: 템플릿 엔진

  - `SQLx`: SQL 비동기 도구

  - `PostgreSQL`: 데이터베이스

  - `Redis`: 토큰 만료 등을 도와주는 라이브러리

## 1. 시작

### 1.1 프로젝트 생성

```shell
cd Rust

mkdir auth-svelte-rust

cd auth-svelte-rust

cargo new backend
```

`cd backend`를 통해 들어가서 `Cargo.toml`에 다음 코드를 삽입해준다.

```toml
# Cargo.toml

[package]
name = "backend"
version = "0.1.0"
authors = "seilylook"
edition = "2021"

[lib]
path = "src/lib.rs"

[[bin]]
path = "src/main.rs"
name = "backend"

[dependencies]
actix-web = "4"
config = { version = "0.13.3", features = ["yaml"] }
dotenv = "0.15.0"
serde = "1.0.160"
tokio = { version = "1.27.0", features = ["macros", "rt-multi-thread"] }
tracing = "0.1.37"
tracing-subscriber = { version = "0.3.17", features = [
    "fmt",
    "std",
    "env-filter",
    "registry",
    'json',
    'tracing-log',
] }
```

먼저 프로젝트의 `lib.rs` 경로를 가리키는 `[lib]`을 설정해준다. 한 개의 프로젝트에서 오직 1개의 `lib.rs`파일만 존재할 수 있다.

다음은 바이너리 세그먼트인 `[[bin]]`이다. 이 중 대괄호는 `toml`에서 배열을 의미한다. Rust 프로젝트에는 두개 이상의 바이너리 패키지가 있을 수 있기 때문에 사용되었다.

이 두 가지 새로운 새그먼트를 사용하면 테스트가 사용된 웹 프레임워크와 독립적으로 통합된 테스트를 쉽게 작성할 수 있다.

`[dependency]` 에서 `tracing`은 다음을 위해 사용되었다. 런타임 시 또는 애플리케이션 배포 단계에 있을 때 요청과 응답에 대해 기록해야 한다. 때때로 사용자가 불만을 제기하거나 에러가 발생할 경우, 우리는 왜 로그를 확인해야 문제를 해결할 수 있다. 즉 애플리케이션을 디버깅하려면 참조 지점이 필요하다. Rust 생태계에서는 `tracing`, `tracing-subscriber`가 널리 사용된다.

### 1.2 프로젝트 구축

```shell
touch src/lib.rs src/startup.rs src/settings.rs src/telemetry.rs

mkdir src/routes && touch src/routes/mod.rs src/routes/health.rs
```

#### src/lib.rs

```Rust
// src/lib.rs

pub mod routes;
pub mod settings;
pub mod startup;
pub mod telemetry;
```

생성된 파일과 폴더를 인식하려면 `lib.rs`에서 모듈화 해줘야 한다.

#### src/telemetry.rs

```Rust
// src/telemetry.rs

use tracing_subscriber::layer::SubscriberExt;

pub fn get_subscriber(debug: bool) -> impl tracing::Subscriber + Send + Sync {
    let env_filter = if debug {
        "trace".to_string()
    } else {
        "info".to_string()
    };
    let env_filter = tracing_subscriber::EnvFilter::try_from_default_env()
        .unwrap_or_else(|_| tracing_subscriber::EnvFilter::new(env_filter));

    let stdout_log = tracing_subscriber::fmt::layer().pretty();
    let subscriber = tracing_subscriber::Registry::default()
        .with(env_filter)
        .with(stdout_log);

    let json_log = if !debug {
        let json_log = tracing_subscriber::fmt::layer().json();
        Some(json_log)
    } else {
        None
    };

    let subscriber = subscriber.with(json_log);

    subscriber
}

pub fn init_subscriber(subscriber: impl tracing::Subscriber + Send + Sync) {
    tracing::subscriber::set_global_default(subscriber).expect("Failed to set subscriber");
}
```

1. `get_subscriber`: 이 함수는 tracing 라이브러리에서 사용할 로깅 구독자를 생성하고 반환한다.

- 먼저, `env_filter` 변수에 디버그 모드에 따라 환경 필터 문자열을 설정한다. 환경 필터는 로그 레벨을 제어하는데 사용된다.

- `tracing_subscriber::EnvFilter::try_from_default_env()`를 호출해서 환경 변수에서 환경 필터를 읽어오려 시도한다. 이것은 환경 변수 `RUST_LOG`를 기반으로 설정된 로그 레벨을 가져올 수 있다. 만약 실패하면 기본으로 설정한 `env_filter`를 사용한다.

- 로그를 콘솔에 출력하기 위해 `stdout_log` 변수에 트레이싱 포맷 레이어 `tracing_subscriber::fmt::layer()`를 추가합니다.

- `tracing_subscriber::Registry::default()`를 사용하여 기본 로깅 구독자 레지스트리를 생성하고, 이를 `env_filter` 및 `stdout_log`와 함께 구성합니다.

- 디버그 모드가 아닌 경우, JSON 형식으로 로그를 출력하기 위한 json_log를 설정하고 로깅 구독자에 추가합니다.

- 최종적으로 구성된 로깅 구독자를 반환합니다.

2. `init_subscriber`: 이 함수는 앞서 생성한 로깅 구독자를 전달받아 전역 default로 설정한다. 이 함수는 애플리케이션 초기화 단계에서 호출되며, 로깅을 사용할 수 있게 한다.

- `tracing::subscriber::set_global_default()` 함수를 사용하여 구독자를 전역 디폴트로 설정합니다.

#### src/settings.rs

```Rust
// src/settings.rs

#[derive(serde::Deserialize, Clone)]
pub struct Settings {
    pub application: ApplicationSettings,
    pub debug: bool,
}

#[derive(serde::Deserialize, Clone)]
pub struct ApplicationSettings {
    pub port: u16,
    pub host: String,
    pub base_url: String,
    pub protocol: String,
}

pub enum Environment {
    Development,
    Production,
}

impl Environment {
    pub fn as_str(&self) -> &'static str {
        match self {
            Environment::Development => "development",
            Environment::Production => "production",
        }
    }
}

impl TryFrom<String> for Environment {
    type Error = String;

    fn try_from(s: String) -> Result<Self, Self::Error> {
        match s.to_lowercase().as_str() {
            "development" => Ok(Self::Development),
            "production" => Ok(Self::Production),
            other => Err(format!(
                "{} is not a supported environment. Use either `development` or `production`.",
                other
            )),
        }
    }
}

pub fn get_settings() -> Result<Settings, config::ConfigError> {
    let base_path = std::env::current_dir().expect("Failed to determine the current directory");
    let settings_directory = base_path.join("settings");

    let environment: Environment = std::env::var("APP_ENVIRONMENT")
        .unwrap_or_else(|_| "development".into())
        .try_into()
        .expect("Failed to parse APP_ENVIRONMENT.");
    let environment_filename = format!("{}.yaml", environment.as_str());
    let settings = config::Config::builder()
        .add_source(config::File::from(settings_directory.join("base.yaml")))
        .add_source(config::File::from(
            settings_directory.join(environment_filename),
        ))
        .add_source(
            config::Environment::with_prefix("APP")
                .prefix_separator("_")
                .separator("__"),
        )
        .build()?;

    settings.try_deserialize::<Settings>()
}
```

`get_settings`: 애플리케이션이 현재 실행 중인 환경을 감지하는 데 도움을 주는 다용도 함수이다. 이 함수는 `APP_ENVIROMENT`환경 변술를 사용해 실행 환경을 확인한다. 환경을 감지한 후, 적절한 `.yaml`파일을 로드하고 해당 `.yaml`파일에 설정된 내용을 재정의하는 환경 변수를 로드한다.

```shell
mkdir settings && touch settings/base.yaml settings/development.yaml settings/production.yaml
```

```yaml
# settings/base.yaml
application:
  port: 5000
```

```yaml
# settings/development.yaml

application:
  protocol: http
  host: 127.0.0.1
  base_url: "http://127.0.0.1"

debug: true
```

```yaml
# settings/production.yaml

application:
  protocol: https
  host: 0.0.0.0
  base_url: ""

debug: false
```

#### src/startup.rs

```Rust
pub struct Application {
    port: u16,
    server: actix_web::dev::Server,
}

impl Application {
    pub async fn build(settings: crate::settings::Settings) -> Result<Self, std::io::Error> {
        let address = format!(
            "{}:{}",
            settings.application.host, settings.application.port
        );

        let listener = std::net::TcpListener::bind(&address)?;
        let port = listener.local_addr().unwrap().port();
        let server = run(listener).await?;

        Ok(Self { port, server })
    }

    pub fn port(&self) -> u16 {
        self.port
    }

    pub async fn run_until_stopped(self) -> Result<(), std::io::Error> {
        self.server.await
    }
}

async fn run(listener: std::net::TcpListener) -> Result<actix_web::dev::Server, std::io::Error> {
    let server = actix_web::HttpServer::new(move || {
        actix_web::App::new().service(crate::routes::health_check)
    })
    .listen(listener)?
    .run();

    Ok(server)
}
```

전체 애플리케이션을 시작하고 구조체 `Application`의 메소드`run_until_stopped`에서 끝납니다. 이렇게 작성하는 이유는 테스트에 용이하기 때문입니다.

#### src/main.rs

```Rust
// src/main.rs

#[tokio::main]
async fn main() -> std::io::Result<()> {
    dotenv::dotenv().ok();

    let settings = backend::settings::get_settings().expect("Failed to read settings.");

    let subscriber = backend::telemetry::get_subscriber(settings.clone().debug);
    backend::telemetry::init_subscriber(subscriber);

    let application = backend::startup::Application::build(settings).await?;

    tracing::event!(target: "backend", tracing::Level::INFO, "Listening on http://127.0.0.1:{}/", application.port());

    application.run_until_stopped().await?;
    Ok(())
}
```

Rust 애플리케이션의 진입점이다. `#[tokio::main]`런타임을 선택했다. 대신 `#[actix_web::main]`을 사용할 수도 있다. 그런 다음 `dotenv`를 사용해 `.env`파일에 있는 모든 환경 변수를 로드하는 데 도움을 주었다. 그런 다음 `src/settings.rs`에 작성된대로 설정을 가져온다. `Telemetry(성능 모니터링)`가 초기화되었다.

전체 앱은 빌드되었고, 이후에 실행되기 전에 앱이 실행될 포트를 개발자에게 알려주기 위해 `tracing::evnet`매크로를 사용한다. 이 포트 정보를 얻을 수 있었던 이유는 `src/startup.rs`에서 이를 사용할 수 있도록 만들었기 때문이다. 이렇게 하면 이 시리즈 동안 이 파일은 `src/main.rs`를 다시 건드릴 필요가 없다. 우리의 접촉 지점은 `src/startup.rs`가 될 것이다.

#### src/routes/health.rs

```Rust
// src/routes/health.rs

#[tracing::instrument]
#[actix_web::get("/health-check/")]
pub async fn health_check() -> actix_web::HttpResponse {
    tracing::event!(target: "backend", tracing::Level::DEBUG, "Accessing health-check endpoint.");
    actix_web::HttpResponse::Ok().json("Application is safe and healthy.")
}
```

온라인 상태인지 여부를 확인하는 간단한 엔드포인트가 있습니다. `actix-web`에서 API 엔드포인트를 작성하는 것이 얼마나 쉬운지 확인할 수 있습니다. 계측 외에도 단 3줄의 코드로 "완전히 작동하는" GET 요청 엔드포인트를 연결할 수 있습니다.

엔드포인트를 살펴보면 `#[tracing::instrument]`모든 요청의 로그를 이 기능에 보관하는데 도움을 준다.

그런 다음 `#[actix-web::get("/health-check/")]`를 사용해 오직 `GET` 요청만 받을 수 있도록 강제해준다. actix-web을 사용하는 이유 중 하나는 비동기 기능에 대한 기본 자원과 매우 빠르다는 사실 때문이다. 우리는 함수를 비동기식으로 만들었다.

다음으로, 이 메서드를 사용할 수 있도록(모듈화 시켜주기)해준다.

#### src/routs/mod.rs

```Rust
// src/routes/mod.rs

mod health;

pub use health::health_check;
```

이렇게 작성하고나면 `src/startup.rs`의 `crate::routes::health_check`에서 액세스해서 사용할 수 있다.

## 2. DB 및 Redis config

### 2.1 모듈 `users`에 하위 모듈 만들기 `routes`

