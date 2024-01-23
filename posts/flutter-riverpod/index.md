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

## Implement

### Reading Providers using ConsumerWidget

먼저, 앞서 말했듯이 root의 main.dart에 ProviderScope를 설정해 하위 모든 위젯에서 Provider를 사용해 데이터를 주시하도록 만들어준다.

#### lib/main.dart

```dart
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_state_management/home_screen.dart';

final nameProvider = Provider<String>((ref) {
  return 'seilyook';
});

void main() {
  runApp(
    const ProviderScope(
      child: MyApp(),
    ),
  );
}

class MyApp extends StatelessWidget {
  ...
}
```

주목할 부분은 `nameProvider` Provider `<Return 값>`이다. 앞서 말했듯이, `ref`를 통해서 다른 위젯에서 값을 캐싱하고 데이터 바인딩을 할 수 있다.

#### lib/home_screen.dart

```dart
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_state_management/main.dart';

class HomeScreen extends ConsumerWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final name = ref.watch(nameProvider);

    return Scaffold(
      body: Center(
        child: Text(
          name,
          style: const TextStyle(
            fontSize: 16,
            fontWeight: FontWeight.bold,
          ),
        ),
      ),
    );
  }
}
```

상위 위젯인 main.dart에서 지정한 `nameProvider`의 데이터를 하위 위젯인 HomeScreen에서 바인딩 할 수 있다.

- `ref.watch`: 위젯의 build 메서드 내부 또는 Provider의 본문 내부에서 사용되어 해당 위젯 또는 프로바이더가 다른 프로바이더를 감시하도록 사용된다.

{{<admonition warning>}}
`watch` 메서드는 비동기적으로 호출되지 않아야 하며 ElevatedButton의 `onPressed` 내부 또는 initState 및 상태 라이프 사이클 내에서 사용해서는 안된다. 이러한 경우는 `ref.read`를 사용하는 것이 좋다.
{{</admonition>}}

- `ref.listen`: 위젯 똔느 프로바이더를 감시하는 것이 가능하다. 두 메서드 간의 주요 차이점은 감시 대상 프로바이더가 변경될 때 위젯/프로바이더를 다시 빌드하는 대신 ref.listen을 사용하면 사용자가 지정한 콜백 함수를 호출한다. 이는 특정 변경이 발생할 떄 액션을 수행하는 데 유용하며, 예를 들어 오류 발생 시 스낵바를 등의 작업에 활용될 수 있다.

ref.listen 메서드는 두 개의 parameter가 필요하며, 첫 번째는 프로바디어이고 두 번째는 상태 변경 시 실행하려는 콜백 함수이다. 호출된 콜백 함에는 이전 상태의 값과 새로운 상태의 값 두 가지 값이 전달된다.

ref.listen 메서드는 프로바이더, 위젯의 body 내부에서 사용될 수 있다.

```dart
@riverpod
class Counter extends _$Counter {
  @override
  int build() => 0;
}

class HomeView extends ConsumerWidget {
  const HomeView({Key? key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    ref.listen<int>(counterProvider, (int? previousCount, int newCount) {
      print('The counter changed $newCount');
    });

    return Container();
  }
}
```

{{<admonition warning>}}
주의: `listen` 메서드는 비동기적으로 호출되지 않아야 하며 ElevatedButton의 onPressed 내부 또는 initState 및 기타 상태 라이프 사이클 내에서 사용해서는 안됩니다.
{{</admonition>}}

- `ref.read`: 일반적으로 사용자 상호작용에서 트리거된 함수 내부에서 자주 사용된다. 예를 들어 사용자가 버튼을 클릭할 때 카운터를 증가시키기 위해 ref.read를 사용한다.

{{<admonition tip>}}
ref.read 사용은 가능한 한 피해야 합니다. 왜냐하면 이는 반응적이지 않기 때문입니다.
{{</admonition>}}

### StateProvider

StateProvider는 상태를 수정하는 방법을 노출하는 프로바이더이다. 이는 매우 간단한 사용 사례에 대한 NotifierProvider의 단순화된 버전으로, 매우 간단한 경우에 Notifier 클래스를 작성하지 않아도 되도록 설계되었다.

StateProvider는 주로 사용자 인터페이스에서 간단한 변수의 수정을 허용하기 위해 존재한다. StateProvider의 상태는 일반적으로 다음 중 하나이다.

