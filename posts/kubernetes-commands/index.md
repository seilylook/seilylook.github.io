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
