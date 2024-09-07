# Create_nodes


## Install the start Minikube

### Install the Minikube

```bash
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-darwin-amd64
sudo install minikube-darwin-amd64 /usr/local/bin/minikube
```

### Start minikube cluster and Check the status

```bash
 {seilylook} 🚀 minikube start
😄  Darwin 14.6.1 (arm64) 의 minikube v1.33.0
✨  기존 프로필에 기반하여 docker 드라이버를 사용하는 중
👍  Starting "minikube" primary control-plane node in "minikube" cluster
🚜  Pulling base image v0.0.43 ...
🤷  docker "minikube" container is missing, will recreate.
🔥  Creating docker container (CPUs=2, Memory=4600MB) ...
🐳  쿠버네티스 v1.30.0 을 Docker 26.0.1 런타임으로 설치하는 중
    ▪ 인증서 및 키를 생성하는 중 ...
    ▪ 컨트롤 플레인을 부팅하는 중 ...
    ▪ RBAC 규칙을 구성하는 중 ...
🔗  bridge CNI (Container Networking Interface) 를 구성하는 중 ...
🔎  Kubernetes 구성 요소를 확인...
    ▪ Using image gcr.io/k8s-minikube/storage-provisioner:v5
🌟  애드온 활성화 : storage-provisioner, default-storageclass
🏄  끝났습니다! kubectl이 "minikube" 클러스터와 "default" 네임스페이스를 기본적으로 사용하도록 구성되었습니다.

 {seilylook} 🚀 minikube status
minikube
type: Control Plane
host: Running
kubelet: Running
apiserver: Running
kubeconfig: Configured
```

### Create 3 Nodes in Cluster

**Command for create nodes**

```bash
minikube start --nodes <NUMBER_OF_NODES> -p <CLUSTER_NAME>
```

```bash
{seilylook} 🚀 minikube start --nodes 3 -p k8scluster
😄  [k8scluster] Darwin 14.6.1 (arm64) 의 minikube v1.33.0
✨  자동적으로 docker 드라이버가 선택되었습니다
📌  Using Docker Desktop driver with root privileges
👍  Starting "k8scluster" primary control-plane node in "k8scluster" cluster
🚜  Pulling base image v0.0.43 ...
🔥  Creating docker container (CPUs=2, Memory=2200MB) ...
🐳  쿠버네티스 v1.30.0 을 Docker 26.0.1 런타임으로 설치하는 중
    ▪ 인증서 및 키를 생성하는 중 ...
    ▪ 컨트롤 플레인을 부팅하는 중 ...
    ▪ RBAC 규칙을 구성하는 중 ...
🔗  CNI (Container Networking Interface) 를 구성하는 중 ...
🔎  Kubernetes 구성 요소를 확인...
    ▪ Using image gcr.io/k8s-minikube/storage-provisioner:v5
🌟  애드온 활성화 : storage-provisioner, default-storageclass

👍  Starting "k8scluster-m02" worker node in "k8scluster" cluster
🚜  Pulling base image v0.0.43 ...
🔥  Creating docker container (CPUs=2, Memory=2200MB) ...
🌐  네트워크 옵션을 찾았습니다
    ▪ NO_PROXY=192.168.58.2
🐳  쿠버네티스 v1.30.0 을 Docker 26.0.1 런타임으로 설치하는 중
    ▪ env NO_PROXY=192.168.58.2
🔎  Kubernetes 구성 요소를 확인...

👍  Starting "k8scluster-m03" worker node in "k8scluster" cluster
🚜  Pulling base image v0.0.43 ...
🔥  Creating docker container (CPUs=2, Memory=2200MB) ...
🌐  네트워크 옵션을 찾았습니다
    ▪ NO_PROXY=192.168.58.2,192.168.58.3
🐳  쿠버네티스 v1.30.0 을 Docker 26.0.1 런타임으로 설치하는 중
    ▪ env NO_PROXY=192.168.58.2
    ▪ env NO_PROXY=192.168.58.2,192.168.58.3
🔎  Kubernetes 구성 요소를 확인...
🏄  끝났습니다! kubectl이 "k8scluster" 클러스터와 "default" 네임스페이스를 기본적으로 사용하도록 구성되었습니다.

 {seilylook} 🚀 kubectl get nodes
NAME             STATUS   ROLES           AGE     VERSION
k8scluster       Ready    control-plane   9m30s   v1.30.0
k8scluster-m02   Ready    <none>          9m10s   v1.30.0
k8scluster-m03   Ready    <none>          9m2s    v1.30.0
```

## Label Nodes

When deploying Redis and Apache Pods, I don't want them to deploy to own `control-plane`. 

To do this, I can use **labels**, **taints**, **affinity**.

In this tutorial, I'll use **labels**.

KEY | Value

node-role.kubernetes.io/worker: worker

```bash
kubectl label node <NODE_NAME> node-role.kubernetes.io/worker=worker
```

