# First Contribution


## Description

`/docs/source/development/testing.rst` 파일을 읽으며 테스트를 시도하는 도중에 다음과 같은 문제가 발생했고, 이 문제를 수정하기로 생각했다.

```bash
24/12/16 20:44:42 WARN Utils: Service 'sparkDriver' could not bind on a random free port. 
You may check whether configuring an appropriate binding address.

24/12/16 20:44:42 ERROR SparkContext: Error initializing SparkContext.
```

에러에서 설명한 대로, PORT가 이미 사용중이라는 뜻으로 생각되어 PORT를 수정하니 에러가 해결되었다.

해결법에 대해서 `docs`에 수정해두었다.

```rst
.. note::

    If the Spark driver is unavailable, you can resolve the issue using the following methods:

    **Set SPARK_LOCAL_IP**:

    Configure the environment variable ``SPARK_LOCAL_IP`` to bind to the local address ``127.0.0.1``::

        export SPARK_LOCAL_IP=127.0.0.1

    Alternatively, run the Spark shell before executing tests.

    **If the issue occurs**:

    When Spark is installed but not yet initialized, you may encounter an error like this::

        24/12/16 20:44:42 WARN Utils: Service 'sparkDriver' could not bind on a random free port. 
        You may check whether configuring an appropriate binding address.
        24/12/16 20:44:42 ERROR SparkContext: Error initializing SparkContext.
```

마지막으로, PR 형식에 맞춰 PR을 보내고 마무리했다.

<img src="/images/contribution/spark/1/1.png">

<img src="/images/contribution/spark/1/2.png">
