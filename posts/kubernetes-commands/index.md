# Kubernetes Commands


# Introduction

자주 사용하고 중요한 Kubectl commands들을 정리.

---

# Kubernetes Architecture Hierarchy

**Deployment >> Replica Set >> Pod >> Container >> Image**

--- 

## Node

### Q: How many nodes are part of the cluster?

```bash
controlplane ~ ➜  kubectl get nodes

NAME           STATUS   ROLES                  AGE   VERSION
controlplane   Ready    control-plane,master   13m   v1.29.0+k3s1
```

> A: 1

### Q. What is the version of Kubernetes running on the nodes ?

```bash
controlplane ~ ➜  kubectl get nodes

NAME           STATUS   ROLES                  AGE   VERSION
controlplane   Ready    control-plane,master   13m   v1.29.0+k3s1
```

> A. v1.29.0+k3s1

### Q. What is the flavor and version of Operating System on which the Kubernetes nodes are running?

```bash
controlplane ~ ➜  kubectl get nodes -o wide

NAME           STATUS   ROLES                  AGE   VERSION        INTERNAL-IP   EXTERNAL-IP   OS-IMAGE             KERNEL-VERSION   CONTAINER-RUNTIME
controlplane   Ready    control-plane,master   16m   v1.29.0+k3s1   192.7.190.6   <none>        Alpine Linux v3.16   5.4.0-1106-gcp   containerd://1.7.11-k3s2
```

> A. Alpine Linux v3.16

## Pods

### Q. How many pods exist on the system? In the current(default) namespace.

```bash
controlplane ~ ✖ kubectl get pods

NAME            READY   STATUS    RESTARTS   AGE
nginx           1/1     Running   0          40s
newpods-dn5jz   1/1     Running   0          22s
newpods-bj2zg   1/1     Running   0          22s
newpods-m9j8x   1/1     Running   0          22s
```

> A. 4

### Q. Create a new pod with the nginx image.

```bash
controlplane ~ ✖ kubectl run nginx --image=nginx
pod/nginx created
```

### Q. What is the image used to create the new pods? You must look at one of the new pods in detail to figure this out.

```bash
controlplane ~ ➜  kubectl get pods
NAME            READY   STATUS    RESTARTS   AGE
nginx           1/1     Running   0          4m23s
newpods-dn5jz   1/1     Running   0          4m5s
newpods-bj2zg   1/1     Running   0          4m5s
newpods-m9j8x   1/1     Running   0          4m5s

controlplane ~ ➜  kubectl describe pod newpods-dn5jz 
Name:             newpods-dn5jz
Namespace:        default
Priority:         0
Service Account:  default
Node:             controlplane/192.168.87.216
Start Time:       Tue, 11 Jun 2024 04:58:01 +0000
Labels:           tier=busybox
Annotations:      <none>
Status:           Running
IP:               10.42.0.11
IPs:
  IP:           10.42.0.11
Controlled By:  ReplicaSet/newpods
Containers:
  busybox:
    Container ID:  containerd://9e6ef1782fef94a200940b9baf69d28fae786a3931ea874987ee90697d20fb29
    Image:         busybox
    Image ID:      docker.io/library/busybox@sha256:9ae97d36d26566ff84e8893c64a6dc4fe8ca6d1144bf5b87b2b85a32def253c7
    Port:          <none>
    Host Port:     <none>
    Command:
      sleep
      1000
    State:          Running
      Started:      Tue, 11 Jun 2024 04:58:02 +0000
    Ready:          True
    Restart Count:  0
    Environment:    <none>
    Mounts:
      /var/run/secrets/kubernetes.io/serviceaccount from kube-api-access-sw7br (ro)
Conditions:
  Type                        Status
  PodReadyToStartContainers   True 
  Initialized                 True 
  Ready                       True 
  ContainersReady             True 
  PodScheduled                True 
Volumes:
  kube-api-access-sw7br:
    Type:                    Projected (a volume that contains injected data from multiple sources)
    TokenExpirationSeconds:  3607
    ConfigMapName:           kube-root-ca.crt
    ConfigMapOptional:       <nil>
    DownwardAPI:             true
QoS Class:                   BestEffort
Node-Selectors:              <none>
Tolerations:                 node.kubernetes.io/not-ready:NoExecute op=Exists for 300s
                             node.kubernetes.io/unreachable:NoExecute op=Exists for 300s
Events:
  Type    Reason     Age    From               Message
  ----    ------     ----   ----               -------
  Normal  Scheduled  4m28s  default-scheduler  Successfully assigned default/newpods-dn5jz to controlplane
  Normal  Pulling    4m28s  kubelet            Pulling image "busybox"
  Normal  Pulled     4m27s  kubelet            Successfully pulled image "busybox" in 302ms (302ms including waiting)
  Normal  Created    4m27s  kubelet            Created container busybox
  Normal  Started    4m27s  kubelet            Started container busybox
```

> A. BUSYBOX

### Q. Which nodes are these pods placed on? You must look at all the pods in detail to figure this out.

