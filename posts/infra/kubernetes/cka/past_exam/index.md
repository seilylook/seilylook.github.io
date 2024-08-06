# Past Exam Questions


## 1. RBAC(Role-Based Access Control)

### Service Account 생성

서비스 어카운트는 파드가 쿠버네티스 API와 통신하기 위해 파드에 할당되는 하나의 ID이다. 파드 생성 시 서비스 어카운트를 할당하고, 해당 서비스 어카운트에 적절한 권한을 부여하여 쿠버네티스 API서버와 통신할 수 있다.

```bash
kubectl create serviceaccount pod-reader
```

쿠버네티스는 역할 기반으로 API 접근을 관리한다. 역할을 부여하기 위한 대상으로 앞서 서비스어카운트를 만들었고, 실제 역할을 만들어 서비스어카운트에 할당하는 것을 바인딩(Binding)이라고 한다.
 
역할은 Role, ClusterRole 두 가지로 분류된다. Role은 특정 네임스페이스에 속하게 되며, ClusterRole은 전체 클러스터에 고유한 역할이 된다. 역할을 서비스어카운트와 바인딩하는 것도 RoleBinding, ClusterRoleBinding 두 가지 방법이 있다. RoleBinding을 통해 바인딩한 Role과 ClusterRole은 특정 네임스페이스에서만 유효하며, ClusterRoleBinding으로 바인딩 시 모든 네임스페이스에 공통적으로 적용된다.


### clusterRole 생성

```bash
kubectl create clusterrole pod-reader-role --verb=get,list,watch --resource=pods
```

### Clusterrolebind

```bash
kubectl create clusterrolebinding myapp-view-binding --clusterrole=pod-reader-role --serviceaccount=mynamespcae:pod-reader
```

## 2. Node Troubleshooting

Node는 쿠버네티스 클러스터를 구성하는 하나의 VM 또는 하드웨어이다.

### Node가 **NotReady** 상태로 나올 때

쿠버네티스의 각 노드에는 kubelet이 실행된다. 이 kubelet은 노드 내에서 실제 컨테이너를 수행하는 역할을 하는데, 해당 프로세스가 제대로 실행되지 않으면 **NotReady** 상태로 조회된다. 아래의 명령을 통해 ssh로 노드에 직접 접속한 후 kubelet을 재실행 시킨다.

```bash
k get nodes

ssh node01

sudo systemctl status kubelet

sudo systemctl restart kubelet
```

### **Taint** 가 적용된 노드 확인하기

테인트는 톨러레이션(Tolerations)와 함께 사용된다. 테인트는 노드에 할당되고, 톨러레이션은 파드에 할당된다. 파드가 스케줄링될 때 어떤 노드에서 실행될지는 중요한 문제인데, 테인트를 통해 이를 컨트롤할 수 있다. 테인트는 일종의 검문소 역할을 하고, 톨러레이션은 해당 검문소를 통과하는 출입증과 같은 역할을 한다. 파드가 스케줄링 될 때 노드의 테인트(검문소)에 대한 톨러레이션(출입증)이 없는 경우, 그 노드에는 스케줄링되지 않는다.
 
테인트가 적용된 노드는 describe 명령을 통해 확인할 수 있다.

```bash
k describe nodes | grep -i taint

echo {노드 개수} > {파일 경로}
```

## 3. 특정 레이블을 가진 Pod 중 CPU 사용량이 가장 많은 Pod 조회

Pod의 CPU 사용량은 kubectl top pod 명령어를 통해 알 수 있다. `-l` 옵션과 레이블 명을 추가해 특정 레이블을 가진 파드의 CPU 사용량을 조회할 수 있다.

```bash
k top pod -l run=frontend --sort-by=cpu

echo {파드 이름} > {파일 경로}
```

## 4. 특정 Node에 Pod 할당

특정 Node에 스케쥴링 되는 파드를 생성한다. Pod가 스케쥴링 되는 노드를 지정하려면 두 가지 방법이 있다. `nodeSelector`, `nodeName`

### nodeSelector

1. 클러스터 내의 Node의 목록과 각 Label을 알아낸다.

