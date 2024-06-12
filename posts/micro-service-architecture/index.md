# Micro Service Architecture


# Work Flow

1. Voting app(Python web): 80 port를 통해 사용자가 접근

2. In-memory(Redis): 6379 port를 통해 Voting app POD & Worker POD가 접근

3. Worker(.Net): 접근할 필요 없음

4. DB(PostgreSQL): 5432 port를 통해 Result app POD & Worker POD가 접근

5. Result(Nodejs): 80 port를 통해 사용자가 접근

# Goals

1. Deploy Container

2. Enable Connectivity

3. External Access

# Steps

1. Deploy PODs

2. Create Services(Cluster IP): 내부적으로 Worker, Voting-app, Result-app이 Redis, DB에 접근할 수 있도록 해주는 용도.

    A. redis

    B. db

3. Create Services(NodePort): 외부에서 사용자가 Voting-app, Result-app에 접근할 수 있도록 해주는 용도.

    A. voting-app

    B. result-app

Conclusion: 5 PODs, 4 Services

## Docker run

```bash
docker run -d --name=redis redis
```

```bash
docker run -d --name=db postgres:9.4
```

```bash
docker run -d --name=vote -p 5000:80 --link redis:redis voting-app
```

```bash
docker run -d --name=result -p 5001:80 --link db:db result-app
```

```bash
docker run -d --name=worker --link db:db --link redis:redis worker
```

## Configuration

### Pods

#### Voting-app

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: voting-app-pod
  labels:
    name: voting-app-pod
    app: demo-voting-app
spec:
  containers:
    - name: voting-app
      image: kodekloud/examplevotingapp_vote:v1
      ports:
        - containerPort: 80
```

#### Result-app

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: result-app-pod
  labels:
    name: result-app-pod
    app: demo-voting-app
spec:
  containers:
    - name: result-app
      image: kodekloud/examplevotingapp_result:v1
      ports:
        - containerPort: 80
```

#### Redis

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: redis-pod
  labels:
    name: redis-pod
    app: demo-voting-app
spec:
  containers:
    - name: redis
      image: redis
      ports:
        - containerPort: 6379
```

#### Postgres

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: postgres-pod
  labels:
    name: postgres-pod
    app: demo-voting-app
spec:
  containers:
    - name: postgres
      image: postgres
      ports:
        - containerPort: 5432
      env:
        - name: POSTGRES_USER
          value: "postgres"
        - name: POSTGRES_PASSWORD
          value: "postgres"
```

#### Worker

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: worker-app-pod
  labels:
    name: worker-app-pod
    app: demo-voting-app
spec:
  containers:
    - name: worker-app
      image: kodekloud/examplevotingapp_worker:v1
```

### Services

#### Redis

```yaml
apiVersion: v1
kind: Service
metadata:
  name: redis
  labels:
    name: redis-service
    app: demo-voting-app
spec:
  ports:
    - port: 6379
      targetPort: 6379
  selector:
    name: redis-pod
    app: demo-voting-app
```

#### Postgres

```yaml
apiVersion: v1
kind: Service
metadata:
  name: db
  labels:
    name: postgres-service
    app: demo-voting-app
spec:
  ports:
    - port: 5432
      targetPort: 5432
  selector:
    name: postgres-pod
    app: demo-voting-app
```

#### Voting-app

```yaml
apiVersion: v1
kind: Service
metadata:
  name: voting-service
  labels:
    name: voting-service
    app: demo-voting-app
spec:
  # 지정해주지 않으면 default 값인 ClusterIP로 적용된다.
  type: NodePort
  ports:
    - port: 80
      targetPort: 80
      nodePort: 30004
  selector:
    name: voting-app-pod
    app: demo-voting-app
```

#### Result-app

```yaml
apiVersion: v1
kind: Service
metadata:
  name: result-service
  labels:
    name: result-service
    app: demo-voting-app
spec:
  # 지정해주지 않으면 default 값인 ClusterIP로 적용된다.
  type: NodePort
  ports:
    - port: 80
      targetPort: 80
      nodePort: 30005
  selector:
    name: result-app-pod
    app: demo-voting-app
```

## Test

### Voting-app

#### Pod, Service 생성

```bash
{seilylook} 🚀 cd pods

{seilylook} 🚀 kubectl create -f voting-app-pod.yaml

{seilylook} 🚀 cd ..

{seilylook} 🚀 cd services

{seilylook} 🚀 kubectl create -f voting-app-service.yaml
```

#### Pod, Service 생성 확인

```bash
{seilylook} 🚀 kubectl get pods
NAME             READY   STATUS    RESTARTS   AGE
voting-app-pod   1/1     Running   0          9m1s

{seilylook} 🚀 kubectl get services
NAME             TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)        AGE
kubernetes       ClusterIP   10.96.0.1       <none>        443/TCP        86m
voting-service   NodePort    10.100.147.17   <none>        80:30004/TCP   8m49s
```

#### URL 확인

```bash
{seilylook} 🚀 minikube service voting-service --url
http://127.0.0.1:51966
❗  darwin 에서 Docker 드라이버를 사용하고 있기 때문에, 터미널을 열어야 실행할 수 있습니다
```

{{<admonition warning>}}
voting-service와 result-service에 지정한 port인 30004, 30005가 아닌 다른 포트 번호가 출력되는 것은 minikube에서 자동으로 다른 포트로 매핑하는 것이기 때문에 신경쓰지 않아도 된다.
{{</admonition>}}

### Redis

#### Pod, Service 생성

```bash
 {seilylook} 🚀 cd pods 
 {seilylook} 🚀 kubectl create -f redis-pod.yaml 
pod/redis-pod created
 {seilylook} 🚀 cd ..  
 {seilylook} 🚀 cd services 
 {seilylook} 🚀 kubectl create -f redis-service.yaml 
```

#### Pod, Service 생성 확인

```bash
 ✘ {seilylook} 🚀 kubectl get pods     
NAME             READY   STATUS    RESTARTS   AGE
redis-pod        1/1     Running   0          2m47s
voting-app-pod   1/1     Running   0          19m

 {seilylook} 🚀 kubectl get svc     
NAME             TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)        AGE
kubernetes       ClusterIP   10.96.0.1        <none>        443/TCP        96m
redis            ClusterIP   10.106.246.206   <none>        6379/TCP       2m33s
voting-service   NodePort    10.100.147.17    <none>        80:30004/TCP   19m
```

### PostgreSQL

#### Pod, Service 생성

```bash
 {seilylook} 🚀 cd pods 
 {seilylook} 🚀 kubectl create -f postgres-pod.yaml 
pod/redis-pod created
 {seilylook} 🚀 cd ..  
 {seilylook} 🚀 cd services 
 {seilylook} 🚀 kubectl create -f postgres-service.yaml 
```

#### Pod, Service 생성 확인

```bash
 ✘ {seilylook} 🚀 kubectl get pods     
NAME             READY   STATUS    RESTARTS   AGE
postgres-pod     1/1     Running   0          2m47s
redis-pod        1/1     Running   0          2m47s
voting-app-pod   1/1     Running   0          19m

 {seilylook} 🚀 kubectl get svc     
NAME             TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)        AGE
db               ClusterIP   10.111.84.234    <none>        5432/TCP       2m40s
kubernetes       ClusterIP   10.96.0.1        <none>        443/TCP        96m
redis            ClusterIP   10.106.246.206   <none>        6379/TCP       2m33s
voting-service   NodePort    10.100.147.17    <none>        80:30004/TCP   19m
```