```bash
controlplane ~ ➜  kubectl get pods
NAME            READY   STATUS    RESTARTS   AGE
nginx           1/1     Running   0          4m23s
newpods-dn5jz   1/1     Running   0          4m5s
newpods-bj2zg   1/1     Running   0          4m5s
newpods-m9j8x   1/1     Running   0          4m5s

controlplane ~ ➜  kubectl describe pod newpods-dn5jz 
Name:             newpods-dn5jz
Namespace:        default
Priority:         0
Service Account:  default
Node:             controlplane/192.168.87.216
Start Time:       Tue, 11 Jun 2024 04:58:01 +0000
Labels:           tier=busybox
Annotations:      <none>
Status:           Running
IP:               10.42.0.11
IPs:
  IP:           10.42.0.11
Controlled By:  ReplicaSet/newpods
Containers:
  busybox:
    Container ID:  containerd://9e6ef1782fef94a200940b9baf69d28fae786a3931ea874987ee90697d20fb29
    Image:         busybox
    Image ID:      docker.io/library/busybox@sha256:9ae97d36d26566ff84e8893c64a6dc4fe8ca6d1144bf5b87b2b85a32def253c7
    Port:          <none>
    Host Port:     <none>
    Command:
      sleep
      1000
    State:          Running
      Started:      Tue, 11 Jun 2024 04:58:02 +0000
    Ready:          True
    Restart Count:  0
    Environment:    <none>
    Mounts:
      /var/run/secrets/kubernetes.io/serviceaccount from kube-api-access-sw7br (ro)
Conditions:
  Type                        Status
  PodReadyToStartContainers   True 
  Initialized                 True 
  Ready                       True 
  ContainersReady             True 
  PodScheduled                True 
Volumes:
  kube-api-access-sw7br:
    Type:                    Projected (a volume that contains injected data from multiple sources)
    TokenExpirationSeconds:  3607
    ConfigMapName:           kube-root-ca.crt
    ConfigMapOptional:       <nil>
    DownwardAPI:             true
QoS Class:                   BestEffort
Node-Selectors:              <none>
Tolerations:                 node.kubernetes.io/not-ready:NoExecute op=Exists for 300s
                             node.kubernetes.io/unreachable:NoExecute op=Exists for 300s
Events:
  Type    Reason     Age    From               Message
  ----    ------     ----   ----               -------
  Normal  Scheduled  4m28s  default-scheduler  Successfully assigned default/newpods-dn5jz to controlplane
  Normal  Pulling    4m28s  kubelet            Pulling image "busybox"
  Normal  Pulled     4m27s  kubelet            Successfully pulled image "busybox" in 302ms (302ms including waiting)
  Normal  Created    4m27s  kubelet            Created container busybox
  Normal  Started    4m27s  kubelet            Started container busybox
```

> A. controlplane

### Q. How many containers are part of the pod webapp? Note: We just created a new POD. Ignore the state of the POD for now.

```bash
controlplane ~ ➜  kubectl get pods
NAME            READY   STATUS         RESTARTS   AGE
nginx           1/1     Running        0          7m45s
newpods-dn5jz   1/1     Running        0          7m27s
newpods-bj2zg   1/1     Running        0          7m27s
newpods-m9j8x   1/1     Running        0          7m27s
webapp          1/2     ErrImagePull   0          66s

controlplane ~ ➜  kubectl describe pods webapp 
Name:             webapp
Namespace:        default
Priority:         0
Service Account:  default
Node:             controlplane/192.168.87.216
Start Time:       Tue, 11 Jun 2024 05:04:22 +0000
Labels:           <none>
Annotations:      <none>
Status:           Pending
IP:               10.42.0.13
IPs:
  IP:  10.42.0.13
Containers:
  nginx:
    Container ID:   containerd://eaf13989492da754c144ce4d611588c1abc79933e9ec9fcb7a03ee345c05dfff
    Image:          nginx
    Image ID:       docker.io/library/nginx@sha256:0f04e4f646a3f14bf31d8bc8d885b6c951fdcf42589d06845f64d18aec6a3c4d
    Port:           <none>
    Host Port:      <none>
    State:          Running
      Started:      Tue, 11 Jun 2024 05:04:24 +0000
    Ready:          True
    Restart Count:  0
    Environment:    <none>
    Mounts:
      /var/run/secrets/kubernetes.io/serviceaccount from kube-api-access-f4bd8 (ro)
  agentx:
    Container ID:   
    Image:          agentx
    Image ID:       
    Port:           <none>
    Host Port:      <none>
    State:          Waiting
      Reason:       ImagePullBackOff
    Ready:          False
    Restart Count:  0
    Environment:    <none>
    Mounts:
      /var/run/secrets/kubernetes.io/serviceaccount from kube-api-access-f4bd8 (ro)
Conditions:
  Type                        Status
  PodReadyToStartContainers   True 
  Initialized                 True 
  Ready                       False 
  ContainersReady             False 
  PodScheduled                True 
Volumes:
  kube-api-access-f4bd8:
    Type:                    Projected (a volume that contains injected data from multiple sources)
    TokenExpirationSeconds:  3607
    ConfigMapName:           kube-root-ca.crt
    ConfigMapOptional:       <nil>
    DownwardAPI:             true
QoS Class:                   BestEffort
Node-Selectors:              <none>
Tolerations:                 node.kubernetes.io/not-ready:NoExecute op=Exists for 300s
                             node.kubernetes.io/unreachable:NoExecute op=Exists for 300s
Events:
  Type     Reason     Age                From               Message
  ----     ------     ----               ----               -------
  Normal   Scheduled  81s                default-scheduler  Successfully assigned default/webapp to controlplane
  Normal   Pulling    80s                kubelet            Pulling image "nginx"
  Normal   Pulled     80s                kubelet            Successfully pulled image "nginx" in 532ms (532ms including waiting)
  Normal   Created    80s                kubelet            Created container nginx
  Normal   Started    79s                kubelet            Started container nginx
  Normal   Pulling    36s (x3 over 79s)  kubelet            Pulling image "agentx"
  Warning  Failed     35s (x3 over 79s)  kubelet            Failed to pull image "agentx": failed to pull and unpack image "docker.io/library/agentx:latest": failed to resolve reference "docker.io/library/agentx:latest": pull access denied, repository does not exist or may require authorization: server message: insufficient_scope: authorization failed
  Warning  Failed     35s (x3 over 79s)  kubelet            Error: ErrImagePull
  Normal   BackOff    11s (x5 over 79s)  kubelet            Back-off pulling image "agentx"
  Warning  Failed     11s (x5 over 79s)  kubelet            Error: ImagePullBackOff
```

