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

