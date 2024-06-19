# Kubernetes Application Lifecycle Management


## Rolloing Updates and Roll Back

### Q. Let us try that. Upgrade the application by setting the image on the deployment to kodekloud/webapp-color:v2

Do not delete and re-create the deployment. Only set the new image name for the existing deployment.

Deployment Name: frontend

Deployment Image: kodekloud/webapp-color:v2

```bash
controlplane ~ ➜  kubectl edit deployment frontend

apiVersion: apps/v1
kind: Deployment
metadata:
  annotations:
    deployment.kubernetes.io/revision: "1"
  creationTimestamp: "2024-06-19T04:55:08Z"
  generation: 1
  name: frontend
  namespace: default
  resourceVersion: "897"
  uid: 4b75042c-8a82-42dd-86f9-c4cd41f4a8e8
spec:
  minReadySeconds: 20
  progressDeadlineSeconds: 600
  replicas: 4
  revisionHistoryLimit: 10
  selector:
    matchLabels:
      name: webapp
  strategy:
    rollingUpdate:
      maxSurge: 25%
      maxUnavailable: 25%
    type: RollingUpdate
  template:
    metadata:
      creationTimestamp: null
      labels:
        name: webapp
    spec:
      containers:
      - image: kodekloud/webapp-color:v2
        imagePullPolicy: IfNotPresent
        name: simple-webapp
        ports:
        - containerPort: 8080
          protocol: TCP
        resources: {}
        terminationMessagePath: /dev/termination-log
        terminationMessagePolicy: File
      dnsPolicy: ClusterFirst
      restartPolicy: Always
      schedulerName: default-scheduler
      securityContext: {}
      terminationGracePeriodSeconds: 30
status:
:wq

deployment.apps/frontend edited
```

### Q. Change the deployment strategy to `Recreate`.

Delete and re-create the deployment if neccessary. Only update the strategy type of the existing deployment.

Deployment Name: frontend

Deployment Image: kodekloud/webapp-color:v2

Strategy: Recreate

```bash
controlplane ~ ✖ kubectl edit deployment frontend

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: frontend
  namespace: default
spec:
  replicas: 4
  selector:
    matchLabels:
      name: webapp
  strategy:
    type: Recreate
  template:
    metadata:
      labels:
        name: webapp
    spec:
      containers:
      - image: kodekloud/webapp-color:v2
        name: simple-webapp
        ports:
        - containerPort: 8080
          protocol: TCP
:wq

deployment.apps/frontend edited
```

## Commands and Arguments

EX.

pod-definition.yaml

```yaml
apiVersion: v1
kind: Pod
metadata: 
  name: ubuntu-sleeper-pod
spec:
  containers:
    - name: ubuntu-sleeper
      image: ubuntu-sleeper
      command: ["sleep2.0"] # -> ENTRYPOINT
      args: ["10"] # -> CMD
```

Docker Image
```Dockerfile
FROM ubuntu

ENTRYPOINT ["sleep"]

CMD ["5"]
```

{{<admonition info>}}
`ENTRYPOINT`와 `CMD`는 Dockerfile에서 컨테이너가 시작될 때 실행할 명령을 지정하는 데 사용되는 두 가지 중요한 지시어입니다. 이 두 가지는 종종 혼동되기 쉬우므로, 각 지시어의 역할과 차이점을 이해하는 것이 중요합니다.

- ENTRYPOINT

    - ENTRYPOINT는 Docker 컨테이너가 시작될 때 실행되는 명령을 지정합니다. 
    
    - ENTRYPOINT로 설정된 명령은 항상 실행되며, 일반적으로 변경되지 않습니다. 

- CMD
    - CMD는 Command에 전달되는 default parameter 입니다.

    - CMD는 컨테이너가 시작될 때 실행할 기본 명령을 지정합니다. 
    
    - CMD는 ENTRYPOINT가 설정되지 않았을 때 실행되며, ENTRYPOINT와 함께 사용되면 ENTRYPOINT에 전달할 기본 인수를 
    제공할 수도 있습니다. 
    
    - CMD는 ENTRYPOINT와 달리, 컨테이너를 실행할 때 명령을 재정의할 수 있습니다.
{{</admonition>}}

### Q. What is the command used to run the pod `ubuntu-sleeper`?

```bash
controlplane ~ ➜  kubectl describe pod ubuntu-sleeper
Name:             ubuntu-sleeper
Namespace:        default
Priority:         0
Service Account:  default
Node:             controlplane/192.9.202.3
Start Time:       Wed, 19 Jun 2024 05:59:09 +0000
Labels:           <none>
Annotations:      <none>
Status:           Running
IP:               10.42.0.9
IPs:
  IP:  10.42.0.9
Containers:
  ubuntu:
    Container ID:  containerd://31ffda30d5faa144528105f8c94028eafc7df17943b2eb901303e9593a5783a0
    Image:         ubuntu
    Image ID:      docker.io/library/ubuntu@sha256:2e863c44b718727c860746568e1d54afd13b2fa71b160f5cd9058fc436217b30
    Port:          <none>
    Host Port:     <none>
    Command:
      sleep
      4800
```

