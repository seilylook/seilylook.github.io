# Flutter Firebase


# Introduction

기존에 만들던 `Calendar Scheduler` 앱에 `Firebase`의 `FireStore` 데이터베이스를 연결해준다.

## Dependency

```yaml
dependencies:
  flutter:
    sdk: flutter

  # The following adds the Cupertino Icons font to your application.
  # Use with the CupertinoIcons class for iOS style icons.
  cupertino_icons: ^1.0.2
  table_calendar: ^3.0.9
  intl: ^0.18.1
  drift: ^2.14.1
  sqlite3_flutter_libs: ^0.5.18
  path_provider: ^2.1.1
  path: ^1.8.3
  get_it: ^7.6.4
  dio: ^5.4.0
  provider: ^6.1.1
  uuid: ^4.2.2
  firebase_core: ^2.24.2
  cloud_firestore: ^4.13.6
```

## `Firebase`란?

파이어베이스는 구글이 인수한 모바일 앱 개발에 최적화된 기능을 제공하는 서비스이다. 플러터 뿐만 아니라 다른 앱 개발 프레임워크 그리고 웹이나 서버에서도 이용할 수 있다. 파이어베이스으이 데이터베이스 기능인 `Firestore`를 사용할 수 있다.

## `Firestore`란?

파이어스토어는 `NoSQL` 데이터베이스이다. 필요한 서버와 인프라 관리를 구글에서 해주기 때문에 백엔드 프로그래밍에 대해 크게 신경쓸 필요가 없다. 클라이언트와 서버의 데이터를 실시간으로 연동하고 오프라인 지원이 자동으로 되어서 네트워크 지연과 인터넷 연결과 관계없이 데이털르 저장할 수 있다. 또한 파이어베이스에서 제공하는 파이어스토어 SDK를 사용하면 따로 HTTP 요청 코드를 작성할 필요 없이 제공되는 SDK로 직관적으로 프로그래밍 할 수 있다.

파이어스토어는 NoSQL 답게 두 가지 데이터 개념이 있다. `Collection`과 `Document`이다. SQL 기반의 데이터베이스와 비교하면 컬렉션은 테이블에 해당되고 문서는 열에 해당된다. NoSQL 문서는 SQL 데이터베이스와 비교해 더 유연한 데이터 구조를 사용할 수 있다. 예를 들어 SQL의 테이블에는 행과 열의 조합으로 하나의 행과 열 조합에는 하나의 값만 입력할 수 있다. 하지만 NoSQL의 문서에서는 키와 값의 조합으로 하나의 값이 들어가는 위치에 리스트나 맵 등 완전한 JSON 구조를 통째로 넣을 수 있다.

### 파이어스토어 문서 삽입

파이어스토어에 문서를 삽입하는 방법은 대표적으로 두가지가 있다. 첫 번째로 `add()` 함수를 이용한 삽입 방법이다. `add()` 함수를 이용해서 문서를 삽입하면 파이어스토어에서 자동으로 문서의 ID 값을 생성해준다.

```dart
final data = {
    'name': 'seilylook',
    'age': 31,
    'favorites': ['guitar', 'coffee', 'beer']
};

FirebaseFirestore.instance
.collection('person')
.add(data);
```

### 파이어스토어 문서 조회

파이어스토어는 아주 강력한 문서 조회 기능을 제공한다. 데이터가 변경될 때마다 실시간으로 (Stream) 업데이트를 받영받을 수 있고 1회성으로 (Future) 데이터를 업데이트 받을 수 있다.

```dart
FirebaseFirestore.intance
.collection('person')
.snapshots();
```

`collection()` 함수에 `snapshots()` 함수를 실행하면 컬렉션의 모든 문서를 Stream<QuerySnapshot> 형태로 받아올 수 있다. Stream 형태로 받아오기 때문에 컬렉션의 데이터가 업데이트되면 즉시 화면에 반영된다.

Stream 형태로 문서를 받아오면 데이터 조회를 과도하게 많이 하게 될 수 있다. 그래서 파이어스토어는 Future 형태로 일회성으로 데이털르 가져오는 기능도 제공한다.

```dart
FirebaseFirestore.intance
.collection('person')
.get();
```

`get()` 함수를 실행하면 Future<QuerySnapshot>이 반환된다. 즉 실행하는 순간 한 번만 데이터를 받아오고 지속적으로 업데이트 하지 않는다.

## 파이어베이스 및 파이어스토어 설치 및 설정

