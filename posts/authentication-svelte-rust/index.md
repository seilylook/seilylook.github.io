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

### 2.1 모듈 `routes`에 하위모듈 `users` 만들기

```Shell
mkdir src/routes/users && touch src/routes/users/mod.rs src/routes/users/register.rs
```

```Rust
// src/routes/users/mod.rs

mod register;
```

```Rust
// src/routes/mod.rs

mod users;
```

### 2.2 데이터베이스 연결 종속성 설치 및 설정

`SQLx`를 사용해 데이터베이스와 비동기적으로 상호 작용하도록 만들어 줄 것이다. 먼저 `SQLx`를 설치해준다.

{{<admonition note SQLx-cli>}}
sqlx 명령어를 실행하기 위해서는 sqlx-cli를 설치해주어야 한다.

```Shell
# supports all databases supported by SQLx
$ cargo install sqlx-cli

# only for postgres
$ cargo install sqlx-cli --no-default-features --features native-tls,postgres

# use vendored OpenSSL (build from source)
$ cargo install sqlx-cli --features openssl-vendored

# use Rustls rather than OpenSSL (be sure to add the features for the databases you intend to use!)
$ cargo install sqlx-cli --no-default-features --features rustls
```

{{</admonition>}}

```Shell
~/rust-auth/backend$ cargo add sqlx --features runtime-actix-rustls,postgres,uuid,chrono,migrate
```

- `runtime-actix-rustls`: actix-web 전용

- `chorono`: 날짜 및 시간에 사용

앞으로 몇개의 SQL 테이블을 migration 해 볼 것이다. 시작하기 앞서, `migrations` 폴더를 루트 디렉터리에 생성해준다.

migration을 진행할때마다, 이 폴더를 참조할 것이다.

```Shell
mkdir migrations
```

이제 `SQLx CLI`를 사용해서 테이블들에 대한 `.sql` 파일들을 `migrations` 폴더에 생성할 수 있다.

```Shell
~/rust-auth/backend$ sqlx migrate add -r users_table
```

성공적으로 `.sql` 파일이 2개 생성된 것을 확인할 수 있다.

#### 데이터 베이스 연결을 위한 설정 추가하기

```YAML
# settings/base.yaml
application:
  port: 5000

database:
  username: "seilylook"
  password: "<your_db_password>"
  port: 5432
  host: "localhost"
  database_name: "rust_auth_db_dev"
  require_ssl: false

redis:
  uri: "redis://127.0.0.1:6379"
  pool_max_open: 16
  pool_max_idle: 8
  pool_timeout_seconds: 1
  pool_expire_seconds: 60
```

이 작업을 통해 PostgreSQL 및 Redis의 로컬 설정을 해줄 수 있다.

다음으로 앞서 만들어둔 `src/settings.rs`에도 설정을 추가해준다.

```Rust
use sqlx::ConnectOptions;

/// Global settings for exposing all preconfigured variables
#[derive(serde::Deserialize, Clone)]
pub struct Settings {
    pub application: ApplicationSettings,
    pub debug: bool,
    pub database: DatabaseSettings,
    pub redis: RedisSettings,
}

/// Application's specific settings to expose `port`,
/// `host`, `protocol`, and possible URL of the application
/// during and after development
#[derive(serde::Deserialize, Clone)]
pub struct ApplicationSettings {
    pub port: u16,
    pub host: String,
    pub base_url: String,
    pub protocol: String,
}

/// The possible runtime environment for our application.
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

/// Multipurpose function that helps detect the current environment the application
/// is running using the `APP_ENVIRONMENT` environment variable.
///
/// \`\`\`
/// APP_ENVIRONMENT = development | production.
/// \`\`\`
///
/// After detection, it loads the appropriate .yaml file
/// then it loads the environment variable that overrides whatever is set in the .yaml file.
/// For this to work, you the environment variable MUST be in uppercase and starts with `APP`,
/// a `_` separator then the category of settings,
/// followed by `__` separator,  and then the variable, e.g.
/// `APP__APPLICATION_PORT=5001` for `port` to be set as `5001`
pub fn get_settings() -> Result<Settings, config::ConfigError> {
    let base_path = std::env::current_dir().expect("Failed to determine the current directory");
    let settings_directory = base_path.join("settings");

    // Detect the running environment.
    // Default to `development` if unspecified.
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
        // Add in settings from environment variables (with a prefix of APP and '__' as separator)
        // E.g. `APP_APPLICATION__PORT=5001 would set `Settings.application.port`
        .add_source(
            config::Environment::with_prefix("APP")
                .prefix_separator("_")
                .separator("__"),
        )
        .build()?;

    settings.try_deserialize::<Settings>()
}