- Enum

- 문자열, 일반적으로 텍스트 필드의 내용

- 체크 박스용 bool 값

- 페이지네이션이나 나이 폼 필드를 위한 숫자

다음 상황에서 StateProvider를 사용하지 않아야 한다.

- 상태에 유효성 검사 논리가 필요한 경우

- 상태가 복잡한 객체인 경우(사용자 정의 클래스, 목록/맵 등)

- 상태를 수정하는 논리가 복잡한 경우

#### lib/main.dart

```dart
final nameProvider = StateProvider<String?>((ref) => null);

...
```

#### lib/home_screen.dart

```dart
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_state_management/main.dart';

class HomeScreen extends ConsumerWidget {
  const HomeScreen({super.key});

  // notifier가 상태 값을 변경하도록 도와준다.
  void onSubmitted(WidgetRef ref, String value) {
    final name = ref.read(nameProvider.notifier).update((state) => value);
  }

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final name = ref.watch(nameProvider) ?? '';

    return Scaffold(
      appBar: AppBar(
        title: const Text(
          'Home',
        ),
      ),
      body: Column(
        children: [
          TextField(
            onSubmitted: (value) {
              onSubmitted(ref, value);
            },
          ),
          Center(
            child: Text(
              name,
              style: const TextStyle(
                fontSize: 16,
                fontWeight: FontWeight.bold,
              ),
            ),
          ),
        ],
      ),
    );
  }
}
```

### StateNotifier & StateNotifierProvider

StateProvider보다 복잡한 데이터의 변경을 위해서 사용하는 것이 `StateNotifier`이다. 데이터 베이스 모델에 담긴 데이터 변경을 위해 주로 사용한다.

#### model - lib/user.dart

```dart
@immutable
class User {
  final String name;
  final int age;

  const User({
    required this.name,
    required this.age,
  });

  User copyWith({
    String? name,
    int? age,
  }) {
    return User(
      name: name ?? this.name,
      age: age ?? this.age,
    );
  }

  Map<String, dynamic> toMap() {
    return <String, dynamic>{
      'name': name,
      'age': age,
    };
  }

  factory User.fromMap(Map<String, dynamic> map) {
    return User(
      name: map['name'] as String,
      age: map['age'] as int,
    );
  }

  String toJson() => json.encode(toMap());

  factory User.fromJson(String source) =>
      User.fromMap(json.decode(source) as Map<String, dynamic>);

  @override
  String toString() => 'User(name: $name, age: $age)';

  @override
  bool operator ==(covariant User other) {
    if (identical(this, other)) return true;

    return other.name == name && other.age == age;
  }

  @override
  int get hashCode => name.hashCode ^ age.hashCode;
}
```

class 안에 final String name, final int age만 적어놓고 data generator를 통해 여러 메서드를 쉽게 생성해준다.

#### StateNotifier - lib/user.dart

```dart
class UserNotifier extends StateNotifier<User> {
  UserNotifier(super.state);

  void updateName(String newName) {
    // state의 모든 값 name, age를 복사하고
    // 그 중에서 name 값만을 번경해준다는 뜻이다.
    state = state.copyWith(name: newName);
  }
}
```

#### StateNotifierProvider - lib/main.dart

```dart
final userProvider = StateNotifierProvider<UserNotifier, User>(
  (ref) => UserNotifier(
    const User(
      name: '',
      age: 0,
    ),
  ),
);
```

마지막으로 StateNotifierProvider를 사용해서 데이터를 읽고, 변경하도록 수정해준다.

#### lib/home_screen.dart

```dart
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_state_management/main.dart';

class HomeScreen extends ConsumerWidget {
  const HomeScreen({super.key});

  // notifier가 상태 값을 변경하도록 도와준다.
  void onSubmitted(WidgetRef ref, String value) {
    ref.read(userProvider.notifier).updateName(value);
  }

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final user = ref.watch(userProvider);

    return Scaffold(
      appBar: AppBar(
        title: const Text(
          'Home',
        ),
      ),
      body: Column(
        children: [
          TextField(
            onSubmitted: (value) {
              onSubmitted(ref, value);
            },
          ),
          Column(
            children: [
              Text(
                user.name,
                style: const TextStyle(
                  fontSize: 16,
                  fontWeight: FontWeight.bold,
                ),
              ),
              Text(
                user.age.toString(),
                style: const TextStyle(
                  fontSize: 16,
                  fontWeight: FontWeight.bold,
                ),
              )
            ],
          ),
        ],
      ),
    );
  }
}
```