### 파이어베이스 CLI 설치 및 로그인하기

```shell
curl -sL https://firebase.tools | bash
```

CLI를 설치해주고 구글 아이디를 통해 로그인을 해준다.

```shell
firebase login
```

### 프로젝트에 파이어베이스 추가하기

플러터 프로젝트에 파이어베이스 설정을 추가하려면 `FlutterFire CLI`를 설치하고 설정 기능을 실행해줘야 한다.

#### 터미널에서 아래의 명령어를 입력해 FlutterFire CLI를 설치해준다.

```shell
dart pub global activate flutterfire_cli
```

#### 환경 변수를 설정해준다.

```shell
export PATH="$PATH":"$HOME/.pub-cache/bin"
```

#### 파이어베이스 console로 가서 프로젝트를 생성해준다.

<img src="/images/firestore/firestore-connection-1.png" />

#### 프로젝트 연결

```shell
cd calendar_scheduler

flutterfire configure
```

프로젝트 설정이 완료되면 lib/firebase_option.dart 파일이 생성된다.

#### 파이어스토어 데이터베이스 생성하기

Firebase console로 이동해서

1. 빌드 탭 클릭

2. Firestore database 탭 클릭

3. 규칙을 `allow read, write: if true;`로 바꿔준다.

<img src="/images/firestore/firestore-connection-4.png" />

<img src="/images/firestore/firestore-connection-3.png" />

## 구현

### firebase_coer를 통해 프로젝트에 파이어베이스 연결

firebase_core 플러그인에서 제공하는 `Firebase.initializeApp()` 함수를 사용하면 플러터 앱에 파이어베이스 설정을 추가할 수 있다.

```dart
import 'package:calendar_scheduler/screens/home_screen.dart';
import 'package:flutter/material.dart';
import 'package:intl/date_symbol_data_local.dart';
import 'package:firebase_core/firebase_core.dart';
import 'package:calendar_scheduler/firebase_options.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();

  await Firebase.initializeApp(
    options: DefaultFirebaseOptions.currentPlatform,
  );

  await initializeDateFormatting();

  runApp(
    const MyApp(),
  );
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      home: HomeScreen(),
    );
  }
}
```

### 일정 데이터 삽입

widgets/schedule_bottom.dart 파일에 있는 ScheduleBottomSheet 위젯의 `onSavePressed()` 함수에서 저장 기능을 실행한다.

```dart
  void onSavePressed(BuildContext context) async {
    if (formKey.currentState!.validate()) {
      formKey.currentState!.save();

      final schedule = ScheduleModel(
        id: Uuid().v4(),
        content: content!,
        date: widget.selectedDate,
        startTime: startTime!,
        endTime: endTime!,
      );

      await FirebaseFirestore.instance
          .collection(
            'schedule',
          )
          .doc(schedule.id)
          .set(schedule.toJson());

      Navigator.of(context).pop();
    }
  }
```

<img src="/images/firestore/firestore-connection-2.png" />

### 일정 데이터 받아오기

lib/screens/home_screen.dart 파일의 HomeScreen 위젯에서 더는 `provider`가 필요 없다. 파이어베이스에서 바로 데이터를 가져올 수 있기 때문이다.

Provider를 사용할 때는 provider의 내부에서 선택된 날짜를 관리했다. 하지만 이제는 provider를 사용하지 않으니 HomeScreen을 `StatefulWidget`으로 변경해서 선택된 날짜와 관련된 상태 관리를 해준다.

