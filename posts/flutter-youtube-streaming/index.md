# Flutter Youtube Streaming


# Introduction

`Flutter` 기능 구현 - YouTube 동영상 데이터 가져오기.

HTTP 요청의 응답을 담을 모델 클래스를 구현하고, UI를 작성한 다음, `Dio`를 사용해서 직접 API 요청을 진행한다. 마지막으로 요청을 다시 실행하고 리스트를 갱신할 수 있는 새로고침 기능을 추가해준다.

## Dependency

- `Dio`
- `youtube_player_flutter`
- `flutter_dotenv`
- API: `YouTube Data API V3`

## 구현

### VideoModel

유튜브 API를 사용하면 굉장히 많은 정보를 가져올 수 있다. 그 중에서 동영상 ID와 제목만 활용해본다. 이 정보를 담을 VideoModel 클래스를 구현해서 데이터를 관리한다.

#### lib/model/video_model.dart

```dart
class VideoModel {
  final String id;
  final String title;

  VideoModel({
    required this.id,
    required this.title,
  });
}
```

### CustomYoutubePlater widget

CustomYoutubePlayer 위젯은 유튜브 동영상을 재생할 수 있는 상태로 제공하는 역할을 한다. 이미 pubspec.yaml에 추가한 `youtube_player_flutter` 플러그인을 사용해서 구현한다.

```dart
import 'package:flutter/material.dart';
import 'package:se_tube/model/video_model.dart';
import 'package:youtube_player_flutter/youtube_player_flutter.dart';

class CustomYouTubePlayer extends StatefulWidget {
  final VideoModel videoModel;

  const CustomYouTubePlayer({
    super.key,
    required this.videoModel,
  });

  @override
  State<CustomYouTubePlayer> createState() => _CustomYouTubePlayerState();
}

class _CustomYouTubePlayerState extends State<CustomYouTubePlayer> {
  YoutubePlayerController? controller;

  @override
  void initState() {
    super.initState();

    controller = YoutubePlayerController(
      initialVideoId: widget.videoModel.id,
      flags: const YoutubePlayerFlags(
        autoPlay: false,
      ),
    );
  }

  @override
  void dispose() {
    super.dispose();
    controller!.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        YoutubePlayer(
          controller: controller!,
          showVideoProgressIndicator: true,
        ),
        const SizedBox(height: 16.0),
        Padding(
          padding: const EdgeInsets.symmetric(horizontal: 8.0),
          child: Text(
            widget.videoModel.title,
            style: const TextStyle(
              color: Colors.white,
              fontSize: 16.0,
              fontWeight: FontWeight.w700,
            ),
          ),
        ),
      ],
    );
  }
}
```

유튜브 동영상을 재생하는 widget은 YoutubePlayer widget으로 youtube_player_flutter 플러그인에서 불러올 수 있다. YoutubePlayer widget을 조정하려면 `YouTubePlayerController`를 사용해야 한다.

{{<admonition tip>}}
Dart에서 Controller를 사용하고 dispose 메서드를 호출하는 이유는 일반적으로 상태를 관리하고 메모리 누수를 방지하기 위해서입니다. 주로 플러터(Flutter) 애플리케이션에서 상태를 관리하는 데에 사용됩니다.

메모리 누수 방지:
Controller는 리소스를 관리하며, 특히 플러터에서는 위젯의 상태를 다루기 위해 사용됩니다. 만약 Controller를 사용한 후에 명시적으로 dispose를 호출하지 않는다면, 해당 Controller에서 사용하는 리소스가 해제되지 않을 수 있습니다. 이러한 경우 메모리 누수가 발생할 수 있으며, 앱이 계속 실행됨에 따라 메모리 사용량이 계속 증가할 수 있습니다.

리소스 정리:
Controller는 종종 외부 리소스를 관리하며, 이 리소스들은 사용이 끝난 후에 정리되어야 합니다. dispose 메서드를 호출하여 해당 리소스를 명시적으로 정리할 수 있습니다.