// Redis settings
#[derive(serde::Deserialize, Clone, Debug)]
pub struct RedisSettings {
    pub uri: String,
    pub pool_max_open: u64,
    pub pool_max_idle: u64,
    pub pool_timeout_seconds: u64,
    pub pool_expire_seconds: u64,
}

// Database settings
#[derive(serde::Deserialize, Clone)]
pub struct DatabaseSettings {
    pub username: String,
    pub password: String,
    pub port: u16,
    pub host: String,
    pub database_name: String,
    pub require_ssl: bool,
}

impl DatabaseSettings {
    pub fn connect_to_db(&self) -> sqlx::postgres::PgConnectOptions {
        let ssl_mode = if self.require_ssl {
            sqlx::postgres::PgSslMode::Require
        } else {
            sqlx::postgres::PgSslMode::Prefer
        };

        let mut options = sqlx::postgres::PgConnectOptions::new()
        .host(&self.host)
        .username(&self.username)
        .password(&self.password)
        .port(self.port)
        .ssl_mode(ssl_mode)
        .database(&self.database_name);

        options.log_statements(tracing::log::LevelFilter::Trace);
        options
    }
}
```

설정 파일에 `RedisSettings`, `DatabaseSettings`를 추가해주고 전역 `global` 객체를 수정해준다.

또한 `connect_to_db` 함수를 만들어 자격 증명을 사용해 데이터베이스에 쉽게 연결할 수 있도록 해준다. 이제 이런 설정들을 application과 통합해준다.

```Rust
pub struct Application {
    port: u16,
    server: actix_web::dev::Server,
}

impl Application {
    pub async fn build(
        settings: crate::settings::Settings,
        test_pool: Option<sqlx::postgres::PgPool>,
    ) -> Result<Self, std::io::Error> {
        let connection_pool = if let Some(pool) = test_pool {
            pool
        } else {
            get_connection_pool(&settings.database).await
        };

        sqlx::migrate!()
            .run(&connection_pool)
            .await
            .expect("Failed to migrate the database.");

        let address = format!(
            "{}:{}",
            settings.application.host, settings.application.port
        );

        let listener = std::net::TcpListener::bind(&address)?;
        let port = listener.local_addr().unwrap().port();
        let server = run(listener, connection_pool, settings).await?;

        Ok(Self { port, server })
    }

    pub fn port(&self) -> u16 {
        self.port
    }

    pub async fn run_until_stopped(self) -> Result<(), std::io::Error> {
        self.server.await
    }
}

pub async fn get_connection_pool(
    settings: &crate::settings::DatabaseSettings,
) -> sqlx::postgres::PgPool {
    sqlx::postgres::PgPoolOptions::new()
        .acquire_timeout(std::time::Duration::from_secs(2))
        .connect_lazy_with(settings.connect_to_db())
}

