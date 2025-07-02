# Ethical Hacker Cookbook


# Configurations

## Kali Linux

[Kali Linux](https://bobostown.tistory.com/7#:~:text=%ED%8C%8C%EC%9D%BC%20%EB%8B%A4%EC%9A%B4%EB%A1%9C%EB%93%9C%20%ED%95%98%EA%B8%B0-,kali%20linux%20%EA%B3%B5%EC%8B%9D%ED%99%88%ED%8E%98%EC%9D%B4%EC%A7%80,-%EB%A1%9C%20%EA%B0%80%EC%84%9C%20%EC%95%A0%ED%94%8C%EC%8B%A4%EB%A6%AC%EC%BD%98%EC%9A%A9)로 가서 애플실리콘 적용 이미지(내것은 M2, Apple Sillicon이니 **ARM64**)를 다운로드 한다.

Installer Image 카테고리를 누르고 Apple Sillicon을 선택한다.

Installer를 눌러 다운로드 한다.

## 가상 머신 설치하기

Kali Linux ISO(운영체제 이미지)를 올릴 가상 머신을 설치해준다.

맥에 가장 적절한 UTM을 사용한다. 

[공식 홈페이지](https://bobostown.tistory.com/7#:~:text=%EB%8B%A4%EC%9A%B4%EB%A1%9C%EB%93%9C%ED%95%98%EB%A9%B4%20%EA%B3%B5%EC%A7%9C%EC%9D%B4%EB%8B%A4.%0A%EB%94%B0%EB%9D%BC%EC%84%9C-,%EA%B3%B5%EC%8B%9D%ED%99%88%ED%8E%98%EC%9D%B4%EC%A7%80,-%EC%97%90%EC%84%9C%20%EB%8B%A4%EC%9A%B4%EB%A1%9C%EB%93%9C%20%ED%95%98%EB%8F%84%EB%A1%9D)에서 다운로드 해준다.

## Kali Linux 올리기

1. 새 가상머신 만들기

2. 가상화

3. Linux

4. 부팅 ISO Image의 찾아보기 -> 기존에 다운로드 받은 Kali Linux ISO 이미지 파이을 넣어준다.

5. CPU, Memory 설정은 필요에 따라 바꿔주고 설정을 마친다.

6. 설정이 끝난 후 바로 가상 머신을 키지 않고 **오른쪽 상단의 네비게이션바** 클릭 -> **장치의 새로 만들기** -> **직렬 포트** -> **저장**해준다.

7. UTM에서 Graphical Install로 하면 설치가 되지않는 이슈가 있으니 **Install**을 선택한다.