예를 들어, 플러터에서 TextEditingController를 사용하는 경우가 있습니다. 이 컨트롤러는 텍스트 필드의 텍스트를 관리하며, 해당 위젯이 더 이상 필요하지 않을 때 dispose 메서드를 호출하여 리소스를 해제합니다.

```dart
TextEditingController _controller = TextEditingController();

@override
void dispose() {
  _controller.dispose();
  super.dispose();
}
```

이와 같은 패턴은 다른 Controller 또는 리소스 관리 클래스에서도 유사하게 사용됩니다. 따라서 Controller를 사용한 후에는 항상 dispose 메서드를 호출하여 리소스 누수를 방지하고 메모리를 효율적으로 관리하는 것이 좋습니다.

{{</admonition>}}

지금까지 모든 컨트롤러에 대해 해왔듯이 `YouTubePlayerController`를 `initState()` 함수에서 초기화해주고 `dispose()` 함수에서 폐기해준다. 추가적으로 `Column` widget을 사용해서 YouTubePlayer widget과 Text widget을 세로로 배치해서 동영상 아래에 동영상의 제목이 있는 형태의 UI를 만들어준다.

- `YouTubePlayerController`: 해당 클래스를 사용하면 YoutubePlayer widget을 조정할 컨트롤러를 생성할 수 있다. `initialVideoId`에 동영상의 ID를 입력해주면 해당되는 동영상을 불러온다. `flags.autoPlay`는 widgete이 화면에 보이자마자 동영상을 재생할 지 결정할 수 있다. 기본값은 true로 화면에 렌더링 되자마자 재생되지만 false를 입력해서 재생 버튼을 눌렀을 때만 재생되도록 하겠습니다.

- `YoutubePlayer`: 유튜브 동영상을 재생할 수 있는 widget이다. controller를 매개변수로 필수로 주어야 하며 `YoutubePlayerController`를 전달해주면 된다. `showVideoProgressIndicator`를 true로 설정하면 동영상 진행 사항을 알려주는 슬라이더를 보여줄 수 있다.

- `dispose`: CustomYouTubePlayerState 클래슥가 삭젣되면 컬트롤러 또한 삭제해서 메모리 누수를 막아준다.

### YouTube API 연결하기

`Dio` 패키지를 이용한 HTTP 요청을 구현해준다. 우선 API end point를 위한 `Constants`를 만들어준다.

#### lib/constants/constant_url.dart

```env
API_KEY=Google Cloud Console에서 발급받은 API key를 입력!!!
YOUTUBE_BASE_URL=https://youtube.googleapis.com/youtube/v3/search
CF_CHANNEL_ID=UCxZ2AlaT0hOmxzZVbF_j_Sw
```

```dart
import 'package:flutter_dotenv/flutter_dotenv.dart';

String API_KEY = dotenv.get('API_KEY');
String YOUTUBE_BASE_URL = dotenv.get('YOUTUBE_BASE_URL');
String CF_CHANNEL_ID = dotenv.get('CF_CHANNEL_ID');
```

채널 ID는 유튜브에서 채널을 생성하면 부엳되는 채널당 고유 ID이다. 채널 페이지에 들어갔을 때 URL의 마지막 부분에서 가져올 수 있다.

Youtube Data API V3는 상당히 많은 기능을 제공한다. 수많은 기능 중 `Search:list API`를 사용해서 특정 채널에서 다수의 동영상을 최신 순서대로 가져온다. API end point로 HTTP GET 요청을 보내면 에러가 없을 경우 다음과 같은 JSON 데이터를 응답받는다.

```json
{
  "kind": "youtube#searchResult",
  "etag": etag,
  "id": {
    "kind": string,
    "videoId": string,
    "channelId": string,
    "playlistId": string
  },
  "snippet": {
    "publishedAt": datetime,
    "channelId": string,
    "title": string,
    "description": string,
    "thumbnails": {
      (key): {
        "url": string,
        "width": unsigned integer,
        "height": unsigned integer
      }
    },
    "channelTitle": string,
    "liveBroadcastContent": string
  }
}
```