async fn run(
    listener: std::net::TcpListener,
    db_pool: sqlx::postgres::PgPool,
    settings: crate::settings::Settings,
) -> Result<actix_web::dev::Server, std::io::Error> {
    // Database connection pool application state
    let pool = actix_web::web::Data::new(db_pool);

    // Redis connection pool
    let cfg = deadpool_redis::Config::from_url(settings.clone().redis.uri);
    let redis_pool = cfg
        .create_pool(Some(deadpool_redis::Runtime::Tokio1))
        .expect("Cannot create deadpool redis.");
    let redis_pool_data = actix_web::web::Data::new(redis_pool);

    let server = actix_web::HttpServer::new(move || {
        actix_web::App::new()
            .service(crate::routes::health_check)
            // Add database pool to application state
            .app_data(pool.clone())
            // Add redis pool to application state
            .app_data(redis_pool_data.clone())
    })
    .listen(listener)?
    .run();
    Ok(server)
}
```

`get_connection_pool`: 애플리케이션을 DB에 느리게 연결한 다음 앱 사용을 위해 해당 연결을 반환하는 새로운 함수

`run`: get_connection_pool 함수에서 반환된 풀과 같은 더 많은 매개 변수를 사용하도록 확장되었다. 많은 엔드포인트가 생성된 DB 및 Redis에 접근해야 하므로 이를 앱 전체에서 사용하도록 해야한다.

이를 위해 actix-web은 `actix_web::web::Data<T>`: 동일한 범위 내의 모든 경로 및 리소스와 함께, 애플리케이션 상태를 공유하는데 도움이 되는 추출기를 제공한다. 그런 다음 이 API를 사용해 `pool` 및 `redis_pool_data`를 만들었으며, 그런 다음 이러한 항목을 `App:app_data()`를 통해 응용 프로그램에 연결해준다.

빌드 메서드의 경우, 테스트가 실행될 때 상요될 선택적 인자 인 `test_pool`을 허용하는 확장도 해준다. 또한 `sqlx::migrate` 매크로를 사용해 DB의 자동 마이그레이션을 허용해준다.

마이그레이션 폴더를 루트 디렉토리 이외의 다른 위치에 만든 경우 이러한 폴더의 경로를 이 매크로에 전달해야 한다. `deadpool-redis`를 설치하기 전에 `main.rs`를 업데이트 해준다.

```Rust
#[tokio::main]
async fn main() -> std::io::Result<()> {
    dotenv::dotenv().ok();

    let settings = backend::settings::get_settings().expect("Failed to read settings.");

    let subscriber = backend::telemetry::get_subscriber(settings.clone().debug);
    backend::telemetry::init_subscriber(subscriber);

    let application = backend::startup::Application::build(settings, None).await?;

    tracing::event!(target: "backend", tracing::Level::INFO, "Listening on http://127.0.0.1:{}/", application.port());

    application.run_until_stopped().await?;
    Ok(())
}
```

다음으로 `deadpool-redis`를 설치해준다.

```Shell
~/rust-auth/backend$ cargo add deadpool-redis
```

### 2.3 사용자 데이터를 위한 DB 테이블 생성

실질적으로 테이블을 생성하도록 코드를 작성한다.

```SQL
-- Add up migration script here
-- User table

