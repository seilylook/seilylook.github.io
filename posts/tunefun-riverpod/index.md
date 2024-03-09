# Tunefun Riverpod


# Introduction

`Riverpod`을 실제 프로젝트에 처음으로 적용해보고 이해한 것을 정리하기 위한 포스팅이다.

## 목표

User Authentication - 회원가입, 로그인 기능 전체를 구현하고 사용자 정보를 Storage에 저장해 로그인 유지를 구축하고 싶었다.

## Dependency

```yaml
dependencies:
  flutter:
    sdk: flutter

  # The following adds the Cupertino Icons font to your application.
  # Use with the CupertinoIcons class for iOS style icons.
  cupertino_icons: ^1.0.2
  flutter_riverpod: ^2.4.10
```

## 구현

### Model 구축하기

사용자 정보에 대한 데이터베이스를 위한 모델을 만들어준다.

```dart
// ignore_for_file: public_member_api_docs, sort_constructors_first
import 'dart:convert';

import 'package:flutter/foundation.dart';

@immutable
class AccountModel {
  final String? username;
  final String? password;
  final String? email;
  final String? nickname;
  final bool? voteProgressNotification;
  final bool? voteEndNotification;
  final bool? voteDeliveryNotification;
  final List<String>? roles;
  final String? accessToken;
  final String? refreshToken;
  final DateTime? lastLoginAt;
  final DateTime? lastLogoutAt;
  final String? profileImageUrl;
  final DateTime? emailVerifiedAt;
  final DateTime? withdrawalAt;
  final DateTime? createdAt;
  final DateTime? updatedAt;
  final DateTime? deletedAt;

  const AccountModel({
    this.username,
    this.password,
    this.email,
    this.nickname,
    this.voteProgressNotification,
    this.voteEndNotification,
    this.voteDeliveryNotification,
    this.roles,
    this.accessToken,
    this.refreshToken,
    this.lastLoginAt,
    this.lastLogoutAt,
    this.profileImageUrl,
    this.emailVerifiedAt,
    this.withdrawalAt,
    this.createdAt,
    this.updatedAt,
    this.deletedAt,
  });

  AccountModel copyWith({
    String? username,
    String? password,
    String? email,
    String? nickname,
    bool? voteProgressNotification,
    bool? voteEndNotification,
    bool? voteDeliveryNotification,
    List<String>? roles,
    String? accessToken,
    String? refreshToken,
    DateTime? lastLoginAt,
    DateTime? lastLogoutAt,
    String? profileImageUrl,
    DateTime? emailVerifiedAt,
    DateTime? withdrawalAt,
    DateTime? createdAt,
    DateTime? updatedAt,
    DateTime? deletedAt,
  }) {
    return AccountModel(
      username: username ?? this.username,
      password: password ?? this.password,
      email: email ?? this.email,
      nickname: nickname ?? this.nickname,
      voteProgressNotification:
          voteProgressNotification ?? this.voteProgressNotification,
      voteEndNotification: voteEndNotification ?? this.voteEndNotification,
      voteDeliveryNotification:
          voteDeliveryNotification ?? this.voteDeliveryNotification,
      roles: roles ?? this.roles,
      accessToken: accessToken ?? this.accessToken,
      refreshToken: refreshToken ?? this.refreshToken,
      lastLoginAt: lastLoginAt ?? this.lastLoginAt,
      lastLogoutAt: lastLogoutAt ?? this.lastLogoutAt,
      profileImageUrl: profileImageUrl ?? this.profileImageUrl,
      emailVerifiedAt: emailVerifiedAt ?? this.emailVerifiedAt,
      withdrawalAt: withdrawalAt ?? this.withdrawalAt,
      createdAt: createdAt ?? this.createdAt,
      updatedAt: updatedAt ?? this.updatedAt,
      deletedAt: deletedAt ?? this.deletedAt,
    );
  }

  Map<String, dynamic> toMap() {
    return <String, dynamic>{
      'username': username,
      'password': password,
      'email': email,
      'nickname': nickname,
      'voteProgressNotification': voteProgressNotification,
      'voteEndNotification': voteEndNotification,
      'voteDeliveryNotification': voteDeliveryNotification,
      'roles': roles,
      'accessToken': accessToken,
      'refreshToken': refreshToken,
      'lastLoginAt': lastLoginAt?.millisecondsSinceEpoch,
      'lastLogoutAt': lastLogoutAt?.millisecondsSinceEpoch,
      'profileImageUrl': profileImageUrl,
      'emailVerifiedAt': emailVerifiedAt?.millisecondsSinceEpoch,
      'withdrawalAt': withdrawalAt?.millisecondsSinceEpoch,
      'createdAt': createdAt?.millisecondsSinceEpoch,
      'updatedAt': updatedAt?.millisecondsSinceEpoch,
      'deletedAt': deletedAt?.millisecondsSinceEpoch,
    };
  }

  factory AccountModel.fromMap(Map<String, dynamic> map) {
    return AccountModel(
      username: map['username'] != null ? map['username'] as String : null,
      password: map['password'] != null ? map['password'] as String : null,
      email: map['email'] != null ? map['email'] as String : null,
      nickname: map['nickname'] != null ? map['nickname'] as String : null,
      voteProgressNotification: map['voteProgressNotification'] != null
          ? map['voteProgressNotification'] as bool
          : null,
      voteEndNotification: map['voteEndNotification'] != null
          ? map['voteEndNotification'] as bool
          : null,
      voteDeliveryNotification: map['voteDeliveryNotification'] != null
          ? map['voteDeliveryNotification'] as bool
          : null,
      roles: map['roles'] != null
          ? List<String>.from((map['roles'] as List<String>))
          : null,
      accessToken:
          map['accessToken'] != null ? map['accessToken'] as String : null,
      refreshToken:
          map['refreshToken'] != null ? map['refreshToken'] as String : null,
      lastLoginAt: map['lastLoginAt'] != null
          ? DateTime.fromMillisecondsSinceEpoch(map['lastLoginAt'] as int)
          : null,
      lastLogoutAt: map['lastLogoutAt'] != null
          ? DateTime.fromMillisecondsSinceEpoch(map['lastLogoutAt'] as int)
          : null,
      profileImageUrl: map['profileImageUrl'] != null
          ? map['profileImageUrl'] as String
          : null,
      emailVerifiedAt: map['emailVerifiedAt'] != null
          ? DateTime.fromMillisecondsSinceEpoch(map['emailVerifiedAt'] as int)
          : null,
      withdrawalAt: map['withdrawalAt'] != null
          ? DateTime.fromMillisecondsSinceEpoch(map['withdrawalAt'] as int)
          : null,
      createdAt: map['createdAt'] != null
          ? DateTime.fromMillisecondsSinceEpoch(map['createdAt'] as int)
          : null,
      updatedAt: map['updatedAt'] != null
          ? DateTime.fromMillisecondsSinceEpoch(map['updatedAt'] as int)
          : null,
      deletedAt: map['deletedAt'] != null
          ? DateTime.fromMillisecondsSinceEpoch(map['deletedAt'] as int)
          : null,
    );
  }

  String toJson() => json.encode(toMap());

  factory AccountModel.fromJson(String source) =>
      AccountModel.fromMap(json.decode(source) as Map<String, dynamic>);

  @override
  String toString() {
    return 'AccountModel(username: $username, password: $password, email: $email, nickname: $nickname, voteProgressNotification: $voteProgressNotification, voteEndNotification: $voteEndNotification, voteDeliveryNotification: $voteDeliveryNotification, roles: $roles, accessToken: $accessToken, refreshToken: $refreshToken, lastLoginAt: $lastLoginAt, lastLogoutAt: $lastLogoutAt, profileImageUrl: $profileImageUrl, emailVerifiedAt: $emailVerifiedAt, withdrawalAt: $withdrawalAt, createdAt: $createdAt, updatedAt: $updatedAt, deletedAt: $deletedAt)';
  }

  @override
  bool operator ==(covariant AccountModel other) {
    if (identical(this, other)) return true;

    return other.username == username &&
        other.password == password &&
        other.email == email &&
        other.nickname == nickname &&
        other.voteProgressNotification == voteProgressNotification &&
        other.voteEndNotification == voteEndNotification &&
        other.voteDeliveryNotification == voteDeliveryNotification &&
        listEquals(other.roles, roles) &&
        other.accessToken == accessToken &&
        other.refreshToken == refreshToken &&
        other.lastLoginAt == lastLoginAt &&
        other.lastLogoutAt == lastLogoutAt &&
        other.profileImageUrl == profileImageUrl &&
        other.emailVerifiedAt == emailVerifiedAt &&
        other.withdrawalAt == withdrawalAt &&
        other.createdAt == createdAt &&
        other.updatedAt == updatedAt &&
        other.deletedAt == deletedAt;
  }

  @override
  int get hashCode {
    return username.hashCode ^
        password.hashCode ^
        email.hashCode ^
        nickname.hashCode ^
        voteProgressNotification.hashCode ^
        voteEndNotification.hashCode ^
        voteDeliveryNotification.hashCode ^
        roles.hashCode ^
        accessToken.hashCode ^
        refreshToken.hashCode ^
        lastLoginAt.hashCode ^
        lastLogoutAt.hashCode ^
        profileImageUrl.hashCode ^
        emailVerifiedAt.hashCode ^
        withdrawalAt.hashCode ^
        createdAt.hashCode ^
        updatedAt.hashCode ^
        deletedAt.hashCode;
  }
}

```

