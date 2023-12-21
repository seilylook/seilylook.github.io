# Flutter Calendar Scheduler


# Introduction

달력 형태의 위젯인 `TableCalendar`를 사용해서 일정 관리 앱 구현.

## Dependency

### Client

- `table_calendar`

- `intl`

- `drift`

- `sqlite3_flutter_libs`

- `path_provider`

- `path`

- `get_it`

- `dio`

- `provider`

- `uuid`

### Server

- `NestJS`

### DB

- `SQLite`

- `Firebase`

## UI 구현

### 테마 색상 설정

#### lib/constants/color.dart

이번 프로젝트에서 사용할 색상은 세 가지이다. 주색상인 초록색, 옅은 회색, 어두운 회색 그릭고 텍스트 필드 배경색이다.

```dart
import 'package:flutter/material.dart';

const PRIMARY_COLOR = Color(0xFF0DB2B2);
final LIGHT_GREY_COLOR = Colors.grey[200]!;
final DARK_GREY_COLOR = Colors.grey[600]!;
final TEXT_FIELD_COLOR = Colors.grey[300]!;
```

### 달력 구현

HomeScreen의 화면 윗부분의 달력을 `MainCalendar` 클래스로 만들어준다.

#### lib/위젯s/main_calendar.dart

```dart
import 'package:calendar_scheduler/constants/constants.dart';
import 'package:flutter/material.dart';
import 'package:table_calendar/table_calendar.dart';

class MainCalendar extends Stateless위젯 {
  final OnDaySelected onDaySelected;
  final DateTime selectedDate;

  const MainCalendar({
    super.key,
    required this.onDaySelected,
    required this.selectedDate,
  });

  @override
  위젯 build(BuildContext context) {
    return TableCalendar(
      onDaySelected: onDaySelected,
      selectedDayPredicate: (date) =>
          date.year == selectedDate.year &&
          date.month == selectedDate.month &&
          date.day == selectedDate.day,
      firstDay: DateTime(1800, 1, 1),
      lastDay: DateTime(3000, 1, 1),
      focusedDay: DateTime.now(),
      headerStyle: const HeaderStyle(
        titleCentered: true,
        formatButtonVisible: false,
        titleTextStyle: TextStyle(
          fontWeight: FontWeight.bold,
          fontSize: 16.0,
        ),
      ),
      calendarStyle: CalendarStyle(
        isTodayHighlighted: false,
        defaultDecoration: BoxDecoration(
          borderRadius: BorderRadius.circular(6.0),
          color: LIGHT_GREY_COLOR,
        ),
        weekendDecoration: BoxDecoration(
          borderRadius: BorderRadius.circular(6.0),
          color: LIGHT_GREY_COLOR,
        ),
        selectedDecoration: BoxDecoration(
          borderRadius: BorderRadius.circular(6.0),
          border: Border.all(
            color: PRIMARY_COLOR,
            width: 1.0,
          ),
        ),
        defaultTextStyle: TextStyle(
          fontWeight: FontWeight.w600,
          color: DARK_GREY_COLOR,
        ),
        weekendTextStyle: TextStyle(
          fontWeight: FontWeight.w600,
          color: DARK_GREY_COLOR,
        ),
        selectedTextStyle: const TextStyle(
          fontWeight: FontWeight.w600,
          color: PRIMARY_COLOR,
        ),
      ),
    );
  }
}
```

- `firstDay`의 매개변수는 ㄷ달력에서 선택할 수 있는 가장 오래된 날짜를 의미한다. `lastDay` 매개변수는 달력에서 선택할 수 있는 제일 미래의 날짜를 의미한다. `focusedDay`는 현재 달력이 화면에서 보여줄 날짜를 의미한다.

- `headerStyle`은 화면 상단의 month && 화살표에 대한 스타일을 지정할 수 있다. `calendarStylee`은 달력의 스타일을 지정할 수 있다.

- `OnDaySelected`는 `table_calendar` 플러그인에서 기본 제공하는 typedef 이다. `onDaySelected`는 달력의 날짜가 탭될 때마다 실행된다. 첫 번째 매개 변수에 선택된 날짜(selectedDay)를 입력받고 두 번째 매개 변수에 현재 화면에 보이는 날짜를 입력받는다(focusedDay).

- `selectedDayPredicatee`는 어떤 날짜를 선택된 날짜로 지정할지 결정하는 함수이다. 현재 달력에 보이는 모든 날짜를 순회하며 실행하는 함수로 true가 반횐되면 선택된 날짜로 표시학고 false가 반환되면 선택되지 않은 날짜로 지정한다.

### 선택된 날의 일정 보여주기: ScheduleCard 위젯

선택된 날짜에 해당되는 일정을 보여주는 위젯을 만들어준다. 각 일정은 시간(시작 시간부터 종료 시간)과 내용으로 이루어져 있다.

#### lib/위젯s/schedule_card.dart

```dart
import 'package:calendar_scheduler/constants/constants.dart';
import 'package:flutter/material.dart';

class ScheduleCard extends Stateless위젯 {
  final int startTime;
  final int endTime;
  final String content;
  const ScheduleCard({
    super.key,
    required this.startTime,
    required this.endTime,
    required this.content,
  });

  @override
  위젯 build(BuildContext context) {
    return Container(
      decoration: BoxDecoration(
        border: Border.all(
          width: 1.0,
          color: PRIMARY_COLOR,
        ),
        borderRadius: BorderRadius.circular(8.0),
      ),
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: IntrinsicHeight(
          child: Row(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              _Time(
                startTime: startTime,
                endTime: endTime,
              ),
              const SizedBox(width: 16.0),
              _Content(content: content),
              const SizedBox(width: 16.0),
            ],
          ),
        ),
      ),
    );
  }
}

class _Time extends Stateless위젯 {
  final int startTime;
  final int endTime;

  const _Time({
    required this.startTime,
    required this.endTime,
  });

  @override
  위젯 build(BuildContext context) {
    const textStyle = TextStyle(
      fontWeight: FontWeight.w600,
      color: PRIMARY_COLOR,
      fontSize: 16.0,
    );

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          '${startTime.toString().padLeft(2, '0')}:00',
          style: textStyle,
        ),
        Text(
          '${endTime.toString().padLeft(2, '0')}:00',
          style: textStyle.copyWith(
            fontSize: 10.0,
          ),
        )
      ],
    );
  }
}

class _Content extends Stateless위젯 {
  final String content;
  const _Content({
    required this.content,
  });

  @override
  위젯 build(BuildContext context) {
    return Expanded(
      child: Text(
        content,
      ),
    );
  }
}
```

`_Time`: 시간을 표현해주는 위젯이다.

`_Content`: 일정을 알려주는 위젯이다.

`IntrinsicHeight`: 내부 위젯들의 높이를 최대 높이로 맞춰준다. \_Time 위젯은 Column 위젯을 사용 중익기 때문에 ScheduleCard 위젯의 최대 크기만큼 높이를 차지한다. \_Content 위젯은 Column 위젯을 사용하지 않기 때문에 최소 크기만 차지하며 세로로 가운데 정렬이 이루어진다.

### 오늘 날짜를 보여주기: TodayBanner 위젯

`TodayBanner` 위젯은 MainCalendar 위젯과 ScheduleCard 위젯 사이에 오늘 날짜를 보여준다.

#### lib/위젯s/today_banneer.dart