```bash
 {seilylook} 🍀   ~/Development/Devlog   main ±  kubectl label node k8scluster-m02 node-role.kubernetes.io/worker=worker
node/k8scluster-m02 labeled

 {seilylook} 🍀   ~/Development/Devlog   main ±  kubectl label node k8scluster-m03 node-role.kubernetes.io/worker=worker
node/k8scluster-m03 labeled

 {seilylook} 🍀   ~/Development/Devlog   main ±  kubectl get nodes                                                      
NAME             STATUS   ROLES           AGE   VERSION
k8scluster       Ready    control-plane   16m   v1.30.0
k8scluster-m02   Ready    worker          16m   v1.30.0
k8scluster-m03   Ready    worker          16m   v1.30.0

 {seilylook} 🍀   ~/Development/Devlog   main ±  kubectl describe node k8scluster-m02                                
Name:               k8scluster-m02
Roles:              worker
Labels:             beta.kubernetes.io/arch=arm64
                    beta.kubernetes.io/os=linux
                    kubernetes.io/arch=arm64
                    kubernetes.io/hostname=k8scluster-m02
                    kubernetes.io/os=linux
                    minikube.k8s.io/commit=86fc9d54fca63f295d8737c8eacdbb7987e89c67
                    minikube.k8s.io/name=k8scluster
                    minikube.k8s.io/primary=false
                    minikube.k8s.io/updated_at=2024_09_07T14_23_16_0700
                    minikube.k8s.io/version=v1.33.0
                    node-role.kubernetes.io/worker=worker
```

## Deployment Pod & Deployment

### Pod

```yaml
# redis-pod.yaml

apiVersion: v1
kind: Pod
metadata:
  name: redis-pod
spec:
  containers:
  - name: redis-pod-container
    image: redis:7.0.9
    resources:
      limits:
        memory: "128Mi"
        cpu: "500m"
    ports:
      - containerPort: 6379
  nodeSelector:
    node-role.kubernetes.io/worker: worker
```

```bash
{seilylook} ⚡️ kubectl apply -f redis-pod.yaml 
pod/redis-pod created

{seilylook} ⚡️ kubectl get pods -o wide
NAME        READY   STATUS    RESTARTS   AGE    IP           NODE             NOMINATED NODE   READINESS GATES
redis-pod   1/1     Running   0          101s   10.244.1.2   k8scluster-m02   <none>           <none>
```

### Deployment

```yaml
# httpd-deploy.yaml

apiVersion: apps/v1
kind: Deployment
metadata:
  name: httpd-deploy
spec:
  replicas: 5
  selector:
    matchLabels:
      app: httpd
  template:
    metadata:
      labels:
        app: httpd
    spec:
      containers:
      - name: httpd-deploy-container
        image: httpd:2.4.56
        resources:
          limits:
            memory: "128Mi"
            cpu: "500m"
        ports:
        - containerPort: 80
      nodeSelector:
        node-role.kubernetes.io/worker: worker
```

```bash
 {seilylook} ⚡️ kubectl get deploy -o wide
NAME           READY   UP-TO-DATE   AVAILABLE   AGE   CONTAINERS               IMAGES         SELECTOR
httpd-deploy   5/5     5            5           36s   httpd-deploy-container   httpd:2.4.56   app=httpd
 {seilylook} ⚡️ kubectl get pods -o wide  
NAME                            READY   STATUS    RESTARTS   AGE     IP           NODE             NOMINATED NODE   READINESS GATES
httpd-deploy-58f57cf68c-7cqkl   1/1     Running   0          45s     10.244.2.4   k8scluster-m03   <none>           <none>
httpd-deploy-58f57cf68c-9485h   1/1     Running   0          45s     10.244.2.2   k8scluster-m03   <none>           <none>
httpd-deploy-58f57cf68c-bwhh6   1/1     Running   0          45s     10.244.1.4   k8scluster-m02   <none>           <none>
httpd-deploy-58f57cf68c-rkhdk   1/1     Running   0          45s     10.244.2.3   k8scluster-m03   <none>           <none>
httpd-deploy-58f57cf68c-vkvlz   1/1     Running   0          45s     10.244.1.3   k8scluster-m02   <none>           <none>
redis-pod                       1/1     Running   0          6m44s   10.244.1.2   k8scluster-m02   <none>           <none>
```

```bash
 {seilylook} ⚡️ kubectl get all -o wide
NAME                                READY   STATUS    RESTARTS   AGE     IP           NODE             NOMINATED NODE   READINESS GATES
pod/httpd-deploy-58f57cf68c-7cqkl   1/1     Running   0          4m25s   10.244.2.4   k8scluster-m03   <none>           <none>
pod/httpd-deploy-58f57cf68c-9485h   1/1     Running   0          4m25s   10.244.2.2   k8scluster-m03   <none>           <none>
pod/httpd-deploy-58f57cf68c-bwhh6   1/1     Running   0          4m25s   10.244.1.4   k8scluster-m02   <none>           <none>
pod/httpd-deploy-58f57cf68c-rkhdk   1/1     Running   0          4m25s   10.244.2.3   k8scluster-m03   <none>           <none>
pod/httpd-deploy-58f57cf68c-vkvlz   1/1     Running   0          4m25s   10.244.1.3   k8scluster-m02   <none>           <none>
pod/redis-pod                       1/1     Running   0          10m     10.244.1.2   k8scluster-m02   <none>           <none>

NAME                 TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)   AGE   SELECTOR
service/kubernetes   ClusterIP   10.96.0.1    <none>        443/TCP   42m   <none>

NAME                           READY   UP-TO-DATE   AVAILABLE   AGE     CONTAINERS               IMAGES         SELECTOR
deployment.apps/httpd-deploy   5/5     5            5           4m25s   httpd-deploy-container   httpd:2.4.56   app=httpd

NAME                                      DESIRED   CURRENT   READY   AGE     CONTAINERS               IMAGES         SELECTOR
replicaset.apps/httpd-deploy-58f57cf68c   5         5         5       4m25s   httpd-deploy-container   httpd:2.4.56   app=httpd,pod-template-hash=58f57cf68c
```