백엔드와 사용자 정보에 대해 의견을 나누고 데이터베이스와 일치하도록 만들어준다. 하지만 이 데이터는 추후에 서비스 상태와 서버 요구에 의해 변할 수 있다.

### UI 작업

기본적인 회원가입 / 로그인 화면을 구성해준다.

#### Log In

```dart
void logIn() {
    ref.watch(authControllerProvider.notifier).login(
        username: usernameController.text,
        password: passwordController.text,
        context: context,
    );
}
```

이제 `Riverpod`을 사용한다. `ConsumerStatefulWidget`을 사용해서 전역 상태의 변화를 실시간으로 관찰할 수 있다.

### Controller 작업

가장 중요한 실질적인 데이터를 처리하기 위한 Controller 작업을 진행한다.

#### lib/auth_controller.dart

##### `authControllerProvider`

```dart
final authControllerProvider =
    StateNotifierProvider<AuthController, bool>((ref) {
  return AuthController(
    authAPI: ref.watch(authAPIProvider),
    userController: ref.watch(userControllerProvider.notifier),
  );
});
```

이 Provider는 StateNotifierProvider로서 상태 변화가 감지되면 이를 알려주는 기능을 수행한다.

중요한 것은 <AuthController, bool>이다.

AuthController는 실질적인 API와 통신하고 Screen에 넘겨줄 데이터에 대한 로직을 담당하는 Class이다.

