# Flutter Amplify


# Introduction

이 포스팅은 Flutter에 Amplify 서비스를 연동하는 과정을 다룬다.

AWS Amplify는 모바일 및 프론트엔드 웹 개발자가 AWS에서 구동되는 안전하고 확장 가능한 풀 스택 애플리케이션을 개발하도록 지원하는 도구 및 서비스이다.

현재 Amplify에서 제공하는 대표적인 서비스는 다음과 같다.

- 소셜 미디어 로그인, OAuth 등을 위한 AWS Cognito

- 미디어 스토리지 파일용 AWS S3

- 앱에 대한 분석 데이터를 수집하는 AWS Analytics

## Amplify 사전 작업

### AWS 계정 생성

[Create Account](https://signin.aws.amazon.com/signin?redirect_uri=https%3A%2F%2Fportal.aws.amazon.com%2Fbilling%2Fsignup%2Fresume&client_id=signup&code_challenge_method=SHA-256&code_challenge=4WC0ztLzwAULzWOGoAv09NnZAJDGEs8nrJ8WvlTGfjk#/start)

### Amplify CLI 설치

Amplify 명령어를 입력하기 위한 툴체인을 설치해준다.

Windows

```shell
curl -sL https://aws-amplify.github.io/amplify-cli/install-win -o install.cmd && install.cmd
```

MAC

```shell
curl -sL https://aws-amplify.github.io/amplify-cli/install | bash && $SHELL
```

### Amplify Configuration

Amplify CLI를 설치한 후, 터미널을 통해 명령어를 실행해준다.

```shell
amplify configure
```

웹 브라우저가 실행되면서 AWS Console에 접속하고 로그인한다. 다시 터미널로 돌아와 엔터를 입력한다.

### AWS IAM 유저 생성

{{<admonition tip>}}
IAM는 AWS 서비스와 리소스에 대한 액세스를 안전하게 관리할 수 있습니다. 또한, AWS 사용자 및 그룹을 만들고 관리하며 AWS 리소스에 대한 액세스를 허용 및 거부할 수 있습니다.

추후에 사용자 회원가입, 로그인을 진행하기 위해서는 필수적으로 필요하다.
{{</admonition>}}

```shell
Specify the AWS Region
? region:  # Your preferred region
Specify the username of the new IAM user:
? user name:  # User name for Amplify IAM user
Complete the user creation using the AWS console
```

지역(서울), username(tunefun-sehyun)를 입력해준다.

이어서, IAM 계정에 `액세스 키`를 생성해준다.

<img src="/images/flutter-amplify-1.png">

생성한 액세스 키 Id, 액세스 키를 입력해준다.

```shell
Enter the access key of the newly created user:
? accessKeyId:  # YOUR_ACCESS_KEY_ID
? secretAccessKey:  # YOUR_SECRET_ACCESS_KEY
This would update/create the AWS Profile in your local machine
? Profile Name:  # (default)

Successfully set up the new user.
```

## Flutter와 Amplify 연동

### Amplify 관련 라이브러리 설치

pubspec.yaml에

```yaml
dependencies:
  ...
  amplify_flutter: ^1.6.1
  amplify_core: ^1.6.3
  amplify_analytics_pinpoint: ^1.6.3
  amplify_auth_cognito: ^1.6.2
  ...
```

### Amplify 초기화

```shell
amplify init
```

프로젝트 특성에 맞게 적절히 입력해준다.

<img src='/images/flutter-amplify-2.png' />

초기화가 성공했다면 다음의 결과 화면이 보인다.

```shell
✔ Successfully created initial AWS cloud resources for deployments.
✔ Initialized provider successfully.
Initialized your environment successfully.

Your project has been successfully initialized and connected to the cloud!
```

### Amplify 서비스 생성

사용자 로그인 `auth`, 앱 데이터 분석을 위한 `analytics`를 추가해준다.

```shell
amplify add auth
```

```shell
amplify add analytics
```

```shell
amplify push
```

올바로 서비스가 추가되었다면 다음과 같다.

<img src="/images/flutter-amplify-3.png" />

<img src="/images/flutter-amplify-4.png" />

### Flutter에서 Amplify 서비스 연결 확인

프로젝트의 루트 디렉토리의 main.dart에 다음 코드를 추가해 연결이 성공적인지 테스트한다.

```dart
import 'package:amplify_analytics_pinpoint/amplify_analytics_pinpoint.dart';
import 'package:amplify_auth_cognito/amplify_auth_cognito.dart';
import 'package:amplify_core/amplify_core.dart';
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:logger/logger.dart';
import 'package:tunefun_front/features/home/views/home_view.dart';
import 'package:tunefun_front/theme/theme.dart';
import 'amplifyconfiguration.dart';

var logger = Logger();

void main() {
  runApp(const ProviderScope(child: MyApp()));
}

class MyApp extends StatefulWidget {
  const MyApp({super.key});

  @override
  State<MyApp> createState() => _MyAppState();
}

class _MyAppState extends State<MyApp> {
  bool isConfigured = false;

  @override
  void initState() {
    super.initState();
    _configureAmplify();
  }

  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'TuneFun',
      debugShowCheckedModeBanner: false,
      theme: AppTheme.theme,
      home: const HomeScreen(),
    );
  }

  void _configureAmplify() async {
    final auth = AmplifyAuthCognito();
    final analytics = AmplifyAnalyticsPinpoint();

    try {
      Amplify.addPlugins([auth, analytics]);
      await Amplify.configure(amplifyconfig);
      isConfigured = true;
    } catch (e) {
      logger.e(e);
    }

    if (isConfigured) {
      logger.i('Successfully configured Amplify 🎉');
    }
  }
}

```

테스트 성공했다면 다음이 디버그 콘솔에 나타난다.

<img src="/images/flutter-amplify-5.png" />

