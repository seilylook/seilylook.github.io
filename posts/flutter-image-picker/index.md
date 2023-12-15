# Flutter Image Picker


# Introduction

`Flutter` 기능 구현 - `Image Pick & Update & Save`

## Chapter 1

### 프로젝트 생성 및 이미지 추가

```shell
flutter create image_picker

cd image_picker
```

Root 디렉토리에 assets/img 폴더를 만들고, 해당 폴더에 사용할 이미지들을 넣어준다.

### pubspec.yaml 설정

```shell
flutter pub add image_picker, image_gallery_saver, uuid
```

```YAML
dependencies:
  flutter:
    sdk: flutter

  # The following adds the Cupertino Icons font to your application.
  # Use with the CupertinoIcons class for iOS style icons.
  cupertino_icons: ^1.0.2
  image_picker: ^1.0.5
  image_gallery_saver: ^2.0.3
  uuid: ^4.2.2

dev_dependencies:
  flutter_test:
    sdk: flutter

  # The "flutter_lints" package below contains a set of recommended lints to
  # encourage good coding practices. The lint set provided by the package is
  # activated in the `analysis_options.yaml` file located at the root of your
  # package. See that file for information about deactivating specific lint
  # rules and activating additional ones.
  flutter_lints: ^2.0.0

# For information on the generic Dart part of this file, see the
# following page: https://dart.dev/tools/pub/pubspec

# The following section is specific to Flutter packages.
flutter:
  # The following line ensures that the Material Icons font is
  # included with your application, so that you can use the icons in
  # the material Icons class.
  uses-material-design: true

  # To add assets to your application, add an assets section, like this:
  assets:
    - assets/img/
```

### 네이티브 권한(모바일 디바이스 권한) 설정

#### ios/Runner/Info.plist

```plist
<key>NSPhotoLibraryUsageDescription</key>
<string>사진첩 접근 권한이 필요합니다.</string>
<key>NSCameraUsageDescription</key>
<string>카메라 권한이 필요합니다.</string>
<key>NSMicrophoneUsageDescription</key>
<string>마이크 권한이 필요합니다.</string>
```

#### android/app/src/main/AndroidManifest.xml

```xml
<application
    android:label="image_editor"
    android:name="${applicationName}"
    android:icon="@mipmap/ic_launcher"
    android:requestLegacyExternalStorage="true">
```