`bool`은 `State`. 변경된 데이터를 ref.watch()를 하는 곳에 넘겨준다.

이 코드는 bool을 넘겨주기 때문에 화면에서 서버에 보낸 Request가 정상적으로 바뀌었는지 확인할 수 있다.

##### `userControllerProvider`

```dart
final userControllerProvider =
    StateNotifierProvider<UserController, AccountModel?>((ref) {
  return UserController(null);
});
```

이 Provider는 로그인 유지를 위해서 사용자의 로그인이 성공했다면 AccountModel의 상태를 변경해줌으로서 로그인을 유지해 줄 수 있다.

기존에 authControllerProvider가 API와 통신은 이미했으니 authAPI는 필요하지 않다.

필요한 것은 UserController class를 참조하도록 해주는 것과

`AccountModel`은 `State`. 서버에서 받은 사용자 데이터를 상태에 저장시켜 ref.watch()를 통해 전역적으로 참조할 수 있게 해준다.

##### UserController

```dart
class UserController extends StateNotifier<AccountModel?> {
  UserController(AccountModel? state) : super(state);

  Future<void> setCurrentUser(AccountModel accountModel) async {
    state = accountModel;
  }
}
```

`StateNotifier`라는 이름에서 알 수 있듯이, 상태가 변한 것을 Provider에 알려준다. `<>`안에 들어있는 것이 state이다.

`AuchController`에서 서버로부터 받아온 사용자 데이터를 UserController의 `setCurrentuser` 함수에 전달해준다.

그럼 setCurrentUser에서 state에 저장해준다.

##### AuthController

```dart
class AuthController extends StateNotifier<bool> {
  final AuthAPI _authAPI;
  final UserController _userController;

  AuthController({
    required AuthAPI authAPI,
    required UserController userController,
  })  : _authAPI = authAPI,
        _userController = userController,
        super(false);

  Future<void> login({
    required String username,
    required String password,
    required BuildContext context,
  }) async {
    state = false;

    final response =
        await _authAPI.login(username: username, password: password);

    state = true;

    response.fold(
      (left) {
        logger.i('Error happened');
        final errorJson = json.decode(left.message);
        final errorMessage = errorJson['message'];
        showSnackBar(context, errorMessage.toString());
        logger.e(errorMessage);
      },
      (right) async {
        final response = utf8.decode(right.bodyBytes);
        final responseJson = json.decode(response);

        if (right.statusCode == 400) {
          final message = responseJson['message'];
          showSnackBar(context, message);
        }

        if (right.statusCode == 500) {
          final message = responseJson['message'];
          showSnackBar(context, message);
        }

        if (right.statusCode == 200) {
          List<String> roles = [];
          var rolesList = responseJson['data']['roles'];
          rolesList.forEach((role) {
            roles.add(role);
          });

          final String accessToken = responseJson['data']['access_token'];
          final String refreshToken = responseJson['data']['refresh_token'];

          AccountModel account = AccountModel(
            username: username,
            roles: roles,
            accessToken: accessToken,
            refreshToken: refreshToken,
          );

          showSnackBar(context, '로그인 성공');
          Navigator.push(context, HomeScreen.route());
          await _userController.setCurrentUser(account);
        }
      },
    );
  }


}
```

간단하게 로그인만 살펴본다.

`AuthController`의 상태 `<>` 는 `bool`이다.

`state = false`를 통해 서버에 요청 보내기 전에는 false로 해놓고, 서버에서 올바르게 데이터가 온다면 `state = true`로 상태를 바꿔준다.

상태를 바꿔주면 `authControllerProvider` == `StateNotifierProvider`에서 변경된 데이터를 참조해 알려준다.

API 요청에 대해 `response` 변수에 저장해주고, 이 값에 따라 left = 실패, right = 성공에 따른 작업을 진행해준다.

right.statusCode == 200. 서버로부터 성공적으로 응답이 온다면, `AccoumtModel`을 만들고

위에서 만들었던 `userController`의 `setCurrentUser`에 AccountModel을 넘겨준다.

이렇게 하면 userController에서 상태를 변화시키고, 마지막으로 `userControllerProvider`에서 변경된 데이터에 대해서 전역으로 알려준다.

