# Airflow Executors


# Apache Airflow란 무엇인가?

## Apache Airflow란?

공식 홈페이지에서 Airflow는 워크 플로를 코드로 작성하고 스케줄링한 뒤 모니터링하는 플랫폼이라고 설명하고 있습니다. 모든 기술이 그렇듯 Airflow에도 당연히 수많은 장점과 단점이 존재합니다. 제가 생각하는 가장 큰 장점은 데이터 조직이라면 필수로 하게 되는 과거 데이터 재처리 작업을 편리하게 수행할 수 있는 점이라고 생각합니다. 이런 이유로 많은 데이터 조직에서 이미 Airflow를 도입해 사용하고 계실 거라고 생각합니다. Airflow는 Apache 인큐베이터 프로젝트로 선정된 지 3년 만에 탑 레벨 프로젝트(Top-Level Project, TLP)로 선정될 만큼 커뮤니티가 빠른 속도로 확장되고 있습니다. 

## Apache Airflow 기본 동작 원리

먼저 Airflow를 구성하는 각 컴포넌트의 역할을 간략하게 짚어본 뒤 실제 Airflow 태스크가 어떠한 형태로 동작하는지 HiveOperator를 예로 들어 간략하게 설명하겠습니다.

<img src="/images/data/airflow/1.png" />

- Scheduler: 가장 중추적 역할을 수행하며 모든 DAG(Directed Acyclic Graph)와 태스크를 모니터링하고 관리합니다. 그리고 주기적으로 실행해야 할 태스크를 찾고 해당 태스크를 실행 가능한 상태로 변경합니다.

- Webserver: Airflow 웹 UI 서버입니다.

- Kerberos: 인증 처리를 위한 티켓 갱신(ticket renewer) 프로세스입니다(선택 사항).

- DAG Script: 개발자가 작성한 Python 워크 플로 스크립트입니다.

- MetaDB: Airflow 메타데이터 저장소입니다. 어떤 DAG가 존재하고 어떤 태스크로 구성되었는지, 어떤 태스크가 실행 중이고, 또 실행 가능한 상태인지 등의 많은 정보가 기입됩니다.

- Executor: 태스크 인스턴스를 실행하는 주체이며 종류가 다양합니다.

- Worker: 실제 작업을 수행하는 주체이며 워커의 동작 방식은 Executor의 종류에 따라 상이합니다.

아래 그림 2는 HiveOperator 작동 방식의 예시입니다.

<img src="/images/data/airflow/2.png" />

개발자가 HiveOperator에 실행하고 싶은 쿼리를 입력하고 태스크를 작성하면 내부적으로 Hive CLI(Command Line Interface) 명령어를 생성합니다. 

아래 `_prepare_cli_cmd` 함수를 보면 개발자가 정의한 DB 호스트 정보, ID 및 패스워드 정보와 함께 쿼리를 이용해 CLI 명령어 문자열을 구성하는 것을 확인할 수 있습니다.

```python
class HiveCliHook(baseHook):
    def _prepare_cli_cmd(self):
            conn = self.conn
            hive_bin = 'hive'
            cmd_extra = []

            if self.use_beeline:
                hive_bin = 'beeline'
                jdbc_url = "jdbc:hive2://{host}:{port}/{schema}".format(
                    host=conn.host, port=conn.port, schema=conn.schema)
                if conf.get('core', 'security') == 'kerberos':
                    template = conn.extra_dejson.get(
                        'principal', "hive/_HOST@EXAMPLE.COM")
                    if "_HOST" in template:
                        template = utils.replace_hostname_pattern(
                            utils.get_components(template))

                    proxy_user = self._get_proxy_user()

                    jdbc_url += ";principal={template};{proxy_user}".format(
                        template=template, proxy_user=proxy_user)
                elif self.auth:
                    jdbc_url += ";auth=" + self.auth

                jdbc_url = '"{}"'.format(jdbc_url)

                cmd_extra += ['-u', jdbc_url]
                if conn.login:
                    cmd_extra += ['-n', conn.login]
                if conn.password:
                    cmd_extra += ['-p', conn.password]

            hive_params_list = self.hive_cli_params.split()

            return [hive_bin] + cmd_extra + hive_params_list
```