```dart
import 'package:calendar_scheduler/constants/constants.dart';
import 'package:calendar_scheduler/model/schedule_model.dart';
import 'package:calendar_scheduler/widgets/main_calendar.dart';
import 'package:calendar_scheduler/widgets/schedule_bottom_sheet.dart';
import 'package:calendar_scheduler/widgets/schedule_card.dart';
import 'package:calendar_scheduler/widgets/today_banner.dart';
import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:flutter/material.dart';

class HomeScreen extends StatefulWidget {
  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  DateTime selectedDate = DateTime.utc(
    // ➋ 선택된 날짜를 관리할 변수
    DateTime.now().year,
    DateTime.now().month,
    DateTime.now().day,
  );

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      floatingActionButton: FloatingActionButton(
        // ➊ 새 일정 버튼
        backgroundColor: PRIMARY_COLOR,
        onPressed: () {
          showModalBottomSheet(
            // ➋ BottomSheet 열기
            context: context,
            isDismissible: true, // ➌ 배경 탭했을 때 BottomSheet 닫기
            isScrollControlled: true,
            builder: (_) => ScheduleBottomSheet(
              selectedDate: selectedDate, // 선택된 날짜 (selectedDate) 넘겨주기
            ),
          );
        },
        child: const Icon(
          Icons.add,
        ),
      ),
      body: SafeArea(
        // 시스템 UI 피해서 UI 구현하기
        child: Column(
          // 달력과 리스트를 세로로 배치
          children: [
            MainCalendar(
              selectedDate: selectedDate, // 선택된 날짜 전달하기

              // 날짜가 선택됐을 때 실행할 함수
              onDaySelected: (selectedDate, focusedDate) =>
                  onDaySelected(selectedDate, focusedDate, context),
            ),
            const SizedBox(height: 8.0),
            StreamBuilder<QuerySnapshot>(
              stream: FirebaseFirestore.instance
                  .collection(
                    'schedule',
                  )
                  .where(
                    'date',
                    isEqualTo:
                        '${selectedDate.year}${selectedDate.month}${selectedDate.day}',
                  )
                  .snapshots(),
              builder: (context, snapshot) {
                return TodayBanner(
                  selectedDate: selectedDate,
                  count: snapshot.data?.docs.length ?? 0,
                );
              },
            ),
            const SizedBox(height: 8.0),
            Expanded(
                child: StreamBuilder<QuerySnapshot>(
              stream: FirebaseFirestore.instance
                  .collection(
                    'schedule',
                  )
                  .where(
                    'date',
                    isEqualTo:
                        '${selectedDate.year}${selectedDate.month}${selectedDate.day}',
                  )
                  .snapshots(),
              builder: (context, snapshot) {
                if (snapshot.hasError) {
                  return const Center(
                    child: Text('일정 정보를 가져오지 못했습니다.'),
                  );
                }
                if (snapshot.connectionState == ConnectionState.waiting) {
                  return const Center(
                    child: CircularProgressIndicator(),
                  );
                }

                final schedules = snapshot.data!.docs
                    .map(
                      (QueryDocumentSnapshot e) => ScheduleModel.fromJson(
                          json: (e.data() as Map<String, dynamic>)),
                    )
                    .toList();

                return ListView.builder(
                  itemCount: schedules.length,
                  itemBuilder: (context, index) {
                    final schedule = schedules[index];

                    return Dismissible(
                      key: ObjectKey(schedule.id),
                      direction: DismissDirection.startToEnd,
                      onDismissed: (DismissDirection direction) {
                        FirebaseFirestore.instance
                            .collection('schedule')
                            .doc(schedule.id)
                            .delete();
                      },
                      child: Padding(
                        padding: const EdgeInsets.only(
                            left: 8.0, right: 8.0, bottom: 8.0),
                        child: ScheduleCard(
                          startTime: schedule.startTime,
                          endTime: schedule.endTime,
                          content: schedule.content,
                        ),
                      ),
                    );
                  },
                );
              },
            ))
          ],
        ),
      ),
    );
  }

  void onDaySelected(
    DateTime selectedDate,
    DateTime focusedDate,
    BuildContext context,
  ) {
    setState(() {
      this.selectedDate = selectedDate;
    });
  }
}
```

1. `FirebaseFirestore.collection('schedule').snapshots()`를 실행하면 파이어스토어의 schedule 컬렉션에 있는 모든 데이터를 스트림으로 받아올 수 있다. 하지만 가져오고 싶은 일정은 selectedDate 값과 date 속성이 같은 일정이기 때문에 `where()` 함수를 싱행해서 필터를 진행한다. `where()` 함수의 첫 번째 매개변수에는 필터를 적용할 필드인 `date`를 입력하고 `isEqualTo` 매개변수에 등가비교할 값인 `selectedDate`를 년, 월, 일 순으로 입력해준다.

2. `QuerySnapshot`의 `data.docs` 값을 불러오면 쿼리에서 제공받은 모든 데이터를 리스트로 받아올 수 있다. 이 각 값은 `QueryDocumentSnapshot` 형태로 제공된다. `ScheduleModel.fromJson` 생성자는 `Map<String, dynamic>` 형태를 입력받기 때문에 `QueryDocumentSnapshot`에 `data()` 함수를 실행해서 `Map<String, dynamic>` 형태로 데이터를 전환하면 `ScheduleModel`로 데이터를 매핑할 수 있다.