> A. sleep 4800

### Q. Create a pod with the ubuntu image to run a container to sleep for 5000 seconds. Modify the file `ubuntu-sleeper-2.yaml`.

Pod Name: ubuntu-sleeper-2

Command: sleep 5000

```bash
controlplane ~ ➜  vim ubuntu-sleeper-2.yaml

---
apiVersion: v1 
kind: Pod 
metadata:
  name: ubuntu-sleeper-2 
spec:
  containers:
  - name: ubuntu
    image: ubuntu
    command:
      - "sleep"
      - "5000"
:wq

controlplane ~ ✖ kubectl create -f ubuntu-sleeper-2.yaml 
pod/ubuntu-sleeper-2 created
```

### Q. Inspect the file `Dockerfile` given at `/root/webapp-color` directory. What command is run at container startup?

```bash
controlplane ~/webapp-color ➜  cat Dockerfile
FROM python:3.6-alpine

RUN pip install flask

COPY . /opt/

EXPOSE 8080

WORKDIR /opt

ENTRYPOINT ["python", "app.py"]
```

> A. python app.py

### Q. Inspect the file `Dockerfile2` given at `/root/webapp-color` directory. What command is run at container startup?

```bash
controlplane ~/webapp-color ➜  cat Dockerfile2
FROM python:3.6-alpine

RUN pip install flask

COPY . /opt/

EXPOSE 8080

WORKDIR /opt

ENTRYPOINT ["python", "app.py"]

CMD ["--color", "red"]
```

> A. python app.py --color red

### Q. Inspect the two files under directory `webapp-color-2`. What command is run at container startup?

```bash
controlplane ~/webapp-color-2 ➜  cat Dockerfile
FROM python:3.6-alpine

RUN pip install flask

COPY . /opt/

EXPOSE 8080

WORKDIR /opt

ENTRYPOINT ["python", "app.py"]

CMD ["--color", "red"]

controlplane ~/webapp-color-2 ➜  cat webapp-color-pod.yaml 
apiVersion: v1 
kind: Pod 
metadata:
  name: webapp-green
  labels:
      name: webapp-green 
spec:
  containers:
  - name: simple-webapp
    image: kodekloud/webapp-color
    command: ["--color","green"]
```

> A. --color green

### Q. Inspect the two files under directory webapp-color-3. What command is run at container startup?

```bash
controlplane ~/webapp-color-3 ➜  cat Dockerfile
FROM python:3.6-alpine

RUN pip install flask

COPY . /opt/

EXPOSE 8080

WORKDIR /opt

ENTRYPOINT ["python", "app.py"]

CMD ["--color", "red"]

controlplane ~/webapp-color-3 ➜  cat webapp-color-pod-2.yaml 
apiVersion: v1 
kind: Pod 
metadata:
  name: webapp-green
  labels:
      name: webapp-green 
spec:
  containers:
  - name: simple-webapp
    image: kodekloud/webapp-color
    command: ["python", "app.py"]
    args: ["--color", "pink"]
```

> A. python app.py --color pink

### Q. Create a pod with the given specifications. By default it displays a `blue` background. Set the given command line arguments to change it to `green`.

Pod Name: webapp-green

Image: kodekloud/webapp-color

Command line arguments: --color=green

```bash
controlplane ~ ➜  vim webapp-green-pod.yaml

---
apiVersion: v1 
kind: Pod 
metadata:
  name: webapp-green
  labels:
      name: webapp-green 
spec:
  containers:
  - name: simple-webapp
    image: kodekloud/webapp-color
    args: ["--color", "green"]
:wq

controlplane ~ ➜  kubectl create -f webapp-green-pod.yaml 
pod/webapp-green created
```

## ENV Variables - ConfigMap

### Q. Update the environment variable on the POD to display a `green` background.

Pod Name: webapp-color

Label Name: webapp-color

Env: APP_COLOR=green

```bash
controlplane ~ ➜  vim webapp-color-pod.yaml

---
apiVersion: v1
kind: Pod
metadata:
  labels:
    name: webapp-color
  name: webapp-color
  namespace: default
spec:
  containers:
  - env:
    - name: APP_COLOR
      value: green
    image: kodekloud/webapp-color
    name: webapp-color

controlplane ~ ➜  kubectl create -f webapp-color-pod.yaml 
pod/webapp-color created
```

### Q. How many `ConfigMaps` exists in the `default` namespace?

```bash
controlplane ~ ➜  kubectl get configmaps
NAME               DATA   AGE
kube-root-ca.crt   1      19m
db-config          3      14s
```

### Q. Create a new ConfigMap for the `webapp-color` POD.

ConfigMap Name: webapp-config-map

Data: APP_COLOR=darkblue

Data: APP_OTHER=disregard