이후에 스케줄러는 Airflow 워커를 생성합니다(Airflow 워커는 Executor의 종류에 따라 동작 방식이 상이함). 

아래 코드는 LocalWorker 클래스에서 프로세스 형태로 워커가 실행되는 함수입니다. 파라미터로 전달받은 명령어는 airflow run으로 시작하는 명령어이며, Airflow 워커 실행 시 수행되는 명령어로 이해하시면 됩니다.

```python
class LocalWorker(multiprocessing.Process, LoggingMixin):
    def execute_work(self, key, command):
        if key is None:
            return
        self.log.info("%s running %s", self.__class__.__name__, command)
        try:
            subprocess.check_call(command, close_fds=True)
            state = State.SUCCESS
        except subprocess.CalledProcessError as e:
            state = State.FAILED
            self.log.error("Failed to execute task %s.", str(e))

        self.result_queue.put((key, state))
```

그리고 최종적으로는 HiveOperator를 통해 만들어진 Hive 명령어가 실행되고 Hive Java 프로세스가 수행되는 원리라고 이해하시면 됩니다.

## Executor의 종류 및 특징과 장단점

앞서 Airflow의 기본 동작 원리를 설명하면서 Airflow에 Executor라는 개념이 있다고 말씀드렸습니다. Executor는 문자 그대로 작업의 한 단위인 태스크 인스턴스를 실행하는 주체입니다. Executor에는 다양한 종류가 있고 각 종류에 따라 동작 원리가 상이합니다. 현재 Airflow에서는 Sequential Executor와 Debug Executor, Local Executor, Dask Executor, Celery Executor, Kubernetes Executor를 제공하고 있으며 Airflow 2.0에서는 CeleryKubernetes Executor가 추가되었습니다. 이 글에서는 글의 주제인 Kubernetes Executor와 비교하기 위해 보편적으로 많이 사용하는 Local Executor와 Celery Executor에 대해 먼저 알아보겠습니다.

### Local Executor

<img src="/images/data/airflow/3.png"/>

단일 장비에 웹 서버와 스케줄러를 같이 기동하고 태스크를 프로세스 형태로 스폰(spawn)해 실행하는 형태입니다. 앞서 Airflow 기본 동작 원리에서 설명한 그대로 Airflow 워커는 스케줄러가 서브 프로세스 형태로 실행하고 해당 워커에서 실제 수행해야 하는 태스크를 실행합니다. Local Executor는 그림 3과 같이 parallelism 설정값에 따라 두 가지 구조로 나뉩니다. 설정값이 0인 경우에는 이론적으로 들어오는 모든 요청에 대해서 무한대로 태스크를 실행합니다. 이때 워커의 구현체는 LocalWorker 클래스입니다. 이에 반해 parallelism 설정값이 0 이상일 경우에는 해당 설정값의 개수만큼 프로세스 수를 제한하여 태스크를 실행합니다. 이때 task_queue의 정보를 이용해 태스크 실행 수에 대한 스로틀링(throttling)을 합니다. Airflow 워커의 구현체는 QueuedLocalWorker 클래스입니다.

아래 코드는 Local Executor 클래스에서 parallelism 설정값이 0이냐 아니냐에 따라 다른 구현체를 생성하고 실행하는 코드입니다.

```python
class LocalExecutor(BaseExecutor)
    def start(self):
            self.manager = multiprocessing.Manager()
            self.result_queue = self.manager.Queue()
            self.workers = []
            self.workers_used = 0
            self.workers_active = 0
            self.impl = (LocalExecutor._UnlimitedParallelism(self) if self.parallelism == 0
                        else LocalExecutor._LimitedParallelism(self))

            self.impl.start()
```

아래 코드는 UnlimitedParallelism 클래스의 일부분입니다. `execute_async` 함수에서 LocalWorker 객체를 생성할 때 result_queue만을 가지고 객체를 생성하는 것을 확인할 수 있습니다.