> A. 2

### Q. What images are used in the new webapp pod? You must look at all the pods in detail to figure this out.

```bash
controlplane ~ ➜  kubectl get pods
NAME            READY   STATUS         RESTARTS   AGE
nginx           1/1     Running        0          7m45s
newpods-dn5jz   1/1     Running        0          7m27s
newpods-bj2zg   1/1     Running        0          7m27s
newpods-m9j8x   1/1     Running        0          7m27s
webapp          1/2     ErrImagePull   0          66s

controlplane ~ ➜  kubectl describe pods webapp 
Name:             webapp
Namespace:        default
Priority:         0
Service Account:  default
Node:             controlplane/192.168.87.216
Start Time:       Tue, 11 Jun 2024 05:04:22 +0000
Labels:           <none>
Annotations:      <none>
Status:           Pending
IP:               10.42.0.13
IPs:
  IP:  10.42.0.13
Containers:
  nginx:
    Container ID:   containerd://eaf13989492da754c144ce4d611588c1abc79933e9ec9fcb7a03ee345c05dfff
    Image:          nginx
    Image ID:       docker.io/library/nginx@sha256:0f04e4f646a3f14bf31d8bc8d885b6c951fdcf42589d06845f64d18aec6a3c4d
    Port:           <none>
    Host Port:      <none>
    State:          Running
      Started:      Tue, 11 Jun 2024 05:04:24 +0000
    Ready:          True
    Restart Count:  0
    Environment:    <none>
    Mounts:
      /var/run/secrets/kubernetes.io/serviceaccount from kube-api-access-f4bd8 (ro)
  agentx:
    Container ID:   
    Image:          agentx
    Image ID:       
    Port:           <none>
    Host Port:      <none>
    State:          Waiting
      Reason:       ImagePullBackOff
    Ready:          False
    Restart Count:  0
    Environment:    <none>
    Mounts:
      /var/run/secrets/kubernetes.io/serviceaccount from kube-api-access-f4bd8 (ro)
Conditions:
  Type                        Status
  PodReadyToStartContainers   True 
  Initialized                 True 
  Ready                       False 
  ContainersReady             False 
  PodScheduled                True 
Volumes:
  kube-api-access-f4bd8:
    Type:                    Projected (a volume that contains injected data from multiple sources)
    TokenExpirationSeconds:  3607
    ConfigMapName:           kube-root-ca.crt
    ConfigMapOptional:       <nil>
    DownwardAPI:             true
QoS Class:                   BestEffort
Node-Selectors:              <none>
Tolerations:                 node.kubernetes.io/not-ready:NoExecute op=Exists for 300s
                             node.kubernetes.io/unreachable:NoExecute op=Exists for 300s
Events:
  Type     Reason     Age                From               Message
  ----     ------     ----               ----               -------
  Normal   Scheduled  81s                default-scheduler  Successfully assigned default/webapp to controlplane
  Normal   Pulling    80s                kubelet            Pulling image "nginx"
  Normal   Pulled     80s                kubelet            Successfully pulled image "nginx" in 532ms (532ms including waiting)
  Normal   Created    80s                kubelet            Created container nginx
  Normal   Started    79s                kubelet            Started container nginx
  Normal   Pulling    36s (x3 over 79s)  kubelet            Pulling image "agentx"
  Warning  Failed     35s (x3 over 79s)  kubelet            Failed to pull image "agentx": failed to pull and unpack image "docker.io/library/agentx:latest": failed to resolve reference "docker.io/library/agentx:latest": pull access denied, repository does not exist or may require authorization: server message: insufficient_scope: authorization failed
  Warning  Failed     35s (x3 over 79s)  kubelet            Error: ErrImagePull
  Normal   BackOff    11s (x5 over 79s)  kubelet            Back-off pulling image "agentx"
  Warning  Failed     11s (x5 over 79s)  kubelet            Error: ImagePullBackOff
```

> A. nginx & agentx

### Q. What is the state of the container agentx in the pod webapp? Wait for it to finish the ContainerCreating state

