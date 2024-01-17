# Flutter Riverpod


# Introduction

`Flutter` 전용 상태 관리 라이브러리인 `Riverpod` 연구를 위한 포스팅. 정의: 리액티브 캐싱, 데이터 바인딩 프레임워크.

## Install

```yaml
dependencies:
  flutter:
    sdk: flutter

  cupertino_icons: ^1.0.2
  flutter_riverpod: ^2.4.9
```

## provider/network request

Network request는 모든 애플리케이션의 가장 중요한 기능이다. 하지만 네트워크 요청을 구축하기 위해서는 필수적으로 고려해야 할 사항들이 있다.

- 요청이 이루어 질 때 보여줄 UI 렌더링

- 에러들은 유연하게 처리되어야 한다.

- 요청은 Caching 되어야 한다.

### Setting up `ProviderScrope`

네트워크 요청을 구축하기 전, `ProviderScope`를 애플리케이션 루트 파일인 main.dart 안에 적용해준다.

```dart
void main() {
  runApp(
    // To install Riverpod, we need to add this widget above everything else.
    // This should not be inside "MyApp" but as direct parameter to "runApp".
    ProviderScope(
      child: MyApp(),
    ),
  );
}
```

### `ConsumerWidget` & `ConsumerStatefulWidget`

{{<admonition info>}}
`Ref`: An object used to interact with other providers.
All providers have one; either as parameter of the provider function, or as a property of a Notifier.
The type of this object is determined by the name of the function/class.
{{</admonition>}}

ConsumerWidget, ConsumerStatefulWidget은 StatelessWidget, StatefulWidget과 Consumer를 효과적으로 합친 것이다.

#### ConsumerWidget

```dart
/// We subclassed "ConsumerWidget" instead of "StatelessWidget".
/// This is equivalent to making a "StatelessWidget" and retuning "Consumer".
class Home extends ConsumerWidget {
  const Home({super.key});

  @override
  // Notice how "build" now receives an extra parameter: "ref"
  Widget build(BuildContext context, WidgetRef ref) {
    // We can use "ref.watch" inside our widget like we did using "Consumer"
    final AsyncValue<Activity> activity = ref.watch(activityProvider);

    // The rendering logic stays the same
    return Center(/* ... */);
  }
}
```

#### ConsumerStatefulWidget

```dart
// We extend ConsumerStatefulWidget.
// This is the equivalent of "Consumer" + "StatefulWidget".
class Home extends ConsumerStatefulWidget {
  const Home({super.key});

  @override
  ConsumerState<ConsumerStatefulWidget> createState() => _HomeState();
}

// Notice how instead of "State", we are extending "ConsumerState".
// This uses the same principle as "ConsumerWidget" vs "StatelessWidget".
class _HomeState extends ConsumerState<Home> {
  @override
  void initState() {
    super.initState();

    // State life-cycles have access to "ref" too.
    // This enables things such as adding a listener on a specific provider
    // to show dialogs/snackbars.
    ref.listenManual(activityProvider, (previous, next) {
      // TODO show a snackbar/dialog
    });
  }

  @override
  Widget build(BuildContext context) {
    // "ref" is not passed as parameter anymore, but is instead a property of "ConsumerState".
    // We can therefore keep using "ref.watch" inside "build".
    final AsyncValue<Activity> activity = ref.watch(activityProvider);

    return Center(/* ... */);
  }
}
```