```python
class _UnlimitedParallelism(object)
    def start(self):
        self.executor.workers_used = 0
        self.executor.workers_active = 0

    def execute_async(self, key, command):
        local_worker = LocalWorker(self.executor.result_queue)
        local_worker.key = key
        local_worker.command = command
        self.executor.workers_used += 1
        self.executor.workers_active += 1
        local_worker.start()
```

아래 코드는 LimitedParallelism 클래스의 일부분입니다. `start` 함수에서 QueuedLocalWorker 객체를 생성할 때 result_queue와 task_queue를 가지고 객체를 생성하는 것을 확인할 수 있습니다. parallelism 설정값만큼 워커를 생성하고, `execute_async` 함수에서 task_queue에 실행할 태스크 인스턴스를 넣고 실제 태스크를 수행합니다.

```python
class _LimitedParallelism(object)
    def start(self):
        self.queue = self.executor.manager.Queue()
        self.executor.workers = [
            QueuedLocalWorker(self.queue, self.executor.result_queue)
            for _ in range(self.executor.parallelism)
        ]

        self.executor.workers_used = len(self.executor.workers)

        for w in self.executor.workers:
            w.start()

    def execute_async(self, key, command):
        self.queue.put((key, command))
```

**장점**

LocalExecutor의 가장 큰 장점은 구성이 간단하다는 점입니다. 그렇기에 대부분의 조직에서 베타 혹은 테스트 환경에 많이 사용하고 있을 거라고 생각합니다. 간혹 환경을 빠르게 구성할 수 있다는 장점으로 실 서비스 환경에 적용하는 사례도 있습니다.

**단점**

단일 장비 환경에서 작동하기 때문에 SPOF(Single point of failure) 문제를 가지고 있으며 매번 프로세스 상태를 체크하며 모니터링해야 합니다. 따라서 실제 서비스 환경에는 적합하지 않습니다.

### Celery Executor

<img src="/images/data/airflow/4.jpg"/>

**특징**

워커를 스케일아웃할 수 있는 방법 중 하나입니다. Celery 백엔드로 메시지 브로커(broker)가 필요하며, 메시지 브로커로는 RabbitMQ나 Redis를 사용할 수 있습니다. 스케줄러는 실행해야 할 태스크를 메시지 브로커에 전달하고, 각 워커 장비의 Celery 워커가 태스크를 실행합니다. 이때 전달되는 태스크의 형태는 명령어 문자열입니다. 

아래 코드는 CeleryExecutor 클래스의 `trigger_task` 함수입니다. task_tuples_to_send 목록에는 실행해야 할 태스크 명령어가 추가되어 있습니다. 명령어의 형태는 airflow run으로 시작하는 문자열입니다. 태스크 명령어 정보에 대한 튜플(tuple) 리스트는 `send_task_to_executor` 함수를 통해 메시지 브로커로 전달됩니다.

```python
class CeleryExecutor(BaseExecutor):
    def trigger_tasks(self, open_slots):
        sorted_queue = sorted(
            [(k, v) for k, v in self.queued_tasks.items()],
            key=lambda x: x[1][1],
            reverse=True)

        task_tuples_to_send = []

        for i in range(min((open_slots, len(self.queued_tasks)))):
            key, (command, _, queue, simple_ti) = sorted_queue.pop(0)
            task_tuples_to_send.append((key, simple_ti, command, queue,
                                        execute_command))

        cached_celery_backend = None
        if task_tuples_to_send:
            tasks = [t[4] for t in task_tuples_to_send]
            cached_celery_backend = tasks[0].backend

        if task_tuples_to_send:
            chunksize = self._num_tasks_per_send_process(len(task_tuples_to_send))
            num_processes = min(len(task_tuples_to_send), self._sync_parallelism)

            send_pool = Pool(processes=num_processes)
            key_and_async_results = send_pool.map(
                send_task_to_executor,
                task_tuples_to_send,
                chunksize=chunksize)

            send_pool.close()
            send_pool.join()
            self.log.debug('Sent all tasks.')

            for key, command, result in key_and_async_results:
                if isinstance(result, ExceptionWithTraceback):
                    self.log.error(  # pylint: disable=logging-not-lazy
                        CELERY_SEND_ERR_MSG_HEADER + ":%s
    %s
    ", result.exception, result.traceback
                    )
                elif result is not None:
                    # Only pops when enqueued successfully, otherwise keep it
                    # and expect scheduler loop to deal with it.
                    self.queued_tasks.pop(key)
                    result.backend = cached_celery_backend
                    self.running[key] = command
                    self.tasks[key] = result
                    self.last_state[key] = celery_states.PENDING
```

