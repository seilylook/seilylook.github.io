# CKA Begin


# Lab 1

## Question

> How many nodes are part of the cluster?

## Answer

```bash
controlplane ~ ➜  kubectl get nodes
NAME           STATUS   ROLES                  AGE   VERSION
controlplane   Ready    control-plane,master   26m   v1.29.0+k3s1
```

## Question

> What is the flavor and version of Operating System on which the Kubernetes nodes are running?

## Answer

```bash
controlplane ~ ✖ kubectl get nodes -o wide

NAME           STATUS   ROLES                  AGE   VERSION        INTERNAL-IP   EXTERNAL-IP   OS-IMAGE             KERNEL-VERSION   CONTAINER-RUNTIME
controlplane   Ready    control-plane,master   30m   v1.29.0+k3s1   192.3.57.8    <none>        Alpine Linux v3.16   5.4.0-1106-gcp   containerd://1.7.11-k3s2
```

# Lab 2

## Question

> Create a new pod with the nginx image.

## Answer

```bash
controlplane ~ ➜  kubectl run nginx --image=nginx

pod/nginx created
```

## Question

> What is the image used to create the new pods?

## Answer

```bash
controlplane ~ ✖ kubectl describe pods

...

Name:             newpods-clqjs
Namespace:        default
Priority:         0
Service Account:  default
Node:             controlplane/192.3.111.8
Start Time:       Fri, 10 May 2024 02:00:24 +0000
Labels:           tier=busybox
Annotations:      <none>
Status:           Running
IP:               10.42.0.10
IPs:
  IP:           10.42.0.10
Controlled By:  ReplicaSet/newpods
Containers:
  busybox:
    Container ID:  containerd://eed5a3854b99372e03bdac3b2459aa99efdc4488aff817ad3b6049d16cd9a9d8
    Image:         busybox

...

```

## Question

> Which nodes are these pods placed on?

## Answer

```bash
controlplane ~ ➜  kubectl describe pods

...

Name:             nginx
Namespace:        default
Priority:         0
Service Account:  default
Node:             controlplane/192.3.111.8

...
```

## Question

> How many containers are part of the pod webapp?

## Answer

```bash
controlplane ~ ✖ kubectl describe pods

...

Name:             webapp
Namespace:        default
Priority:         0
Service Account:  default
Node:             controlplane/192.3.111.8
Start Time:       Fri, 10 May 2024 02:06:08 +0000
Labels:           <none>
Annotations:      <none>
Status:           Pending
IP:               10.42.0.13
IPs:
  IP:  10.42.0.13
Containers:
  nginx:
    Container ID:   containerd://98f2483da37c1a2192f09dec87559734dcf23dbacd194d7219d53a726a6eff13
    Image:          nginx
    Image ID:       docker.io/library/nginx@sha256:32e76d4f34f80e479964a0fbd4c5b4f6967b5322c8d004e9cf0cb81c93510766
    Port:           <none>
    Host Port:      <none>
    State:          Running
      Started:      Fri, 10 May 2024 02:06:09 +0000
    Ready:          True
    Restart Count:  0
    Environment:    <none>
    Mounts:
      /var/run/secrets/kubernetes.io/serviceaccount from kube-api-access-64psz (ro)
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
      /var/run/secrets/kubernetes.io/serviceaccount from kube-api-access-64psz (ro)

...
```

## Question

> What is the state of the container agentx in the pod webapp?

## Answer

```bash
controlplane ~ ✖ kubectl describe pods

...

  Warning  Failed     3m25s (x3 over 4m10s)  kubelet            Error: ErrImagePull
  Normal   BackOff    2m47s (x5 over 4m9s)   kubelet            Back-off pulling image "agentx"
  Warning  Failed     2m47s (x5 over 4m9s)   kubelet            Error: ImagePullBackOff
  Normal   Pulling    2m33s (x4 over 4m10s)  kubelet            Pulling image "agentx"
  Warning  Failed     2m32s (x4 over 4m10s)  kubelet            Failed to pull image "agentx": failed to pull and unpack image "docker.io/library/agentx:latest": failed to resolve reference "docker.io/library/agentx:latest": pull access denied, repository does not exist or may require authorization: server message: insufficient_scope: authorization failed

...
```

## Question

> Delete the webapp Pod.

## Answer

```bash
controlplane ~ ➜  kubectl delete pod webapp

pod "webapp" deleted
```

## Question

> Create a new pod with the name redis and the image redis123.

## Answer

```bash
controlplane ~ ➜  kubectl run redis --image=redis123 --dry-run=client -o yaml > redis-definition.yaml

controlplane ~ ➜  ls
redis-definition.yaml  sample.yaml

controlplane ~ ➜  kubectl create -f redis-definition.yaml
pod/redis created

controlplane ~ ➜  kubectl get pods
NAME            READY   STATUS             RESTARTS       AGE
nginx           1/1     Running            0              20m
newpods-clqjs   1/1     Running            1 (3m7s ago)   19m
newpods-qlj8k   1/1     Running            1 (3m7s ago)   19m
newpods-k4sks   1/1     Running            1 (3m7s ago)   19m
redis           0/1     ImagePullBackOff   0              16s
```

## Question

> Now change the image on this pod to redis. Once done, the pod should be in a running state.

## Answer

```bash
# 1. vi를 사용해 직접 수정
# 2. kubectl CMD

controlplane ~ ➜  kubectl edit pod redis
pod/redis edited

controlplane ~ ➜  kubectl apply -f redis-definition.yaml
pod/redis configured
```

# Lab 3

## Question

> Scale the ReplicaSet to 5 PODs. Use kubectl scale command or edit the replicaset using kubectl edit replicaset.

## Anaswer

```bash
# modify the replicas and then save the file
controlplane ~ ➜  kubectl edit replicaset new-replica-set

controlplane ~ ➜  kubectl scale rs new-replica-set --replicas=5
```

## Question

> Now scale the ReplicaSet down to 2 PODs. Use the kubectl scale command or edit the replicaset using kubectl edit replicaset.

## Answer

```bash
controlplane ~ ➜  kubectl scale rs new-replica-set --replicas=2
replicaset.apps/new-replica-set scaled
```