만약 직접 값을 변경하고자 한다면, 다음과 같이 수정할 수 있다.

#### StateNotifier - lib/user.dart

```dart
class UserNotifier extends StateNotifier<User> {
  UserNotifier()
      : super(
          const User(name: '', age: 0),
        );

  void updateName(String newName) {
    // state의 모든 값 name, age를 복사하고
    // 그 중에서 name 값만을 번경해준다는 뜻이다.
    state = state.copyWith(name: newName);
  }

  void updateAge(int newAge) {
    state = state.copyWith(age: newAge);
  }
}
```

#### StateNotifierProvider - lib/main.dart

```dart
final userProvider = StateNotifierProvider<UserNotifier, User>(
  (ref) => UserNotifier(),
);
```

### StreamProvider를 사용해 비동기 데이터 가져오기

사용하는 프로바이더에 따라서, 취득 가능한 값의 종류가 다양해 질 수 있다. 예를 들어 `StreamProvider`를 사용할 때를 생각해보자.

{{<admonition tip>}}
StreamProvider는 FutureProvider와 유사하지만 Future 대신에 Stream에 대한 것입니다.

StreamProvider는 일반적으로 다음과 같은 용도로 사용됩니다:

Firebase 또는 웹 소켓을 듣기 위해
몇 초마다 다른 프로바이더를 다시 빌드하기 위해
스트림이 자연스럽게 업데이트를 듣기 위한 방법을 노출하므로 어떤 사람들은 StreamProvider를 사용하는 것이 가치가 낮다고 생각할 수 있습니다. 특히 Flutter의 StreamBuilder를 사용하여 스트림을 듣는 것만으로 충분하다고 여길 수 있지만, 이는 오해입니다.

StreamProvider를 StreamBuilder 대신 사용하는 것에는 여러 가지 이점이 있습니다:

ref.watch를 사용하여 다른 프로바이더가 스트림을 듣도록 허용합니다.
AsyncValue 덕분에 로딩 및 오류 상황이 적절히 처리됩니다.
브로드캐스트 스트림 대 일반 스트림을 구별할 필요가 없어집니다.
스트림에 의해 방출된 가장 최신 값이 캐시되어, 이벤트가 방출된 후에 리스너가 추가되더라도 리스너가 가장 최신 이벤트에 즉시 액세스할 수 있도록 보장합니다.
StreamProvider를 오버라이드하여 테스트 중에 간단하게 스트림을 모의화할 수 있습니다.
{{</admonition>}}

```dart
final userProvider = StreamProvider<User>(...);
```

`userProvider`를 읽으려고 할 때 아래와 같이 사용할 수 있다.

- `userProvider` 자체를 읽는 것으로 동기화된 현재 상태 값을 읽을 수 있다.

```dart
Widget build(BuildContext context, WidgetRef ref) {
  AsyncValue<User> user = ref.watch(userProvider);

  return user.when(
    loading: () => const CircularProgressIndicator(),
    error: (error, stack) => const Text('Oops'),
    data: (user) => Text(user.name),
  );
}
```

- `userProvider.stream`을 사용해 연결된 Stream을 얻을 수 있다.

{{<admonition tip>}}
What is Stream?

비동기 데이터 이벤트의 소스.

스트림은 이벤트의 시퀀스를 수신하는 방법을 제공합니다. 각 이벤트는 데이터 이벤트 또는 스트림의 요소라고도 하는 것이거나 실패했다는 것을 알리는 오류 이벤트 중 하나입니다. 스트림이 모든 이벤트를 방출하면 "done" 이벤트 하나가 청취자에게 끝이 도달했음을 알리게 됩니다.

스트림을 청취하여 이벤트 생성을 시작하고, 이벤트를 받는 청취자를 설정합니다. 청취할 때는 이벤트를 제공하는 활성 객체 인 StreamSubscription 개체를 받습니다. 이 객체는 이벤트를 제공하며 청취를 중지하거나 구독에서 일시적으로 이벤트를 일시 중지하는 데 사용할 수 있습니다.

