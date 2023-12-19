# Flutter Calendar Scheduler


# Introduction

달력 형태의 위젯인 `TableCalendar`를 사용해서 일정 관리 앱 구현.

## Dependency

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

## 구현

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