```dart
import 'package:calendar_scheduler/constants/constants.dart';
import 'package:flutter/material.dart';

class TodayBanner extends Stateless위젯 {
  final DateTime selectedDate;
  final int count;
  const TodayBanner({
    super.key,
    required this.selectedDate,
    required this.count,
  });

  @override
  위젯 build(BuildContext context) {
    const textStyle = TextStyle(
      fontWeight: FontWeight.w600,
      color: Colors.white,
    );

    return Container(
      color: PRIMARY_COLOR,
      child: Padding(
        padding: const EdgeInsets.symmetric(horizontal: 16.0, vertical: 8.0),
        child: Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Text(
              '${selectedDate.year}년 ${selectedDate.month}월 ${selectedDate.day}일',
              style: textStyle,
            ),
            Text(
              '$count개',
              style: textStyle,
            ),
          ],
        ),
      ),
    );
  }
}
```

`HomeScreen`의 `MainCalendar`와 `ScheduleCard` 사이에 넣어준다.

### 일정 작성하기

`ScheduleBottomSheet`는 사용자가 새로 추가할 일정을 입력할 수 있는 위젯이다. 텍스트 필드 3개와 버튼 하나로 이루어져 있다. 시작 시간, 종료 시간, 일정 내용을 입력한 후 저장 버튼을 누르면 선택된 날짜를 기준으로 일정을 생성한다.

#### lib/위젯s/schedule_bottom_sheet.dart

```dart
import 'package:calendar_scheduler/constants/constants.dart';
import 'package:calendar_scheduler/위젯s/custom_text_field.dart';
import 'package:flutter/material.dart';

class ScheduleBottomSheet extends Stateful위젯 {
  const ScheduleBottomSheet({super.key});

  @override
  State<ScheduleBottomSheet> createState() => _ScheduleBottomSheetState();
}

class _ScheduleBottomSheetState extends State<ScheduleBottomSheet> {
  @override
  위젯 build(BuildContext context) {
    final bottomInset = MediaQuery.of(context).viewInsets.bottom;

    return SafeArea(
      child: Container(
        height: MediaQuery.of(context).size.height / 2 + bottomInset,
        color: Colors.white,
        child: Padding(
          padding:
              EdgeInsets.only(left: 8, right: 8, top: 8, bottom: bottomInset),
          child: Column(
            children: [
              const Row(
                children: [
                  Expanded(
                    child: CustomTextField(
                      label: '시작 시간',
                      isTime: true,
                    ),
                  ),
                  SizedBox(width: 16.0),
                  Expanded(
                    child: CustomTextField(
                      label: '종료 시간',
                      isTime: true,
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 8.0),
              const Expanded(
                child: CustomTextField(
                  label: '내용',
                  isTime: false,
                ),
              ),
              SizedBox(
                width: double.infinity,
                child: ElevatedButton(
                  onPressed: onSavePressed,
                  style: ElevatedButton.styleFrom(
                    backgroundColor: PRIMARY_COLOR,
                  ),
                  child: const Text('저장'),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  void onSavePressed() {}
}
```

`HomeScreen`에서 `FloatingActionButton`을 누르면 ScheduleBottomSheet가 화면에 나오도록 동작한다.

- `floatingActionButton`매개 변수에 FloatingActionButton 위젯을 입력해준 후 bottom sheet를 실행하는 `showModalButtomSheet()` 함수를 이용해서 ScheduleBottomSheet 위젯을 bottom sheet로 실행한다.

- `showModalBottomSheet`의 `isDismissible` 매개 변수에 true 값을 입력해서 배경을 눌렀을 때 ScheduleBottomSheet가 닫히게 해준다.

### 일정 내용 필드 구현

#### lib/위젯s/custom_text_field.dart

```dart
import 'package:calendar_scheduler/constants/constants.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

class CustomTextField extends Stateless위젯 {
  final String label;
  final bool isTime;
  const CustomTextField({
    super.key,
    required this.label,
    required this.isTime,
  });

  @override
  위젯 build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          label,
          style: const TextStyle(
            color: PRIMARY_COLOR,
            fontWeight: FontWeight.w600,
          ),
        ),
        Expanded(
          flex: isTime ? 0 : 1,
          child: TextFormField(
            cursorColor: Colors.grey,
            maxLines: isTime ? 1 : null,
            expands: !isTime,
            keyboardType:
                isTime ? TextInputType.number : TextInputType.multiline,
            inputFormatters: isTime
                ? [
                    FilteringTextInputFormatter.digitsOnly,
                  ]
                : [],
            decoration: InputDecoration(
              border: InputBorder.none,
              filled: true,
              fillColor: Colors.grey[300],
              suffixText: isTime ? '시' : null,
            ),
          ),
        ),
        TextFormField(),
      ],
    );
  }
}
```

플러터에서 텍스트 필드는 `TextField` VS `TextFormField`로 나눌 수 있다. TextField 위젯은 각 텍스트 필드가 독립된 형태일 때 많이 사용되고 TextFormField는 여러개의 텍스트 필드를 하나의 폼으로 제어할 때 사용한다. 저장 버튼을 눌렀을 때 시간 텍스트(시작, 종료) 필드 2개와 내용 텍스트 필드 하나를 제어할 계획이니 `TextFormField`를 사용해준다.

텍스트 필드의 제목과 텍스트 필드가 위아래로 위치해야 하므로 Column 위젯을 사용해서 Text 위젯과 TextFormField 위젯을 세로로 배치해준다.

- `maxLines`: 텍스트 필드에 값을 입력할 때 허락되는 최대 줄 개수이다. int 값을 입력할 수 있으며 null을 넣으면 개수를 제한하지 않는다. 시간을 입력할 때는 한 줄만 입력하도록 하고 아니면 제한을 두지 않는다.

- `expands`: 텍스트 필드를 부모 위젯 크기만큼 세로로 늘릴지 결정한다. 기본값은 false이며 true로 입력하면 부모의 위젯 크기만큼 텍스트 필드를 늘릴 수 있다.

- `keyboardType`: 텍스트 필드를 선택했을 때 화면에 어떤 키보드가 보여질 지 선택할 수 있다. `TextInputType.number`는 숫자만 입력하는 키보드를 보여줄 수 있고 `TextInputType.multIline`은 줄바꿈 키가 존재하는 일반 키보드를 보여줄 수 있다.

- `inputFormatters`: 텍스트 필드에 입력되는 값들을 제한할 수 있다. 어뜻 보면 키보드의 종류를 정의 하는 keyboardType 과 비슷해보이지만 큰 차이가 있다. keyboardType 매개변수는 핸드폰에서 보여주는 키보드만 제한할 수 있고 블루투스 키보드나 보안 키보드처럼 커스텀 구현된 키보드를 사용할 때는 입력되는 값을 제한할 수 없다. inputFormatters 매개변수의 경우 특정 입력 자체를 강제할 수 있다. 리스트로 원하는 만큼 제한을 넣어줄 수 있으며 `FilteringTextInputFormatter.digitsOnly`는 숫자만 입력되도록 제한한다.

- 시간과 관련된 텍스트 필드는 최소한의 높이를, 내용 텍스트 필드는 최대한의 높이를 차지한다. 추가적으로 `isTime`을 false로 지정할 경우 `expands` 매개변수가 true로 지정되니 Column 위젯 안에서 최대한 크기를 차지하도록 Expanded 위젯을 사용해줘야 한다.

