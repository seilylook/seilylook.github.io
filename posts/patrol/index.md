# Patrol


# Introduction

Flutter는 테스트 코드 작성을 도와주는 자체 라이브러리인 `integrated test package`가 존재한다. 하지만 한계점도 존재하는데, 이 한계를 해결하기 위해 등장한 라이브러리가 바로 `Patrol`이다.

# Patrol 설치

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

<img src="/images/patrol/patrol-doctor.png" />

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

# 모바일 디바이스와 통합하기

## Android

1. `android/app/src` 디렉토리에 `android/app/src/androidTest/java/com/example/myapp/` 이런식으로 생성해준다. 앞서 알아봤던 bundle.gradle의 app's package name을 적어준다.

2. `MainActivityTest.java` 파일을 생성하고 다음 코드를 적어준다.

```java
package com.example.myapp; // replace "com.example.myapp" with your app's package

import androidx.test.platform.app.InstrumentationRegistry;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.junit.runners.Parameterized;
import org.junit.runners.Parameterized.Parameters;
import pl.leancode.patrol.PatrolJUnitRunner;

@RunWith(Parameterized.class)
public class MainActivityTest {
    @Parameters(name = "{0}")
    public static Object[] testCases() {
        PatrolJUnitRunner instrumentation = (PatrolJUnitRunner) InstrumentationRegistry.getInstrumentation();
        // replace "MainActivity.class" with "io.flutter.embedding.android.FlutterActivity.class"
        // if your AndroidManifest is using: android:name="io.flutter.embedding.android.FlutterActivity"
        instrumentation.setUp(MainActivity.class);
        instrumentation.waitForPatrolAppService();
        return instrumentation.listDartTests();
    }

    public MainActivityTest(String dartTestName) {
        this.dartTestName = dartTestName;
    }

    private final String dartTestName;

    @Test
    public void runDartTest() {
        PatrolJUnitRunner instrumentation = (PatrolJUnitRunner) InstrumentationRegistry.getInstrumentation();
        instrumentation.runDartTest(dartTestName);
    }
}

```

3. `android/app/build.gradle`에 접근해서 다음 코드를 `defaultConfig` section에 넣어준다.

```gradle
  testInstrumentationRunner "pl.leancode.patrol.PatrolJUnitRunner"
  testInstrumentationRunnerArguments clearPackageData: "true"
```

4. `android` section에 다음 코드를 넣어준다.

```gradle
  testOptions {
    execution "ANDROIDX_TEST_ORCHESTRATOR"
  }
```

5. `dependencies` section에 다음 코드를 넣어준다.

```gradle
  androidTestUtil "androidx.test:orchestrator:1.4.2"
```

## iOS

참고로 iOS는 상당히 복잡하다.

1. `ios/Runner.xcworkspace`를 xcode로 열어준다.

2. `File > New > Target`을 선택한다. `UI Testing Bundle`을 선택한다. `Product Name`을 `RunnerUITests`으로 바꿔준다. `Organization Identifier`을 `Runner`와 동일하게 바꿔준다. `Target to Tested`를 `Runner` 그리고 언어를 `Objective-c`로 바꾸고 finish.

<img src="/images/patrol/patrol-setting-1.png" />
<img src="/images/patrol/patrol-setting-2.png" />
<img src="/images/patrol/patrol-setting-3.png" />

3. 2개의 파일이 생성된다. `RunnerUITest.m` & `RunnerUITestsLaunchTests.m`. `RunnerUITestsLaunchTests.m` 파일은 삭제한다.

4. `RunnerUITests`의 Build Settins의 iOS Deployment Target을 `Runner`와 동일하게 해준다. iOS version을 의미한다.

<img src="/images/patrol/patrol-setting-6.png" />

5. `RunnerUITests.m` 파일에 있는 코드를 모두 지우고 다음 코드를 적는다.

```swift
@import XCTest;
@import patrol;
@import ObjectiveC.runtime;

PATROL_INTEGRATION_TEST_IOS_RUNNER(RunnerUITests)
```

프로젝트의 `ios/Podfile`에 다음 코드를 적는다.

```ruby
target 'Runner' do
  # Do not change existing lines.
  ...

  target 'RunnerUITests' do
    inherit! :complete
  end
end

```

<img src="/images/patrol/patrol-setting-8.png" />

6. Root Directory에 `integration_test/example_test.dart` 폴더와 파일을 만들어준다. 그리고 다음 명령어를 입력해준다.

```shell
$ flutter build ios --config-only integration_test/example_test.dart
```

<img src="/images/patrol/patrol-setting-10.png" />

7. `ios` 디렉토리로 이동해서 다음 명령어를 입력해준다.

```shell
pod install --repo-update
```

<img src="/images/patrol/patrol-setting-11.png" />

8. Xcode를 열어서 각각의 build configuration, `RunnerUITests`이 `Runner`와 동일하게 바꿔준다.

<img src="/images/patrol/patrol-setting-12.png" />

9. RunnerUITests => Build Phases으로 들어가서 2개의 `Run Script Phase`를 추가해준다. 각각의 이름을 `xcode_backend build` & `xcode_backend embed_and_thin`으로 설정해준다.

<img src="/images/patrol/patrol-setting-13.png" />

10. 작성한 2개의 Script Phase의 위치를 다음과 같이 수정해준다.

<img src="/images/patrol/patrol-setting-14.png" />

11. `xcode_backend build`에 다음 코드를 적는다.

```shell
/bin/sh "$FLUTTER_ROOT/packages/flutter_tools/bin/xcode_backend.sh" build
```

<img src="/images/patrol/patrol-setting-15.png" />

12. `xcode_backend embed_and_thin`에 다음 코드를 적는다.

```shell
/bin/sh "$FLUTTER_ROOT/packages/flutter_tools/bin/xcode_backend.sh" embed_and_thin
```

<img src="/images/patrol/patrol-setting-16.png" />

13. parallel execution을 disable로 바꿔준다.

<img src="/images/patrol/patrol-setting-17.png" />
<img src="/images/patrol/patrol-setting-18.png" />
<img src="/images/patrol/patrol-setting-19.png" />
<img src="/images/patrol/patrol-setting-20.png" />

14. `RunnerUITests` => `Build Settins`에 들어가서, `User Script Sandboxing`을 찾아서 `No`로 변경해준다.

<img src="/images/patrol/patrol-setting-21.png" />

