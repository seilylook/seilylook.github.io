# S3


# Introduction

데이터 스토리지는 대량의 데이터를 저장, 관리, 그리고 검색하도록 설계된 스토리지 인프라다.

어플리케이션 및 서비스가 작동하는 방식으로 빅데이터를 대량의 데이터를 쉽게 액세스하고 사용할 수 있고 처리할 수 있도록 저장 및 정렬을 할 수 있다. 또한 필요에 따라서 크기를 유연하게 확장시킬 수 있다.

# What is S3?

Amazon Simple Storage Service(Amazon S3)는 업계 최고의 확장성, 데이터 가용성, 보안 및 성능을 제공하는 객체 스토리지 서비스입니다. 모든 규모와 업종의 고객은 Amazon S3를 사용하여 데이터 레이크, 웹 사이트, 모바일 애플리케이션, 백업 및 복원, 아카이브, 엔터프라이즈 애플리케이션, IoT 디바이스, 빅 데이터 분석 등 다양한 사용 사례에서 원하는 양의 데이터를 저장하고 보호할 수 있습니다. Amazon S3는 특정 비즈니스, 조직 및 규정 준수 요구 사항에 맞게 데이터에 대한 액세스를 최적화, 구조화 및 구성할 수 있는 관리 기능을 제공합니다.

# Bucket?

## Versioning

Means of keeping multiple variants of an object in the same bucket. For example, you can have `two objects with the same key`, but `different version IDs`, such as photo.gif(version 11111) and photo.gif(version 121212)

## Server Access Logging

To track requests for access to your bucket, you can enable access logging. `Each access log record` provides details about a single access request, such as `a requester, bucket name, request action, response status, and error code`.

# 버킷 생성

<img src="/images/s3/s3-1.png"/>

# 파일(객체) 업로드

<img src="/images/s3-2.png"/>

```xml
This XML file does not appear to have any style information associated with it. The document tree is shown below.
<Error>
    <Code>AccessDenied</Code>
    <Message>Access Denied</Message>
    <RequestId>TNXA9QVCN72YQK6J</RequestId>
    <HostId>
        4B4Xg8AX0J4PzI3HFImdeusNL4fvOiSFfRp/DN3lTo1p0KNoHiscDbHC7xU0im0xuZlO9tVrFgk=
    </HostId>
</Error>
```

위의 access denied를 해결하기 위해서는 다음 동작을 취해주어야 한다.

# Public Bucket

publicly accessible s3 bucket

- Customize ACL(Access Control List)

- Add Bucket Policy

{{<admonition info>}}
Access Control List

접근 제어 목록 또는 액세스 제어 목록은 객체나 개체 속성에 적용되어 있는 허가 목록.

(이 목록은 누가 또는 무엇인 객체 접근 허가를 받는지, 어떤 작업이 객체에 수행되도록 허가를 받을지를 지정한다.)
{{</admonition>}}

<img src="/images/s3/s3-4.png"/>

<img src="/images/s3/s3-3.png"/>

# Bucket Policy

[Bucket Policy Generator](https://awspolicygen.s3.amazonaws.com/policygen.html)

<img src="/images/s3/s3-5.png"/>

<img src="/images/s3/s3-6.png"/>

<img src="/images/s3/s3-7.png"/>

<img src="/images/s3/s3-8.png"/>

<img src="/images/s3/s3-9.png"/>

<img src="/images/s3/s3-10.png"/>

<img src="/images/s3/s3-11.png"/>

<img src="/images/s3/s3-12.png"/>

<img src="/images/s3/s3-13.png"/>

<img src="/images/s3/s3-14.png"/>

# Lifecycle Bucket

<img src="/images/s3/s3-15.png"/>

<img src="/images/s3/s3-16.png"/>

<img src="/images/s3/s3-17.png"/>

# 실습

## aws credential 설정

```bash
vim ~/.aws/config

[default]
region = ap-northest-2

vim ~/.aws/credentials

[default]
aws_access_key_id = <KEY ID OF DEFAULT ACCOUNT>
aws_secret_access_key = <SECRET ACCESS KEY OF DEFAULT ACCOUNT>
```

## boto3

```bash
pip3 install boto3
```

```python
import boto3

session = boto3.Session(profile_name='default')

s3 = session.resource('s3')

for bucket in s3.buckets.all():
    print(bucket.name)
```

```bash
(venv)  {seilylook} 🦄 python3 s3_list.py

2024-big-data-course-seilylook
```

## Object Download

```python
import os
import boto3
import time

bucket = "2024-big-data-course-seilylook"
folder_name = "2024/"
path = "test.jpg"
obj = "test.jpg"

session = boto3.Session(profile_name="default")
s3 = session.client('s3')

print(folder_name + os.path.basename(path))

s3.download_file(bucket, folder_name+os.path.basename(path), "./"+os.path.basename(path))
```

```bash
(venv)  {seilylook} 🦄 python3 s3_download.py
2024/test.jpg

(venv)  {seilylook} 🦄 ll

total 88
-rw-r--r--@ 1 seilylook  staff   347B  4 26 14:45 s3_download.py
-rw-r--r--@ 1 seilylook  staff   144B  4 26 14:21 s3_list.py
-rw-r--r--@ 1 seilylook  staff    33K  4 26 14:46 test.jpg
drwxr-xr-x@ 6 seilylook  staff   192B  4 26 14:15 venv
```

## Object Upload

```python
import os
import boto3
import time

bucket = "2024-big-data-course-seilylook"
obj = "test.jpg"
local_file_path = os.getcwd() + "/" + obj
target_file_name = "new_test_image.jpg"

session = boto3.Session(profile_name="default")
s3 = session.client('s3')

s3.upload_file(local_file_path, bucket, target_file_name)
```

## Object ACL Public

```python
import os
import boto3
import time

bucket = "2024-big-data-course-seilylook"
obj = "test.jpg"
local_file_path = os.getcwd() + "/" + obj
target_file_name = "new_test_image.jpg"

session = boto3.Session(profile_name="default")
s3 = session.client('s3')

s3.put_object_acl(ACL="public-read", Bucket=bucket, Key=target_file_name)
```

# Lambda Service

AWS Lambda은(는) 서버를 프로비저닝하거나 관리하지 않고도 코드를 실행할 수 있게 해주는 컴퓨팅 서비스입니다.

Lambda는 고가용성 컴퓨팅 인프라에서 코드를 실행하고 서버와 운영 체제 유지 관리, 용량 프로비저닝 및 자동 조정, 코드 및 보안 패치 배포, 로깅 등 모든 컴퓨팅 리소스 관리를 수행합니다. Lambda를 사용하면 Lambda가 지원하는 언어 런타임 중 하나로 코드를 제공하기만 하면 됩니다.

Lambda 함수에 코드를 구성합니다. Lambda 서비스는 필요할 때만 함수를 실행하고 자동으로 확장됩니다. 사용한 컴퓨팅 시간만큼만 비용을 지불하고, 코드가 실행되지 않을 때는 요금이 부과되지 않습니다.

## Use case 1

AWS Lambda를 활용한 썸네일 생성하기

1. 큰 이미지 업로드

2. AWS s3 파일 업로드

3. AWS lambda 코드 실행

4. 압축 및 파일 크기 변경

5. AWS s3에 저장

<img src="/images/lambda1.png" />

