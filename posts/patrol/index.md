# Patrol


# Introduction

Flutter는 테스트 코드 작성을 도와주는 자체 라이브러리인 `integrated test package`가 존재한다. 하지만 한계점도 존재하는데, 이 한계를 해결하기 위해 등장한 라이브러리가 바로 `Patrol`이다.

## Patrol 설치

```yaml
dependencies:
  # ...

dev_dependencies:
  # ...

patrol:
  app_name: My App
  android:
    package_name: com.example.myapp
  ios:
    bundle_id: com.example.MyApp
  macos:
    bundle_id: com.example.macos.MyApp
```

app_name, package_name, ios: bundle_id, macos: bundle_id는 각 프로젝트에 맞게 설정해 주어야 한다.

### Android

{{<admonition info>}}
Where do I get `package_name` from?

Go to `android/app/build.gradle` and look for `applicationId` in `defaultConfig` section.
{{</admonition>}}

### iOS & macOS

{{<admonition info>}}
Where do I get `bundle_id` from?

For iOS go to `ios/Runner.xcodeproj/project.pbxproj` and look for `PRODUCT_BUNDLE_IDENTIFIER`.

For macOS go to `macos/Runner.xcodeproj/project.pbxproj` and look for `PRODUCT_BUNDLE_IDENTIFIER`.
{{</admonition>}}

## Patrol CLI 설치

Patrol CLI는 Patrol UI 테스트를 가능하게 해주는 작은 프로그램이다.

```shell
dart pub global activate patrol_cli
```

## Patrol 실행

```terminal
patrol doctor
```

이 명령어를 입력했을 때, 다음과 같이 떠야 정상적으로 설치된 것이다.

<img src="/images/patrol-doctor.png" />

{{<admonition danger>}}
만약 설치 이후에도, `partol doctor` 명령어가 실행되지 않는다면 환경 변수를 설정해주지 않아서이다.
{{</admonition>}}

### 해결

mac에서 실행했을 때, ios/macos 가상 기기의 위치를 찾을 수 없다고 뜨는 경우 `log`에서 알려주는 환경 변수를 설정해주면 된다. 그대로 복사해서 터미널에 입력해주면 알아서 iOS / maxOS 위치를 설정해준다. 비교적 쉬운 이유는 내장된 기기로 설정이 되어있기 때문인 듯 하다.

문제는 안드로이드에서 발생했다. 안드로이드는 직접 환경 변수를 설졍해주어야 한다.

나는 `zsh`를 사용하기 때문에 `zshrc`를 수정해준다.

1. 루트 디렉토리에 `.zshrc`가 있는지 확인해준다.

   ```shell
   ll -al
   ```

2. `zshrc` 파일을 열어준다.

   ```shell
   vim ./.zshrc
   ```

3. `a`를 눌러 수정할 수 있도록(INSERT mode)로 바꿔준다.

4. 파일의 가장 아래로 내려가 다음을 적어준다.

   ```text
   export ANDROID_HOME=/Users/<사용자이름>/Library/Android
   export PATH=$PATH:$ANDROID_HOME/bin
   export PATH=$PATH:$ANDROID_HOME/sdk/platform-tools
   ```

5. ESC를 눌러 수정을 끝낸다.

6. `:wq`를 입력해 저장 후 닫는다.

7. 마지막으로 명령어를 입력해 변경을 반영되도록 해준다.

   ```shell
   source ./.zshrc
   ```