아래 코드는 cli.py의 `worker` 함수입니다. 실제 Celery Executor를 사용할 때 관리자가 워커 장비에서 airflow worker 명령어를 수행하면 아래 Python 함수가 수행됩니다. 여기서 워커는 Airflow의 워커가 아니라 Celery project의 Celery 워커라고 이해하시면 됩니다. 

따라서 실제 워커 장비에서 기동되는 프로세스는 Celery 워커 프로세스입니다. 메시지 브로커로 전송된 태스크를 Celery 워커에서 소비(consume)해 실행하는 구조입니다. 태스크는 Celery 워커에서 생성한 서브 프로세스 형태로 실행됩니다.

```python
# ci.py

@cli_utils.action_logging
def worker(args):
    env = os.environ.copy()
    env['AIRFLOW_HOME'] = settings.AIRFLOW_HOME

    if not settings.validate_session():
        log.error("Worker exiting... database connection precheck failed! ")
        sys.exit(1)

    # Celery worker
    from airflow.executors.celery_executor import app as celery_app
    from celery import maybe_patch_concurrency
    from celery.bin import worker

    autoscale = args.autoscale
    skip_serve_logs = args.skip_serve_logs

    if autoscale is None and conf.has_option("celery", "worker_autoscale"):
        autoscale = conf.get("celery", "worker_autoscale")

    worker = worker.worker(app=celery_app)
    options = {
        'optimization': 'fair',
        'O': 'fair',
        'queues': args.queues,
        'concurrency': args.concurrency,
        'autoscale': autoscale,
        'hostname': args.celery_hostname,
        'loglevel': conf.get('core', 'LOGGING_LEVEL'),
    }

    if conf.has_option("celery", "pool"):
        pool = conf.get("celery", "pool")
        options["pool"] = pool
        maybe_patch_concurrency(['-P', pool])

    if args.daemon:
        pid, stdout, stderr, log_file = setup_locations("worker",
                                                        args.pid,
                                                        args.stdout,
                                                        args.stderr,
                                                        args.log_file)
        handle = setup_logging(log_file)
        stdout = open(stdout, 'w+')
        stderr = open(stderr, 'w+')

        ctx = daemon.DaemonContext(
            pidfile=TimeoutPIDLockFile(pid, -1),
            files_preserve=[handle],
            stdout=stdout,
            stderr=stderr,
        )
        with ctx:
            sp = _serve_logs(env, skip_serve_logs)
            worker.run(**options)

        stdout.close()
        stderr.close()
    else:
        signal.signal(signal.SIGINT, sigint_handler)
        signal.signal(signal.SIGTERM, sigint_handler)

        sp = _serve_logs(env, skip_serve_logs)

        worker.run(**options)

    if sp:
        sp.kill()
```

**장점**

워커를 2대 이상 구성할 수 있다는 부분에서 SPOF 단점을 어느 정도 개선할 수 있다는 장점이 있습니다. 이런 이유로 서비스 환경에서 많이 사용하고 있습니다.

**단점**

Master에 대한 SPOF 단점은 그대로 가지고 있습니다. 따라서 이에 대한 프로세스 모니터링이 필요합니다. 또한 메시지 브로커가 추가로 필요하기 때문에 관리 포인트가 늘어난다는 단점이 있습니다.

출처: https://engineering.linecorp.com/ko/blog/data-engineering-with-airflow-k8s-1