- 시작 시간과 종료 시간을 표현할 텍스트 필드는 하나의 `Row` 위젯에 감싸서 좌우로 펼쳐지게 한다. 그리고 해당 Row 위젯을 `Column` 위젯에 한 번 더 감싸서 내용을 담는 텍스트 필드가 남는 공간을 모두 차지하게 한다. 마지막으로 `ElevatedButton`을 하단에 추가해준다.

- `MediaQuery`의 `viewInsets`를 가져오면 시스템이 차지하는 화면 아랫부분 크기를 알 수 있다. 일반적으로 이 값은 키보드가 보일 때 차지하는 크기가 된다. 최대 높이에 키보드 크기만큼 높이를 더해줘서 키보드가 화면에 보일 때 컨테이너 크기를 늘려준다. `Container`의 높이가 늘어난 만큼 아래에 패딩을 추가해줘서 위젯들이 잘 보이는 위치로 끌어올려 준다.

#### lib/screens/home_screen.dart

```dart
import 'package:calendar_scheduler/constants/constants.dart';
import 'package:calendar_scheduler/widgets/main_calendar.dart';
import 'package:calendar_scheduler/widgets/schedule_bottom_sheet.dart';
import 'package:calendar_scheduler/widgets/schedule_card.dart';
import 'package:calendar_scheduler/widgets/today_banner.dart';
import 'package:flutter/material.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  DateTime selectedDate = DateTime.utc(
    DateTime.now().year,
    DateTime.now().month,
    DateTime.now().day,
  );

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      floatingActionButton: FloatingActionButton(
        backgroundColor: PRIMARY_COLOR,
        onPressed: () {
          showModalBottomSheet(
            context: context,
            isDismissible: true,
            builder: (_) => ScheduleBottomSheet(),
            isScrollControlled: true,
          );
        },
        child: const Icon(
          Icons.add,
        ),
      ),
      body: SafeArea(
        child: Column(
          children: [
            MainCalendar(
              selectedDate: selectedDate,
              onDaySelected: onDaySelected,
            ),
            TodayBanner(selectedDate: selectedDate, count: 0),
            const SizedBox(height: 8.0),
            ScheduleCard(startTime: 12, endTime: 14, content: 'flutter 프로젝트'),
          ],
        ),
      ),
    );
  }

  void onDaySelected(DateTime selectedDate, DateTime focusedDate) {
    setState(() {
      this.selectedDate = selectedDate;
    });
  }
}
```

`HomeScreen` 위젯에서 `showModalBottomSheet()` 함수를 약간 변경해줘야 한다. showModalBottomSheet() 함수는 기본적으로 최대 높이를 화면의 밖으로 규정한다. 하지만 `isScrollControlled` 매개변수에 true를 넣어주면서 간단하게 최대 높이를 화면 전체로 변경할 수 있다. 코드를 변경한 후 `ScheduleBottomSheet`에서 텍스트 필드를 선택할 경우 키보드가 보이는 만큼 ScheduleBottomSheet 위젯이 위로 이동되는 것을 볼 수 있다.

### i18n 적용하기

`intl` 패키지와 `TableCalendar`의 언어를 변경한다. main.dart 파일에서 intl 패키지를 초기화해준다. main() 함수를 비동기로 변경하고 코드 두 줄을 추가해서 간단하게 intl 패키지를 프로젝트에서 사용할 수 있다.

```dart
import 'package:calendar_scheduler/screens/home_screen.dart';
import 'package:flutter/material.dart';
import 'package:intl/date_symbol_data_local.dart';

void main() async {
  WidgetsFlutterBinding();
  await initializeDateFormatting();
  runApp(const MyApp());
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

## DB 연결

`Drift` 플러그인을 사용하면 직접 SQL을 작성하지 않고도 SQLite를 사용할 수 있다.

{{<admonition tip SQLite>}}
SQLite는 프론트엔드에서 흔히 사용하는 가벼운 데이터베이스이다.
{{</admonition>}}

### Model 구축

드리프트를 사용하면 클래스를 선언해서 테이블을 생성할 수 있다. 테이블은 드리프크 패키지의 Table 클래스를 상속하면 선언할 수 있다. 그 다음 자식 클래스에 열로 정의하고 싶은 값들을 Getter로 선언해주면 된ㄷ다. 열 선언은 세가지 요로소 나누어 진다. 열의 타입, 열의 이름, 열의 속성읻다. 열의 타입으로는 IntColumn, TextColumn, DateTimeColumn 등이 있다.

#### lib/model/schedules.dart

```dart
import 'package:drift/drift.dart';

class Schedules extends Table {
  IntColumn get id => integer().autoIncrement()();
  TextColumn get content => text()();
  DateTimeColumn get date => dateTime()();
  IntColumn get startTime => integer()();
  IntColumn get endTime => integer()();
}
```

드리프트에 생성한 `Schedules` 테이블을 등록해주면 자동으로 테이블과 관련된 기능을 코드로 생성한다.

{{<admonition info Part>}}
어떤 플러터 패키지에서든 코드 생성을 사용하려면 `part` 파일을 지정해줘야 한다. `part` 파일은 `part` 키워드를 사용해서 지정하면 된다. 코드 생성을 사용하는 각각 패키지별로 `part` 파일의 이름 패턴은 약간 다르지만, 대부분은 현재 파일 이름에 `.g.dart`를 추가하는 형식이다. 드리프트 또한 현재 파일명에 `.g.dart`를 추가하면 된다. 해당 파일이 아직 존재하지 않을 때 코드 생성을 실행하면 자동으로 `<FILENAME>.g.dart`가 생성된다.
{{</admonition>}}

#### lib/database/schedule.dart

```dart
import 'dart:io';

import 'package:calendar_scheduler/model/schedule.dart';
import 'package:drift/drift.dart';
import 'package:drift/native.dart';
import 'package:path_provider/path_provider.dart';
import 'package:path/path.dart' as p;

part 'drift_database.g.dart';

@DriftDatabase(
  tables: [
    Schedules,
  ],
)
class LocalDatabase extends _$LocalDatabase {
  LocalDatabase() : super(_openConnection());
  Stream<List<Schedule>> watchSchedules(DateTime date) =>
      (select(schedules)..where((tbl) => tbl.date.equals(date))).watch();

  Future<int> createSchedule(SchedulesCompanion data) =>
      into(schedules).insert(data);

  Future<int> removeSchedule(int id) =>
      (delete(schedules)..where((tbl) => tbl.id.equals(id))).go();

  @override
  int get schemaVersion => 1;
}