```bash
controlplane ~ ➜  kubectl describe pods webapp 

Name:             webapp
Namespace:        default
Priority:         0
Service Account:  default
Node:             controlplane/192.168.87.216
Start Time:       Tue, 11 Jun 2024 05:04:22 +0000
Labels:           <none>
Annotations:      <none>
Status:           Pending
IP:               10.42.0.13
IPs:
  IP:  10.42.0.13
Containers:
  nginx:
    Container ID:   containerd://eaf13989492da754c144ce4d611588c1abc79933e9ec9fcb7a03ee345c05dfff
    Image:          nginx
    Image ID:       docker.io/library/nginx@sha256:0f04e4f646a3f14bf31d8bc8d885b6c951fdcf42589d06845f64d18aec6a3c4d
    Port:           <none>
    Host Port:      <none>
    State:          Running
      Started:      Tue, 11 Jun 2024 05:04:24 +0000
    Ready:          True
    Restart Count:  0
    Environment:    <none>
    Mounts:
      /var/run/secrets/kubernetes.io/serviceaccount from kube-api-access-f4bd8 (ro)
  agentx:
    Container ID:   
    Image:          agentx
    Image ID:       
    Port:           <none>
    Host Port:      <none>
    State:          Waiting
      Reason:       ErrImagePull
    Ready:          False
    Restart Count:  0
    Environment:    <none>
    Mounts:
      /var/run/secrets/kubernetes.io/serviceaccount from kube-api-access-f4bd8 (ro)
Conditions:
  Type                        Status
  PodReadyToStartContainers   True 
  Initialized                 True 
  Ready                       False 
  ContainersReady             False 
  PodScheduled                True 
Volumes:
  kube-api-access-f4bd8:
    Type:                    Projected (a volume that contains injected data from multiple sources)
    TokenExpirationSeconds:  3607
    ConfigMapName:           kube-root-ca.crt
    ConfigMapOptional:       <nil>
    DownwardAPI:             true
QoS Class:                   BestEffort
Node-Selectors:              <none>
Tolerations:                 node.kubernetes.io/not-ready:NoExecute op=Exists for 300s
                             node.kubernetes.io/unreachable:NoExecute op=Exists for 300s
Events:
  Type     Reason     Age                    From               Message
  ----     ------     ----                   ----               -------
  Normal   Scheduled  3m27s                  default-scheduler  Successfully assigned default/webapp to controlplane
  Normal   Pulling    3m26s                  kubelet            Pulling image "nginx"
  Normal   Pulled     3m26s                  kubelet            Successfully pulled image "nginx" in 532ms (532ms including waiting)
  Normal   Created    3m26s                  kubelet            Created container nginx
  Normal   Started    3m25s                  kubelet            Started container nginx
  Normal   Pulling    2m42s (x3 over 3m25s)  kubelet            Pulling image "agentx"
  Warning  Failed     2m41s (x3 over 3m25s)  kubelet            Failed to pull image "agentx": failed to pull and unpack image "docker.io/library/agentx:latest": failed to resolve reference "docker.io/library/agentx:latest": pull access denied, repository does not exist or may require authorization: server message: insufficient_scope: authorization failed
  Warning  Failed     2m41s (x3 over 3m25s)  kubelet            Error: ErrImagePull
  Normal   BackOff    2m2s (x6 over 3m25s)   kubelet            Back-off pulling image "agentx"
  Warning  Failed     2m2s (x6 over 3m25s)   kubelet            Error: ImagePullBackOff
```

> A. Error or Waiting

### Q. Why do you think the container agentx in pod webapp is in error? Try to figure it out from the events section of the pod.

```bash
controlplane ~ ➜  kubectl describe pods webapp 

Name:             webapp
Namespace:        default
Priority:         0
Service Account:  default
Node:             controlplane/192.168.87.216
Start Time:       Tue, 11 Jun 2024 05:04:22 +0000
Labels:           <none>
Annotations:      <none>
Status:           Pending
IP:               10.42.0.13
IPs:
  IP:  10.42.0.13
Containers:
  nginx:
    Container ID:   containerd://eaf13989492da754c144ce4d611588c1abc79933e9ec9fcb7a03ee345c05dfff
    Image:          nginx
    Image ID:       docker.io/library/nginx@sha256:0f04e4f646a3f14bf31d8bc8d885b6c951fdcf42589d06845f64d18aec6a3c4d
    Port:           <none>
    Host Port:      <none>
    State:          Running
      Started:      Tue, 11 Jun 2024 05:04:24 +0000
    Ready:          True
    Restart Count:  0
    Environment:    <none>
    Mounts:
      /var/run/secrets/kubernetes.io/serviceaccount from kube-api-access-f4bd8 (ro)
  agentx:
    Container ID:   
    Image:          agentx
    Image ID:       
    Port:           <none>
    Host Port:      <none>
    State:          Waiting
      Reason:       ErrImagePull
    Ready:          False
    Restart Count:  0
    Environment:    <none>
    Mounts:
      /var/run/secrets/kubernetes.io/serviceaccount from kube-api-access-f4bd8 (ro)
Conditions:
  Type                        Status
  PodReadyToStartContainers   True 
  Initialized                 True 
  Ready                       False 
  ContainersReady             False 
  PodScheduled                True 
Volumes:
  kube-api-access-f4bd8:
    Type:                    Projected (a volume that contains injected data from multiple sources)
    TokenExpirationSeconds:  3607
    ConfigMapName:           kube-root-ca.crt
    ConfigMapOptional:       <nil>
    DownwardAPI:             true
QoS Class:                   BestEffort
Node-Selectors:              <none>
Tolerations:                 node.kubernetes.io/not-ready:NoExecute op=Exists for 300s
                             node.kubernetes.io/unreachable:NoExecute op=Exists for 300s
Events:
  Type     Reason     Age                    From               Message
  ----     ------     ----                   ----               -------
  Normal   Scheduled  3m27s                  default-scheduler  Successfully assigned default/webapp to controlplane
  Normal   Pulling    3m26s                  kubelet            Pulling image "nginx"
  Normal   Pulled     3m26s                  kubelet            Successfully pulled image "nginx" in 532ms (532ms including waiting)
  Normal   Created    3m26s                  kubelet            Created container nginx
  Normal   Started    3m25s                  kubelet            Started container nginx
  Normal   Pulling    2m42s (x3 over 3m25s)  kubelet            Pulling image "agentx"
  Warning  Failed     2m41s (x3 over 3m25s)  kubelet            Failed to pull image "agentx": failed to pull and unpack image "docker.io/library/agentx:latest": failed to resolve reference "docker.io/library/agentx:latest": pull access denied, repository does not exist or may require authorization: server message: insufficient_scope: authorization failed
  Warning  Failed     2m41s (x3 over 3m25s)  kubelet            Error: ErrImagePull
  Normal   BackOff    2m2s (x6 over 3m25s)   kubelet            Back-off pulling image "agentx"
  Warning  Failed     2m2s (x6 over 3m25s)   kubelet            Error: ImagePullBackOff
```

> A. A Docker image with this name does not exist on Docker Hub

### Q. What does the READY column in the output of the kubectl get pods command indicate?

```bash
controlplane ~ ➜  kubectl get pods

NAME            READY   STATUS             RESTARTS   AGE
nginx           1/1     Running            0          13m
newpods-dn5jz   1/1     Running            0          13m
newpods-bj2zg   1/1     Running            0          13m
newpods-m9j8x   1/1     Running            0          13m
webapp          1/2     ImagePullBackOff   0          6m58s
```

