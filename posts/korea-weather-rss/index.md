# Korea Weather RSS


# URL Format

<img src="/images/URI_syntax_diagram.svg" />

Ex)

- https://ce.snu.ac.kr?key1=v1&key2=v2

# Shebang?

스크립트 언어를 표현한다.

`#!/bin/sh`

`#!/bin/bash`

`#!/usr/bin/env python3`

```python
#!/user/bin/env python3

import sys
import urllib.request as req
import urllib.parse as parse
```

위와 같이 적으면, 패캐지들을 설치하거나 실행할 때 python3를 입력하지 않아도 된다.

# Virtual Env configuration

```shell
(venv)  {seilylook} 🍻 python3 -m virtualenv venv

(venv)  {seilylook} 🍻 source venv/bin/activate
```

# 원본 데이터

```xml
This XML file does not appear to have any style information associated with it. The document tree is shown below.
<rss version="2.0">
<channel>
<title>기상청 육상 중기예보</title>
<link>http://www.kma.go.kr/weather/forecast/mid-term_02.jsp</link>
<description>기상청 날씨 웹서비스</description>
<language>ko</language>
<generator>기상청</generator>
<pubDate>2024년 04월 17일 (수)요일 06:00</pubDate>
<item>
<author>기상청</author>
<category>육상중기예보</category>
<title>서울,경기도 육상 중기예보 - 2024년 04월 17일 (수)요일 06:00 발표</title>
<link>http://www.kma.go.kr/weather/forecast/mid-term_02.jsp</link>
<guid>http://www.kma.go.kr/weather/forecast/mid-term_02.jsp</guid>
<description>
<header>
<title>서울,경기도 육상중기예보</title>
<tm>202404170600</tm>
<wf>
<![CDATA[ ○ (강수) 20일(토) 오후는 비가 내리겠습니다.<br />○ (기온) 이번 예보기간 아침 기온은 7~14도, 낮 기온은 17~23도로 평년(최저기온 5~10도, 최고기온 18~21도)보다 조금 높겠습니다. <br />○ (해상) 서해중부해상의 물결은 20일(토) 오후에 1.0~2.5m로 일겠고, 그 밖의 날은 0.5~2.0m로 일겠습니다.<br />○ (주말전망) 20일(토)은 대체로 흐리고 오후에 비가 내리겠습니다. 21일(일)은 오전에 구름많다가 오후에 맑아지겠습니다. 아침 기온은 9~14도, 낮 기온은 17~23도가 되겠습니다.<br /><br />* 20일(토)~21일(일)과 23일(화)~24일(수)은 기압골의 발달 정도와 이동 속도에 따라 강수지역과 시점이 변동될 가능성이 있으니, 앞으로 발표되는 최신 예보를 참고하기 바랍니다. ]]>
</wf>
</header>
<body>
<location wl_ver="3">
<province>서울ㆍ인천ㆍ경기도</province>
<city>서울</city>
<data>
<mode>A02</mode>
<tmEf>2024-04-20 00:00</tmEf>
<wf>흐림</wf>
<tmn>14</tmn>
<tmx>17</tmx>
<reliability/>
<rnSt>40</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-20 12:00</tmEf>
<wf>흐리고 비</wf>
<tmn>14</tmn>
<tmx>17</tmx>
<reliability/>
<rnSt>70</rnSt>
</data>
<data>
...
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-21 12:00</tmEf>
<wf>맑음</wf>
<tmn>11</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>10</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-22 00:00</tmEf>
<wf>맑음</wf>
<tmn>11</tmn>
<tmx>23</tmx>
<reliability/>
<rnSt>10</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-22 12:00</tmEf>
<wf>구름많음</wf>
<tmn>11</tmn>
<tmx>23</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-23 00:00</tmEf>
<wf>구름많음</wf>
<tmn>11</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-23 12:00</tmEf>
<wf>구름많음</wf>
<tmn>11</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-24 00:00</tmEf>
<wf>맑음</wf>
<tmn>12</tmn>
<tmx>21</tmx>
<reliability/>
<rnSt>20</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-24 12:00</tmEf>
<wf>맑음</wf>
<tmn>12</tmn>
<tmx>21</tmx>
<reliability/>
<rnSt>10</rnSt>
</data>
<data>
<mode>A01</mode>
<tmEf>2024-04-25 00:00</tmEf>
<wf>맑음</wf>
<tmn>12</tmn>
<tmx>23</tmx>
<reliability/>
<rnSt>10</rnSt>
</data>
<data>
<mode>A01</mode>
<tmEf>2024-04-26 00:00</tmEf>
<wf>맑음</wf>
<tmn>12</tmn>
<tmx>23</tmx>
<reliability/>
<rnSt>20</rnSt>
</data>
<data>
<mode>A01</mode>
<tmEf>2024-04-27 00:00</tmEf>
<wf>구름많음</wf>
<tmn>12</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
</location>
<location wl_ver="3">
<province>서울ㆍ인천ㆍ경기도</province>
<city>인천</city>
<data>
<mode>A02</mode>
<tmEf>2024-04-20 00:00</tmEf>
<wf>흐림</wf>
<tmn>13</tmn>
<tmx>17</tmx>
<reliability/>
<rnSt>40</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-20 12:00</tmEf>
<wf>흐리고 비</wf>
<tmn>13</tmn>
<tmx>17</tmx>
<reliability/>
<rnSt>70</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-21 00:00</tmEf>
<wf>구름많음</wf>
<tmn>11</tmn>
<tmx>20</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-21 12:00</tmEf>
<wf>맑음</wf>
<tmn>11</tmn>
<tmx>20</tmx>
<reliability/>
<rnSt>10</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-22 00:00</tmEf>
<wf>맑음</wf>
<tmn>11</tmn>
<tmx>20</tmx>
<reliability/>
<rnSt>10</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-22 12:00</tmEf>
<wf>구름많음</wf>
<tmn>11</tmn>
<tmx>20</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-23 00:00</tmEf>
<wf>구름많음</wf>
<tmn>11</tmn>
<tmx>19</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-23 12:00</tmEf>
<wf>구름많음</wf>
<tmn>11</tmn>
<tmx>19</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-24 00:00</tmEf>
<wf>맑음</wf>
<tmn>10</tmn>
<tmx>19</tmx>
<reliability/>
<rnSt>20</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-24 12:00</tmEf>
<wf>맑음</wf>
<tmn>10</tmn>
<tmx>19</tmx>
<reliability/>
<rnSt>10</rnSt>
</data>
<data>
<mode>A01</mode>
<tmEf>2024-04-25 00:00</tmEf>
<wf>맑음</wf>
<tmn>11</tmn>
<tmx>19</tmx>
<reliability/>
<rnSt>10</rnSt>
</data>
<data>
<mode>A01</mode>
<tmEf>2024-04-26 00:00</tmEf>
<wf>맑음</wf>
<tmn>11</tmn>
<tmx>18</tmx>
<reliability/>
<rnSt>20</rnSt>
</data>
<data>
<mode>A01</mode>
<tmEf>2024-04-27 00:00</tmEf>
<wf>구름많음</wf>
<tmn>11</tmn>
<tmx>18</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
</location>
<location wl_ver="3">
<province>서울ㆍ인천ㆍ경기도</province>
<city>수원</city>
<data>
<mode>A02</mode>
<tmEf>2024-04-20 00:00</tmEf>
<wf>흐림</wf>
<tmn>12</tmn>
<tmx>17</tmx>
<reliability/>
<rnSt>40</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-20 12:00</tmEf>
<wf>흐리고 비</wf>
<tmn>12</tmn>
<tmx>17</tmx>
<reliability/>
<rnSt>70</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-21 00:00</tmEf>
<wf>구름많음</wf>
<tmn>11</tmn>
<tmx>21</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-21 12:00</tmEf>
<wf>맑음</wf>
<tmn>11</tmn>
<tmx>21</tmx>
<reliability/>
<rnSt>10</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-22 00:00</tmEf>
<wf>맑음</wf>
<tmn>10</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>10</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-22 12:00</tmEf>
<wf>구름많음</wf>
<tmn>10</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-23 00:00</tmEf>
<wf>구름많음</wf>
<tmn>10</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-23 12:00</tmEf>
<wf>구름많음</wf>
<tmn>10</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-24 00:00</tmEf>
<wf>맑음</wf>
<tmn>9</tmn>
<tmx>21</tmx>
<reliability/>
<rnSt>20</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-24 12:00</tmEf>
<wf>맑음</wf>
<tmn>9</tmn>
<tmx>21</tmx>
<reliability/>
<rnSt>10</rnSt>
</data>
<data>
<mode>A01</mode>
<tmEf>2024-04-25 00:00</tmEf>
<wf>맑음</wf>
<tmn>10</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>10</rnSt>
</data>
<data>
<mode>A01</mode>
<tmEf>2024-04-26 00:00</tmEf>
<wf>맑음</wf>
<tmn>10</tmn>
<tmx>23</tmx>
<reliability/>
<rnSt>20</rnSt>
</data>
<data>
<mode>A01</mode>
<tmEf>2024-04-27 00:00</tmEf>
<wf>구름많음</wf>
<tmn>10</tmn>
<tmx>23</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
</location>
<location wl_ver="3">
<province>서울ㆍ인천ㆍ경기도</province>
<city>파주</city>
<data>
<mode>A02</mode>
<tmEf>2024-04-20 00:00</tmEf>
<wf>흐림</wf>
<tmn>10</tmn>
<tmx>18</tmx>
<reliability/>
<rnSt>40</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-20 12:00</tmEf>
<wf>흐리고 비</wf>
<tmn>10</tmn>
<tmx>18</tmx>
<reliability/>
<rnSt>70</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-21 00:00</tmEf>
<wf>구름많음</wf>
<tmn>9</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-21 12:00</tmEf>
<wf>맑음</wf>
<tmn>9</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>10</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-22 00:00</tmEf>
<wf>맑음</wf>
<tmn>7</tmn>
<tmx>23</tmx>
<reliability/>
<rnSt>10</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-22 12:00</tmEf>
<wf>구름많음</wf>
<tmn>7</tmn>
<tmx>23</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-23 00:00</tmEf>
<wf>구름많음</wf>
<tmn>8</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-23 12:00</tmEf>
<wf>구름많음</wf>
<tmn>8</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-24 00:00</tmEf>
<wf>맑음</wf>
<tmn>8</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>20</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-24 12:00</tmEf>
<wf>맑음</wf>
<tmn>8</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>10</rnSt>
</data>
<data>
<mode>A01</mode>
<tmEf>2024-04-25 00:00</tmEf>
<wf>맑음</wf>
<tmn>8</tmn>
<tmx>23</tmx>
<reliability/>
<rnSt>10</rnSt>
</data>
<data>
<mode>A01</mode>
<tmEf>2024-04-26 00:00</tmEf>
<wf>맑음</wf>
<tmn>9</tmn>
<tmx>23</tmx>
<reliability/>
<rnSt>20</rnSt>
</data>
<data>
<mode>A01</mode>
<tmEf>2024-04-27 00:00</tmEf>
<wf>구름많음</wf>
<tmn>8</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
</location>
<location wl_ver="3">
<province>서울ㆍ인천ㆍ경기도</province>
<city>이천</city>
<data>
<mode>A02</mode>
<tmEf>2024-04-20 00:00</tmEf>
<wf>흐림</wf>
<tmn>11</tmn>
<tmx>18</tmx>
<reliability/>
<rnSt>40</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-20 12:00</tmEf>
<wf>흐리고 비</wf>
<tmn>11</tmn>
<tmx>18</tmx>
<reliability/>
<rnSt>70</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-21 00:00</tmEf>
<wf>구름많음</wf>
<tmn>11</tmn>
<tmx>23</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-21 12:00</tmEf>
<wf>맑음</wf>
<tmn>11</tmn>
<tmx>23</tmx>
<reliability/>
<rnSt>10</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-22 00:00</tmEf>
<wf>맑음</wf>
<tmn>8</tmn>
<tmx>23</tmx>
<reliability/>
<rnSt>10</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-22 12:00</tmEf>
<wf>구름많음</wf>
<tmn>8</tmn>
<tmx>23</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-23 00:00</tmEf>
<wf>구름많음</wf>
<tmn>8</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-23 12:00</tmEf>
<wf>구름많음</wf>
<tmn>8</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-24 00:00</tmEf>
<wf>맑음</wf>
<tmn>9</tmn>
<tmx>21</tmx>
<reliability/>
<rnSt>20</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-24 12:00</tmEf>
<wf>맑음</wf>
<tmn>9</tmn>
<tmx>21</tmx>
<reliability/>
<rnSt>10</rnSt>
</data>
<data>
<mode>A01</mode>
<tmEf>2024-04-25 00:00</tmEf>
<wf>맑음</wf>
<tmn>9</tmn>
<tmx>23</tmx>
<reliability/>
<rnSt>10</rnSt>
</data>
<data>
<mode>A01</mode>
<tmEf>2024-04-26 00:00</tmEf>
<wf>맑음</wf>
<tmn>10</tmn>
<tmx>23</tmx>
<reliability/>
<rnSt>20</rnSt>
</data>
<data>
<mode>A01</mode>
<tmEf>2024-04-27 00:00</tmEf>
<wf>구름많음</wf>
<tmn>9</tmn>
<tmx>23</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
</location>
<location wl_ver="3">
<province>서울ㆍ인천ㆍ경기도</province>
<city>평택</city>
<data>
<mode>A02</mode>
<tmEf>2024-04-20 00:00</tmEf>
<wf>흐림</wf>
<tmn>12</tmn>
<tmx>17</tmx>
<reliability/>
<rnSt>40</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-20 12:00</tmEf>
<wf>흐리고 비</wf>
<tmn>12</tmn>
<tmx>17</tmx>
<reliability/>
<rnSt>70</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-21 00:00</tmEf>
<wf>구름많음</wf>
<tmn>12</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-21 12:00</tmEf>
<wf>맑음</wf>
<tmn>12</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>10</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-22 00:00</tmEf>
<wf>맑음</wf>
<tmn>10</tmn>
<tmx>23</tmx>
<reliability/>
<rnSt>10</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-22 12:00</tmEf>
<wf>구름많음</wf>
<tmn>10</tmn>
<tmx>23</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-23 00:00</tmEf>
<wf>구름많음</wf>
<tmn>9</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-23 12:00</tmEf>
<wf>구름많음</wf>
<tmn>9</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-24 00:00</tmEf>
<wf>맑음</wf>
<tmn>9</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>20</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-24 12:00</tmEf>
<wf>맑음</wf>
<tmn>9</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>10</rnSt>
</data>
<data>
<mode>A01</mode>
<tmEf>2024-04-25 00:00</tmEf>
<wf>맑음</wf>
<tmn>10</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>10</rnSt>
</data>
<data>
<mode>A01</mode>
<tmEf>2024-04-26 00:00</tmEf>
<wf>맑음</wf>
<tmn>10</tmn>
<tmx>21</tmx>
<reliability/>
<rnSt>20</rnSt>
</data>
<data>
<mode>A01</mode>
<tmEf>2024-04-27 00:00</tmEf>
<wf>구름많음</wf>
<tmn>9</tmn>
<tmx>23</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
</location>
<location wl_ver="3">
<province>서울ㆍ인천ㆍ경기도</province>
<city>백령도</city>
<data>
<mode>A02</mode>
<tmEf>2024-04-20 00:00</tmEf>
<wf>흐림</wf>
<tmn>10</tmn>
<tmx>15</tmx>
<reliability/>
<rnSt>40</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-20 12:00</tmEf>
<wf>흐리고 비</wf>
<tmn>10</tmn>
<tmx>15</tmx>
<reliability/>
<rnSt>70</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-21 00:00</tmEf>
<wf>구름많음</wf>
<tmn>8</tmn>
<tmx>15</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-21 12:00</tmEf>
<wf>맑음</wf>
<tmn>8</tmn>
<tmx>15</tmx>
<reliability/>
<rnSt>10</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-22 00:00</tmEf>
<wf>맑음</wf>
<tmn>9</tmn>
<tmx>15</tmx>
<reliability/>
<rnSt>10</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-22 12:00</tmEf>
<wf>구름많음</wf>
<tmn>9</tmn>
<tmx>15</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-23 00:00</tmEf>
<wf>구름많음</wf>
<tmn>9</tmn>
<tmx>15</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-23 12:00</tmEf>
<wf>구름많음</wf>
<tmn>9</tmn>
<tmx>15</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-24 00:00</tmEf>
<wf>맑음</wf>
<tmn>9</tmn>
<tmx>15</tmx>
<reliability/>
<rnSt>20</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-24 12:00</tmEf>
<wf>맑음</wf>
<tmn>9</tmn>
<tmx>15</tmx>
<reliability/>
<rnSt>10</rnSt>
</data>
<data>
<mode>A01</mode>
<tmEf>2024-04-25 00:00</tmEf>
<wf>맑음</wf>
<tmn>9</tmn>
<tmx>16</tmx>
<reliability/>
<rnSt>10</rnSt>
</data>
<data>
<mode>A01</mode>
<tmEf>2024-04-26 00:00</tmEf>
<wf>맑음</wf>
<tmn>10</tmn>
<tmx>16</tmx>
<reliability/>
<rnSt>20</rnSt>
</data>
<data>
<mode>A01</mode>
<tmEf>2024-04-27 00:00</tmEf>
<wf>구름많음</wf>
<tmn>9</tmn>
<tmx>15</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
</location>
<location wl_ver="3">
<province>서울ㆍ인천ㆍ경기도</province>
<city>과천</city>
<data>
<mode>A02</mode>
<tmEf>2024-04-20 00:00</tmEf>
<wf>흐림</wf>
<tmn>12</tmn>
<tmx>17</tmx>
<reliability/>
<rnSt>40</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-20 12:00</tmEf>
<wf>흐리고 비</wf>
<tmn>12</tmn>
<tmx>17</tmx>
<reliability/>
<rnSt>70</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-21 00:00</tmEf>
<wf>구름많음</wf>
<tmn>12</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-21 12:00</tmEf>
<wf>맑음</wf>
<tmn>12</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>10</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-22 00:00</tmEf>
<wf>맑음</wf>
<tmn>9</tmn>
<tmx>23</tmx>
<reliability/>
<rnSt>10</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-22 12:00</tmEf>
<wf>구름많음</wf>
<tmn>9</tmn>
<tmx>23</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-23 00:00</tmEf>
<wf>구름많음</wf>
<tmn>9</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-23 12:00</tmEf>
<wf>구름많음</wf>
<tmn>9</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-24 00:00</tmEf>
<wf>맑음</wf>
<tmn>8</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>20</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-24 12:00</tmEf>
<wf>맑음</wf>
<tmn>8</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>10</rnSt>
</data>
<data>
<mode>A01</mode>
<tmEf>2024-04-25 00:00</tmEf>
<wf>맑음</wf>
<tmn>10</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>10</rnSt>
</data>
<data>
<mode>A01</mode>
<tmEf>2024-04-26 00:00</tmEf>
<wf>맑음</wf>
<tmn>10</tmn>
<tmx>23</tmx>
<reliability/>
<rnSt>20</rnSt>
</data>
<data>
<mode>A01</mode>
<tmEf>2024-04-27 00:00</tmEf>
<wf>구름많음</wf>
<tmn>9</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
</location>
<location wl_ver="3">
<province>서울ㆍ인천ㆍ경기도</province>
<city>광명</city>
<data>
<mode>A02</mode>
<tmEf>2024-04-20 00:00</tmEf>
<wf>흐림</wf>
<tmn>15</tmn>
<tmx>17</tmx>
<reliability/>
<rnSt>40</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-20 12:00</tmEf>
<wf>흐리고 비</wf>
<tmn>15</tmn>
<tmx>17</tmx>
<reliability/>
<rnSt>70</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-21 00:00</tmEf>
<wf>구름많음</wf>
<tmn>13</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-21 12:00</tmEf>
<wf>맑음</wf>
<tmn>13</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>10</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-22 00:00</tmEf>
<wf>맑음</wf>
<tmn>12</tmn>
<tmx>23</tmx>
<reliability/>
<rnSt>10</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-22 12:00</tmEf>
<wf>구름많음</wf>
<tmn>12</tmn>
<tmx>23</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-23 00:00</tmEf>
<wf>구름많음</wf>
<tmn>12</tmn>
<tmx>21</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-23 12:00</tmEf>
<wf>구름많음</wf>
<tmn>12</tmn>
<tmx>21</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-24 00:00</tmEf>
<wf>맑음</wf>
<tmn>12</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>20</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-24 12:00</tmEf>
<wf>맑음</wf>
<tmn>12</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>10</rnSt>
</data>
<data>
<mode>A01</mode>
<tmEf>2024-04-25 00:00</tmEf>
<wf>맑음</wf>
<tmn>12</tmn>
<tmx>21</tmx>
<reliability/>
<rnSt>10</rnSt>
</data>
<data>
<mode>A01</mode>
<tmEf>2024-04-26 00:00</tmEf>
<wf>맑음</wf>
<tmn>12</tmn>
<tmx>23</tmx>
<reliability/>
<rnSt>20</rnSt>
</data>
<data>
<mode>A01</mode>
<tmEf>2024-04-27 00:00</tmEf>
<wf>구름많음</wf>
<tmn>11</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
</location>
<location wl_ver="3">
<province>서울ㆍ인천ㆍ경기도</province>
<city>강화</city>
<data>
<mode>A02</mode>
<tmEf>2024-04-20 00:00</tmEf>
<wf>흐림</wf>
<tmn>10</tmn>
<tmx>17</tmx>
<reliability/>
<rnSt>40</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-20 12:00</tmEf>
<wf>흐리고 비</wf>
<tmn>10</tmn>
<tmx>17</tmx>
<reliability/>
<rnSt>70</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-21 00:00</tmEf>
<wf>구름많음</wf>
<tmn>8</tmn>
<tmx>19</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-21 12:00</tmEf>
<wf>맑음</wf>
<tmn>8</tmn>
<tmx>19</tmx>
<reliability/>
<rnSt>10</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-22 00:00</tmEf>
<wf>맑음</wf>
<tmn>9</tmn>
<tmx>20</tmx>
<reliability/>
<rnSt>10</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-22 12:00</tmEf>
<wf>구름많음</wf>
<tmn>9</tmn>
<tmx>20</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-23 00:00</tmEf>
<wf>구름많음</wf>
<tmn>9</tmn>
<tmx>20</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-23 12:00</tmEf>
<wf>구름많음</wf>
<tmn>9</tmn>
<tmx>20</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-24 00:00</tmEf>
<wf>맑음</wf>
<tmn>8</tmn>
<tmx>20</tmx>
<reliability/>
<rnSt>20</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-24 12:00</tmEf>
<wf>맑음</wf>
<tmn>8</tmn>
<tmx>20</tmx>
<reliability/>
<rnSt>10</rnSt>
</data>
<data>
<mode>A01</mode>
<tmEf>2024-04-25 00:00</tmEf>
<wf>맑음</wf>
<tmn>9</tmn>
<tmx>19</tmx>
<reliability/>
<rnSt>10</rnSt>
</data>
<data>
<mode>A01</mode>
<tmEf>2024-04-26 00:00</tmEf>
<wf>맑음</wf>
<tmn>9</tmn>
<tmx>20</tmx>
<reliability/>
<rnSt>20</rnSt>
</data>
<data>
<mode>A01</mode>
<tmEf>2024-04-27 00:00</tmEf>
<wf>구름많음</wf>
<tmn>9</tmn>
<tmx>19</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
</location>
<location wl_ver="3">
<province>서울ㆍ인천ㆍ경기도</province>
<city>김포</city>
<data>
<mode>A02</mode>
<tmEf>2024-04-20 00:00</tmEf>
<wf>흐림</wf>
<tmn>12</tmn>
<tmx>18</tmx>
<reliability/>
<rnSt>40</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-20 12:00</tmEf>
<wf>흐리고 비</wf>
<tmn>12</tmn>
<tmx>18</tmx>
<reliability/>
<rnSt>70</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-21 00:00</tmEf>
<wf>구름많음</wf>
<tmn>11</tmn>
<tmx>21</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-21 12:00</tmEf>
<wf>맑음</wf>
<tmn>11</tmn>
<tmx>21</tmx>
<reliability/>
<rnSt>10</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-22 00:00</tmEf>
<wf>맑음</wf>
<tmn>10</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>10</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-22 12:00</tmEf>
<wf>구름많음</wf>
<tmn>10</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-23 00:00</tmEf>
<wf>구름많음</wf>
<tmn>10</tmn>
<tmx>20</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-23 12:00</tmEf>
<wf>구름많음</wf>
<tmn>10</tmn>
<tmx>20</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-24 00:00</tmEf>
<wf>맑음</wf>
<tmn>8</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>20</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-24 12:00</tmEf>
<wf>맑음</wf>
<tmn>8</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>10</rnSt>
</data>
<data>
<mode>A01</mode>
<tmEf>2024-04-25 00:00</tmEf>
<wf>맑음</wf>
<tmn>10</tmn>
<tmx>21</tmx>
<reliability/>
<rnSt>10</rnSt>
</data>
<data>
<mode>A01</mode>
<tmEf>2024-04-26 00:00</tmEf>
<wf>맑음</wf>
<tmn>10</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>20</rnSt>
</data>
<data>
<mode>A01</mode>
<tmEf>2024-04-27 00:00</tmEf>
<wf>구름많음</wf>
<tmn>9</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
</location>
<location wl_ver="3">
<province>서울ㆍ인천ㆍ경기도</province>
<city>시흥</city>
<data>
<mode>A02</mode>
<tmEf>2024-04-20 00:00</tmEf>
<wf>흐림</wf>
<tmn>12</tmn>
<tmx>17</tmx>
<reliability/>
<rnSt>40</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-20 12:00</tmEf>
<wf>흐리고 비</wf>
<tmn>12</tmn>
<tmx>17</tmx>
<reliability/>
<rnSt>70</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-21 00:00</tmEf>
<wf>구름많음</wf>
<tmn>11</tmn>
<tmx>21</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-21 12:00</tmEf>
<wf>맑음</wf>
<tmn>11</tmn>
<tmx>21</tmx>
<reliability/>
<rnSt>10</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-22 00:00</tmEf>
<wf>맑음</wf>
<tmn>9</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>10</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-22 12:00</tmEf>
<wf>구름많음</wf>
<tmn>9</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-23 00:00</tmEf>
<wf>구름많음</wf>
<tmn>9</tmn>
<tmx>20</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-23 12:00</tmEf>
<wf>구름많음</wf>
<tmn>9</tmn>
<tmx>20</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-24 00:00</tmEf>
<wf>맑음</wf>
<tmn>8</tmn>
<tmx>21</tmx>
<reliability/>
<rnSt>20</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-24 12:00</tmEf>
<wf>맑음</wf>
<tmn>8</tmn>
<tmx>21</tmx>
<reliability/>
<rnSt>10</rnSt>
</data>
<data>
<mode>A01</mode>
<tmEf>2024-04-25 00:00</tmEf>
<wf>맑음</wf>
<tmn>10</tmn>
<tmx>20</tmx>
<reliability/>
<rnSt>10</rnSt>
</data>
<data>
<mode>A01</mode>
<tmEf>2024-04-26 00:00</tmEf>
<wf>맑음</wf>
<tmn>9</tmn>
<tmx>21</tmx>
<reliability/>
<rnSt>20</rnSt>
</data>
<data>
<mode>A01</mode>
<tmEf>2024-04-27 00:00</tmEf>
<wf>구름많음</wf>
<tmn>9</tmn>
<tmx>21</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
</location>
<location wl_ver="3">
<province>서울ㆍ인천ㆍ경기도</province>
<city>안산</city>
<data>
<mode>A02</mode>
<tmEf>2024-04-20 00:00</tmEf>
<wf>흐림</wf>
<tmn>12</tmn>
<tmx>17</tmx>
<reliability/>
<rnSt>40</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-20 12:00</tmEf>
<wf>흐리고 비</wf>
<tmn>12</tmn>
<tmx>17</tmx>
<reliability/>
<rnSt>70</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-21 00:00</tmEf>
<wf>구름많음</wf>
<tmn>12</tmn>
<tmx>21</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-21 12:00</tmEf>
<wf>맑음</wf>
<tmn>12</tmn>
<tmx>21</tmx>
<reliability/>
<rnSt>10</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-22 00:00</tmEf>
<wf>맑음</wf>
<tmn>9</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>10</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-22 12:00</tmEf>
<wf>구름많음</wf>
<tmn>9</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-23 00:00</tmEf>
<wf>구름많음</wf>
<tmn>9</tmn>
<tmx>21</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-23 12:00</tmEf>
<wf>구름많음</wf>
<tmn>9</tmn>
<tmx>21</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-24 00:00</tmEf>
<wf>맑음</wf>
<tmn>8</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>20</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-24 12:00</tmEf>
<wf>맑음</wf>
<tmn>8</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>10</rnSt>
</data>
<data>
<mode>A01</mode>
<tmEf>2024-04-25 00:00</tmEf>
<wf>맑음</wf>
<tmn>10</tmn>
<tmx>21</tmx>
<reliability/>
<rnSt>10</rnSt>
</data>
<data>
<mode>A01</mode>
<tmEf>2024-04-26 00:00</tmEf>
<wf>맑음</wf>
<tmn>9</tmn>
<tmx>23</tmx>
<reliability/>
<rnSt>20</rnSt>
</data>
<data>
<mode>A01</mode>
<tmEf>2024-04-27 00:00</tmEf>
<wf>구름많음</wf>
<tmn>9</tmn>
<tmx>23</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
</location>
<location wl_ver="3">
<province>서울ㆍ인천ㆍ경기도</province>
<city>부천</city>
<data>
<mode>A02</mode>
<tmEf>2024-04-20 00:00</tmEf>
<wf>흐림</wf>
<tmn>13</tmn>
<tmx>17</tmx>
<reliability/>
<rnSt>40</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-20 12:00</tmEf>
<wf>흐리고 비</wf>
<tmn>13</tmn>
<tmx>17</tmx>
<reliability/>
<rnSt>70</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-21 00:00</tmEf>
<wf>구름많음</wf>
<tmn>11</tmn>
<tmx>21</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-21 12:00</tmEf>
<wf>맑음</wf>
<tmn>11</tmn>
<tmx>21</tmx>
<reliability/>
<rnSt>10</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-22 00:00</tmEf>
<wf>맑음</wf>
<tmn>11</tmn>
<tmx>21</tmx>
<reliability/>
<rnSt>10</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-22 12:00</tmEf>
<wf>구름많음</wf>
<tmn>11</tmn>
<tmx>21</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-23 00:00</tmEf>
<wf>구름많음</wf>
<tmn>10</tmn>
<tmx>20</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-23 12:00</tmEf>
<wf>구름많음</wf>
<tmn>10</tmn>
<tmx>20</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-24 00:00</tmEf>
<wf>맑음</wf>
<tmn>10</tmn>
<tmx>21</tmx>
<reliability/>
<rnSt>20</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-24 12:00</tmEf>
<wf>맑음</wf>
<tmn>10</tmn>
<tmx>21</tmx>
<reliability/>
<rnSt>10</rnSt>
</data>
<data>
<mode>A01</mode>
<tmEf>2024-04-25 00:00</tmEf>
<wf>맑음</wf>
<tmn>11</tmn>
<tmx>20</tmx>
<reliability/>
<rnSt>10</rnSt>
</data>
<data>
<mode>A01</mode>
<tmEf>2024-04-26 00:00</tmEf>
<wf>맑음</wf>
<tmn>11</tmn>
<tmx>20</tmx>
<reliability/>
<rnSt>20</rnSt>
</data>
<data>
<mode>A01</mode>
<tmEf>2024-04-27 00:00</tmEf>
<wf>구름많음</wf>
<tmn>12</tmn>
<tmx>20</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
</location>
<location wl_ver="3">
<province>서울ㆍ인천ㆍ경기도</province>
<city>의정부</city>
<data>
<mode>A02</mode>
<tmEf>2024-04-20 00:00</tmEf>
<wf>흐림</wf>
<tmn>12</tmn>
<tmx>18</tmx>
<reliability/>
<rnSt>40</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-20 12:00</tmEf>
<wf>흐리고 비</wf>
<tmn>12</tmn>
<tmx>18</tmx>
<reliability/>
<rnSt>70</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-21 00:00</tmEf>
<wf>구름많음</wf>
<tmn>10</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-21 12:00</tmEf>
<wf>맑음</wf>
<tmn>10</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>10</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-22 00:00</tmEf>
<wf>맑음</wf>
<tmn>9</tmn>
<tmx>23</tmx>
<reliability/>
<rnSt>10</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-22 12:00</tmEf>
<wf>구름많음</wf>
<tmn>9</tmn>
<tmx>23</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-23 00:00</tmEf>
<wf>구름많음</wf>
<tmn>8</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-23 12:00</tmEf>
<wf>구름많음</wf>
<tmn>8</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-24 00:00</tmEf>
<wf>맑음</wf>
<tmn>8</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>20</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-24 12:00</tmEf>
<wf>맑음</wf>
<tmn>8</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>10</rnSt>
</data>
<data>
<mode>A01</mode>
<tmEf>2024-04-25 00:00</tmEf>
<wf>맑음</wf>
<tmn>9</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>10</rnSt>
</data>
<data>
<mode>A01</mode>
<tmEf>2024-04-26 00:00</tmEf>
<wf>맑음</wf>
<tmn>10</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>20</rnSt>
</data>
<data>
<mode>A01</mode>
<tmEf>2024-04-27 00:00</tmEf>
<wf>구름많음</wf>
<tmn>10</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
</location>
<location wl_ver="3">
<province>서울ㆍ인천ㆍ경기도</province>
<city>고양</city>
<data>
<mode>A02</mode>
<tmEf>2024-04-20 00:00</tmEf>
<wf>흐림</wf>
<tmn>12</tmn>
<tmx>18</tmx>
<reliability/>
<rnSt>40</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-20 12:00</tmEf>
<wf>흐리고 비</wf>
<tmn>12</tmn>
<tmx>18</tmx>
<reliability/>
<rnSt>70</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-21 00:00</tmEf>
<wf>구름많음</wf>
<tmn>10</tmn>
<tmx>23</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-21 12:00</tmEf>
<wf>맑음</wf>
<tmn>10</tmn>
<tmx>23</tmx>
<reliability/>
<rnSt>10</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-22 00:00</tmEf>
<wf>맑음</wf>
<tmn>9</tmn>
<tmx>24</tmx>
<reliability/>
<rnSt>10</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-22 12:00</tmEf>
<wf>구름많음</wf>
<tmn>9</tmn>
<tmx>24</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-23 00:00</tmEf>
<wf>구름많음</wf>
<tmn>8</tmn>
<tmx>23</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-23 12:00</tmEf>
<wf>구름많음</wf>
<tmn>8</tmn>
<tmx>23</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-24 00:00</tmEf>
<wf>맑음</wf>
<tmn>8</tmn>
<tmx>23</tmx>
<reliability/>
<rnSt>20</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-24 12:00</tmEf>
<wf>맑음</wf>
<tmn>8</tmn>
<tmx>23</tmx>
<reliability/>
<rnSt>10</rnSt>
</data>
<data>
<mode>A01</mode>
<tmEf>2024-04-25 00:00</tmEf>
<wf>맑음</wf>
<tmn>9</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>10</rnSt>
</data>
<data>
<mode>A01</mode>
<tmEf>2024-04-26 00:00</tmEf>
<wf>맑음</wf>
<tmn>9</tmn>
<tmx>23</tmx>
<reliability/>
<rnSt>20</rnSt>
</data>
<data>
<mode>A01</mode>
<tmEf>2024-04-27 00:00</tmEf>
<wf>구름많음</wf>
<tmn>8</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
</location>
<location wl_ver="3">
<province>서울ㆍ인천ㆍ경기도</province>
<city>양주</city>
<data>
<mode>A02</mode>
<tmEf>2024-04-20 00:00</tmEf>
<wf>흐림</wf>
<tmn>11</tmn>
<tmx>18</tmx>
<reliability/>
<rnSt>40</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-20 12:00</tmEf>
<wf>흐리고 비</wf>
<tmn>11</tmn>
<tmx>18</tmx>
<reliability/>
<rnSt>70</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-21 00:00</tmEf>
<wf>구름많음</wf>
<tmn>9</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-21 12:00</tmEf>
<wf>맑음</wf>
<tmn>9</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>10</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-22 00:00</tmEf>
<wf>맑음</wf>
<tmn>7</tmn>
<tmx>23</tmx>
<reliability/>
<rnSt>10</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-22 12:00</tmEf>
<wf>구름많음</wf>
<tmn>7</tmn>
<tmx>23</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-23 00:00</tmEf>
<wf>구름많음</wf>
<tmn>7</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-23 12:00</tmEf>
<wf>구름많음</wf>
<tmn>7</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-24 00:00</tmEf>
<wf>맑음</wf>
<tmn>7</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>20</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-24 12:00</tmEf>
<wf>맑음</wf>
<tmn>7</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>10</rnSt>
</data>
<data>
<mode>A01</mode>
<tmEf>2024-04-25 00:00</tmEf>
<wf>맑음</wf>
<tmn>8</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>10</rnSt>
</data>
<data>
<mode>A01</mode>
<tmEf>2024-04-26 00:00</tmEf>
<wf>맑음</wf>
<tmn>9</tmn>
<tmx>23</tmx>
<reliability/>
<rnSt>20</rnSt>
</data>
<data>
<mode>A01</mode>
<tmEf>2024-04-27 00:00</tmEf>
<wf>구름많음</wf>
<tmn>7</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
</location>
<location wl_ver="3">
<province>서울ㆍ인천ㆍ경기도</province>
<city>동두천</city>
<data>
<mode>A02</mode>
<tmEf>2024-04-20 00:00</tmEf>
<wf>흐림</wf>
<tmn>11</tmn>
<tmx>19</tmx>
<reliability/>
<rnSt>40</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-20 12:00</tmEf>
<wf>흐리고 비</wf>
<tmn>11</tmn>
<tmx>19</tmx>
<reliability/>
<rnSt>70</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-21 00:00</tmEf>
<wf>구름많음</wf>
<tmn>10</tmn>
<tmx>23</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-21 12:00</tmEf>
<wf>맑음</wf>
<tmn>10</tmn>
<tmx>23</tmx>
<reliability/>
<rnSt>10</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-22 00:00</tmEf>
<wf>맑음</wf>
<tmn>9</tmn>
<tmx>24</tmx>
<reliability/>
<rnSt>10</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-22 12:00</tmEf>
<wf>구름많음</wf>
<tmn>9</tmn>
<tmx>24</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-23 00:00</tmEf>
<wf>구름많음</wf>
<tmn>9</tmn>
<tmx>23</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-23 12:00</tmEf>
<wf>구름많음</wf>
<tmn>9</tmn>
<tmx>23</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-24 00:00</tmEf>
<wf>맑음</wf>
<tmn>9</tmn>
<tmx>23</tmx>
<reliability/>
<rnSt>20</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-24 12:00</tmEf>
<wf>맑음</wf>
<tmn>9</tmn>
<tmx>23</tmx>
<reliability/>
<rnSt>10</rnSt>
</data>
<data>
<mode>A01</mode>
<tmEf>2024-04-25 00:00</tmEf>
<wf>맑음</wf>
<tmn>10</tmn>
<tmx>23</tmx>
<reliability/>
<rnSt>10</rnSt>
</data>
<data>
<mode>A01</mode>
<tmEf>2024-04-26 00:00</tmEf>
<wf>맑음</wf>
<tmn>10</tmn>
<tmx>24</tmx>
<reliability/>
<rnSt>20</rnSt>
</data>
<data>
<mode>A01</mode>
<tmEf>2024-04-27 00:00</tmEf>
<wf>구름많음</wf>
<tmn>9</tmn>
<tmx>23</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
</location>
<location wl_ver="3">
<province>서울ㆍ인천ㆍ경기도</province>
<city>연천</city>
<data>
<mode>A02</mode>
<tmEf>2024-04-20 00:00</tmEf>
<wf>흐림</wf>
<tmn>10</tmn>
<tmx>17</tmx>
<reliability/>
<rnSt>40</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-20 12:00</tmEf>
<wf>흐리고 비</wf>
<tmn>10</tmn>
<tmx>17</tmx>
<reliability/>
<rnSt>70</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-21 00:00</tmEf>
<wf>구름많음</wf>
<tmn>7</tmn>
<tmx>21</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-21 12:00</tmEf>
<wf>맑음</wf>
<tmn>7</tmn>
<tmx>21</tmx>
<reliability/>
<rnSt>10</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-22 00:00</tmEf>
<wf>맑음</wf>
<tmn>7</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>10</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-22 12:00</tmEf>
<wf>구름많음</wf>
<tmn>7</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-23 00:00</tmEf>
<wf>구름많음</wf>
<tmn>6</tmn>
<tmx>20</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-23 12:00</tmEf>
<wf>구름많음</wf>
<tmn>6</tmn>
<tmx>20</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-24 00:00</tmEf>
<wf>맑음</wf>
<tmn>7</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>20</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-24 12:00</tmEf>
<wf>맑음</wf>
<tmn>7</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>10</rnSt>
</data>
<data>
<mode>A01</mode>
<tmEf>2024-04-25 00:00</tmEf>
<wf>맑음</wf>
<tmn>8</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>10</rnSt>
</data>
<data>
<mode>A01</mode>
<tmEf>2024-04-26 00:00</tmEf>
<wf>맑음</wf>
<tmn>9</tmn>
<tmx>23</tmx>
<reliability/>
<rnSt>20</rnSt>
</data>
<data>
<mode>A01</mode>
<tmEf>2024-04-27 00:00</tmEf>
<wf>구름많음</wf>
<tmn>7</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
</location>
<location wl_ver="3">
<province>서울ㆍ인천ㆍ경기도</province>
<city>포천</city>
<data>
<mode>A02</mode>
<tmEf>2024-04-20 00:00</tmEf>
<wf>흐림</wf>
<tmn>11</tmn>
<tmx>18</tmx>
<reliability/>
<rnSt>40</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-20 12:00</tmEf>
<wf>흐리고 비</wf>
<tmn>11</tmn>
<tmx>18</tmx>
<reliability/>
<rnSt>70</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-21 00:00</tmEf>
<wf>구름많음</wf>
<tmn>10</tmn>
<tmx>23</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-21 12:00</tmEf>
<wf>맑음</wf>
<tmn>10</tmn>
<tmx>23</tmx>
<reliability/>
<rnSt>10</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-22 00:00</tmEf>
<wf>맑음</wf>
<tmn>8</tmn>
<tmx>23</tmx>
<reliability/>
<rnSt>10</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-22 12:00</tmEf>
<wf>구름많음</wf>
<tmn>8</tmn>
<tmx>23</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-23 00:00</tmEf>
<wf>구름많음</wf>
<tmn>7</tmn>
<tmx>21</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-23 12:00</tmEf>
<wf>구름많음</wf>
<tmn>7</tmn>
<tmx>21</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-24 00:00</tmEf>
<wf>맑음</wf>
<tmn>7</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>20</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-24 12:00</tmEf>
<wf>맑음</wf>
<tmn>7</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>10</rnSt>
</data>
<data>
<mode>A01</mode>
<tmEf>2024-04-25 00:00</tmEf>
<wf>맑음</wf>
<tmn>8</tmn>
<tmx>23</tmx>
<reliability/>
<rnSt>10</rnSt>
</data>
<data>
<mode>A01</mode>
<tmEf>2024-04-26 00:00</tmEf>
<wf>맑음</wf>
<tmn>9</tmn>
<tmx>23</tmx>
<reliability/>
<rnSt>20</rnSt>
</data>
<data>
<mode>A01</mode>
<tmEf>2024-04-27 00:00</tmEf>
<wf>구름많음</wf>
<tmn>7</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
</location>
<location wl_ver="3">
<province>서울ㆍ인천ㆍ경기도</province>
<city>가평</city>
<data>
<mode>A02</mode>
<tmEf>2024-04-20 00:00</tmEf>
<wf>흐림</wf>
<tmn>10</tmn>
<tmx>15</tmx>
<reliability/>
<rnSt>40</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-20 12:00</tmEf>
<wf>흐리고 비</wf>
<tmn>10</tmn>
<tmx>15</tmx>
<reliability/>
<rnSt>70</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-21 00:00</tmEf>
<wf>구름많음</wf>
<tmn>9</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-21 12:00</tmEf>
<wf>맑음</wf>
<tmn>9</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>10</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-22 00:00</tmEf>
<wf>맑음</wf>
<tmn>6</tmn>
<tmx>23</tmx>
<reliability/>
<rnSt>10</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-22 12:00</tmEf>
<wf>구름많음</wf>
<tmn>6</tmn>
<tmx>23</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-23 00:00</tmEf>
<wf>구름많음</wf>
<tmn>6</tmn>
<tmx>21</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-23 12:00</tmEf>
<wf>구름많음</wf>
<tmn>6</tmn>
<tmx>21</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-24 00:00</tmEf>
<wf>맑음</wf>
<tmn>6</tmn>
<tmx>21</tmx>
<reliability/>
<rnSt>20</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-24 12:00</tmEf>
<wf>맑음</wf>
<tmn>6</tmn>
<tmx>21</tmx>
<reliability/>
<rnSt>10</rnSt>
</data>
<data>
<mode>A01</mode>
<tmEf>2024-04-25 00:00</tmEf>
<wf>맑음</wf>
<tmn>7</tmn>
<tmx>23</tmx>
<reliability/>
<rnSt>10</rnSt>
</data>
<data>
<mode>A01</mode>
<tmEf>2024-04-26 00:00</tmEf>
<wf>맑음</wf>
<tmn>8</tmn>
<tmx>23</tmx>
<reliability/>
<rnSt>20</rnSt>
</data>
<data>
<mode>A01</mode>
<tmEf>2024-04-27 00:00</tmEf>
<wf>구름많음</wf>
<tmn>6</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
</location>
<location wl_ver="3">
<province>서울ㆍ인천ㆍ경기도</province>
<city>구리</city>
<data>
<mode>A02</mode>
<tmEf>2024-04-20 00:00</tmEf>
<wf>흐림</wf>
<tmn>13</tmn>
<tmx>18</tmx>
<reliability/>
<rnSt>40</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-20 12:00</tmEf>
<wf>흐리고 비</wf>
<tmn>13</tmn>
<tmx>18</tmx>
<reliability/>
<rnSt>70</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-21 00:00</tmEf>
<wf>구름많음</wf>
<tmn>12</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-21 12:00</tmEf>
<wf>맑음</wf>
<tmn>12</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>10</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-22 00:00</tmEf>
<wf>맑음</wf>
<tmn>10</tmn>
<tmx>24</tmx>
<reliability/>
<rnSt>10</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-22 12:00</tmEf>
<wf>구름많음</wf>
<tmn>10</tmn>
<tmx>24</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-23 00:00</tmEf>
<wf>구름많음</wf>
<tmn>10</tmn>
<tmx>23</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-23 12:00</tmEf>
<wf>구름많음</wf>
<tmn>10</tmn>
<tmx>23</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-24 00:00</tmEf>
<wf>맑음</wf>
<tmn>10</tmn>
<tmx>23</tmx>
<reliability/>
<rnSt>20</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-24 12:00</tmEf>
<wf>맑음</wf>
<tmn>10</tmn>
<tmx>23</tmx>
<reliability/>
<rnSt>10</rnSt>
</data>
<data>
<mode>A01</mode>
<tmEf>2024-04-25 00:00</tmEf>
<wf>맑음</wf>
<tmn>10</tmn>
<tmx>23</tmx>
<reliability/>
<rnSt>10</rnSt>
</data>
<data>
<mode>A01</mode>
<tmEf>2024-04-26 00:00</tmEf>
<wf>맑음</wf>
<tmn>10</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>20</rnSt>
</data>
<data>
<mode>A01</mode>
<tmEf>2024-04-27 00:00</tmEf>
<wf>구름많음</wf>
<tmn>10</tmn>
<tmx>21</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
</location>
<location wl_ver="3">
<province>서울ㆍ인천ㆍ경기도</province>
<city>남양주</city>
<data>
<mode>A02</mode>
<tmEf>2024-04-20 00:00</tmEf>
<wf>흐림</wf>
<tmn>12</tmn>
<tmx>18</tmx>
<reliability/>
<rnSt>40</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-20 12:00</tmEf>
<wf>흐리고 비</wf>
<tmn>12</tmn>
<tmx>18</tmx>
<reliability/>
<rnSt>70</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-21 00:00</tmEf>
<wf>구름많음</wf>
<tmn>11</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-21 12:00</tmEf>
<wf>맑음</wf>
<tmn>11</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>10</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-22 00:00</tmEf>
<wf>맑음</wf>
<tmn>9</tmn>
<tmx>24</tmx>
<reliability/>
<rnSt>10</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-22 12:00</tmEf>
<wf>구름많음</wf>
<tmn>9</tmn>
<tmx>24</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-23 00:00</tmEf>
<wf>구름많음</wf>
<tmn>8</tmn>
<tmx>23</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-23 12:00</tmEf>
<wf>구름많음</wf>
<tmn>8</tmn>
<tmx>23</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-24 00:00</tmEf>
<wf>맑음</wf>
<tmn>8</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>20</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-24 12:00</tmEf>
<wf>맑음</wf>
<tmn>8</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>10</rnSt>
</data>
<data>
<mode>A01</mode>
<tmEf>2024-04-25 00:00</tmEf>
<wf>맑음</wf>
<tmn>9</tmn>
<tmx>23</tmx>
<reliability/>
<rnSt>10</rnSt>
</data>
<data>
<mode>A01</mode>
<tmEf>2024-04-26 00:00</tmEf>
<wf>맑음</wf>
<tmn>10</tmn>
<tmx>23</tmx>
<reliability/>
<rnSt>20</rnSt>
</data>
<data>
<mode>A01</mode>
<tmEf>2024-04-27 00:00</tmEf>
<wf>구름많음</wf>
<tmn>8</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
</location>
<location wl_ver="3">
<province>서울ㆍ인천ㆍ경기도</province>
<city>양평</city>
<data>
<mode>A02</mode>
<tmEf>2024-04-20 00:00</tmEf>
<wf>흐림</wf>
<tmn>12</tmn>
<tmx>18</tmx>
<reliability/>
<rnSt>40</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-20 12:00</tmEf>
<wf>흐리고 비</wf>
<tmn>12</tmn>
<tmx>18</tmx>
<reliability/>
<rnSt>70</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-21 00:00</tmEf>
<wf>구름많음</wf>
<tmn>12</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-21 12:00</tmEf>
<wf>맑음</wf>
<tmn>12</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>10</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-22 00:00</tmEf>
<wf>맑음</wf>
<tmn>9</tmn>
<tmx>23</tmx>
<reliability/>
<rnSt>10</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-22 12:00</tmEf>
<wf>구름많음</wf>
<tmn>9</tmn>
<tmx>23</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-23 00:00</tmEf>
<wf>구름많음</wf>
<tmn>8</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-23 12:00</tmEf>
<wf>구름많음</wf>
<tmn>8</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-24 00:00</tmEf>
<wf>맑음</wf>
<tmn>9</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>20</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-24 12:00</tmEf>
<wf>맑음</wf>
<tmn>9</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>10</rnSt>
</data>
<data>
<mode>A01</mode>
<tmEf>2024-04-25 00:00</tmEf>
<wf>맑음</wf>
<tmn>10</tmn>
<tmx>23</tmx>
<reliability/>
<rnSt>10</rnSt>
</data>
<data>
<mode>A01</mode>
<tmEf>2024-04-26 00:00</tmEf>
<wf>맑음</wf>
<tmn>11</tmn>
<tmx>23</tmx>
<reliability/>
<rnSt>20</rnSt>
</data>
<data>
<mode>A01</mode>
<tmEf>2024-04-27 00:00</tmEf>
<wf>구름많음</wf>
<tmn>11</tmn>
<tmx>23</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
</location>
<location wl_ver="3">
<province>서울ㆍ인천ㆍ경기도</province>
<city>하남</city>
<data>
<mode>A02</mode>
<tmEf>2024-04-20 00:00</tmEf>
<wf>흐림</wf>
<tmn>13</tmn>
<tmx>18</tmx>
<reliability/>
<rnSt>40</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-20 12:00</tmEf>
<wf>흐리고 비</wf>
<tmn>13</tmn>
<tmx>18</tmx>
<reliability/>
<rnSt>70</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-21 00:00</tmEf>
<wf>구름많음</wf>
<tmn>13</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-21 12:00</tmEf>
<wf>맑음</wf>
<tmn>13</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>10</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-22 00:00</tmEf>
<wf>맑음</wf>
<tmn>10</tmn>
<tmx>23</tmx>
<reliability/>
<rnSt>10</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-22 12:00</tmEf>
<wf>구름많음</wf>
<tmn>10</tmn>
<tmx>23</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-23 00:00</tmEf>
<wf>구름많음</wf>
<tmn>9</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-23 12:00</tmEf>
<wf>구름많음</wf>
<tmn>9</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-24 00:00</tmEf>
<wf>맑음</wf>
<tmn>9</tmn>
<tmx>23</tmx>
<reliability/>
<rnSt>20</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-24 12:00</tmEf>
<wf>맑음</wf>
<tmn>9</tmn>
<tmx>23</tmx>
<reliability/>
<rnSt>10</rnSt>
</data>
<data>
<mode>A01</mode>
<tmEf>2024-04-25 00:00</tmEf>
<wf>맑음</wf>
<tmn>10</tmn>
<tmx>23</tmx>
<reliability/>
<rnSt>10</rnSt>
</data>
<data>
<mode>A01</mode>
<tmEf>2024-04-26 00:00</tmEf>
<wf>맑음</wf>
<tmn>11</tmn>
<tmx>24</tmx>
<reliability/>
<rnSt>20</rnSt>
</data>
<data>
<mode>A01</mode>
<tmEf>2024-04-27 00:00</tmEf>
<wf>구름많음</wf>
<tmn>9</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
</location>
<location wl_ver="3">
<province>서울ㆍ인천ㆍ경기도</province>
<city>안양</city>
<data>
<mode>A02</mode>
<tmEf>2024-04-20 00:00</tmEf>
<wf>흐림</wf>
<tmn>15</tmn>
<tmx>16</tmx>
<reliability/>
<rnSt>40</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-20 12:00</tmEf>
<wf>흐리고 비</wf>
<tmn>15</tmn>
<tmx>16</tmx>
<reliability/>
<rnSt>70</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-21 00:00</tmEf>
<wf>구름많음</wf>
<tmn>13</tmn>
<tmx>21</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-21 12:00</tmEf>
<wf>맑음</wf>
<tmn>13</tmn>
<tmx>21</tmx>
<reliability/>
<rnSt>10</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-22 00:00</tmEf>
<wf>맑음</wf>
<tmn>11</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>10</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-22 12:00</tmEf>
<wf>구름많음</wf>
<tmn>11</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-23 00:00</tmEf>
<wf>구름많음</wf>
<tmn>11</tmn>
<tmx>21</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-23 12:00</tmEf>
<wf>구름많음</wf>
<tmn>11</tmn>
<tmx>21</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-24 00:00</tmEf>
<wf>맑음</wf>
<tmn>11</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>20</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-24 12:00</tmEf>
<wf>맑음</wf>
<tmn>11</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>10</rnSt>
</data>
<data>
<mode>A01</mode>
<tmEf>2024-04-25 00:00</tmEf>
<wf>맑음</wf>
<tmn>12</tmn>
<tmx>21</tmx>
<reliability/>
<rnSt>10</rnSt>
</data>
<data>
<mode>A01</mode>
<tmEf>2024-04-26 00:00</tmEf>
<wf>맑음</wf>
<tmn>12</tmn>
<tmx>23</tmx>
<reliability/>
<rnSt>20</rnSt>
</data>
<data>
<mode>A01</mode>
<tmEf>2024-04-27 00:00</tmEf>
<wf>구름많음</wf>
<tmn>9</tmn>
<tmx>23</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
</location>
<location wl_ver="3">
<province>서울ㆍ인천ㆍ경기도</province>
<city>오산</city>
<data>
<mode>A02</mode>
<tmEf>2024-04-20 00:00</tmEf>
<wf>흐림</wf>
<tmn>11</tmn>
<tmx>17</tmx>
<reliability/>
<rnSt>40</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-20 12:00</tmEf>
<wf>흐리고 비</wf>
<tmn>11</tmn>
<tmx>17</tmx>
<reliability/>
<rnSt>70</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-21 00:00</tmEf>
<wf>구름많음</wf>
<tmn>10</tmn>
<tmx>21</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-21 12:00</tmEf>
<wf>맑음</wf>
<tmn>10</tmn>
<tmx>21</tmx>
<reliability/>
<rnSt>10</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-22 00:00</tmEf>
<wf>맑음</wf>
<tmn>9</tmn>
<tmx>23</tmx>
<reliability/>
<rnSt>10</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-22 12:00</tmEf>
<wf>구름많음</wf>
<tmn>9</tmn>
<tmx>23</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-23 00:00</tmEf>
<wf>구름많음</wf>
<tmn>8</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-23 12:00</tmEf>
<wf>구름많음</wf>
<tmn>8</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-24 00:00</tmEf>
<wf>맑음</wf>
<tmn>8</tmn>
<tmx>21</tmx>
<reliability/>
<rnSt>20</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-24 12:00</tmEf>
<wf>맑음</wf>
<tmn>8</tmn>
<tmx>21</tmx>
<reliability/>
<rnSt>10</rnSt>
</data>
<data>
<mode>A01</mode>
<tmEf>2024-04-25 00:00</tmEf>
<wf>맑음</wf>
<tmn>9</tmn>
<tmx>23</tmx>
<reliability/>
<rnSt>10</rnSt>
</data>
<data>
<mode>A01</mode>
<tmEf>2024-04-26 00:00</tmEf>
<wf>맑음</wf>
<tmn>10</tmn>
<tmx>24</tmx>
<reliability/>
<rnSt>20</rnSt>
</data>
<data>
<mode>A01</mode>
<tmEf>2024-04-27 00:00</tmEf>
<wf>구름많음</wf>
<tmn>8</tmn>
<tmx>24</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
</location>
<location wl_ver="3">
<province>서울ㆍ인천ㆍ경기도</province>
<city>화성</city>
<data>
<mode>A02</mode>
<tmEf>2024-04-20 00:00</tmEf>
<wf>흐림</wf>
<tmn>12</tmn>
<tmx>17</tmx>
<reliability/>
<rnSt>40</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-20 12:00</tmEf>
<wf>흐리고 비</wf>
<tmn>12</tmn>
<tmx>17</tmx>
<reliability/>
<rnSt>70</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-21 00:00</tmEf>
<wf>구름많음</wf>
<tmn>12</tmn>
<tmx>21</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-21 12:00</tmEf>
<wf>맑음</wf>
<tmn>12</tmn>
<tmx>21</tmx>
<reliability/>
<rnSt>10</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-22 00:00</tmEf>
<wf>맑음</wf>
<tmn>10</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>10</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-22 12:00</tmEf>
<wf>구름많음</wf>
<tmn>10</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-23 00:00</tmEf>
<wf>구름많음</wf>
<tmn>10</tmn>
<tmx>21</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-23 12:00</tmEf>
<wf>구름많음</wf>
<tmn>10</tmn>
<tmx>21</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-24 00:00</tmEf>
<wf>맑음</wf>
<tmn>9</tmn>
<tmx>21</tmx>
<reliability/>
<rnSt>20</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-24 12:00</tmEf>
<wf>맑음</wf>
<tmn>9</tmn>
<tmx>21</tmx>
<reliability/>
<rnSt>10</rnSt>
</data>
<data>
<mode>A01</mode>
<tmEf>2024-04-25 00:00</tmEf>
<wf>맑음</wf>
<tmn>9</tmn>
<tmx>20</tmx>
<reliability/>
<rnSt>10</rnSt>
</data>
<data>
<mode>A01</mode>
<tmEf>2024-04-26 00:00</tmEf>
<wf>맑음</wf>
<tmn>9</tmn>
<tmx>21</tmx>
<reliability/>
<rnSt>20</rnSt>
</data>
<data>
<mode>A01</mode>
<tmEf>2024-04-27 00:00</tmEf>
<wf>구름많음</wf>
<tmn>9</tmn>
<tmx>20</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
</location>
<location wl_ver="3">
<province>서울ㆍ인천ㆍ경기도</province>
<city>성남</city>
<data>
<mode>A02</mode>
<tmEf>2024-04-20 00:00</tmEf>
<wf>흐림</wf>
<tmn>13</tmn>
<tmx>17</tmx>
<reliability/>
<rnSt>40</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-20 12:00</tmEf>
<wf>흐리고 비</wf>
<tmn>13</tmn>
<tmx>17</tmx>
<reliability/>
<rnSt>70</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-21 00:00</tmEf>
<wf>구름많음</wf>
<tmn>12</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-21 12:00</tmEf>
<wf>맑음</wf>
<tmn>12</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>10</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-22 00:00</tmEf>
<wf>맑음</wf>
<tmn>10</tmn>
<tmx>23</tmx>
<reliability/>
<rnSt>10</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-22 12:00</tmEf>
<wf>구름많음</wf>
<tmn>10</tmn>
<tmx>23</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-23 00:00</tmEf>
<wf>구름많음</wf>
<tmn>9</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-23 12:00</tmEf>
<wf>구름많음</wf>
<tmn>9</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-24 00:00</tmEf>
<wf>맑음</wf>
<tmn>9</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>20</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-24 12:00</tmEf>
<wf>맑음</wf>
<tmn>9</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>10</rnSt>
</data>
<data>
<mode>A01</mode>
<tmEf>2024-04-25 00:00</tmEf>
<wf>맑음</wf>
<tmn>10</tmn>
<tmx>23</tmx>
<reliability/>
<rnSt>10</rnSt>
</data>
<data>
<mode>A01</mode>
<tmEf>2024-04-26 00:00</tmEf>
<wf>맑음</wf>
<tmn>11</tmn>
<tmx>23</tmx>
<reliability/>
<rnSt>20</rnSt>
</data>
<data>
<mode>A01</mode>
<tmEf>2024-04-27 00:00</tmEf>
<wf>구름많음</wf>
<tmn>10</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
</location>
<location wl_ver="3">
<province>서울ㆍ인천ㆍ경기도</province>
<city>의왕</city>
<data>
<mode>A02</mode>
<tmEf>2024-04-20 00:00</tmEf>
<wf>흐림</wf>
<tmn>12</tmn>
<tmx>17</tmx>
<reliability/>
<rnSt>40</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-20 12:00</tmEf>
<wf>흐리고 비</wf>
<tmn>12</tmn>
<tmx>17</tmx>
<reliability/>
<rnSt>70</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-21 00:00</tmEf>
<wf>구름많음</wf>
<tmn>11</tmn>
<tmx>21</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-21 12:00</tmEf>
<wf>맑음</wf>
<tmn>11</tmn>
<tmx>21</tmx>
<reliability/>
<rnSt>10</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-22 00:00</tmEf>
<wf>맑음</wf>
<tmn>9</tmn>
<tmx>23</tmx>
<reliability/>
<rnSt>10</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-22 12:00</tmEf>
<wf>구름많음</wf>
<tmn>9</tmn>
<tmx>23</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-23 00:00</tmEf>
<wf>구름많음</wf>
<tmn>9</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-23 12:00</tmEf>
<wf>구름많음</wf>
<tmn>9</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-24 00:00</tmEf>
<wf>맑음</wf>
<tmn>7</tmn>
<tmx>21</tmx>
<reliability/>
<rnSt>20</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-24 12:00</tmEf>
<wf>맑음</wf>
<tmn>7</tmn>
<tmx>21</tmx>
<reliability/>
<rnSt>10</rnSt>
</data>
<data>
<mode>A01</mode>
<tmEf>2024-04-25 00:00</tmEf>
<wf>맑음</wf>
<tmn>9</tmn>
<tmx>21</tmx>
<reliability/>
<rnSt>10</rnSt>
</data>
<data>
<mode>A01</mode>
<tmEf>2024-04-26 00:00</tmEf>
<wf>맑음</wf>
<tmn>10</tmn>
<tmx>23</tmx>
<reliability/>
<rnSt>20</rnSt>
</data>
<data>
<mode>A01</mode>
<tmEf>2024-04-27 00:00</tmEf>
<wf>구름많음</wf>
<tmn>8</tmn>
<tmx>24</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
</location>
<location wl_ver="3">
<province>서울ㆍ인천ㆍ경기도</province>
<city>군포</city>
<data>
<mode>A02</mode>
<tmEf>2024-04-20 00:00</tmEf>
<wf>흐림</wf>
<tmn>14</tmn>
<tmx>17</tmx>
<reliability/>
<rnSt>40</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-20 12:00</tmEf>
<wf>흐리고 비</wf>
<tmn>14</tmn>
<tmx>17</tmx>
<reliability/>
<rnSt>70</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-21 00:00</tmEf>
<wf>구름많음</wf>
<tmn>13</tmn>
<tmx>21</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-21 12:00</tmEf>
<wf>맑음</wf>
<tmn>13</tmn>
<tmx>21</tmx>
<reliability/>
<rnSt>10</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-22 00:00</tmEf>
<wf>맑음</wf>
<tmn>11</tmn>
<tmx>23</tmx>
<reliability/>
<rnSt>10</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-22 12:00</tmEf>
<wf>구름많음</wf>
<tmn>11</tmn>
<tmx>23</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-23 00:00</tmEf>
<wf>구름많음</wf>
<tmn>11</tmn>
<tmx>21</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-23 12:00</tmEf>
<wf>구름많음</wf>
<tmn>11</tmn>
<tmx>21</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-24 00:00</tmEf>
<wf>맑음</wf>
<tmn>10</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>20</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-24 12:00</tmEf>
<wf>맑음</wf>
<tmn>10</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>10</rnSt>
</data>
<data>
<mode>A01</mode>
<tmEf>2024-04-25 00:00</tmEf>
<wf>맑음</wf>
<tmn>12</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>10</rnSt>
</data>
<data>
<mode>A01</mode>
<tmEf>2024-04-26 00:00</tmEf>
<wf>맑음</wf>
<tmn>12</tmn>
<tmx>23</tmx>
<reliability/>
<rnSt>20</rnSt>
</data>
<data>
<mode>A01</mode>
<tmEf>2024-04-27 00:00</tmEf>
<wf>구름많음</wf>
<tmn>9</tmn>
<tmx>23</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
</location>
<location wl_ver="3">
<province>서울ㆍ인천ㆍ경기도</province>
<city>안성</city>
<data>
<mode>A02</mode>
<tmEf>2024-04-20 00:00</tmEf>
<wf>흐림</wf>
<tmn>12</tmn>
<tmx>18</tmx>
<reliability/>
<rnSt>40</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-20 12:00</tmEf>
<wf>흐리고 비</wf>
<tmn>12</tmn>
<tmx>18</tmx>
<reliability/>
<rnSt>70</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-21 00:00</tmEf>
<wf>구름많음</wf>
<tmn>12</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-21 12:00</tmEf>
<wf>맑음</wf>
<tmn>12</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>10</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-22 00:00</tmEf>
<wf>맑음</wf>
<tmn>10</tmn>
<tmx>23</tmx>
<reliability/>
<rnSt>10</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-22 12:00</tmEf>
<wf>구름많음</wf>
<tmn>10</tmn>
<tmx>23</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-23 00:00</tmEf>
<wf>구름많음</wf>
<tmn>9</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-23 12:00</tmEf>
<wf>구름많음</wf>
<tmn>9</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-24 00:00</tmEf>
<wf>맑음</wf>
<tmn>9</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>20</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-24 12:00</tmEf>
<wf>맑음</wf>
<tmn>9</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>10</rnSt>
</data>
<data>
<mode>A01</mode>
<tmEf>2024-04-25 00:00</tmEf>
<wf>맑음</wf>
<tmn>9</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>10</rnSt>
</data>
<data>
<mode>A01</mode>
<tmEf>2024-04-26 00:00</tmEf>
<wf>맑음</wf>
<tmn>10</tmn>
<tmx>23</tmx>
<reliability/>
<rnSt>20</rnSt>
</data>
<data>
<mode>A01</mode>
<tmEf>2024-04-27 00:00</tmEf>
<wf>구름많음</wf>
<tmn>9</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
</location>
<location wl_ver="3">
<province>서울ㆍ인천ㆍ경기도</province>
<city>용인</city>
<data>
<mode>A02</mode>
<tmEf>2024-04-20 00:00</tmEf>
<wf>흐림</wf>
<tmn>11</tmn>
<tmx>17</tmx>
<reliability/>
<rnSt>40</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-20 12:00</tmEf>
<wf>흐리고 비</wf>
<tmn>11</tmn>
<tmx>17</tmx>
<reliability/>
<rnSt>70</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-21 00:00</tmEf>
<wf>구름많음</wf>
<tmn>11</tmn>
<tmx>21</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-21 12:00</tmEf>
<wf>맑음</wf>
<tmn>11</tmn>
<tmx>21</tmx>
<reliability/>
<rnSt>10</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-22 00:00</tmEf>
<wf>맑음</wf>
<tmn>9</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>10</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-22 12:00</tmEf>
<wf>구름많음</wf>
<tmn>9</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-23 00:00</tmEf>
<wf>구름많음</wf>
<tmn>8</tmn>
<tmx>20</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-23 12:00</tmEf>
<wf>구름많음</wf>
<tmn>8</tmn>
<tmx>20</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-24 00:00</tmEf>
<wf>맑음</wf>
<tmn>8</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>20</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-24 12:00</tmEf>
<wf>맑음</wf>
<tmn>8</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>10</rnSt>
</data>
<data>
<mode>A01</mode>
<tmEf>2024-04-25 00:00</tmEf>
<wf>맑음</wf>
<tmn>9</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>10</rnSt>
</data>
<data>
<mode>A01</mode>
<tmEf>2024-04-26 00:00</tmEf>
<wf>맑음</wf>
<tmn>9</tmn>
<tmx>23</tmx>
<reliability/>
<rnSt>20</rnSt>
</data>
<data>
<mode>A01</mode>
<tmEf>2024-04-27 00:00</tmEf>
<wf>구름많음</wf>
<tmn>8</tmn>
<tmx>21</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
</location>
<location wl_ver="3">
<province>서울ㆍ인천ㆍ경기도</province>
<city>광주</city>
<data>
<mode>A02</mode>
<tmEf>2024-04-20 00:00</tmEf>
<wf>흐림</wf>
<tmn>12</tmn>
<tmx>17</tmx>
<reliability/>
<rnSt>40</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-20 12:00</tmEf>
<wf>흐리고 비</wf>
<tmn>12</tmn>
<tmx>17</tmx>
<reliability/>
<rnSt>70</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-21 00:00</tmEf>
<wf>구름많음</wf>
<tmn>12</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-21 12:00</tmEf>
<wf>맑음</wf>
<tmn>12</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>10</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-22 00:00</tmEf>
<wf>맑음</wf>
<tmn>9</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>10</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-22 12:00</tmEf>
<wf>구름많음</wf>
<tmn>9</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-23 00:00</tmEf>
<wf>구름많음</wf>
<tmn>8</tmn>
<tmx>21</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-23 12:00</tmEf>
<wf>구름많음</wf>
<tmn>8</tmn>
<tmx>21</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-24 00:00</tmEf>
<wf>맑음</wf>
<tmn>8</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>20</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-24 12:00</tmEf>
<wf>맑음</wf>
<tmn>8</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>10</rnSt>
</data>
<data>
<mode>A01</mode>
<tmEf>2024-04-25 00:00</tmEf>
<wf>맑음</wf>
<tmn>9</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>10</rnSt>
</data>
<data>
<mode>A01</mode>
<tmEf>2024-04-26 00:00</tmEf>
<wf>맑음</wf>
<tmn>10</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>20</rnSt>
</data>
<data>
<mode>A01</mode>
<tmEf>2024-04-27 00:00</tmEf>
<wf>구름많음</wf>
<tmn>8</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
</location>
<location wl_ver="3">
<province>서울ㆍ인천ㆍ경기도</province>
<city>여주</city>
<data>
<mode>A02</mode>
<tmEf>2024-04-20 00:00</tmEf>
<wf>흐림</wf>
<tmn>12</tmn>
<tmx>18</tmx>
<reliability/>
<rnSt>40</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-20 12:00</tmEf>
<wf>흐리고 비</wf>
<tmn>12</tmn>
<tmx>18</tmx>
<reliability/>
<rnSt>70</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-21 00:00</tmEf>
<wf>구름많음</wf>
<tmn>12</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-21 12:00</tmEf>
<wf>맑음</wf>
<tmn>12</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>10</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-22 00:00</tmEf>
<wf>맑음</wf>
<tmn>8</tmn>
<tmx>23</tmx>
<reliability/>
<rnSt>10</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-22 12:00</tmEf>
<wf>구름많음</wf>
<tmn>8</tmn>
<tmx>23</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-23 00:00</tmEf>
<wf>구름많음</wf>
<tmn>8</tmn>
<tmx>21</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-23 12:00</tmEf>
<wf>구름많음</wf>
<tmn>8</tmn>
<tmx>21</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-24 00:00</tmEf>
<wf>맑음</wf>
<tmn>8</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>20</rnSt>
</data>
<data>
<mode>A02</mode>
<tmEf>2024-04-24 12:00</tmEf>
<wf>맑음</wf>
<tmn>8</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>10</rnSt>
</data>
<data>
<mode>A01</mode>
<tmEf>2024-04-25 00:00</tmEf>
<wf>맑음</wf>
<tmn>9</tmn>
<tmx>23</tmx>
<reliability/>
<rnSt>10</rnSt>
</data>
<data>
<mode>A01</mode>
<tmEf>2024-04-26 00:00</tmEf>
<wf>맑음</wf>
<tmn>10</tmn>
<tmx>22</tmx>
<reliability/>
<rnSt>20</rnSt>
</data>
<data>
<mode>A01</mode>
<tmEf>2024-04-27 00:00</tmEf>
<wf>구름많음</wf>
<tmn>8</tmn>
<tmx>21</tmx>
<reliability/>
<rnSt>30</rnSt>
</data>
</location>
</body>
</description>
</item>
</channel>
</rss>
```

