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