LazyDatabase _openConnection() {
  return LazyDatabase(() async {
    final dbFolder = await getApplicationDocumentsDirectory();
    final file = File(p.join(dbFolder.path, 'db.sqlite'));
    return NativeDatabase(file);
  });
}
```

1. 드리프트 관련 쿼리를 작성할 클래스를 하나 작성하고 이 클래스의 이름 앞에 `_$`를 추가한 부모 클래스를 상속한다. 이 클래스는 현재 존재하지 않지만 코드 생성을 실행하면 생성된다.

{{<admonition tip>}}
`part` 파일은 import와 비슷한 기능을 갖고 있다. part 파일로 파일을 지정하면 해당 파일의 값들을 현재 파일에서 사용할 수 있다. 하지만 public 값들만 사용할 수 있는 import 기능과 달리 part 파일은 private 값들도 사용가능 하기에 보안에 유의해야 한다.
{{</admonition>}}

2. 이제 코드 생성을 통해 쿼리를 작성하는 데 필요한 기능을 생성해야 한다. `flutter pub run build_runner build` 명령어를 실행해서 코드 생성을 진행한다.

- `watchSchedules`: 이 함수가 반환하는 값을 `watch()` 또는 `get()` 함수를 실행할 수 있다. 특정 날짜에 해당되는 일정만 불러오기 때문에 `where` 함수를 통해서 관련 일정을 먼저 필터링해야 한다. 결론적으로 `where()` 함수가 아닌 `select()` 함수에 `watch()` 함수가 직접 실행되어야 하기 때문에 괄호가 한 번 더 감싸진 형태이다.

- `createSchedule`: `into()` 함수를 먼저 사용해서 어떤 테이블에 데이터를 넣을 지 지정해준 다음 `insert()` 함수를 이어서 사용해야 한다. 추가적으로 코드 생성을 실행하면 몯든 테이블의 `Companion` 클래스가 생성된다. 데이터를 생성할 때는 꼭 생성된 `Companion` 클래스를 통해서 값들을 넣어줘야 하기 때문에 Schedules 테이블에 해당되는 SchedulesCompanion 클래스를 입력받아서 insert() 함수에 전달해준다.

- `removeSchedule`: `delete()` 함수에는 `go()` 함수를 실행해줘야 삭제가 된다. 특정 ID에 해당되는 값만 삭제해야 하니 매개 변수에 id를 입력받고 해당 id에 일치하는 일정만 삭제해준다.

- 드리프트 데이터베이스 클래스는 필수로 `schemaVersion` 값을 지정해줘야 한다. 기본적으로 1부터 시작하고 테이블의 변화가 있을 때마다 1씩 올려줘서 테이블 구조가 변경된다는 걸 드리프트에 인지키셔주는 기능이다.

- 드리프트 테이터베이스 객체는 부모 생성자에 `LazyDatabase`를 필수로 넣어줘야 한다. `LazyDatabase` 객체에는 데이터베이스를 생성할 위치에 대한 정보를 입력해준다.

### 데이터베이스 초기화

#### lib/main.dart

```dart
import 'package:calendar_scheduler/screens/home_screen.dart';
import 'package:flutter/material.dart';
import 'package:intl/date_symbol_data_local.dart';
import 'package:calendar_scheduler/database/drift_database.dart';
import 'package:get_it/get_it.dart';