두 가지 종류의 스트림이 있습니다: "단일 구독" 스트림과 "브로드캐스트" 스트림.

단일 구독 스트림은 스트림의 전체 수명 동안 하나의 청취자만 허용합니다. 청취자가 없을 때 이벤트 생성을 시작하지 않으며 청취자가 구독을 취소하면 이벤트를 더 제공할 수 있는 이벤트 소스라도 이벤트 전송을 중단합니다.

단일 구독 스트림에 두 번 청취하는 것은 허용되지 않으며, 첫 번째 구독이 취소된 후에도 불가능합니다.

단일 구독 스트림은 일반적으로 파일 I/O와 같은 큰 연속 데이터의 청크를 스트리밍하는 데 사용됩니다.

브로드캐스트 스트림은 여러 청취자를 허용하며, 청취자가 있든 없든 이벤트가 준비되면 해당 이벤트를 발생시킵니다.

브로드캐스트 스트림은 독립적인 이벤트/옵저버에 사용됩니다.
{{</admonition>}}

```dart
Widget build(BuildContext context, WidgetRef ref) {
  Stream<User> user = ref.watch(userProvider.stream);
}
```

- `userProvider.future`를 사용해 가장 최근 상태값을 가진 Future를 얻을 수 있다.

{{<admonition tip>}}
What is Future?

지연된 계산을 나타내는 객체이다.

Future는 미래에 어떤 시점에 사용 가능한 잠재적인 값 또는 오류를 나타내기 위해 사용됩니다. Future의 수신자는 값 또는 오류를 처리하는 콜백을 등록할 수 있습니다. Future는 두 가지 방법으로 완료될 수 있습니다: 값으로 ("미래가 성공함") 또는 오류로 ("미래가 실패함"). 사용자는 각 경우에 대한 콜백을 설치할 수 있습니다.
{{</admonition>}}

### Select

widget/provider의 재빌드를 수를 감소하거나 제한하는 방법이 있다. 프로바이더를 지켜보는 것은, 그 프로바이더가 공개하는 객체의 모든 속성을 감시하는 것이다. 그러나 특정 경우에는 바라보는 범위를 좁히고 특정 속성만 모니터링 대상으로 만들 수 있다.

예를 들어, 프로바이더는 `User` 상태값을 가진다고 가정해본다.

```dart
abstract class User {
  String get name;
  int get age;
}
```

그런데 위젯에서는 단순히 `User`와 `name` 값만 사용하고 있다.

```dart
Widget build(BuildContext context, WidgetRef ref) {
  User user = ref.watch(userProvider);
  return Text(user.name);
}
```

만약 `ref.watch`를 사용하면 `User`의 `age` 속성이 변경되면 위젯이 재빌드 될 것이다.

여기서 해결방법은 `select`를 사용하는 것이다. select는 Riverpod에서 `User`의 특정 속성만 관찰하고 싶을 떄 사용한다. 앞서 widget을 다음과 같이 수정할 수 있다.

```dart
Widget build(BuildContext context, WidgetRef ref) {
  String name = ref.watch(userProvider.select((user) => user.name));
  return Text(name);
}
```

`select`를 통해 관찰하고 싶은 상태값을 선택하고 선택한 속성 값의 변화가 발생했을 때 사용할 수 있다.

그리고 `User` 값이 변하면, Riverpod은 이 함수를 호출해 이전 값과 새로운 값을 비교한다. 만약 상태값이 다르다면(예를 들어 name이 변경 되었다면), Riverpod은 위젯을 다시 빌드하는 작업을 처리할 것이다. 그러나 만약 값이 같다면(예를 들어 `age`만 변경되었다면), Riverpod은 위젯을 재빌드하지 않을 것이다.

{{<admonition info>}}
select는 ref.listen과 함께 사용할 수 있다.

```dart
ref.listen<String>(
  userProvider.select((user) => user.name),
  (String? previousName, String newName) {
    print('The user name changed $newName');
  }
);
```

{{</admonition>}}

{{<admonition tip>}}
`select`를 사용하는 경우 반환하는 값이 반드시 객체일 필요는 없다. `==` 연산자의 오버라이드로 객체 동일하다고 정의된다면 반환 값으로 무엇이 오든 상관없다.

```dart
final label = ref.watch(userProvider.select((user) => 'Mr ${user.name}'));
```