```bash
k get nodes --show-labels

NAME      STATUS    ROLES    AGE     VERSION        LABELS
worker0   Ready     <none>   1d      v1.13.0        ...,kubernetes.io/hostname=worker0
worker1   Ready     <none>   1d      v1.13.0        ...,kubernetes.io/hostname=worker1
worker2   Ready     <none>   1d      v1.13.0        ...,kubernetes.io/hostname=worker2
```

2. 원하는 Node에 Label을 추가해준다.

```bash
kubectl label nodes <your-node-name> disktype=ssd
```

3. 제대로 Label이 적용되었는지 확인해준다.

```bash
kubectl get nodes --show-labels

NAME      STATUS    ROLES    AGE     VERSION        LABELS
worker0   Ready     <none>   1d      v1.13.0        ...,disktype=ssd,kubernetes.io/hostname=worker0
worker1   Ready     <none>   1d      v1.13.0        ...,kubernetes.io/hostname=worker1
worker2   Ready     <none>   1d      v1.13.0        ...,kubernetes.io/hostname=worker2
```

4. Pod를 생성하고 할당

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx
  labels:
    env: test
spec:
  containers:
  - name: nginx
    image: nginx
    imagePullPolicy: IfNotPresent
  nodeSelector:
    disktype: ssd
```

### nodeName

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx
spec:
  nodeName: foo-node # schedule pod to specific node
  containers:
  - name: nginx
    image: nginx
    imagePullPolicy: IfNotPresent
```

## 5. Pod의 Log를 파일로 출력

```bash
kubectl logs {POD_NAME} > {FILE_PATH}
```

## 6. hostPath PV 생성

문제에서 주어진 조건대로 PV를 생성한다. Pod는 기본적으로 stateless로 Pod 삭제 시 내부에 파일 시스템에 작성되었더 내용들도 모두 삭제된다. 이를 막기 위해 영속성이 필요한 데이터들은 PV, PVC를 활용해 관리한다. 

PV는 어떤 스토리지를 사용할 지에 대한 부분이고, PVC는 Pod가 어떤 PV를 사용할 지에 대한 정의이다. PV는 다양한 스토리지와 연결해 사용할 수 있는데, `hostPath`의 경우 실제 컨테이너가 실행되는 host machine의 파일 시스템을 사용한다.

```yaml
# pv-volume.yaml

apiVersion: v1
kind: PersistentVolume
metadata:
  name: task-pv-volume
  labels:
    type: local
spec:
  storageClassName: manual
  capacity:
    storage: 10Gi
  accessModes:
    - ReadWriteOnce
  hostPath:
    path: "/mnt/data"
```

## 7. PV, PVC 생성해 nginx Pod에 volume mount

### PV 생성

spec 부분에 `storage`, `accessModes`, `path` 부분을 문제에서 주어진 요구대로 생성하면 된다.

```yaml
# pv-volume.yaml

apiVersion: v1
kind: PersistentVolume
metadata:
  name: task-pv-volume
  labels:
    type: local
spec:
  storageClassName: manual
  capacity:
    storage: 10Gi
  accessModes:
    - ReadWriteOnce
  hostPath:
    path: "/mnt/data"                           65s
```

### PVC 생성

생성한 혹은 문제에서 주어진 PV에 맞게 PVC를 생성한다.

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: task-pv-claim
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 3Gi
```

```bash
k get pv, pvc

NAME                              CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS   CLAIM                   STORAGECLASS   REASON   AGE
persistentvolume/task-pv-volume   10Gi       RWO            Retain           Bound    default/task-pv-claim                           5m28s

NAME                                  STATUS   VOLUME           CAPACITY   ACCESS MODES   STORAGECLASS   AGE
persistentvolumeclaim/task-pv-claim   Bound    task-pv-volume   10Gi       RWO                           6s
```

PV, PVC 조회 시 `Bound`가 되어야 한다. 

### Pod 생성 및 PVC 연결

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: task-pv-pod
spec:
  volumes:
    - name: task-pv-storage
      persistentVolumeClaim:
        claimName: task-pv-claim
  containers:
    - name: task-pv-container
      image: nginx
      ports:
        - containerPort: 80
          name: "http-server"
      volumeMounts:
        - mountPath: "/usr/share/nginx/html"
          name: task-pv-storage
```