void main() async {
  WidgetsFlutterBinding();
  await initializeDateFormatting();
  final database = LocalDatabase();
  GetIt.I.registerSingleton<LocalDatabase>(database);
  runApp(const MyApp());
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

미리 정의핻둔 `LocalDatabase` 클래스를 인스터화해준다.

- `get_it`: Dependency Injection 의존성 주입을 구현하는 플러그인이다. LocalDatabase 클래스를 프로젝트 전역에서 사용할 수 있어야 하는데 서브 위젯으로 계속 값을 넘겨주기에는 반복적인 코드를 너무 많이 사용해야 한다. `GetIt`으로 값을 한 번 등록해주면 어디서든 처음에 주입한 값 즉, 같은 database 변수를 `GetIt`을 통해 전역적으로 사용 가능하다.

### 일정 데이터 생성

텍스트 필드를 TextFormField 위젯을 기반으로 구현했기 때문에 상위에 Form 위젯을 사용해주면 쉽게 데이터를 가져올 수 있다.

#### lib/widgets/custom_text_field.dart

```dart
import 'package:calendar_scheduler/constants/constants.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

class CustomTextField extends StatelessWidget {
  final String label;
  final bool isTime; // 시간 선택하는 텍스트 필드인지 여부
  final FormFieldSetter<String> onSaved;
  final FormFieldValidator<String> validator;

  const CustomTextField({
    required this.label,
    required this.isTime,
    required this.onSaved,
    required this.validator,
    Key? key,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Column(
      // ➋ 세로로 텍스트와 텍스트 필드를 위치
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          label,
          style: TextStyle(
            color: PRIMARY_COLOR,
            fontWeight: FontWeight.w600,
          ),
        ),
        Expanded(
          flex: isTime ? 0 : 1, // ➏
          child: TextFormField(
            onSaved: onSaved, // ➊ 폼 저장했을 때 실행할 함수
            validator: validator,
            cursorColor: Colors.grey, // 커서 색상 변경
            maxLines: isTime ? 1 : null, // ➊ 시간 관련 텍스트 필드가 아니면 한 줄이상 작성 가능
            expands: !isTime, // ➋ 시간 관련 텍스트 필드는 공간 최대 차지
            keyboardType: isTime
                ? TextInputType.number
                : TextInputType
                    .multiline, // ➌ 시간 관련 텍스트 필드는 기본 숫자 키보드 아니면 일반 글자 키보드 보여주기
            inputFormatters: isTime
                ? [
                    FilteringTextInputFormatter.digitsOnly,
                  ]
                : [], // ➍ 시간 관련 텍스트 필드는 숫자만 입력하도록 제한
            decoration: InputDecoration(
              border: InputBorder.none, // 테두리 삭제
              filled: true, // 배경색을 지정하겠다는 선언
              fillColor: Colors.grey[300], // 배경색
              suffixText: isTime ? '시' : null, // ➎ 시간 관련 텍스트 필드는 ‘시' 접미사 추가
            ),
          ),
        ),
      ],
    );
  }
}
```

이어서 CustomTextField 위젯을 사용하는 상위 위젯은 ScheduleBottomSheet도 작성해준다.

#### lib/widgets/schedule_bottom_sheet.dart

```dart
import 'package:calendar_scheduler/constants/constants.dart';
import 'package:calendar_scheduler/widgets/custom_text_field.dart';
import 'package:flutter/material.dart';
import 'package:drift/drift.dart' hide Column;
import 'package:get_it/get_it.dart';
import 'package:calendar_scheduler/database/drift_database.dart';

class ScheduleBottomSheet extends StatefulWidget {
  final DateTime selectedDate;

  const ScheduleBottomSheet({
    required this.selectedDate,
    Key? key,
  }) : super(key: key);

  @override
  State<ScheduleBottomSheet> createState() => _ScheduleBottomSheetState();
}

class _ScheduleBottomSheetState extends State<ScheduleBottomSheet> {
  final GlobalKey<FormState> formKey = GlobalKey();

  int? startTime; // 시작 시간 저장 변수
  int? endTime; // 종료 시간 저장 변수
  String? content; // 일정 내용 저장 변수

  @override
  Widget build(BuildContext context) {
    final bottomInset = MediaQuery.of(context).viewInsets.bottom;

    return Form(
      // ➊ 텍스트 필드를 한 번에 관리할 수 있는 폼
      key: formKey, // ➋ Form을 조작할 키값
      child: SafeArea(
        child: Container(
          height: MediaQuery.of(context).size.height / 2 +
              bottomInset, // ➋ 화면 반 높이에 키보드 높이 추가하기
          color: Colors.white,
          child: Padding(
            padding:
                EdgeInsets.only(left: 8, right: 8, top: 8, bottom: bottomInset),
            child: Column(
              // ➋ 시간 관련 텍스트 필드와 내용관련 텍스트 필드 세로로 배치
              children: [
                Row(
                  // ➊ 시작 시간 종료 시간 가로로 배치
                  children: [
                    Expanded(
                      child: CustomTextField(
                        // 시작시간 입력 필드
                        label: '시작 시간',
                        isTime: true,
                        onSaved: (String? val) {
                          // 저장이 실행되면 startTime 변수에 텍스트 필드 값 저장
                          startTime = int.parse(val!);
                        },
                        validator: timeValidator,
                      ),
                    ),
                    const SizedBox(width: 16.0),
                    Expanded(
                      child: CustomTextField(
                        // 종료시간 입력 필드
                        label: '종료 시간',
                        isTime: true,
                        onSaved: (String? val) {
                          // 저장이 실행되면 endTime 변수에 텍스트 필드 값 저장
                          endTime = int.parse(val!);
                        },
                        validator: timeValidator,
                      ),
                    ),
                  ],
                ),
                SizedBox(height: 8.0),
                Expanded(
                  child: CustomTextField(
                    // 내용 입력 필드
                    label: '내용',
                    isTime: false,
                    onSaved: (String? val) {
                      // 저장이 실행되면 content 변수에 텍스트 필드 값 저장
                      content = val;
                    },
                    validator: contentValidator,
                  ),
                ),
                SizedBox(
                  width: double.infinity,
                  child: ElevatedButton(
                    // [저장] 버튼
                    // ➌ [저장] 버튼
                    onPressed: onSavePressed,
                    style: ElevatedButton.styleFrom(
                      primary: PRIMARY_COLOR,
                    ),
                    child: Text('저장'),
                  ),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }

  void onSavePressed() async {
    if (formKey.currentState!.validate()) {
      // ➊ 폼 검증하기
      formKey.currentState!.save(); // ➋ 폼 저장하기

      await GetIt.I<LocalDatabase>().createSchedule(
        // ➊ 일정 생성하기
        SchedulesCompanion(
          startTime: Value(startTime!),
          endTime: Value(endTime!),
          content: Value(content!),
          date: Value(widget.selectedDate),
        ),
      );

      Navigator.of(context).pop();
    }
  }

  String? timeValidator(String? val) {
    if (val == null) {
      return '값을 입력해주세요';
    }

    int? number;

    try {
      number = int.parse(val);
    } catch (e) {
      return '숫자를 입력해주세요';
    }

    if (number < 0 || number > 24) {
      return '0시부터 24시 사이를 입력해주세요';
    }

    return null;
  } // 시간값 검증

  String? contentValidator(String? val) {
    if (val == null || val.length == 0) {
      return '값을 입력해주세요';
    }

    return null;
  } // 내용값 검증
}
```

- `formKey`: `save()` 함수와 `validate()` 함수를 실행할 수 있다. validate() 함수를 실행하면 Form 서브에 있는 모든 TextFormField들의 validator 매개 변수에 제공된 함수가 실행된다. 이 함수의 첫 번째 매개 변수에는 입력된 값이 제공되며 에러가 있을 경우 해당 에러 메시지를 String 값으로 반환하고 에러가 없으면 null을 반환한다.

- `timeValidator`: 시간이 잘 입력되었는 지 검증하는 함수이다. 값이 입력되지 않았거나 숫자가 입력되지 않았을 때 0과 24 사이의 값이 아니라면 해당 에러 메세지를 반환한다.

- `contentValidator`: 일정 내용을 검증하는 함수다. null 값이 입력되거나 글자 길이가 0이면 에러 메세지를 반환한다.

- `onSavePressed`

1. `validate()` 함수는 Form의 서브에 있는 모든 TextFormField의 validate 매개 변수에 입력된 함수들을 실행한다. 모든 함수들이 null을 반환하면 `validate()` 함수가 true를 반환하고 만약에 어느 한 함수라도 String 값을 반환해서 에러를 발생시키면 `validate()` 함수는 false를 반환한다.

2. `save()`: 모든 서브 TextFormField들에 `onSaved` 매개 변수에 입력된 함수를 실행한다. 이 함수들은 작성한 것처럼 텍스트 필드의 값을 변수에 저장하는 역할을 한다. 그러니 `validate()` 함수를 실행해서 true를 반환받으면 텍스트 필드 검증에 문제가 없다느 뜻이니 `save()` 함수를 실행해서 테스트 필드의 값들을 변수에 저장하면 된다.

- `createSchedule()`: 설계한 대로 일정 데이터를 SQLite 데이터베이스에 입력할 수 있다. 다만 매개 변수에 꼭 `SchedulesCompanion` 을 입력해줘야 하는데 SchedulesCompanion에는 실제 Schedules 테이블에 입력된 값들을 드리프트 패키지에서 제공하는 `Value` 클래스로 감싸서 입력해준다.

### 일정 데이터 일기

#### lib/screens/home_screen.dart

일정을 저장하는 기능은 끝났지만 값이 제대로 저장되는지 아직 확인할 길이 없다. `LocalDatabase` 클래스의 `watchSchedules()` 함수를 사용해서 달력에서 선택한 날짜에 해당되는 일정들을 불러와 화면에 반영한다.

```dart
import 'package:calendar_scheduler/constants/constants.dart';
import 'package:calendar_scheduler/database/drift_database.dart';
import 'package:calendar_scheduler/widgets/main_calendar.dart';
import 'package:calendar_scheduler/widgets/schedule_bottom_sheet.dart';
import 'package:calendar_scheduler/widgets/schedule_card.dart';
import 'package:calendar_scheduler/widgets/today_banner.dart';
import 'package:flutter/material.dart';
import 'package:get_it/get_it.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  DateTime selectedDate = DateTime.utc(
    DateTime.now().year,
    DateTime.now().month,
    DateTime.now().day,
  );

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      floatingActionButton: FloatingActionButton(
        backgroundColor: PRIMARY_COLOR,
        onPressed: () {
          showModalBottomSheet(
            context: context,
            isDismissible: true,
            builder: (_) => ScheduleBottomSheet(
              selectedDate: selectedDate,
            ),
            isScrollControlled: true,
          );
        },
        child: const Icon(
          Icons.add,
        ),
      ),
      body: SafeArea(
        child: Column(
          children: [
            MainCalendar(
              selectedDate: selectedDate,
              onDaySelected: onDaySelected,
            ),
            const SizedBox(height: 8.9),
            StreamBuilder<List<Schedule>>(
              stream: GetIt.I<LocalDatabase>().watchSchedules(selectedDate),
              builder: (context, snapshot) {
                return TodayBanner(
                  selectedDate: selectedDate,
                  count: snapshot.data?.length ?? 0,
                );
              },
            ),
            const SizedBox(height: 8.0),
            Expanded(
              child: StreamBuilder<List<Schedule>>(
                stream: GetIt.I<LocalDatabase>().watchSchedules(selectedDate),
                builder: (context, snapshot) {
                  if (!snapshot.hasData) {
                    return Container();
                  }
                  return ListView.builder(
                    itemCount: snapshot.data!.length,
                    itemBuilder: (context, index) {
                      final schedule = snapshot.data![index];
                      return Dismissible(
                        key: ObjectKey(schedule.id),
                        direction: DismissDirection.startToEnd,
                        onDismissed: (DismissDirection direction) {
                          GetIt.I<LocalDatabase>().removeSchedule(schedule.id);
                        },
                        child: Padding(
                          padding: const EdgeInsets.only(
                            bottom: 8.0,
                            left: 8.0,
                            right: 8.0,
                          ),
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
              ),
            )
          ],
        ),
      ),
    );
  }

  void onDaySelected(DateTime selectedDate, DateTime focusedDate) {
    setState(() {
      this.selectedDate = selectedDate;
    });
  }
}
```

달력과 현재 날짜 외의 모든 공간을 리스트가 차지하도록 `Expanded` 위젯을 사용해준다.

- `watchSchedules()`: 이 함수는 `Stream`을 반환해준다. 그렇기 때문에 StreamBuilder를 사용해서 일정 관련 데이터가 변경될 때마다 위젯들을 새로 렌더링해준다. `watchSchedules()` 함수에 매개변수로 `selectedDate`를 입력해서 선택한 날짜의 일정만 따로 필터링해서 불러온다. 일정이 존재하지 않으면 아무것도 들어 있지 않은 `Container` 위젯을 렌더링해준다.

- `ListView.builder`를 사용하면 여러 개의 위젯을 스크롤 가능한 위젯에 구현할 수 있다. 주요 매개 변수로는 구현할 리스트의 객체 개수를 입력할 수 있는 `itemCount`와 각 객체를 구현할 수 있는 `itemBuilder`가 있다. itemBuilder 매개 변수로 입력되는 함수에는 context와 index 변수가 순서대로 제공되어 순서별로 원하는 위젯을 그려낼 수 있다.

- `Dismissible`: 사용자 제스처에 따라 일정을 삭제하는 기능을 제공하는 위젯이다. `key` 매개변수에는 각 일정별로 절대 겹치지 않은 값을 `ObjectKey`에 감싸서 입력해줘야 한다. 이 값은 삭제 제스처가 어디에 적용됐는지 구분할 수 있는 요소로 사용된다. `direction` 매개변수는 밀기 제스처를 어떻게 제한할지 지정할 수 있다. `DismissDirection.endToStart`를 적용해줌녀 끝부터 시작, 즉 글을 읽는 방향의 반대인 왼쪽부터 오른쪽으로 미는 제스처만 인식한다. `onDismissed` 매개변수에 입력되는 함수는 제스처가 인식됐을 때 실행할 함수를 입력할 수 있다. 첫번째 매개 변수로 어떤 방향으로 제스처가 입력됐는지 알 수 있다.

- 일정을 삭제했을 때 `TodayBanner`에 나타나던 일정 개수가 변하도록 적용한다. `ListView`에 적용했듯이 `StreamBuilder`로 `TodayBanner`를 감싸준 다음에 일정 개수를 `count` 매개변수에 넣어주면 된다. 만약 값이 없을 떄를 대비해서 null 값이 입력되면 0이 입력되도록 설정해준다.

## 서버 연동

### 상태 관리

기존에는 `StatefulWidget`의 `setState()` 함수를 호출하면서 상태관리를 해왔다. 리액트와 마찬가지로 Component || Widget의 개수가 많아질수록 이런 방식은 매우 비효율적이기에 `글로버 상태 관리 툴`을 사용해서 전역 상태 관리가 가능하도록 수정해준다. 플러터에서는 주로 사용하는 `Bloc`, `GetX`, `Riverpod`, `Provider` 같은 상태 관리 플러그인이 있다.

### 캐시와 긍정적 응답

실제 서버를 운영하는 상황에는 서벗를 구매하거나 클라우드에서 운영하게 되는데 그러면 자녕적으로 지연이 생기게 된다. 현재는 서버와 앱을 같은 컴퓨터 즉, local 환경에서 실행하고 있기 때문에 네트워크 요청에 대한 지연이 존재하지 않는다. 이는 실제와 다르고 실제는 약간의 지연이 작용할 수 밖에 없다. 이 지연되는 시간 동안 사용자는 내부 구현 과정에 대해서 모르고 동작에만 관심이 있기 때문에 앱이 느리니까 별로이다고 생각한다. 이런 문제를 해결하기 위해 `Cache` 캐싱이라는 기법을 사용한다.

캐싱은 데이터를 기억한다는 뜻이다. 예를 들어 현재 구현한 `ScheduleProvider`에는 `cache`라는 변수가 존재하며 이 변수에는 GET 메서드로 불러온 모든 일정 정보가 전부 담겨 있다. 그렇기 때문에 특정 날짜를 처음 선택했을 때는 데이터를 불러오는 시간이 걸리지만 같은 날짜를 다시 요청할 때는 기존 요청에서 기억하는 데이터를 지연 없이 불러올 수 있다.

<img src="/images/provider-logic.PNG" />

1. 사용자가 달력에서 날짜를 선택한다.

2. 날짜가 선택되면 `ScheduleProvider`의 `changeSelectedDate()`함수가 실행된다. changeSelectedDate()의 로직이 모두 실행되면 UI를 다시 build() 하기 위해

3. `notifyListeners()`함수가 실행된다. notifyListeners()가 실행되면 HomeScreen 위젯의 build()가 재실행되며 변경된 selectedDate 변수에 따른

4. UI 업데이트가 진행된다. 이때 해당되는 날짜에 한 번도 GET 메서드로 일정을 가져온 적이 없다면 UI 업데이트까지 수행해 빈 리스트가 화면에 보여진다. 하지만 기존에 GET 메서드를 사용해 가져온 데
   이터가 저장되어 있다면 API 요청을 기다리지 않고 즉시 화면에 현재 cache값을 반영할 수 있다. changeSelectedDate() 함수의 실행이 끝나면

5. `getSchedules()`함수가 실행된다. getSchedules() 함수 내부에는 ScheduleAPI를 통해서

6. `getSchedules()`함수를 추가로 실행한다. 이 함수로 선택한 날짜에 해당되는 데이터를 서버에서 가져온다. ScheduleAPI의 getSchedules() 함수를 실행해서 가져온 값으로

7. `cache`를 업데이트한다. GET 메서드로 일정들을 가져오는 데 성공하며

8. `notifyListeners()`함수가 실행된다. notifyListeners() 함수가 실행되녀 HomeScreen 위젯의 build() 함수가 재실행된다. 만약 ScheduleAPI의 getSchedules() 함수에서 가져온 값들이 이미 cache 변수에 존재하면 일정 리스트 UI는 변화가 없다. 하지만 만약에 다른 값이 들어온다면 변경된 값을 화면에 다시 반영해주게 된다. cache 변수에 있는 값을 미리 보여주었기 때문에 사용자는 로딩이 전혀 없었던 것 같이 느낀다.

### 구현

#### 모델 구축 lib/model/schedule_model.dart

```dart
class ScheduleModel {
  final String id;
  final String content;
  final DateTime date;
  final int startTime;
  final int endTime;

  ScheduleModel({
    required this.id,
    required this.content,
    required this.date,
    required this.startTime,
    required this.endTime,
  });

  ScheduleModel.fromJson({
    // ➊ JSON으로부터 모델을 만들어내는 생성자
    required Map<String, dynamic> json,
  })  : id = json['id'],
        content = json['content'],
        date = DateTime.parse(json['date']),
        startTime = json['startTime'],
        endTime = json['endTime'];

  Map<String, dynamic> toJson() {
    // ➋ 모델을 다시 JSON으로 변환하는 함수
    return {
      'id': id,
      'content': content,
      'date':
          '${date.year}${date.month.toString().padLeft(2, '0')}${date.day.toString().padLeft(2, '0')}',
      'startTime': startTime,
      'endTime': endTime,
    };
  }

  ScheduleModel copyWith({
    // ➌ 현재 모델을 특정 속성만 변환해서 새로 생성
    String? id,
    String? content,
    DateTime? date,
    int? startTime,
    int? endTime,
  }) {
    return ScheduleModel(
      id: id ?? this.id,
      content: content ?? this.content,
      date: date ?? this.date,
      startTime: startTime ?? this.startTime,
      endTime: endTime ?? this.endTime,
    );
  }
}
```

1. REST API 요청 응답을 받으면 JSON 형식의 데이터로 받게 된다. JSON 형식 그대로 `fromJson` 생성자에 넣어주면 자동으로 `ScheduleModel`에 매핑된다.

2. `toJson()`은 ScheduleModel을 JSON 형식으로 변환하는 함수이다. 플러터에서 데이터를 관리할 때는 클래스 형태로 관리하면 편하지만 서버로 네트워크 요청을 보낼 때는 다시 JSON 형식으로 데이터를 변환해야 한다.

3. `copyWith()`함수는 플러터에서 흔히 사용되는 함수이다. 현대에는 불변성 즉, 한번 선언한 인스턴스를 다시 변경하지 않는 기법을 많이 사용한다. 하지만 이미 존재하는 인스턴스에서 몇 개의 값만 변경해야할 경우가 생긴다. 그럴 때 copyWith() 같은 함수를 생성해 입력하지 않은 값들을 그대로 보존하고 입력해준 값들을 새로 저장할 수 있다.

#### API 요청 구현 lib/apis/schedule_api.dart

```dart
import 'dart:async';
import 'dart:io';

import 'package:calendar_scheduler/model/schedule_model.dart';
import 'package:dio/dio.dart';

class ScheduleAPI {
  final _dio = Dio();
  final _targetUrl =
      'http://${Platform.isAndroid ? '10.0.2.2' : 'localhost'}:3000/schedule';

  Future<List<ScheduleModel>> getSchedules({required DateTime date}) async {
    final response = await _dio.get(
      _targetUrl,
      queryParameters: {
        'date':
            '${date.year}${date.month.toString().padLeft(2, '0')}${date.day.toString().padLeft(2, '0')}',
      },
    );

    return response.data
        .map<ScheduleModel>(
          (x) => ScheduleModel.fromJson(
            json: x,
          ),
        )
        .toList();
  }

  Future<String> createSchedule({required ScheduleModel schedule}) async {
    final json = schedule.toJson();
    final response = await _dio.post(_targetUrl, data: json);
    return response.data?['id'];
  }

  Future<String> deleteSchedule({required String id}) async {
    final response = await _dio.delete(_targetUrl, data: {
      'id': id,
    });

    return response.data?['id'];
  }
}
```

#### Global 상태 관리 구현: ScheduleProvider

`Provider`는 `ChangeNotifier`를 상속하기만 하면 어떤 클래스든 프로바이더로 상태 관리를 하도록 만들 수 있다.

- `ScheduleProvider`클래스를 생성하고 `material` 패키지에서 제공하는 `ChangeNotifier` 클래스를 상속받는다. ScheduleProvider에는 변수 3개가 필요하다. 첫 번째는 `ScheduleAPI`, 두번째는 `selectedDate`, 마지막으로 API 요청을 통해서 받아온 일정 정보를 저장할 `cache` 변수이다.

```dart
import 'package:calendar_scheduler/model/schedule_model.dart';
import 'package:calendar_scheduler/apis/schedule_api.dart';

import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:uuid/uuid.dart';

class ScheduleProvider extends ChangeNotifier {
  final ScheduleAPI api;

  DateTime selectedDate = DateTime.utc(
    DateTime.now().year,
    DateTime.now().month,
    DateTime.now().day,
  );

  Map<DateTime, List<ScheduleModel>> cache = {};

  ScheduleProvider({required this.api}) : super() {
    getSchedules(date: selectedDate);
  }

  void getSchedules({required DateTime date}) async {
    final response = await api.getSchedules(date: date);
    cache.update(date, (value) => response, ifAbsent: () => response);
    notifyListeners();
  }

  void createSchedule({required ScheduleModel schedule}) async {
    final targetDate = schedule.date;
    final uuid = Uuid();
    final tempId = uuid.v4();
    final newSchedule = schedule.copyWith(id: tempId);
    final savedSchedule = await api.createSchedule(schedule: schedule);

    cache.update(
      targetDate,
      (value) => [
        ...value,
        newSchedule,
      ]..sort(
          (a, b) => a.startTime.compareTo(
            b.startTime,
          ),
        ),
      ifAbsent: () => [newSchedule],
    );

    notifyListeners();

    try {
      final savedSchedule = await api.createSchedule(schedule: schedule);

      cache.update(
        targetDate,
        (value) => value
            .map((e) => e.id == tempId
                ? e.copyWith(
                    id: savedSchedule,
                  )
                : e)
            .toList(),
      );
    } catch (e) {
      cache.update(
          targetDate, (value) => value.where((e) => e.id != tempId).toList());
    }
  }

  void deleteSchedule({required DateTime date, required String id}) async {
    final targetSchedule =
        cache[date]!.firstWhere((element) => element.id == id);

    cache.update(
      date,
      (value) => value.where((element) => element.id != id).toList(),
      ifAbsent: () => [],
    );

    try {
      await api.deleteSchedule(id: id);
    } catch (e) {
      cache.update(
        date,
        (value) => [...value, targetSchedule]..sort(
            (a, b) => a.startTime.compareTo(b.startTime),
          ),
      );
    }
    notifyListeners();
  }

  void changeSelectedDate({required DateTime date}) {
    selectedDate = date;
    notifyListeners();
  }
}
```

- `api`: API 요청 로직을 담은 ScheduleAPI이다.

- `selectedDate`: 서버에서 불러온 일정을 저장할 변수이다. 일정을 날짜별로 정리하기 위해 DateTime을 키로 입력받고 `List<ScheduleModel>`을 값으로 입력받는다. 원하는 날짜에 해당되는 일정들을 가져올 때 `cache`변수에 해당되는 날짜를 key 값으로 제공해주면 일정들을 리스트로 받아올 수 있다.

- `cache`: 일정 정보를 저장해둘 캐시 변수. 키값에 날짜를 입력하고 날짜에 해당되는 일정들을 리스트로 값에 저장한다.

- `notifyListeners()`: 현재 클래스를 watch()하는 모든 위젯들의 build() 함수를 다시 실행한다. 위젯들은 cache 변수를 바라보도록 할 계획이니 cache 변수가 업데이트될 때마다 notifyListeners() 함수를 실행해서 위젯을 다시 빌드해준다.

#### Provider 초기화하기 lib/main.dart

프로바이더는 글로벌 상태 관리 툴이기 때문에 한 번 최상위에 선언을 해줌녀 최하단 위젯까지 모두 프로바디어의 속성들을 사용할 수 있어야 한다. 이렇게 하려면 프로젝트 최상위(lib/main.dart)에 `ScheduleProvider`를 초기화해야 한다.

1. 먼저 `ScheduleAPI` & `ScheduleProvider`를 인스턴스화 해준다. 그리고 `ChangeNotifierProvider` 위젯으로 `MaterialApp` 위젯을 감싸준다. ChangeNotifierProvider 위젯은 프로바이더를 현재 위치에 주입시키고 주입한 위치의 서브에 있는 모든 위젯에서 프로바이더를 사용해준다.

```dart
import 'package:calendar_scheduler/apis/schedule_api.dart';
import 'package:calendar_scheduler/provider/schedule_provider.dart';
import 'package:calendar_scheduler/screens/home_screen.dart';
import 'package:flutter/material.dart';
import 'package:intl/date_symbol_data_local.dart';
import 'package:calendar_scheduler/database/drift_database.dart';
import 'package:get_it/get_it.dart';
import 'package:provider/provider.dart';

void main() async {
  WidgetsFlutterBinding();
  await initializeDateFormatting();
  final database = LocalDatabase();
  GetIt.I.registerSingleton<LocalDatabase>(database);
  final api = ScheduleAPI();
  final scheduleProvider = ScheduleProvider(api: api);

  runApp(
    ChangeNotifierProvider(
      create: (_) => scheduleProvider,
      child: const MyApp(),
    ),
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

#### Drift를 Provider로 대체하기

드리프트를 사용할 때는 StreamBuilder를 사용해서 Stream 값을 리스닝했지만 프로바이더를 사용하면 더는 StreamBuilder를 사용할 필요가 없다. 프로바이더는 데이터를 불러올 수 있는 `watch()` & `read()` 함수를 제공해주기 때문이다. `watch()` 함수는 StreamBuilder와 같이 지속적으로 값이 변경될 때마다 즉, `notifyListeners()` 함수가 실행될 때마다 build() 함수를 재실행해준다. `read()` 함수의 경우 FutureBuilder와 유사하며 단발성으로 값을 가져올 때 사용된다.

한 변수의 값에 따라 UI를 다르게 보여줘야 할 경우 `watch`

버튼 탭 같은 특정 액션 후에 값을 가져올 떄는 `read()`

Provider를 사용하기에 HomeScreen을 Stateful Widget이 아닌 Stateless Widget으로 바꿔준다.

```dart
import 'package:calendar_scheduler/constants/constants.dart';
import 'package:calendar_scheduler/provider/schedule_provider.dart';
import 'package:calendar_scheduler/widgets/main_calendar.dart';
import 'package:calendar_scheduler/widgets/schedule_bottom_sheet.dart';
import 'package:calendar_scheduler/widgets/schedule_card.dart';
import 'package:calendar_scheduler/widgets/today_banner.dart';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

class HomeScreen extends StatelessWidget {
  DateTime selectedDate = DateTime.utc(
    // ➋ 선택된 날짜를 관리할 변수
    DateTime.now().year,
    DateTime.now().month,
    DateTime.now().day,
  );

  @override
  Widget build(BuildContext context) {
    final provider =
        context.watch<ScheduleProvider>(); // ➋ 프로바이더 변경이 있을 때마다 build() 함수 재실행
    final selectedDate = provider.selectedDate; // ➌ 선택된 날짜 가져오기
    final schedules = provider.cache[selectedDate] ?? [];

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
            TodayBanner(
              // ➊ 배너 추가하기
              selectedDate: selectedDate,
              count: schedules.length,
            ),
            const SizedBox(height: 8.0),
            Expanded(
              child: ListView.builder(
                itemCount: schedules.length,
                itemBuilder: (context, index) {
                  final schedule = schedules[index];

                  return Dismissible(
                    key: ObjectKey(schedule.id),
                    direction: DismissDirection.startToEnd,
                    onDismissed: (DismissDirection direction) {
                      provider.deleteSchedule(
                          date: selectedDate, id: schedule.id); // ➊
                    },
                    child: Padding(
                      padding: const EdgeInsets.only(
                          bottom: 8.0, left: 8.0, right: 8.0),
                      child: ScheduleCard(
                        startTime: schedule.startTime,
                        endTime: schedule.endTime,
                        content: schedule.content,
                      ),
                    ),
                  );
                },
              ),
            ),
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
    final provider = context.read<ScheduleProvider>();
    provider.changeSelectedDate(
      date: selectedDate,
    );
    provider.getSchedules(date: selectedDate);
  }
}
```

Provider 패키지를 불러오면 BuildContext가 제공되는 어느 곳에서든 `context.watch()` 함수 및 `context.read()` 함수를 실행할 수 있다. `context.watch()` 함수에는 불러오고 싶은 Provider 타입을 제네릭으로 전달해주면 된다. `context.watch()`가 build() 함수 내에서 실행되는 순간 불러온 Provider에서 notifyListeners() 함수가 실행되면 build() 함수가 다시 실행된다. 결과적으로 새로 갱신된 값에 의해서 위젯이 새로 렌더링된다. `context.watch()`는 main.dart에 선언해둔 같은 인스턴스의 scheduleProvider 변수에 반환해준다.

`selectedDate` 변수를 이제 더는 위젯에서 관리하지 않고 프로바이더에서 관리하기 때문에 provider로부터 selectedDate 값을 가져와야 한다.

`ScheduleProvider`에는 일정을 날짜별로 정리한 `cache` 값을 저장해두었다. 그러니 현재 선택한 날짜에 해당되는 일정들을 불러오려면 `cache` 변수에서 `selectedDate key`에 해당되는 value를 불러온다.

#### Cache 적용하기 lib/providers/schedule_provider.dart

```dart
  void createSchedule({required ScheduleModel schedule}) async {
    final targetDate = schedule.date;
    final uuid = Uuid();
    final tempId = uuid.v4();
    final newSchedule = schedule.copyWith(id: tempId);
    final savedSchedule = await api.createSchedule(schedule: schedule);

    cache.update(
      targetDate,
      (value) => [
        ...value,
        newSchedule,
      ]..sort(
          (a, b) => a.startTime.compareTo(
            b.startTime,
          ),
        ),
      ifAbsent: () => [newSchedule],
    );

    notifyListeners();

    try {
      final savedSchedule = await api.createSchedule(schedule: schedule);

      cache.update(
        targetDate,
        (value) => value
            .map((e) => e.id == tempId
                ? e.copyWith(
                    id: savedSchedule,
                  )
                : e)
            .toList(),
      );
    } catch (e) {
      cache.update(
          targetDate, (value) => value.where((e) => e.id != tempId).toList());
    }
  }

  void deleteSchedule({required DateTime date, required String id}) async {
    final targetSchedule =
        cache[date]!.firstWhere((element) => element.id == id);

    cache.update(
      date,
      (value) => value.where((element) => element.id != id).toList(),
      ifAbsent: () => [],
    );

    try {
      await api.deleteSchedule(id: id);
    } catch (e) {
      cache.update(
        date,
        (value) => [...value, targetSchedule]..sort(
            (a, b) => a.startTime.compareTo(b.startTime),
          ),
      );
    }
    notifyListeners();
  }
```

1. API 요청이 성공하면 임시로 저장한 일정의 ID만 서버에서 생성된 값으로 변경해준다.

2. 에러가 발생한다면 일정 값이 제대로 저장되지 않았다는 뜻이다. 그러니 캐시에서도 일정을 삭제해준다.

3. 일정을 삭제하는 API 요청을 보낸다. 이미 일정을 삭제했기 때문에 만약에 요청이 성공하면 캐시를 따로 수정할 필요가 없다.

4. 만약에 API 요청에서 에러가 난다면 기억해둔 일정을 다시 캐시에 추가한다.