# Tutorial 1

`Extract` infomation from a forecast-weather center

## 파이썬 파일 생성 및 편집기 실행

```shell
파일 생성 및 편집기 열기

vim 1_weather.py
```

## 데이터 가져올 파이썬 코드 작성

```python
#!/usr/bin/env python3
import sys
import urllib.request as req
import urllib.parse as parse

if len(sys.argv) <= 1:
        print("usage: download-forecast-argv < region number: ")
        sys.exit()

# region number 저장
regionNumber = sys.argv[1]

# Root URL 주소
api_address = "https://www.kma.go.kr/weather/forecast/mid-term-rss3.jsp"

# dict 타입으로 stnId 저장
values = {
        'stnId': regionNumber
}

params = parse.urlencode(values)

url = api_address + "?" + params

print("URL= ", url)

data = req.urlopen(url).read()

text = data.decode("utf-8")

print(text)
```

## 실행

```shell
(venv)  {seilylook} 🍻 ~/Development/DataEngineering/2024_BIGDATA  python3 1_weather.py 109 | more
```

# Tutorial 2

## package install

```shell
(venv)  {seilylook} 🚀 ~/Development/DataEngineering/2024_BIGDATA pip3 install requests

(venv)  {seilylook} 🚀 ~/Development/DataEngineering/2024_BIGDATA pip3 install beautifulsoup4
```