> A. Running Containers in POD / Total Containers in POD

### Q. Delete the webapp Pod. Once deleted, wait for the pod to fully terminate.

```bash
controlplane ~ ➜  kubectl delete pod webapp 

pod "webapp" deleted
```

### Q. Create a new pod with the name redis and the image redis123. Use a pod-definition YAML file. And yes the image name is wrong!

```bash
controlplane ~ ➜  kubectl get pods
NAME            READY   STATUS    RESTARTS      AGE
nginx           1/1     Running   0             17m
newpods-m9j8x   1/1     Running   1 (10s ago)   16m
newpods-bj2zg   1/1     Running   1 (10s ago)   16m
newpods-dn5jz   1/1     Running   1 (10s ago)   16m

controlplane ~ ➜  kubectl run redis --image=redis123 --dry-run=client -o yaml > redis-definition.yaml

controlplane ~ ➜  ls
redis-definition.yaml  sample.yaml

controlplane ~ ➜  kubectl create -f redis-definition.yaml 
pod/redis created

controlplane ~ ➜  kubectl get pods
NAME            READY   STATUS         RESTARTS      AGE
nginx           1/1     Running        0             18m
newpods-m9j8x   1/1     Running        1 (64s ago)   17m
newpods-bj2zg   1/1     Running        1 (64s ago)   17m
newpods-dn5jz   1/1     Running        1 (64s ago)   17m
redis           0/1     ErrImagePull   0             6s
```

### Q. Now change the image on this pod to redis. Once done, the pod should be in a running state.

```bash
controlplane ~ ➜ kubectl edit pod redis

apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  labels:
    run: redis
  name: redis
spec:
  containers:
  - image: redis
    name: redis
    resources: {}
  dnsPolicy: ClusterFirst
  restartPolicy: Always
status: {}
~                                                                                       ~                     
~                                                                
~                                                                
~                                                                
:wq

controlplane ~ ➜ kubectl apply -f redis-definition.yaml

controlplane ~ ➜ kubectl get pods
NAME            READY   STATUS    RESTARTS        AGE
nginx           1/1     Running   0               20m
newpods-m9j8x   1/1     Running   1 (3m58s ago)   20m
newpods-bj2zg   1/1     Running   1 (3m58s ago)   20m
newpods-dn5jz   1/1     Running   1 (3m58s ago)   20m
redis           1/1     Running   0               3m
```

## Replica Set

### Q. How many replica sets?

```bash
controlplane ~ ➜  kubectl get rs
NAME              DESIRED   CURRENT   READY   AGE
new-replica-set   4         4         0       5s
```

> A. 1

### Q. How many PODs are DESIRED in the new-replica-set?

```bash
controlplane ~ ➜  kubectl get rs
NAME              DESIRED   CURRENT   READY   AGE
new-replica-set   4         4         0       5s
```

> A. 4

### Q. What is the image used to create the pods in the new-replica-set?

```bash
controlplane ~ ➜  kubectl describe rs new-replica-set 
Name:         new-replica-set
Namespace:    default
Selector:     name=busybox-pod
Labels:       <none>
Annotations:  <none>
Replicas:     4 current / 4 desired
Pods Status:  0 Running / 4 Waiting / 0 Succeeded / 0 Failed
Pod Template:
  Labels:  name=busybox-pod
  Containers:
   busybox-container:
    Image:      busybox777
    Port:       <none>
    Host Port:  <none>
    Command:
      sh
      -c
      echo Hello Kubernetes! && sleep 3600
    Environment:  <none>
    Mounts:       <none>
  Volumes:        <none>
Events:
  Type    Reason            Age    From                   Message
  ----    ------            ----   ----                   -------
  Normal  SuccessfulCreate  2m41s  replicaset-controller  Created pod: new-replica-set-4jm4s
  Normal  SuccessfulCreate  2m41s  replicaset-controller  Created pod: new-replica-set-8pj5l
  Normal  SuccessfulCreate  2m41s  replicaset-controller  Created pod: new-replica-set-7gbl5
  Normal  SuccessfulCreate  2m41s  replicaset-controller  Created pod: new-replica-set-2jcnr
```

> A. busybox777

### Q. How many PODs are READY in the new-replica-set?

```bash
controlplane ~ ➜  kubectl get rs
NAME              DESIRED   CURRENT   READY   AGE
new-replica-set   4         4         0       4m30s
```

> A. 0

### Q. Why do you think the PODs are not ready?

```bash
controlplane ~ ➜  kubectl get rs
NAME              DESIRED   CURRENT   READY   AGE
new-replica-set   4         4         0       4m30s
```

> A. The image BUSYBOX777 does not exist

### Q. Delete any one of the 4 PODs

```bash
controlplane ~ ➜  kubectl get rs
NAME              DESIRED   CURRENT   READY   AGE
new-replica-set   4         4         0       4m30s

controlplane ~ ➜  kubectl get pods
NAME                    READY   STATUS             RESTARTS   AGE
new-replica-set-7gbl5   0/1     ImagePullBackOff   0          6m
new-replica-set-4jm4s   0/1     ErrImagePull       0          6m
new-replica-set-8pj5l   0/1     ErrImagePull       0          6m
new-replica-set-2jcnr   0/1     ErrImagePull       0          6m

controlplane ~ ➜  kubectl delete pod new-replica-set-7gbl5 
pod "new-replica-set-7gbl5" deleted

controlplane ~ ➜  kubectl get pods
NAME                    READY   STATUS             RESTARTS   AGE
new-replica-set-4jm4s   0/1     ImagePullBackOff   0          6m39s
new-replica-set-8pj5l   0/1     ImagePullBackOff   0          6m39s
new-replica-set-2jcnr   0/1     ImagePullBackOff   0          6m39s
new-replica-set-f2p2k   0/1     ImagePullBackOff   0          27s
```

