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

## Chpater 2

가장 먼저 메인 화면을 위한 준비를 해준다. 이미지를 선택하는 화면을 제외한 나머지 화면은 HomeScreen에서 작업한다. HomeScreen UI 작업이 끝나면 스티커 붙이기 기능을 구현하고 마지막으로 이미지 선택, 이미지 저장에 해당되는 기능을 구현해준다.

### Appbar

```dart
import 'package:flutter/material.dart';

class MainAppBar extends StatelessWidget {
  final VoidCallback onPickImage;
  final VoidCallback onSaveImage;
  final VoidCallback onDeleteItem;

  const MainAppBar({
    super.key,
    required this.onPickImage,
    required this.onSaveImage,
    required this.onDeleteItem,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      height: 100,
      decoration: BoxDecoration(
        color: Colors.white.withOpacity(0.9),
      ),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceAround,
        crossAxisAlignment: CrossAxisAlignment.end,
        children: [
          IconButton(
            onPressed: onPickImage,
            icon: Icon(
              Icons.image_search_outlined,
              color: Colors.grey[700],
            ),
          ),
          IconButton(
            onPressed: onDeleteItem,
            icon: Icon(
              Icons.delete_forever_outlined,
              color: Colors.grey[700],
            ),
          ),
          IconButton(
            onPressed: onSaveImage,
            icon: Icon(
              Icons.save,
              color: Colors.grey[700],
            ),
          )
        ],
      ),
    );
  }
}
```

### Image 삽입, 삭제, 저장

```dart
  void onPickImage() async {
    final image = await ImagePicker().pickImage(source: ImageSource.gallery);
    setState(() {
      this.image = image;
    });
  }

  void onDeleteItem() async {
    setState(() {
      stickers = stickers.where((sticker) => sticker.id != selectedId).toSet();
    });
  }

  void onSaveImage() async {
    // 1
    RenderRepaintBoundary boundary =
        imgKey.currentContext!.findRenderObject() as RenderRepaintBoundary;
    // 2
    ui.Image image = await boundary.toImage();
    // 3
    ByteData? byteData = await image.toByteData(format: ui.ImageByteFormat.png);
    // 4
    Uint8List pngBytes = byteData!.buffer.asUint8List();

    await ImageGallerySaver.saveImage(pngBytes, quality: 100);

    // ignore: use_build_context_synchronously
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(
        content: Text('이미지가 저장되었습니다.'),
      ),
    );
  }
```

1. `toImage()` 함수를 실행해서 `RepaintBoundary`가 감싸고 있는 영역을 이미지로 변환할 수 있다. 이미지 갤러리에 저장할 때 사용할 플러그인인 `ImageGallerySaver`는 이미지를 저장하기에 앞서 이미지를 바이트 데이터로 변환해야 한다.

2. 이미지는 Byte 데이터로 변환한다. 변환된느 확장자는 png로 지정했다.

3. Byte 데이터를 8비트 정수형으로 변환한다. `ImageGallerySaver` 플러그인은 Byte 데이터가 8비트 정수형으로 변환되어 있는 걸 요구하기 때문이다. 이는 웹에서 이미지를 저장할 떄도 비슷한 변환 과정을 거친다.

4. 변환된 이미지 데이터를 `ImageGallerySaver.saveImage()` 함수에 입력해주고 갤러리에 이미지를 저장한ㄷ다. 추가적으로 ScaffoldMessenger의 `showSnackBar()`를 통해 이미지가 저장됐음을 알려준다.

### Footer

```dart
import 'package:flutter/material.dart';

typedef OnEmotionTap = void Function(int id);

class Footer extends StatelessWidget {
  final OnEmotionTap onEmotionTap;
  const Footer({
    super.key,
    required this.onEmotionTap,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      color: Colors.white.withOpacity(0.9),
      height: 150,
      child: SingleChildScrollView(
        scrollDirection: Axis.horizontal,
        child: Row(
          children: List.generate(
            7,
            (index) => Padding(
              padding: const EdgeInsets.symmetric(horizontal: 8.0),
              child: GestureDetector(
                onTap: () {
                  onEmotionTap(index + 1);
                },
                child: Image.asset(
                  'assets/img/emoticon_${index + 1}.png',
                  height: 100,
                ),
              ),
            ),
          ),
        ),
      ),
    );
  }
}
```

### 이모티콘 sticker widget

