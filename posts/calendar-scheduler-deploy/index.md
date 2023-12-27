# Calendar Scheduler Deploy


# Introduction

기존에 작업하던 `calendar-scheduler`를 배포.

## 앱 Bundle ID 설정하기

`Bundle ID`는 앱을 식별하는 유일한 값이다. 세 개의 단어를 마침표로 구분해서 입력하며 같은 플랫폼(안드로이드, iOS 등) 내에서 다른 앱과 절대로 겹칠 수가 없다. 일반적으로 도메인을 거꾸로 입력한 형태를 띈다.

직접 모든 파일에 적힌 Bundle ID를 변경해 줄 수도 있지만 그러면 실수가 생길 수도 있고 시간이 오래 걸리기 때문에 플러그인을 사용한다.

### change_app_package_name 설치

```shell
flutter pub add change_app_package_name
```

### bundle id 바꿔주기

```shell
flutter pub run change_app_package_name:main <바꿔 줄 이름>
```

### 변경된 Bundle ID를 피어어베이스에 등록해주기 위해 설정해준다.

```shell
flutterfire configure
```

## 안드로이드 앱 배포하기

안드로이드 앱을 배포하려면 키를 생성하고 안드로이드 프로젝트에 등록해줘야 한다. 그 다음 `appbundle`을 빌드한 후 구글 플레이에 업로드해야 한다.

### 자바 설치

```shell
brew install openjdk@11
```

```shell
sudo ln -sfn /opt/homebrew/opt/openjdk@11/libexec/openjdk.jdk /Library/Java/JavaVirtualMachines/openjdk-11.jdk
```

```shell
echo 'export PATH="/opt/homebrew/opt/openjdk@11/bin:$PATH"' >> ~/.zshrc
```

```shell
export CPPFLAGS="-I/opt/homebrew/opt/openjdk@11/include"
```

### 업로드 키 생성

구글 플레이에 앱을 업로드하려면 업로드 키를 생성해야 한다. 이 업로드 키가 있어야 추후 추가 업데이트가 가능하다. 아래 명령어를 실행하면 키 파일을 생성할 수 있다. 특정 위치에 생성하고 싶다면 `-keystore` 뒤에 원하는 경로를 넣어주면 된다.

```shell
keytool -genkey -v -keystore ~/Development/Flutter/calendar_scheduler/android/upload-keystore.jks -keyalg RSA -keysize 2048 -validity 10000 -alias upload
```

### 업로드 키 등록

android 폴더에 `key.properties` 파일을 생성해준다. 이 파일은 자동으로 gitignore가 적용되어 있으니 비밀번호가 유출된 걱정은 하지 않아도 된다.

```properties
storePassword=<키를 생성할 때 입력한 비밀번호>
keyPassword=<키를 생성할 때 입력한 비밀번호>
keyAlias=upload
storeFile=<생성한 upload.keystore.jks 파일 오른쪽 클릭 후 절대 경로를 복사해서 넣어준다.> !상대경로를 넣으면 안된다.
```

### build.gradle 설정

android/app/build.gradle에 접근해서 설정을 추가해준다.

```gradle
def keystoreProperties = new Properties()
def keystorePropertiesFile = rootProject.file('key.properties')
if (keystorePropertiesFile.exists()) {
    keystoreProperties.load(new FileInputStream(keystorePropertiesFile))
}

android {
    ...생략...
}
```

```gradle
android {
    ...생략...

    signingConfigs {
        release {
            keyAlias keystoreProperties['keyAlias']
            keyPassword keystoreProperties['keyPassword']
            storeFile keystoreProperties['storeFile'] ? file(keystoreProperties['storeFile']) : null
            storePassword keystoreProperties['storePassword']
        }
    }

    buildTypes {
        release {
            // TODO: Add your own signing config for the release build.
            // Signing with the debug keys for now, so `flutter run --release` works.
            signingConfig signingConfigs.release
        }
    }
}
```

이제 appbundle을 생성해주기 위한 준비가 모두 끝났다.

```shell
flutter build appbundle
```

정상적으로 `appbundle`이 생성되었다면, 다음과 같이 뜬다.

```shell
Running Gradle task 'bundleRelease'...                             27.7s
✓ Built build/app/outputs/bundle/release/app-release.aab (26.3MB).
```

빌드된 파일은 `build/app/outputs/bundle/release/`에 있다.