### Q. Why are there still 4 PODs, even after you deleted one?

> A. ReplicaSet ensures that desired number of PODs always run

### Q. Create a ReplicaSet using the replicaset-definition-1.yaml file located at /root/. There is an issue with the file, so try to fix it.

```bash
controlplane ~ ➜  vim replicaset-definition-1.yaml

apiVersion: v1 (x) -> apps/v1
kind: ReplicaSet
metadata:
  name: replicaset-1
spec:
  replicas: 2
  selector:
    matchLabels:
      tier: frontend
  template:
    metadata:
      labels:
        tier: frontend
    spec:
      containers:
      - name: nginx
        image: nginx
~
~
~
~
:wq

controlplane ~ ➜  kubectl create -f replicaset-definition-1.yaml 
replicaset.apps/replicaset-1 created
```

### Q. Fix the issue in the replicaset-definition-2.yaml file and create a ReplicaSet using it. This file is located at /root/.

```bash
controlplane ~ ➜  vim replicaset-definition-2.yaml

apiVersion: apps/v1
kind: ReplicaSet
metadata:
  name: replicaset-2
spec:
  replicas: 2
  selector:
    matchLabels:
      tier: nginx
  template:
    metadata:
      labels:
        tier: nginx
    spec:
      containers:
      - name: nginx
        image: nginx
~
~
~                                                           
:wq

controlplane ~ ➜  kubectl create -f replicaset-definition-2.yaml 
replicaset.apps/replicaset-2 created
```

### Q. Delete the two newly created ReplicaSets - replicaset-1 and replicaset-2

```bash
controlplane ~ ✖ kubectl get rs
NAME              DESIRED   CURRENT   READY   AGE
new-replica-set   4         4         0       22m
replicaset-1      2         2         2       11m
replicaset-2      2         2         2       41s

controlplane ~ ➜  kubectl delete rs replicaset-1 
replicaset.apps "replicaset-1" deleted

controlplane ~ ➜  kubectl delete rs replicaset-2 
replicaset.apps "replicaset-2" deleted

controlplane ~ ➜  kubectl get rs
NAME              DESIRED   CURRENT   READY   AGE
new-replica-set   4         4         0       23m
```

### Q. Fix the original replica set new-replica-set to use the correct busybox image. Either delete and recreate the ReplicaSet or Update the existing ReplicaSet and then delete all PODs, so new ones with the correct image will be created.

```bash
controlplane ~ ➜  kubectl edit rs new-replica-set 

apiVersion: apps/v1
kind: ReplicaSet
metadata:
  creationTimestamp: "2024-06-11T05:57:22Z"
  generation: 1
  name: new-replica-set
  namespace: default
  resourceVersion: "1130"
  uid: 1e1c0ce5-d403-4bae-b53f-3b18ab954e2a
spec:
  replicas: 4
  selector:
    matchLabels:
      name: busybox-pod
  template:
    metadata:
      creationTimestamp: null
      labels:
        name: busybox-pod
    spec:
      containers:
      - command:
        - sh
        - -c
        - echo Hello Kubernetes! && sleep 3600
        image: busybox
        imagePullPolicy: Always
        name: busybox-container
        resources: {}
        terminationMessagePath: /dev/termination-log
        terminationMessagePolicy: File
      dnsPolicy: ClusterFirst
      restartPolicy: Always
      schedulerName: default-scheduler
      securityContext: {}
      terminationGracePeriodSeconds: 30
status:
  fullyLabeledReplicas: 4
  observedGeneration: 1
  replicas: 4
~
~
~
~
:wq

replicaset.apps/new-replica-set edited

controlplane ~ ➜  kubectl get pods
NAME                    READY   STATUS    RESTARTS   AGE
new-replica-set-4hj6z   1/1     Running   0          5s
new-replica-set-2fjtt   1/1     Running   0          5s
new-replica-set-5h2xp   1/1     Running   0          5s
new-replica-set-rvglt   1/1     Running   0          5s

controlplane ~ ➜  kubectl delete pod new-replica-set-4hj6z

controlplane ~ ➜  kubectl get pods
NAME                    READY   STATUS    RESTARTS   AGE
new-replica-set-7fsds   1/1     Running   0          5s
new-replica-set-2fjtt   1/1     Running   0          5s
new-replica-set-5h2xp   1/1     Running   0          5s
new-replica-set-rvglt   1/1     Running   0          5s
```

### Q. Scale the ReplicaSet to 5 PODs. Use kubectl scale command or edit the replicaset using kubectl edit replicaset.

```bash
controlplane ~ ➜  kubectl edit rs new-replica-set 

apiVersion: apps/v1
kind: ReplicaSet
metadata:
  creationTimestamp: "2024-06-11T05:57:22Z"
  generation: 1
  name: new-replica-set
  namespace: default
  resourceVersion: "1130"
  uid: 1e1c0ce5-d403-4bae-b53f-3b18ab954e2a
spec:
  replicas: 5
  selector:
    matchLabels:
      name: busybox-pod
  template:
    metadata:
      creationTimestamp: null
      labels:
        name: busybox-pod
    spec:
      containers:
      - command:
        - sh
        - -c
        - echo Hello Kubernetes! && sleep 3600
        image: busybox
        imagePullPolicy: Always
        name: busybox-container
        resources: {}
        terminationMessagePath: /dev/termination-log
        terminationMessagePolicy: File
      dnsPolicy: ClusterFirst
      restartPolicy: Always
      schedulerName: default-scheduler
      securityContext: {}
      terminationGracePeriodSeconds: 30
status:
  fullyLabeledReplicas: 4
  observedGeneration: 1
  replicas: 4
~
~
~
~
:wq

replicaset.apps/new-replica-set edited

controlplane ~ ➜  kubectl get rs
NAME              DESIRED   CURRENT   READY   AGE
new-replica-set   5         5         5       2m57s
```