CREATE TABLE IF NOT EXISTS users(
    id UUID NOT NULL PRIMARY KEY DEFAULT gen_random_uuid(),
    email TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    is_active BOOLEAN DEFAULT FALSE,
    is_staff BOOLEAN DEFAULT FALSE,
    is_superuser BOOLEAN DEFAULT FALSE,
    thumbnail TEXT NULL,
    date_joined TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS users_id_email_is_active_indx ON users (id, email, is_active);
-- Create a domain for phone data type
CREATE DOMAIN phone AS TEXT CHECK(
    octet_length(VALUE) BETWEEN 1
    /*+*/
    + 8 AND 1
    /*+*/
    + 15 + 3
    AND VALUE ~ '^\+\d+$'
);
-- User details table (One-to-one relationship)
CREATE TABLE user_profile (
    id UUID NOT NULL PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL UNIQUE,
    phone_number phone NULL,
    birth_date DATE NULL,
    github_link TEXT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS users_detail_id_user_id ON user_profile (id, user_id);
```

SQL 코드에 따르면, 1대1 관계를 가진 `users`, `user_profile`이 생성되었다.

올바로 생성되었는지 확인해보기

```shell
# psql <데이터베이스 이름>
psql rust_auth_db_dev

psql (14.9 (Homebrew))

Type "help" for help.

rust_auth_db_dev=# \dt
               List of relations
 Schema |       Name       | Type  |   Owner
--------+------------------+-------+-----------
 public | _sqlx_migrations | table | seilylook
 public | user_profile     | table | seilylook
 public | users            | table | seilylook
(3 rows)
```

```Shell
rust_auth_db_dev=# SELECT * FROM users;

id | email | password | first_name | last_name | is_active | is_staff | is_superuser | thumbnail | date_joined
---+-------+----------+------------+-----------+-----------+----------+--------------+-----------+------------
```

```Shell
rust_auth_db_dev=# SELECT * FROM user_profile;

id | user_id | phone_number | birth_date | gibhub_link
---+---------+--------------+------------+------------
```

## 3. 만들어둔 데이터베이스에 사용자 등록 코드 작성

### 3.1 dependency 설치

이 프로젝트에 사용할 crate들을 설치해준다.

```shell
~/rust-auth/backend$ cargo add pasetors once_cell hex chrono argon2

~/rust-auth/backend$ cargo add uuid --features="v4,serde"

~/rust-auth/backend$ cargo add serde_json --features="raw_value"

~/rust-auth/backend$ cargo add minijinja --features="source"

~/rust-auth/backend$ cargo add lettre --features="builder,tokio1-native-tls"
```

- [x] `pasetors`: 보안 토큰을 생성하고 증명하는 라이브러리

- [x] `once cell`: 템플릿 소스 코드를 가져오고 필요할 때 사용가능하도록 해준다.

- [x] `hex`: Redis에 토큰을 일시적으로 저장하는 데 사용된 세션 키로 사용되었던 임의로 생성된 128바이트의 데이터

- [x] `chrono`: 날짜와 시간을 사용하기 위한 라이브러리

- [x] `argon2`: 비밀번호를 해쉬화하고 증명하고 또한 암호화된 보안 데이터를 생성해주는 라이브러리.

- [x] `uuid`: 고유한 식별자를 생성하기 위해 사용되는 128비트 길이의 식별자 생성해주는 라이브러리.

- [x] `minijinja`: 사용자에게 보내는 HTML 또는 다중 부분 이메일을 해당 컨텍스트 값과 함께 렌더링하는 것.

- [x] `lettre`: 비동기적으로 안전하게 사용자에게 이메일을 보내주는 라이브러리

### 3.2 토큰과 해시를 위한 로직 작성

이제 토근을 안전하게 생성 및 증명하고 비밀번호를 해쉬화하고 증명하기 위한 로직을 만들어준다. 이를 위해서는 새로운 `utils`라는 모듈이 필요하다.

폴더를 만들어주고 이를 모듈화해준다. 보다 체계적으로 구성하기 위해 토큰 및 비밀번호 로직이 존재하는 하위 모듈 `auth`를 만들어준다.

먼저 비밀번호부터 시작한다.

```Rust
// src/utils/auth/password.rs

use argon2::{
    password_hash::{rand_core::OsRng, PasswordHash, PasswordHasher, PasswordVerifier, SaltString},
    Argon2,
};

#[tracing::instrument(name = "Hashing user password", skip(password))]
pub async fn hash(password: &[u8]) -> String {
    let salt = SaltString::generate(&mut OsRng);
    Argon2::default()
        .hash_password(password, &salt)
        .expect("Unable to hash password.")
        .to_string()
}

#[tracing::instrument(name = "Verifying user password", skip(password, hash))]
pub async fn verify_password(
    hash: &str,
    password: &[u8],
) -> Result<(), argon2::password_hash::Error> {
    let parsed_hash = PasswordHash::new(hash)?;
    Argon2::default().verify_password(password, &parsed_hash)
}
```

해시를 생성하고 확인하기 위해 `argon2`의 기본 설정을 사용하고 있다.

다음으로 토큰 생성 및 확인을 위한 로직을 작성한다.

```Rust
// src/utils/auth/token.rs

use argon2::password_hash::rand_core::{OsRng, RngCore};
use core::convert::TryFrom;
use deadpool_redis::redis::AsyncCommands;
use hex;
use pasetors::claims::{Claims, ClaimsValidationRules};
use pasetors::keys::SymmetricKey;
use pasetors::token::UntrustedToken;
use pasetors::{local, version4::V4, Local};

/// Store the session key prefix as a const so it can't be typo'd anywhere it's used.
const SESSION_KEY_PREFIX: &str = "valid_session_key_for_{}";

/// Issues a pasetor token to a user. The token has the user's id encoded.
/// A session_key is also encoded. This key is used to destroy the token
/// as soon as it's been verified. Depending on its usage, the token issued
/// has at most an hour to live. Which means, it is destroyed after its time-to-live.
#[tracing::instrument(name = "Issue pasetors token", skip(redis_connection))]
pub async fn issue_confirmation_token_pasetors(
    user_id: uuid::Uuid,
    redis_connection: &mut deadpool_redis::redis::aio::Connection,
    is_for_password_change: Option<bool>,
) -> Result<String, deadpool_redis::redis::RedisError> {
    // I just generate 128 bytes of random data for the session key
    // from something that is cryptographically secure (rand::CryptoRng)
    //
    // You don't necessarily need a random value, but you'll want something
    // that is sufficiently not able to be guessed (you don't want someone getting
    // an old token that is supposed to not be live, and being able to get a valid
    // token from that).
    let session_key: String = {
        let mut buff = [0_u8; 128];
        OsRng.fill_bytes(&mut buff);
        hex::encode(buff)
    };

    let redis_key = {
        if is_for_password_change.is_some() {
            format!(
                "{}{}is_for_password_change",
                SESSION_KEY_PREFIX, session_key
            )
        } else {
            format!("{}{}", SESSION_KEY_PREFIX, session_key)
        }
    };

    redis_connection
        .set(
            redis_key.clone(),
            // I just want to validate that the key exists to indicate the session is "live".
            String::new(),
        )
        .await
        .map_err(|e| {
            tracing::event!(target: "backend", tracing::Level::ERROR, "RedisError (set): {}", e);
            e
        })?;

    let settings = crate::settings::get_settings().expect("Cannot load settings.");
    let current_date_time = chrono::Local::now();
    let dt = {
        if is_for_password_change.is_some() {
            current_date_time + chrono::Duration::hours(1)
        } else {
            current_date_time + chrono::Duration::minutes(settings.secret.token_expiration)
        }
    };

    let time_to_live = {
        if is_for_password_change.is_some() {
            chrono::Duration::hours(1)
        } else {
            chrono::Duration::minutes(settings.secret.token_expiration)
        }
    };

    redis_connection
        .expire(
            redis_key.clone(),
            time_to_live.num_seconds().try_into().unwrap(),
        )
        .await
        .map_err(|e| {
            tracing::event!(target: "backend", tracing::Level::ERROR, "RedisError (expiry): {}", e);
            e
        })?;

    let mut claims = Claims::new().unwrap();
    // Set custom expiration, default is 1 hour
    claims.expiration(&dt.to_rfc3339()).unwrap();
    claims
        .add_additional("user_id", serde_json::json!(user_id))
        .unwrap();
    claims
        .add_additional("session_key", serde_json::json!(session_key))
        .unwrap();

    let sk = SymmetricKey::<V4>::from(settings.secret.secret_key.as_bytes()).unwrap();
    Ok(local::encrypt(
        &sk,
        &claims,
        None,
        Some(settings.secret.hmac_secret.as_bytes()),
    )
    .unwrap())
}

/// Verifies and destroys a token. A token is destroyed immediately
/// it has successfully been verified and all encoded data extracted.
/// Redis is used for such destruction.
#[tracing::instrument(name = "Verify pasetors token", skip(token, redis_connection))]
pub async fn verify_confirmation_token_pasetor(
    token: String,
    redis_connection: &mut deadpool_redis::redis::aio::Connection,
    is_password: Option<bool>,
) -> Result<crate::types::ConfirmationToken, String> {
    let settings = crate::settings::get_settings().expect("Cannot load settings.");
    let sk = SymmetricKey::<V4>::from(settings.secret.secret_key.as_bytes()).unwrap();

    let validation_rules = ClaimsValidationRules::new();
    let untrusted_token = UntrustedToken::<Local, V4>::try_from(&token)
        .map_err(|e| format!("TokenValiation: {}", e))?;
    let trusted_token = local::decrypt(
        &sk,
        &untrusted_token,
        &validation_rules,
        None,
        Some(settings.secret.hmac_secret.as_bytes()),
    )
    .map_err(|e| format!("Pasetor: {}", e))?;

    let claims = trusted_token.payload_claims().unwrap();

    let uid = serde_json::to_value(claims.get_claim("user_id").unwrap()).unwrap();

    match serde_json::from_value::<String>(uid) {
        Ok(uuid_string) => match uuid::Uuid::parse_str(&uuid_string) {
            Ok(user_uuid) => {
                let sss_key =
                    serde_json::to_value(claims.get_claim("session_key").unwrap()).unwrap();
                let session_key = match serde_json::from_value::<String>(sss_key) {
                    Ok(session_key) => session_key,
                    Err(e) => return Err(format!("{}", e)),
                };

                let redis_key = {
                    if is_password.is_some() {
                        format!(
                            "{}{}is_for_password_change",
                            SESSION_KEY_PREFIX, session_key
                        )
                    } else {
                        format!("{}{}", SESSION_KEY_PREFIX, session_key)
                    }
                };

                if redis_connection
                    .get::<_, Option<String>>(redis_key.clone())
                    .await
                    .map_err(|e| format!("{}", e))?
                    .is_none()
                {
                    return Err("Token has been used or expired.".to_string());
                }
                redis_connection
                    .del(redis_key.clone())
                    .await
                    .map_err(|e| format!("{}", e))?;
                Ok(crate::types::ConfirmationToken { user_id: user_uuid })
            }
            Err(e) => Err(format!("{}", e)),
        },

        Err(e) => Err(format!("{}", e)),
    }
}
```

`issue_confirmation_token_pasetors`: 등록된 모든 사용자에 대해 암호화된 사용자 ID로 안전한 pasetor 토큰을 생성하는 데 도움을 준다. 사용자가 이메일 주소를 확인한 후 또는 어떤 이유로 이메일 주소를 확인하지 못한 경우 이런 토큰이 파긷되도록 하기 위해 생성된 토큰을 Redis에 저장하고 Redis의 TTL(Time to live)를 활용한다. 각 토큰의 TTL은 파일이나 환경 변수를 통해 설정해 줄 수 있다.

`verify_confirmation_token_pasetor`: 우리는 다른 사용자의 토큰을 실수로 파기하지 않도록 Redis에 토큰을 저장하는 키를 인코딩하고 올바른 사용자인지 증명한다.

### 3.3 Type 생성 및 설정 업데이트

`ConfirmationToken`의 type 및 기타 설정 변수가 누락되어 현재 코드가 컴파일되지 않는다. 설정을 업데이트 해준다.

```YAML
# settings/base.yaml
...
email:
  host: "smtp.gmail.com"
  host_user: ""
  host_user_password: ""

# settings/development.yaml
...
secret:
  secret_key: <MY_SECRET_KEY>
  token_expiration: 30
  hmac_secret: <MY_HMAC_SECRET>

frontend_url: "https://localhost:3000"

# settings/production.yaml
...
secret:
  secret_key: ""
  token_expiration: 0
  hmac_secret: ""

frontend_url: ""
```

Gmail을 SMTP 서버로 사용할 것이다.

{{<admonition note STMP>}}
SMTP(전자메일 전송 프로토콜, Simple Mail Transfer Protocol)은 전자메일을 보내는 데 사용되는 표준 프로토콜 중 하나입니다. SMTP는 전자메일 클라이언트(보통 이메일 송신자)에서 전자메일 서버(이메일 수신자의 서버)로 이메일을 전송하는 데 사용됩니다. 다음은 SMTP의 주요 특징과 작동 방식에 대한 개요입니다:

이메일 전송: SMTP는 이메일 메시지를 송신자의 클라이언트 또는 애플리케이션에서 수신자의 이메일 서버로 전송하는 데 사용됩니다.

간단한 프로토콜: SMTP는 간단하며 텍스트 기반의 프로토콜로, 이메일 메시지의 헤더, 본문, 첨부 파일 및 수신자 정보를 처리하는 데에 사용됩니다.

포트 25: SMTP 서버는 일반적으로 TCP 포트 25를 사용하여 수신 대기하며, 클라이언트는 해당 포트를 통해 연결하여 이메일을 전송합니다. 하지만 보안 및 스팸 대응을 위해 SSL 또는 TLS를 통한 보안 연결을 사용하는 경우도 있습니다.

SMTP 서버 유형: SMTP 서버는 두 가지 주요 유형으로 나뉩니다. MTA(Mail Transfer Agent)는 이메일을 다른 서버로 전송하는 역할을 하며, MSA(Mail Submission Agent)는 이메일 클라이언트에서 전송된 이메일을 수신하여 전송을 위해 MTA로 전달합니다.

인증 및 보안: SMTP 서버는 보안을 강화하기 위해 사용자 인증을 지원할 수 있으며, SSL 또는 TLS를 통해 데이터 암호화를 제공하기도 합니다.

오류 처리: SMTP는 전송 중 오류를 처리하고 오류 메시지를 생성하여 이메일 송신자에게 오류 상황을 알려줍니다.

SMTP는 전자메일 시스템에서 중요한 역할을 하며, 전 세계적으로 널리 사용되고 있습니다. 그러나 SMTP는 이메일 전송에만 사용되며, 이메일 수신과 관련된 작업은 POP3 또는 IMAP과 같은 다른 프로토콜을 사용합니다.
{{</admonition>}}

`secret`: 토큰 생성에 있어 중요한 데이터를 보관하고 있다. 개발 환경 / 배포 환경에 다른 문자를 사용해야 한다.

`APP_SECRET__SECRET_KEY`, `APP_SECRRET__HMAC_SECRET`: 상수로 선언하고 환경 변수에서 설정한 값을 사용할 수 있다.

`token_expiration`: 생성한 토큰을 삭제하도록 시간을 지정해 줄 수 있다.

`frontend_url`: front-end 의 URL을 담고 있다.

`yaml`에 설정한 값들을 실제로 사용하기 위해 `src/settings.rs`에 추가해준다.

```Rust
/// Global settings for the exposing all preconfigured variables
#[derive(serde::Deserialize, Clone)]
pub struct Settings {
    ...
    pub secret: Secret,
    pub email: EmailSettings,
    pub frontend_url: String,
}

...
#[derive(serde::Deserialize, Clone)]
pub struct Secret {
    pub secret_key: String,
    pub token_expiration: i64,
    pub hmac_secret: String,
}

#[derive(serde::Deserialize, Clone)]
pub struct EmailSettings {
    pub host: String,
    pub host_user: String,
    pub host_user_password: String,
}
...
```

`types` 모둘을 만들어주고 토큰 생성을 위한 로직을 추가해준다.

```Rust
// src/types/tokens.rs

#[derive(serde::Serialize, serde::Deserialize, Debug, Clone)]
pub struct ConfirmationToken {
    pub user_id: uuid::Uuid,
}
```

### 3.4 템플릿을 로드하고 이메일 로직을 작성한다.