```bash
controlplane ~ ➜  kubectl create configmap webapp-config-map --from-literal=APP_COLOR=darkblue --from-literal=APP_OTHER=disregard
configmap/webapp-config-map created
```

### Q. Update the cnvironment variable on the POD to use only the `APP_COLOR` key from the newly created ConfigMap.

```bash
controlplane ~ ➜  vim webapp-color-pod.yaml

---
apiVersion: v1
kind: Pod
metadata:
  labels:
    name: webapp-color
  name: webapp-color
  namespace: default
spec:
  containers:
  - env:
    - name: APP_COLOR
      valueFrom:
       configMapKeyRef:
         name: webapp-config-map
         key: APP_COLOR
    image: kodekloud/webapp-color
    name: webapp-color

controlplane ~ ➜  kubectl create -f webapp-color-pod.yaml 
pod/webapp-color created
```

## Secrets

### Q. The reason that the application is failed is because we have no created the secrets yet. Create a new secret named `db-secret` wit hthe data given below.

Secret Name: db-secret

Secret 1: DB_Host=sql01

Secret 2: DB_User=root

Secret 3: DB_Password=password123

```bash
controlplane ~ ➜  kubectl create secret generic db-secret --from-literal=DB_Host=sql01 --from-literal=DB_User=root --from-literal=DB_Password=password123
secret/db-secret created
```

### Q. Configure `webapp-pod` to load environment variables from the newly created secret.

Pod name: webapp-pod

Image name: kodekloud/simple-webapp-mysql

Env From: Secret=db-secret

```bash
controlplane ~ ➜  vim webapp-pod.yaml

---
apiVersion: v1 
kind: Pod 
metadata:
  labels:
    name: webapp-pod
  name: webapp-pod
  namespace: default 
spec:
  containers:
  - image: kodekloud/simple-webapp-mysql
    imagePullPolicy: Always
    name: webapp
    envFrom:
    - secretRef:
        name: db-secret

controlplane ~ ➜  kubectl create -f webapp-pod.yaml 
pod/webapp-pod created
```

## Multi Container PODs

### Q. Create a multi-container pod with 2 containers.

If the pod goes into the `crashloopbackoff` then add the command `sleep 1000` in the `lemon` container.

Name: yellow

Container 1 Name: lemon

Container 1 Image: busybox

Container 2 Name: gold

Container 2 Image: redis

```bash
controlplane ~ ➜  vim yellow-pod.yaml

apiVersion: v1
kind: Pod
metadata:
  name: yellow
spec:
  containers:
  - name: lemon
    image: busybox
    command:
      - sleep
      - "1000"

  - name: gold
    image: redis

controlplane ~ ➜  k create -f yellow-pod.yaml 
pod/yellow created
```

### Q. The application outputs logs to the file `/log/app.log`. View the logs and try to identify the user having issues with Login.

```bash
controlplane ~ ➜  kubectl -n elastic-stack exec -it app -- cat /log/app.log
```

### Q. Edit the pod in the `elastic-stack` namespace to add a sidecar container to send logs to Elastic Search. Mount the log volume to the sidecar container.

Only add a new container. Do not modify anything else. Use the spec provided below.

Name: app

Container Name: sidecar

Container Image: kodekloud/filebeat-configured

Volume Mount: log-volume

Mount Path: /var/log/event-simulator/

Existing Container Name: app

Existing Container Image: kodekloud/event-simulator

```bash
controlplane ~/elastic-search ✖ k edit pod app -n elastic-stack
error: pods "app" is invalid
A copy of your changes has been stored to "/tmp/kubectl-edit-1753133961.yaml"
error: Edit cancelled, no valid changes were saved.

---
apiVersion: v1
kind: Pod
metadata:
  name: app
  namespace: elastic-stack
  labels:
    name: app
spec:
  containers:
  - name: app
    image: kodekloud/event-simulator
    volumeMounts:
    - mountPath: /log
      name: log-volume

  - name: sidecar
    image: kodekloud/filebeat-configured
    volumeMounts:
    - mountPath: /var/log/event-simulator/
      name: log-volume

  volumes:
  - name: log-volume
    hostPath:
      # directory location on host
      path: /var/log/webapp
      # this field is optional
      type: DirectoryOrCreate

controlplane ~/elastic-search ✖ k replace --force -f /tmp/kubectl-edit-1753133961.yaml
pod "app" deleted
pod/app replaced
```

## Init Containers

### Q. Update the pod red to use an initContainer that uses the busybox image and sleeps for 20 seconds

Delete and re-create the pod if necessary. But make sure no other configurations change.

Pod: red

initContainer Configured Correctly

```bash
---
apiVersion: v1
kind: Pod
metadata:
  name: red
  namespace: default
spec:
  containers:
  - command:
    - sh
    - -c
    - echo The app is running! && sleep 3600
    image: busybox:1.28
    name: red-container
  initContainers:
  - image: busybox
    name: red-initcontainer
    command: 
      - "sleep"
      - "20"
```