### Q. Now scale the ReplicaSet down to 2 PODs. Use the kubectl scale command or edit the replicaset using kubectl edit replicaset.

```bash
controlplane ~ ➜  kubectl edit rs new-replica-set 

apiVersion: apps/v1
kind: ReplicaSet
metadata:
  creationTimestamp: "2024-06-11T05:57:22Z"
  generation: 1
  name: new-replica-set
  namespace: default
  resourceVersion: "1130"
  uid: 1e1c0ce5-d403-4bae-b53f-3b18ab954e2a
spec:
  replicas: 2
  selector:
    matchLabels:
      name: busybox-pod
  template:
    metadata:
      creationTimestamp: null
      labels:
        name: busybox-pod
    spec:
      containers:
      - command:
        - sh
        - -c
        - echo Hello Kubernetes! && sleep 3600
        image: busybox
        imagePullPolicy: Always
        name: busybox-container
        resources: {}
        terminationMessagePath: /dev/termination-log
        terminationMessagePolicy: File
      dnsPolicy: ClusterFirst
      restartPolicy: Always
      schedulerName: default-scheduler
      securityContext: {}
      terminationGracePeriodSeconds: 30
status:
  fullyLabeledReplicas: 4
  observedGeneration: 1
  replicas: 4
~
~
~
~
:wq

replicaset.apps/new-replica-set edited

controlplane ~ ➜  kubectl get rs
NAME              DESIRED   CURRENT   READY   AGE
new-replica-set   2         2         2       5m17s
```

## Deployment

### Q. How many Deployments exist on the system? 

```bash
controlplane ~ ➜  kubectl get deployments
NAME                  READY   UP-TO-DATE   AVAILABLE   AGE
frontend-deployment   0/4     4            0           9s
```

> A. 1

### Q. How many ReplicaSets exist on the system now?

```bash
controlplane ~ ➜  kubectl get rs
NAME                             DESIRED   CURRENT   READY   AGE
frontend-deployment-7b9984b987   4         4         0       55s
```

> A. 1

### Q. How many PODs exist on the system?

```bash
controlplane ~ ➜  kubectl get pods
NAME                                   READY   STATUS             RESTARTS   AGE
frontend-deployment-7b9984b987-v58w9   0/1     ImagePullBackOff   0          96s
frontend-deployment-7b9984b987-jrmbt   0/1     ImagePullBackOff   0          96s
frontend-deployment-7b9984b987-hpxnn   0/1     ImagePullBackOff   0          96s
frontend-deployment-7b9984b987-rth5d   0/1     ImagePullBackOff   0          96s
```

> A. 4

### Q. What is the image used to create the pods in the new deployment?

```bash
controlplane ~ ➜  kubectl describe deployment frontend-deployment 
Name:                   frontend-deployment
Namespace:              default
CreationTimestamp:      Tue, 11 Jun 2024 06:55:55 +0000
Labels:                 <none>
Annotations:            deployment.kubernetes.io/revision: 1
Selector:               name=busybox-pod
Replicas:               4 desired | 4 updated | 4 total | 0 available | 4 unavailable
StrategyType:           RollingUpdate
MinReadySeconds:        0
RollingUpdateStrategy:  25% max unavailable, 25% max surge
Pod Template:
  Labels:  name=busybox-pod
  Containers:
   busybox-container:
    Image:      busybox888
    Port:       <none>
    Host Port:  <none>
    Command:
      sh
      -c
      echo Hello Kubernetes! && sleep 3600
    Environment:  <none>
    Mounts:       <none>
  Volumes:        <none>
Conditions:
  Type           Status  Reason
  ----           ------  ------
  Available      False   MinimumReplicasUnavailable
  Progressing    True    ReplicaSetUpdated
OldReplicaSets:  <none>
NewReplicaSet:   frontend-deployment-7b9984b987 (4/4 replicas created)
Events:
  Type    Reason             Age    From                   Message
  ----    ------             ----   ----                   -------
  Normal  ScalingReplicaSet  2m56s  deployment-controller  Scaled up replica set frontend-deployment-7b9984b987 to 4
```

> A. BUSYBOX888

### Q. Create a new Deployment using the deployment-definition-1.yaml file located at /root/. There is an issue with the file, so try to fix it.

```bash
controlplane ~ ➜  vim deployment-definition-1.yaml 
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: deployment-1
spec:
  replicas: 2
  selector:
    matchLabels:
      name: busybox-pod
  template:
    metadata:
      labels:
        name: busybox-pod
    spec:
      containers:
      - name: busybox-container
        image: busybox888
        command:
        - sh
        - "-c"
        - echo Hello Kubernetes! && sleep 3600
~
~
~
~
:wq

controlplane ~ ➜  kubectl create -f deployment-definition-1.yaml 
deployment.apps/deployment-1 created
```

### Q. Create a new Deployment with the below attributes using your own deployment definition file.


Name: httpd-frontend;
Replicas: 3;
Image: httpd:2.4-alpine

```bash
controlplane ~ ➜  vim deployment-definition-httpd.yaml

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: httpd-frontend
spec:
  replicas: 3
  selector:
    matchLabels:
      name: httpd-frontend
  template:
    metadata:
      labels:
        name: httpd-frontend
    spec:
      containers:
      - name: httpd-frontend
        image: httpd:2.4-alpine
~
~
~
~
:wq

controlplane ~ ➜  kubectl create -f deployment-definition-httpd.yaml 
deployment.apps/httpd-frontend created

controlplane ~ ➜  kubectl get deployments
NAME                  READY   UP-TO-DATE   AVAILABLE   AGE
frontend-deployment   0/4     4            0           9m23s
deployment-1          0/2     2            0           3m15s
httpd-frontend        3/3     3            3           17s
```