## 8. Storageclass에 맞는 PVC 생성

storageClass는 PVC에 맞는 PV를 자동으로 연결해준다. 만약 문제에서 이미 생성된 PV에 맞도록 PVC를 생성하라고 요구한다면, `storageclass`를 주의깊게 살펴보고 맞추어야 한다.

### PV 확인

```bash
kubectl describe pv task-pv-volume
Name:            task-pv-volume
Labels:          type=local
Annotations:     <none>
Finalizers:      [kubernetes.io/pv-protection]
StorageClass:    slow
Status:          Terminating
Claim:
Reclaim Policy:  Delete
Access Modes:    RWO
Capacity:        1Gi
Message:
Source:
    Type:          HostPath (bare host directory volume)
    Path:          /tmp/data
    HostPathType:
Events:            <none>
```

### PVC 생성

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: task-pv-claim
spec:
  storageClassName: slow
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 1Gi
```

## 9. 멀티 컨테이너 Pod 배포(사이트카 패턴)

두 개의 컨테이너가 하나의 볼륨을 공유하도록 배포해야 한다. 클러스터에는 nginx 싱글 컨테이너만 존재한다. 해당 nginx의 로그 파일이 저장되는 경로에 컨테이너 volume을 마운트하고, 해당 볼륨을 log-container라는 이름의 새로운 컨테이너에도 마운트한다. 두 컨테이너가 동일한 볼륨을 공유하게 되고, 따라서 log-container 접근 시 nginx의 log를 조회할 수 있어야 한다.

기존에 존재하는 Pod에 [Loggin Architecture](https://kubernetes.io/docs/concepts/cluster-administration/logging/#streaming-sidecar-container)에 있는 다음 코드를 붙여넣고 문제에서 말하는 명령어로 수정해준다.

```yaml
  - name: count-log-1
    image: busybox:1.28
    args: [/bin/sh, -c, 'tail -n+1 -F /var/log/1.log']
    volumeMounts:
    - name: varlog
      mountPath: /var/log
```

```bash
[root@k8s-master ~]$ cat nginx.yaml

apiVersion: v1
kind: Pod
metadata:
  name: two-containers
spec:
  volumes:
  - name: shared-data
    emptyDir: {}
  containers:
  - name: nginx-container
    image: nginx
    volumeMounts:
    - name: shared-data
      mountPath: var/log/nginx
  - name: log-container
    image: centos
    command: ["/bin/sh"]
    args: ["-c", "while true; do ls log; sleep 5;done"]
    volumeMounts:
    - name: shared-data
      mountPath: log
```

```bash
k logs two-containers -c log-container

access.log
error.log
```

## 10. Ingress 생성

문제에서 요구하는 Ingress를 생성해야 한다. Ingress는 L7 스위치 역할을 논리적으로 수행해 클러스터로 접근하는 URL 별로 다른 서비스에 트래픽을 분산한다. 

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: minimal-ingress
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  rules:
  - http:
      paths:
      - path: {문제에서주어지는경로}
        pathType: Prefix
        backend:
          service:
            name: {문제에서주어지는서비스명}
            port:
              number: {문제에서주어지는포트}
```

## 11. Network Policy 생성

`Network Policy`를 사용하면 클러스터 내 네트워크 트래픽을 제한할 수 있다. 문제의 경우 특정 Namespace(mynx)의 특정 Port(80)에서 Pod(mypod)에 오는 Ingress 트래픽을 허용해야 한다.

주의할 점은 Pod & Namespace에 `Label`을 신경써야 한다.

```bash
# 특정 Pod에 label 적용
k label pod mypod role=app

# 특정 Namespace에 label 적용
k label ns mynx node=accept
```

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: test-network-policy
  namespace: default
spec:
  podSelector:
    matchLabels:
      role: app  # <- 목표 Pod의 Label과 동일
  policyTypes:
  - Ingress
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          node: accept  # <- 목표 Namespace의 Label과 동일 
    ports:
    - protocol: TCP
      port: 80
```
