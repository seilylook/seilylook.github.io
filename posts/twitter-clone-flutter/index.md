# Twitter Clone Flutter


# Introduction

`Flutter`를 활용한 `twitter` clone mobile service

## Tech stack

- `Flutter`: Flutter transforms the entire app development process. Build, test, and deploy beautiful mobile, web, desktop, and embedded apps from a single codebase.
- `Appwrite`: Appwrite's open-source platform lets you add Auth, DBs, Functions and Storage to your product and build any application at any scale, own your data, and use your preferred coding languages and tools.
- `Riverpod`: Reactive caching and data-binding framework

## Chapter 1

### 1.1 Appwrite & Docker 설치

Docker를 먼저 설치해 주어야 한다. 설치 이후 실행시켜 놓는다.

이어서 [Docker를 이용한 Appwrite를 설치해준다.](https://appwrite.io/docs/advanced/self-hosting)

MacOS

```shell
docker run -it --rm \
    --volume /var/run/docker.sock:/var/run/docker.sock \
    --volume "$(pwd)"/appwrite:/usr/src/code/appwrite:rw \
    --entrypoint="install" \
    appwrite/appwrite:1.4.9

```

Window

```shell
// CMD
docker run -it --rm ^
    --volume //var/run/docker.sock:/var/run/docker.sock ^
    --volume "%cd%"/appwrite:/usr/src/code/appwrite:rw ^
    --entrypoint="install" ^
    appwrite/appwrite:1.4.9

// powershell
docker run -it --rm `
    --volume /var/run/docker.sock:/var/run/docker.sock `
    --volume ${pwd}/appwrite:/usr/src/code/appwrite:rw `
    --entrypoint="install" `
    appwrite/appwrite:1.4.9

```

설치가 완료되었다면, docker를 통해 Appwrite가 실행중이다.

http://localhost/login으로 접속하면 appwrite 로그인을 할 수 있다.

회원가입 / 로그인을 하고 나서 프로젝트 이름을 생성해준다. `Twitter Clone`

### 1.2 Flutter 프로젝트 생성.

```shell
cd development

flutter create twitter_clone

cd twitter_clone
```

VScode 하단을 콜릭해서 `emulator`를 실행시켜주고 실행 > 디버깅 없이 실행을 클릭해준다.

### 1.3 Appwrite에 Flutter project 생성 및 설정.

appwrite에 접속해서 flutter project android를 생성해준다.

1. 프로젝트 이름 설정.

2. package name: 이것은 android/app/src/build.gradle의 default config의 `applicationId`: `com.example.twitter_clone`을 복사해서 넣어준다.

3. Get the sdk에서 설정하라는대로 `appwrite: ^8.2.0`을 복사해서 root 디렉토리의 pubspec.yam의 `dependencies`에 추가해준다.

4. 마찬가지로 database를 새로 만들어준다.

5. lib 디렉토리에 `constants` 폴더를 생성하고, `appwrite_constants.dart`를 생성하고 앞서 만들었던 데이터베이스 Id, flutter 프로젝트 Id, endpoint를 설정해준다.

#### lib/constants/appwrite_constants.dart

```dart
class AppWriteConstants {
  static const String databaseId = "654e050ed3a78ffe0eba";
  static const String projectId = "654df273acbe3b7b61c2";
  static const String endPoint = 'http://localhost';
}
```

### 1.4 assets 이미지 설정하기

`pubspec.yaml`의 `assets`의 주석들을 지우고 svg 파일이 존재하는 경로를 설정해준다.

```yaml
assets:
  - assets/svgs/
```

파일들을 편리하게 사용하기 위해 index.ts에서 하던 작업같이 객체화 시켜준다.

#### lib/constants/assets_constants.dart

```dart
class AssetsConstants {
  static const String _svgsPath = 'assets/svgs';
  static const String twitterLogo = '$_svgsPath/twitter_logo.svg';
  static const String homeFilledIcon = '$_svgsPath/home_filled.svg';
  static const String homeOutlinedIcon = '$_svgsPath/home_outlined.svg';
  static const String notifFilledIcon = '$_svgsPath/notif_filled.svg';
  static const String notifOutlinedIcon = '$_svgsPath/notif_outlined.svg';
  static const String searchIcon = '$_svgsPath/search.svg';
  static const String gifIcon = '$_svgsPath/gif.svg';
  static const String emojiIcon = '$_svgsPath/emoji.svg';
  static const String galleryIcon = '$_svgsPath/gallery.svg';
  static const String commentIcon = '$_svgsPath/comment.svg';
  static const String retweetIcon = '$_svgsPath/retweet.svg';
  static const String likeOutlinedIcon = '$_svgsPath/like_outlined.svg';
  static const String likeFilledIcon = '$_svgsPath/like_filled.svg';
  static const String viewsIcon = '$_svgsPath/views.svg';
  static const String verifiedIcon = '$_svgsPath/verified.svg';
}
```

마지막으로 export 작업을 통해 import가 편리하도록 해준다.

#### lib/constants/constants.dart

```dart
export './appwrite_constants.dart';
export './assets_constants.dart';

// import "appwrite_constants.dart"
// import "assets_constants.dart"

// 기존에 index.ts만들어서 모든 파일들 export 해주는 것과 같은 역할 수행.
```

### 1.5 Pallete 컬러 객체화 하기

lib 안에 theme 폴더를 만들고 theme 설정과 관련된 코드를 저장한다.

#### lib/theme/app_theme.dart

```dart
import 'package:flutter/material.dart';
import 'package:twitter_clone/theme/pallete.dart';

class AppTheme {
  static ThemeData theme = ThemeData.dark().copyWith(
    scaffoldBackgroundColor: Pallete.backgroundColor,
    appBarTheme: const AppBarTheme(
      backgroundColor: Pallete.backgroundColor,
      elevation: 0,
    ),
    floatingActionButtonTheme: const FloatingActionButtonThemeData(
      backgroundColor: Pallete.blueColor,
    ),
  );
}
```

이어서 사용할 색상들을 전역적으로 사용하기 위해 pallete를 만들어준다.

### lib/theme/pallete.dart

```dart
import 'package:flutter/material.dart';

class Pallete {
  static const Color backgroundColor = Colors.black;
  static const Color searchBarColor = Color.fromRGBO(32, 35, 39, 1);
  static const Color blueColor = Color.fromRGBO(29, 155, 240, 1);
  static const Color whiteColor = Colors.white;
  static const Color greyColor = Colors.grey;
  static const Color redColor = Color.fromRGBO(249, 25, 127, 1);
}
```

마찬가지로 모두 export 해준다.

#### lib/theme/theme.dart

```dart
export './app_theme.dart';
export './pallete.dart';
```

### 1.6 설정한 boiler plate를 적용한다.

#### lib/main.dart

```dart
import 'package:flutter/material.dart';
import 'package:twitter_clone/features/auth/view/login_view.dart';
import 'package:twitter_clone/theme/theme.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter Demo',
      theme: AppTheme.theme,
    );
  }
}
```

## Chapter 2

### 2.1 Login UI

로그인을 구현하기 위해 `features/auth`폴더를 생성한다. `auth` 폴더 안에 `view`, `widgets` 폴더를 생성한다. view 폴더 안에는 화면 상에 보여줄 화면을 구성한다.

#### lib/features/auth/view/login_view.dart

```dart
import 'package:flutter/gestures.dart';
import 'package:flutter/material.dart';
import 'package:twitter_clone/common/rounded_small_button.dart';
import 'package:twitter_clone/constants/ui_constants.dart';
import 'package:twitter_clone/features/auth/widgets/auth_field.dart';
import 'package:twitter_clone/theme/pallete.dart';

class LoginView extends StatefulWidget {
  const LoginView({super.key});

  @override
  State<LoginView> createState() => _LoginViewState();
}

class _LoginViewState extends State<LoginView> {
  final appbar = UIConstants.appBar();
  final emailController = TextEditingController();
  final passwordController = TextEditingController();

  // dispose의 역할: 컨트롤러 객체가 제거 될 때 변수에 할당된 메모리를 제거하기 위해서 사용한다.
  @override
  void dispose() {
    super.dispose();
    emailController.dispose();
    passwordController.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        appBar: appbar,
        body: Center(
          child: SingleChildScrollView(
            child: Padding(
              padding: const EdgeInsets.symmetric(horizontal: 20),
              child: Column(
                children: [
                  AuthField(
                    controller: emailController,
                    hintText: 'Email',
                  ),
                  const SizedBox(height: 25),
                  AuthField(
                    controller: passwordController,
                    hintText: 'Password',
                  ),
                  const SizedBox(height: 40),
                  Align(
                    alignment: Alignment.topRight,
                    child: RoundedSmallButton(
                      onTap: () {},
                      label: 'Done',
                    ),
                  ),
                  const SizedBox(height: 40),
                  RichText(
                      text: TextSpan(
                          text: "Don't have account?",
                          style: TextStyle(
                            fontSize: 16,
                          ),
                          children: [
                        TextSpan(
                            text: ' Sign Up',
                            style: TextStyle(
                              color: Pallete.blueColor,
                              fontSize: 16,
                            ),
                            recognizer: TapGestureRecognizer()..onTap = () {}),
                      ]))
                ],
              ),
            ),
          ),
        ));
  }
}
```

이메일, 비밀번호 입력 폼은 동일하기에 컴포넌트화 해주기 위해 분리한다.

#### lib/features/auth/widgets/auth_field.dart

```dart
import 'package:flutter/material.dart';
import 'package:twitter_clone/theme/pallete.dart';

class AuthField extends StatelessWidget {
  final TextEditingController controller;
  final String hintText;
  const AuthField(
      {super.key, required this.controller, required this.hintText});

  @override
  Widget build(BuildContext context) {
    return TextFormField(
      controller: controller,
      decoration: InputDecoration(
          focusedBorder: OutlineInputBorder(
            borderRadius: BorderRadius.circular(5),
            borderSide: const BorderSide(
              color: Pallete.blueColor,
              width: 3,
            ),
          ),
          enabledBorder: OutlineInputBorder(
            borderRadius: BorderRadius.circular(5),
            borderSide: const BorderSide(
              color: Pallete.greyColor,
            ),
          ),
          contentPadding: const EdgeInsets.all(22),
          hintText: hintText,
          hintStyle: const TextStyle(
            fontSize: 18,
          )),
    );
  }
}
```

마지막으로 로그인 버튼을 만들어준다. 버튼은 여러곳에서 계속 사용할 것이니까 `lib` 폴더 안에 `common` 폴더를 만들어, 이곳에 코드를 작성해준다.

#### lib/common/rounded_small_button.dart

```dart
import 'package:flutter/material.dart';
import 'package:twitter_clone/theme/pallete.dart';

class RoundedSmallButton extends StatelessWidget {
  final VoidCallback onTap;
  final String label;
  final Color backgroundColor;
  final Color textColor;

  const RoundedSmallButton({
    super.key,
    required this.onTap,
    required this.label,
    this.backgroundColor = Pallete.whiteColor,
    this.textColor = Pallete.backgroundColor,
  });

  @override
  Widget build(BuildContext context) {
    return Chip(
      label: Text(label, style: TextStyle(color: textColor, fontSize: 20)),
      backgroundColor: backgroundColor,
      labelPadding: const EdgeInsets.symmetric(
        horizontal: 15,
        vertical: 8,
      ),
    );
  }
}
```

### 2.2 SignUp UI

