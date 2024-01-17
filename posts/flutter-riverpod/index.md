# Flutter Riverpod


# Introduction

`Flutter` 전용 상태 관리 라이브러리인 `Riverpod` 연구를 위한 포스팅. Flutter는 선언형 UI이며 각각의 상태를 포함하고 있는 위젯 트리를 기반으로 구성되기 때문에 `State management`가 매우 중요하다. 단일 위젯에서만 사용하는 상태일 경우는 상태 관리가 특별하기 관리되지 않아도 괜찮지만, 프로젝트 규모가 커질 수록 여러 위젯에섯 여러 상태에 대해 접근해야 된다. 이런 여러 위젯에서 사용하는 상태를 App State라고 부르며 App State 관리를 지원하는 여러 라이브러리가 존재하는데 Riverpod가 그 중 가장 대중적이다.

## What is Riverpod?

Riverpod은 InheritedWidget과 비슷한 동작을 하는 새로운 매커니즘으로 재구현한 상태 관리 패키지이다. Riverpod는 리액티브 캐싱, 데이터 바인딩을 지원하는 프레임워크이다.

### Reactive Caching

리액티브 캐싱이란, 데이터를 비동기적으로 계산할 때 캐싱해 해당 데이터가 필요한 모든 곳에서 쉽게 접근할 수 있도록 하는 기술이다. Riverpod에서는 Provider를 이용해 상태를 지속적으로 캐시하고 노출함으로써 데이터를 쉽게 공유하고 동기화할 수 있다. 예를 들어, Riverpod의 Provider를 사용하면, 처음 데이터를 가져온 뒤에는 동일한 데이터를 다른 컴포넌트에서 다시 가져올 필요 없이, 이미 캐시된 데이터를 활용해 중복 호출을 줄이며 상태를 효율적으로 관리하고 성능을 향상시킬 수 있다.

### Data Binding

데이터 바인딩이란, UI와 데이터를 결합하는 기술로 데이터의 변경에 따라 UI를 자동으로 변경하도록 해준다. Riverpod를 이용하면 상태를 나타내는 Provider 및 `ref` 객체의 `watch` 메소드를 통해 상태의 변경을 관찰해 상태가 변경되면 UI가 자동으로 업데이트 되도록 할 수 있다. 즉, Riverpod을 이용하며 MVVM 패턴을 구현할 수 있다.

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