```dart
import 'package:flutter/material.dart';

class EmoticonPicker extends StatefulWidget {
  final VoidCallback onTransform;
  final String imgPath;
  final bool isSelected;
  const EmoticonPicker({
    super.key,
    required this.imgPath,
    required this.onTransform,
    required this.isSelected,
  });

  @override
  State<EmoticonPicker> createState() => _EmoticonPickerState();
}

class _EmoticonPickerState extends State<EmoticonPicker> {
  double scale = 1;
  double hTransform = 0;
  double vTransform = 0;
  double actualScale = 1;

  @override
  Widget build(BuildContext context) {
    return Transform(
      transform: Matrix4.identity()
        ..translate(hTransform, vTransform)
        ..scale(scale, scale),
      child: Container(
          decoration: widget.isSelected
              ? BoxDecoration(
                  borderRadius: BorderRadius.circular(4.0),
                  border: Border.all(
                    color: Colors.blue,
                    width: 1.0,
                  ),
                )
              : BoxDecoration(
                  border: Border.all(
                    color: Colors.transparent,
                    width: 1.0,
                  ),
                ),
          child: GestureDetector(
            onTap: () {
              widget.onTransform();
            },
            onScaleUpdate: (ScaleUpdateDetails details) {
              setState(() {
                scale = details.scale * actualScale;
                vTransform += details.focalPointDelta.dy;
                hTransform += details.focalPointDelta.dx;
              });
            },
            onScaleEnd: (ScaleEndDetails details) {
              actualScale = scale;
            },
            child: Image.asset(widget.imgPath),
          )),
    );
  }
}
```

해당 class를 자세히 살펴본다. 먼저, `onScaleUpdate` 이 제스처는 `ScaleUpdateDetail`값을 첫 번째 매개 변수로 입력받는다. `ScaleUpdateDetail`는 굉장히 많은 정보를 제공한다. 여기서 사용할 정보는 두가지이다.

첫번쨰는 확대 비율에 해당되는 `detail.scale`이다. 이 값을 double로 제공되며 확대/축소 제스처가 시작된 순간을 기준으로 몇 배율의 변화가 있는지 알려준다. 배율은 위젯의 초기 크기 기준이 아니기 때문에 확대/축소 제스처가 끝나는 순간을 알려주는 `onScaleEnd`매개변수가 실행될 때 현재 배율을 꼭 기억해두어야 한다. 그래야 최근 배율 \* details.scale를 계산해서 위젯의 초기 크기 기준으로 배율을 계산할 수 있다.

두번째로 사용할 값은 `details.focalPointDelta`이다. 이 값은 dy, dx 값을 갖고 있으며 각각 세로축, 가로축으로 이동한 수치를 반환받을 수 있다. 가로와 세로로 이동한 수치와 확대 및 축소가 된 수치를 변수로 저장해두고 확대/축소 제스처에 대한 콜백이 실행될 때마다 변수들을 업데이트해주면 사용자가 의도한 위젯의 변화를 상태 관리할 수 있다.

### 스티커 붙이기

이제 스티커 붙이기 기능을 구현한다. 여러 개의 스티커를 한번에 관리하기 편하도록 lib/model/sticker_model.dart 파일에 StickerModel 클래스를 구현해서 각각 스티커에 필요한 정보를 저장한다. 현재 필요한 각각 스티커의 정보는 ID 값과 스티커 이미지 경로 값이다.

```dart
class StickerModel {
  final String id;
  final String imgPath;

  StickerModel({required this.id, required this.imgPath});

  // 1
  @override
  bool operator ==(Object other) {
    return (other as StickerModel).id == id;
  }

  // 2
  int get hashCode => id.hashCode;
}
```

1. 하나의 인스턴스가 다른 인스턴스와 같은 지 비교할 때 사용한다. StickerModel은 id에 유일한 값을 입력하고 만약에 겹치면 중복 데이터를 제거한다.

2. Set 등 해시값을 사용하는 데이터 구조에서 사용하는 Getter이다. 마찬가지로 id값만 유일하면 되니 id의 hashCode값만 반환해준다.

```dart
  void onEmotionTap(int index) {
    setState(() {
      stickers = {
        ...stickers,
        StickerModel(
          // 1
          id: const Uuid().v4(),
          imgPath: 'assets/img/emoticon_$index.png',
        )
      };
    });
  }
```

1. `UUID` 패키지의 `Uuid().v4()` 함수를 사용하면 절대로 겹치지 않는 String 값을 생성할 수 있다. 화면에 스티커를 생성할 때마다 유일한 id 값을 소유하는 StickerModel을 만들어야 하니 id 값에 매전 새로운 UUID 값을 생성해서 저장한다.

### 스티커 삭제하기

스티커 삭제는 Set 형태인 stickers 변수에 모든 스티커 정보를 다 저장해놨으니 스티커 삭제 버튼이 눌릴 때마다 stickers 변수에서 각 StickerModel을 순회하며 id를 비교해서 `selectedId` 변수와 다른 것만 남겨주면 된다.

```dart
  void onDeleteItem() async {
    setState(() {
      stickers = stickers.where((sticker) => sticker.id != selectedId).toSet();
    });
  }
```