{{</admonition>}}

### FutureProvider

비동기 통신에 사용되는 Provider이다. 사용 방법은 다음과 같다.

#### lib/main.dart

```dart
final fetchUserProvider = FutureProvider((ref) async {
  const url = 'https://jsonplaceholder.typicode.com/todos/1';

  final res = await http.get(Uri.parse(url));

  logger.d(res.body);
  return User.fromJson(res.body);
});
```

`http` 라이브러리를 설치해서, http request를 쉽게 보내준다. `Uri`는 flutter 자체 내장 라이브러리이다. 가져온 데이터를 `User Model`에서 미리 만들어 둔, `fromJson`을 사용해서 가공해준다.

#### lib/user.dart

```dart
// ignore_for_file: public_member_api_docs, sort_constructors_first

import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

@immutable
class User {
  final int userId;
  final int id;
  final String title;
  final bool completed;

  const User({
    required this.userId,
    required this.id,
    required this.title,
    required this.completed,
  });

  Map<String, dynamic> toMap() {
    return <String, dynamic>{
      'userId': userId,
      'id': id,
      'title': title,
      'completed': completed,
    };
  }

  factory User.fromMap(Map<String, dynamic> map) {
    return User(
      userId: map['userId'] as int,
      id: map['id'] as int,
      title: map['title'] as String,
      completed: map['completed'] as bool,
    );
  }

  String toJson() => json.encode(toMap());

  factory User.fromJson(String source) =>
      User.fromMap(json.decode(source) as Map<String, dynamic>);

  User copyWith({
    int? userId,
    int? id,
    String? title,
    bool? completed,
  }) {
    return User(
      userId: userId ?? this.userId,
      id: id ?? this.id,
      title: title ?? this.title,
      completed: completed ?? this.completed,
    );
  }

  @override
  String toString() {
    return 'User(userId: $userId, id: $id, title: $title, completed: $completed)';
  }

  @override
  bool operator ==(covariant User other) {
    if (identical(this, other)) return true;

    return other.userId == userId &&
        other.id == id &&
        other.title == title &&
        other.completed == completed;
  }

  @override
  int get hashCode {
    return userId.hashCode ^ id.hashCode ^ title.hashCode ^ completed.hashCode;
  }
}
```

마지막으로 가장 핵심인 U를 보여주는 작업을 해준다. `FutureBuilder` 이므로 비동기적으로 데이터를 사용해야 한다. `when` 메서드를 사용해서 구현할 수 있다.

#### lib/home_screen.dart

```dart
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_state_management/main.dart';
import 'package:logger/logger.dart';

var logger = Logger();

class HomeScreen extends ConsumerWidget {
  const HomeScreen({super.key});

  // notifier가 상태 값을 변경하도록 도와준다.

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return ref.watch(fetchUserProvider).when(data: (data) {
      return Scaffold(
        appBar: AppBar(),
        body: Column(
          children: [
            Center(
              child: Text(data.userId.toString()),
            ),
            Center(
              child: Text(data.id.toString()),
            ),
            Center(
              child: Text(data.title),
            ),
            Center(
                child: Checkbox(
              onChanged: (value) => null,
              value: data.completed,
            ))
          ],
        ),
      );
    }, error: (error, st) {
      return Center(
        child: Text(
          error.toString(),
        ),
      );
    }, loading: () {
      return const Center(child: CircularProgressIndicator());
    });
  }
}
```

#### .family

`family`는 API 요청할 때 Query Parameter로 전달할 수 있도록 도와주는 라이브러리이다.

예를 들어, family을 FutureProvider와 결합해 원하는 ID의 데이터를 가져올 수 있다.

```dart
final messagesFamily = FutureProvider.family<Message, String>((ref, id) async {
  return dio.get('http://my_api.dev/messages/$id');
});
```

provider에 호출할 때는 편하게 매개변수로 넣어주면 된다.

```dart
class _MyHomePageState extends ConsumerState<MyHomePage> {
  String userNo = '1';

  @override
  Widget build(BuildContext context) {
    return ref.watch(fetchUserProvider(userNo)).when(data: (data) {
      return Scaffold(
        appBar: AppBar(),
        body: Column(
          children: [
            TextField(
              onSubmitted: (value) => setState(() {
                userNo = value;
              }),
            ),
  ...
  ]))})}}
```

