# Three.js


`Three.js`: three.js는 3D 그래픽을 생성하고 렌더링하기 위한 JavaScript 3D 라이브러리입니다. 웹 브라우저에서 3D 그래픽을 만들고 다루기 위해 사용되며, WebGL 기술을 기반으로 하여 다양한 3D 시각화 및 인터랙티브 웹 애플리케이션을 개발할 수 있게 해줍니다.

# Three.js

> https://threejs.org/

## 1. 시작

### 1.1 설치

three.js는 `npm`을 포함한 빌드 툴에서 설치가 가능하고, `CDN`이나 static 호스팅으로 빠르게 사용이 가능하다. 대부분의 경우 `npm`을 통한 설치가 가장 좋은 선택이다.

three.js의 모든 메서드들은 ES modules에 기반하고 있으며, 마지막 프로젝트에 필요한 부분만 불러오도록 할 것이다.

#### npm으로 설치하기

three npm 모듈을 설치하려면, 프로젝트 폴더의 터미널을 열고 다음을 실행한다.

```shell
npm install three
```

패키지가 다운로드 및 설치 될 것이며, 다음과 같이 코드에서 불러올 수 있을 것이다.

```Javascript
// Option 1: Import the entire three.js core library.
import * as THREE from 'three';

const scene = new THREE.Scene();


// Option 2: Import just the parts you need.
import { Scene } from 'three';

const scene = new Scene();
```