## 데이터 가져와서 정제하는 파이썬 코드

```python
#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup

def main():
    url = "https://www.kma.go.kr/weather/forecast/mid-term-rss3.jsp"
    response = requests.get(url)

    soup = BeautifulSoup(response.text)
    locations = soup.find_all('location')

    for location in locations:
        city = location.find('city').text
        date = location.find('data').find('tmef').text
        weather = location.find('data').find('wf').text

        print(f'City: {city} | Date: {date} | Weather: {weather}')

if __name__ == "__main__":
    main()
```

## 실행 및 결과 확인

```shell
(venv)  {seilylook} 🚀 python3 2_weather.py | more

City: 서울 | Date: 2024-04-20 00:00 | Weather: 흐림
City: 인천 | Date: 2024-04-20 00:00 | Weather: 흐림
City: 수원 | Date: 2024-04-20 00:00 | Weather: 흐림
City: 파주 | Date: 2024-04-20 00:00 | Weather: 흐림
City: 이천 | Date: 2024-04-20 00:00 | Weather: 흐림
City: 평택 | Date: 2024-04-20 00:00 | Weather: 흐림
City: 춘천 | Date: 2024-04-20 00:00 | Weather: 흐림
City: 원주 | Date: 2024-04-20 00:00 | Weather: 흐림
City: 강릉 | Date: 2024-04-20 00:00 | Weather: 흐림
City: 대전 | Date: 2024-04-20 00:00 | Weather: 흐림
City: 세종 | Date: 2024-04-20 00:00 | Weather: 흐림
City: 홍성 | Date: 2024-04-20 00:00 | Weather: 흐림
City: 청주 | Date: 2024-04-20 00:00 | Weather: 흐림
City: 충주 | Date: 2024-04-20 00:00 | Weather: 흐림
City: 영동 | Date: 2024-04-20 00:00 | Weather: 흐림
City: 광주 | Date: 2024-04-20 00:00 | Weather: 흐리고 비
City: 목포 | Date: 2024-04-20 00:00 | Weather: 흐리고 비
City: 여수 | Date: 2024-04-20 00:00 | Weather: 흐리고 비
City: 순천 | Date: 2024-04-20 00:00 | Weather: 흐리고 비
City: 광양 | Date: 2024-04-20 00:00 | Weather: 흐리고 비
City: 나주 | Date: 2024-04-20 00:00 | Weather: 흐리고 비
City: 전주 | Date: 2024-04-20 00:00 | Weather: 흐리고 비
City: 군산 | Date: 2024-04-20 00:00 | Weather: 흐리고 비
City: 정읍 | Date: 2024-04-20 00:00 | Weather: 흐리고 비
City: 남원 | Date: 2024-04-20 00:00 | Weather: 흐리고 비
City: 고창 | Date: 2024-04-20 00:00 | Weather: 흐리고 비
City: 무주 | Date: 2024-04-20 00:00 | Weather: 흐리고 비
City: 부산 | Date: 2024-04-20 00:00 | Weather: 흐림
City: 울산 | Date: 2024-04-20 00:00 | Weather: 흐림
City: 창원 | Date: 2024-04-20 00:00 | Weather: 흐림
City: 진주 | Date: 2024-04-20 00:00 | Weather: 흐림
City: 거창 | Date: 2024-04-20 00:00 | Weather: 흐림
City: 통영 | Date: 2024-04-20 00:00 | Weather: 흐림
City: 대구 | Date: 2024-04-20 00:00 | Weather: 흐림
City: 안동 | Date: 2024-04-20 00:00 | Weather: 흐림
City: 포항 | Date: 2024-04-20 00:00 | Weather: 흐림
City: 경주 | Date: 2024-04-20 00:00 | Weather: 흐림
City: 울진 | Date: 2024-04-20 00:00 | Weather: 흐림
City: 울릉도 | Date: 2024-04-20 00:00 | Weather: 흐림
City: 제주 | Date: 2024-04-20 00:00 | Weather: 흐리고 비
City: 서귀포 | Date: 2024-04-20 00:00 | Weather: 흐리고 비
```

# Tutorial 3

네이버 증권 데이터 `Extract` 해오기

