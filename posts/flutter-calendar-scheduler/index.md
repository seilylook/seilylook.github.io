# Flutter Calendar Scheduler


# Introduction

달력 형태의 Widget인 `TableCalendar`를 사용해서 일정 관리 앱 구현.

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

#### lib/widgets/main_calendar.dart

```dart
import 'package:calendar_scheduler/constants/constants.dart';
import 'package:flutter/material.dart';
import 'package:table_calendar/table_calendar.dart';

class MainCalendar extends StatelessWidget {
  final OnDaySelected onDaySelected;
  final DateTime selectedDate;

  const MainCalendar({
    super.key,
    required this.onDaySelected,
    required this.selectedDate,
  });

  @override
  Widget build(BuildContext context) {
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

### 선택된 날의 일정 보여주기: ScheduleCard widget

선택된 날짜에 해당되는 일정을 보여주는 widget을 만들어준다. 각 일정은 시간(시작 시간부터 종료 시간)과 내용으로 이루어져 있다.

#### lib/widgets/schedule_card.dart

```dart
import 'package:calendar_scheduler/constants/constants.dart';
import 'package:flutter/material.dart';

class ScheduleCard extends StatelessWidget {
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
  Widget build(BuildContext context) {
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

class _Time extends StatelessWidget {
  final int startTime;
  final int endTime;

  const _Time({
    required this.startTime,
    required this.endTime,
  });

  @override
  Widget build(BuildContext context) {
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

class _Content extends StatelessWidget {
  final String content;
  const _Content({
    required this.content,
  });

  @override
  Widget build(BuildContext context) {
    return Expanded(
      child: Text(
        content,
      ),
    );
  }
}
```

`_Time`: 시간을 표현해주는 widget이다.

`_Content`: 일정을 알려주는 widget이다.

`IntrinsicHeight`: 내부 위젯들의 높이를 최대 높이로 맞춰준다. \_Time widget은 Column widget을 사용 중익기 때문에 ScheduleCard widget의 최대 크기만큼 높이를 차지한다. \_Content widget은 Column widget을 사용하지 않기 때문에 최소 크기만 차지하며 세로로 가운데 정렬이 이루어진다.

### 오늘 날짜를 보여주기: TodayBanner widget

`TodayBanner` widget은 MainCalendar widget과 ScheduleCard widget 사이에 오늘 날짜를 보여준다.

#### lib/widgets/today_banneer.dart

```dart
import 'package:calendar_scheduler/constants/constants.dart';
import 'package:flutter/material.dart';

class TodayBanner extends StatelessWidget {
  final DateTime selectedDate;
  final int count;
  const TodayBanner({
    super.key,
    required this.selectedDate,
    required this.count,
  });

  @override
  Widget build(BuildContext context) {
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