## Rolling Updates and Rollback

### Q. Inspect the deployment and identify the current strategy

```bash
controlplane ~ ➜  kubectl describe deployment
Name:                   frontend
Namespace:              default
CreationTimestamp:      Tue, 11 Jun 2024 07:17:28 +0000
Labels:                 <none>
Annotations:            deployment.kubernetes.io/revision: 1
Selector:               name=webapp
Replicas:               4 desired | 4 updated | 4 total | 4 available | 0 unavailable
StrategyType:           RollingUpdate
MinReadySeconds:        20
RollingUpdateStrategy:  25% max unavailable, 25% max surge
Pod Template:
  Labels:  name=webapp
  Containers:
   simple-webapp:
    Image:        kodekloud/webapp-color:v1
    Port:         8080/TCP
    Host Port:    0/TCP
    Environment:  <none>
    Mounts:       <none>
  Volumes:        <none>
Conditions:
  Type           Status  Reason
  ----           ------  ------
  Available      True    MinimumReplicasAvailable
  Progressing    True    NewReplicaSetAvailable
OldReplicaSets:  <none>
NewReplicaSet:   frontend-685dfcc44 (4/4 replicas created)
Events:
  Type    Reason             Age   From                   Message
  ----    ------             ----  ----                   -------
  Normal  ScalingReplicaSet  101s  deployment-controller  Scaled up replica set frontend-685dfcc44 to 4
```

> A. RollingUpdate

### Q. If you were to upgrade the application now what would happen?

> A. PODs are upgraded few at a time

### Q. Let us try that. Upgrade the application by setting the image on the deployment to kodekloud/webapp-color:v2. Do not delete and re-create the deployment. Only set the new image name for the existing deployment.

```bash
controlplane ~ ➜  kubectl edit deployment frontend 

# Please edit the object below. Lines beginning with a '#' will b
e ignored,
# and an empty file will abort the edit. If an error occurs while
 saving this file will be
# reopened with the relevant failures.
#
apiVersion: apps/v1
kind: Deployment
metadata:
  annotations:
    deployment.kubernetes.io/revision: "1"
  creationTimestamp: "2024-06-11T07:17:28Z"
  generation: 1
  name: frontend
  namespace: default
  resourceVersion: "819"
  uid: d8caa22d-e29d-4c2f-b896-9436b3245d0a
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

:wq

deployment.apps/frontend edited
```

### Q. Up to how many PODs can be down for upgrade at a time Consider the current strategy settings and number of PODs - 4

```bash
controlplane ~ ➜  kubectl describe deployment
Name:                   frontend
Namespace:              default
CreationTimestamp:      Tue, 11 Jun 2024 07:17:28 +0000
Labels:                 <none>
Annotations:            deployment.kubernetes.io/revision: 1
Selector:               name=webapp
Replicas:               4 desired | 4 updated | 4 total | 4 available | 0 unavailable
StrategyType:           RollingUpdate
MinReadySeconds:        20
RollingUpdateStrategy:  25% max unavailable, 25% max surge
Pod Template:
  Labels:  name=webapp
  Containers:
   simple-webapp:
    Image:        kodekloud/webapp-color:v1
    Port:         8080/TCP
    Host Port:    0/TCP
    Environment:  <none>
    Mounts:       <none>
  Volumes:        <none>
Conditions:
  Type           Status  Reason
  ----           ------  ------
  Available      True    MinimumReplicasAvailable
  Progressing    True    NewReplicaSetAvailable
OldReplicaSets:  <none>
NewReplicaSet:   frontend-685dfcc44 (4/4 replicas created)
Events:
  Type    Reason             Age   From                   Message
  ----    ------             ----  ----                   -------
  Normal  ScalingReplicaSet  101s  deployment-controller  Scaled up replica set frontend-685dfcc44 to 4
```

> A. Look at the Max Unavailable value under RollingUpdateStrategy in deployment details -> 총 4개의 POD 중의 25%니까 1

### Q. Change the deployment strategy to Recreate. Delete and re-create the deployment if necessary. Only update the strategy type for the existing deployment.

```bash
controlplane ~ ➜  kubectl edit deployment frontend


apiVersion: apps/v1
kind: Deployment
metadata:
  annotations:
    deployment.kubernetes.io/revision: "2"
  creationTimestamp: "2024-06-11T07:17:28Z"
  generation: 2
  name: frontend
  namespace: default
  resourceVersion: "1074"
  uid: d8caa22d-e29d-4c2f-b896-9436b3245d0a
spec:
  minReadySeconds: 20
  progressDeadlineSeconds: 600
  replicas: 4
  revisionHistoryLimit: 10
  selector:
    matchLabels:
      name: webapp
  strategy:
    type: Recreate
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
  availableReplicas: 4
:wq

deployment.apps/frontend edited
```

### Q. Upgrade the application by setting the image on the deployment to kodekloud/webapp-color:v3. 

```bash
apiVersion: apps/v1
kind: Deployment
metadata:
  annotations:
    deployment.kubernetes.io/revision: "2"
  creationTimestamp: "2024-06-11T07:17:28Z"
  generation: 3
  name: frontend
  namespace: default
  resourceVersion: "1150"
  uid: d8caa22d-e29d-4c2f-b896-9436b3245d0a
spec:
  minReadySeconds: 20
  progressDeadlineSeconds: 600
  replicas: 4
  revisionHistoryLimit: 10
  selector:
    matchLabels:
      name: webapp
  strategy:
    type: Recreate
  template:
    metadata:
      creationTimestamp: null
      labels:
        name: webapp
    spec:
      containers:
      - image: kodekloud/webapp-color:v3
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
  availableReplicas: 4
:wq

deployment.apps/frontend edited
```

