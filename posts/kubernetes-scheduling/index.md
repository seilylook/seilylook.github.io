# Kubernetes Scheduling


## Labels and Selectors

### Q. We have deployed a number of PODs. They are labelled with tier, env and bu. How many PODs exist in the dev environment (env)?

```bash
controlplane ~ ➜  kubectl get pods --selector env=dev
NAME          READY   STATUS    RESTARTS   AGE
app-1-5hskg   1/1     Running   0          71s
app-1-8m5gl   1/1     Running   0          71s
db-1-jfd5z    1/1     Running   0          70s
app-1-jnd7g   1/1     Running   0          71s
db-1-54kdk    1/1     Running   0          70s
db-1-xcxv7    1/1     Running   0          70s
db-1-2tffc    1/1     Running   0          70s

OR 

kubectl get pods --selector env=dev --no-headers | wc -l
```

> A. 7

### Q. How many PODs are in the finance business unit (bu)?

```bash
controlplane ~ ➜  kubectl get pod --selector bu=finance
NAME          READY   STATUS    RESTARTS   AGE
app-1-5hskg   1/1     Running   0          2m13s
app-1-8m5gl   1/1     Running   0          2m13s
db-2-mp75n    1/1     Running   0          2m12s
auth          1/1     Running   0          2m12s
app-1-jnd7g   1/1     Running   0          2m13s
app-1-zzxdf   1/1     Running   0          2m12s

OR

kubectl get pods --selector bu=finance --no-headers | wc -l
```

> A. 6

### Q. How many objects are in the prod environment including PODs, ReplicaSets and any other objects?

```bash
controlplane ~ ➜  kubectl get all --selector env=prod
NAME              READY   STATUS    RESTARTS   AGE
pod/db-2-zkq5x    1/1     Running   0          9m9s
pod/auth          1/1     Running   0          9m9s
pod/app-1-zzxdf   1/1     Running   0          9m9s
pod/app-2-cjp6w   1/1     Running   0          9m9s

NAME            TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)    AGE
service/app-1   ClusterIP   10.43.116.128   <none>        3306/TCP   9m9s

NAME                    DESIRED   CURRENT   READY   AGE
replicaset.apps/db-2    1         1         1       9m9s
replicaset.apps/app-2   1         1         1       9m9s

OR

controlplane ~ ➜  kubectl get all --selector env=prod --no-headers | wc -l
7
```

> A. 7

### Q. Identify the POD which is part of the prod environment, the finance BU and of frontend tier?

```bash
controlplane ~ ➜  kubectl get pods --selector env=prod,bu=finance,tier=frontend
ontend
NAME              READY   STATUS    RESTARTS   AGE
pod/app-1-zzxdf   1/1     Running   0          11m
```

> A. app-1-zzxdf

### Q. A ReplicaSet definition file is given replicaset-definition-1.yaml. Attempt to create the replicaset; you will encounter an issue with the file. Try to fix it.


Once you fix the issue, create the replicaset from the definition file.

```bash
controlplane ~ ➜  vim replicaset-definition-1.yaml 

---
apiVersion: apps/v1
kind: ReplicaSet
metadata:
   name: replicaset-1
spec:
   replicas: 2
   selector:
      matchLabels:
        tier: front-end
   template:
     metadata:
       labels:
        tier: nginx(X) -> front-end(O)
     spec:
       containers:
       - name: nginx
         image: nginx

controlplane ~ ➜  kubectl apply -f replicaset-definition-1.yaml 
replicaset.apps/replicaset-1 created
```

## Taints and Tolerations

### Q. Do any taints exist on node01 node?

```bash
controlplane ~ ✖ kubectl describe node node01
Name:               node01
Roles:              <none>
Labels:             beta.kubernetes.io/arch=amd64
                    beta.kubernetes.io/os=linux
                    kubernetes.io/arch=amd64
                    kubernetes.io/hostname=node01
                    kubernetes.io/os=linux
Annotations:        flannel.alpha.coreos.com/backend-data: {"VNI":1,"VtepMAC":"72:10:2d:a2:75:8d"}
                    flannel.alpha.coreos.com/backend-type: vxlan
                    flannel.alpha.coreos.com/kube-subnet-manager: true
                    flannel.alpha.coreos.com/public-ip: 192.14.218.6
                    kubeadm.alpha.kubernetes.io/cri-socket: unix:///var/run/containerd/containerd.sock
                    node.alpha.kubernetes.io/ttl: 0
                    volumes.kubernetes.io/controller-managed-attach-detach: true
CreationTimestamp:  Mon, 17 Jun 2024 08:28:32 +0000
Taints:             <none>
...
```

> A. None

### Q. Create a taint on node01 with key of spray, value of mortein and effect of NoSchedule

```bash
controlplane ~ ➜  kubectl taint nodes node01 spray=mortein:NoSchedule
node/node01 tainted

controlplane ~ ➜  kubectl describe node node01
Name:               node01
Roles:              <none>
Labels:             beta.kubernetes.io/arch=amd64
                    beta.kubernetes.io/os=linux
                    kubernetes.io/arch=amd64
                    kubernetes.io/hostname=node01
                    kubernetes.io/os=linux
Annotations:        flannel.alpha.coreos.com/backend-data: {"VNI":1,"VtepMAC":"72:10:2d:a2:75:8d"}
                    flannel.alpha.coreos.com/backend-type: vxlan
                    flannel.alpha.coreos.com/kube-subnet-manager: true
                    flannel.alpha.coreos.com/public-ip: 192.14.218.6
                    kubeadm.alpha.kubernetes.io/cri-socket: unix:///var/run/containerd/containerd.sock
                    node.alpha.kubernetes.io/ttl: 0
                    volumes.kubernetes.io/controller-managed-attach-detach: true
CreationTimestamp:  Mon, 17 Jun 2024 08:28:32 +0000
Taints:             spray=mortein:NoSchedule
...
```

### Q. Create another pod names bee with the nginx image, which has a toleration set to the taint mortein.

Image name: nginx

Key: spray

Value: mortein

Effects: NoSchedule

Status: Running

```bash
controlplane ~ ➜  vim bee-pod.yaml

apiVersion: v1
kind: Pod
metadata:
  name: bee
spec:
  containers:
    - image: nginx
      name: bee
  tolerations:
    - key: spray
      value: mortein
      effect: NoSchedule
      operator: Equal
:wq

controlplane ~ ➜  kubectl create -f bee-pod.yaml 
```

### Q. Do you see any taints on controlplane node?

```bash
controlplane ~ ➜  kubectl describe node controlplane
Name:               controlplane
Roles:              control-plane
Labels:             beta.kubernetes.io/arch=amd64
                    beta.kubernetes.io/os=linux
                    kubernetes.io/arch=amd64
                    kubernetes.io/hostname=controlplane
                    kubernetes.io/os=linux
                    node-role.kubernetes.io/control-plane=
                    node.kubernetes.io/exclude-from-external-load-balancers=
Annotations:        flannel.alpha.coreos.com/backend-data: {"VNI":1,"VtepMAC":"aa:0d:ad:10:90:1d"}
                    flannel.alpha.coreos.com/backend-type: vxlan
                    flannel.alpha.coreos.com/kube-subnet-manager: true
                    flannel.alpha.coreos.com/public-ip: 192.14.218.3
                    kubeadm.alpha.kubernetes.io/cri-socket: unix:///var/run/containerd/containerd.sock
                    node.alpha.kubernetes.io/ttl: 0
                    volumes.kubernetes.io/controller-managed-attach-detach: true
CreationTimestamp:  Mon, 17 Jun 2024 08:27:49 +0000
Taints:             node-role.kubernetes.io/control-plane:NoSchedule
...
```

### Q. Remove the taint on controlplane, which currently has the taint effect of NoSchedule.

```bash
controlplane ~ ➜  kubectl taint nodes controlplane node-role.kubernetes.io/control-plane:NoSchedule-
node/controlplane untainted

controlplane ~ ➜  kubectl describe node controlplane
Name:               controlplane
Roles:              control-plane
Labels:             beta.kubernetes.io/arch=amd64
                    beta.kubernetes.io/os=linux
                    kubernetes.io/arch=amd64
                    kubernetes.io/hostname=controlplane
                    kubernetes.io/os=linux
                    node-role.kubernetes.io/control-plane=
                    node.kubernetes.io/exclude-from-external-load-balancers=
Annotations:        flannel.alpha.coreos.com/backend-data: {"VNI":1,"VtepMAC":"aa:0d:ad:10:90:1d"}
                    flannel.alpha.coreos.com/backend-type: vxlan
                    flannel.alpha.coreos.com/kube-subnet-manager: true
                    flannel.alpha.coreos.com/public-ip: 192.14.218.3
                    kubeadm.alpha.kubernetes.io/cri-socket: unix:///var/run/containerd/containerd.sock
                    node.alpha.kubernetes.io/ttl: 0
                    volumes.kubernetes.io/controller-managed-attach-detach: true
CreationTimestamp:  Mon, 17 Jun 2024 08:27:49 +0000
Taints:             <none>
```

### Q. Which node is the POD mosquito on now?

```bash
controlplane ~ ➜  kubectl get pod mosquito -o wide
NAME       READY   STATUS    RESTARTS   AGE   IP           NODE           NOMINATED NODE   READINESS GATES
mosquito   1/1     Running   0          15m   10.244.0.4   controlplane   <none>           <none>
```

> A. controlplane

## Node Affinity

### Q. How many Labels exist on node node01?

```bash
controlplane ~ ➜  kubectl describe node node01
Name:               node01
Roles:              <none>
Labels:             beta.kubernetes.io/arch=amd64
                    beta.kubernetes.io/os=linux
                    kubernetes.io/arch=amd64
                    kubernetes.io/hostname=node01
                    kubernetes.io/os=linux
...
```

> A. 5

### Q. Apply a label color=blue to node node01

```bash
controlplane ~ ➜  kubectl label node node01 color=blue
node/node01 labeled

controlplane ~ ➜  kubectl describe node node01
Name:               node01
Roles:              <none>
Labels:             beta.kubernetes.io/arch=amd64
                    beta.kubernetes.io/os=linux
                    color=blue
                    kubernetes.io/arch=amd64
                    kubernetes.io/hostname=node01
                    kubernetes.io/os=linux
...
```

### Q. Which node can the pods for the blue deployment be placed on?

```bash
controlplane ~ ➜  kubectl get nodes
NAME           STATUS   ROLES           AGE   VERSION
controlplane   Ready    control-plane   15m   v1.29.0
node01         Ready    <none>          15m   v1.29.0

controlplane ~ ➜  kubectl describe node controlplane
Name:               controlplane
Roles:              control-plane
Labels:             beta.kubernetes.io/arch=amd64
                    beta.kubernetes.io/os=linux
                    kubernetes.io/arch=amd64
                    kubernetes.io/hostname=controlplane
                    kubernetes.io/os=linux
                    node-role.kubernetes.io/control-plane=
                    node.kubernetes.io/exclude-from-external-load-balancers=
Annotations:        flannel.alpha.coreos.com/backend-data: {"VNI":1,"VtepMAC":"ce:19:08:31:7b:c5"}
                    flannel.alpha.coreos.com/backend-type: vxlan
                    flannel.alpha.coreos.com/kube-subnet-manager: true
                    flannel.alpha.coreos.com/public-ip: 192.16.90.9
                    kubeadm.alpha.kubernetes.io/cri-socket: unix:///var/run/containerd/containerd.sock
                    node.alpha.kubernetes.io/ttl: 0
                    volumes.kubernetes.io/controller-managed-attach-detach: true
CreationTimestamp:  Mon, 17 Jun 2024 09:28:48 +0000
Taints:             <none>
...

controlplane ~ ➜  kubectl describe node node01
Name:               node01
Roles:              <none>
Labels:             beta.kubernetes.io/arch=amd64
                    beta.kubernetes.io/os=linux
                    color=blue
                    kubernetes.io/arch=amd64
                    kubernetes.io/hostname=node01
                    kubernetes.io/os=linux
Annotations:        flannel.alpha.coreos.com/backend-data: {"VNI":1,"VtepMAC":"32:2f:80:a3:e7:70"}
                    flannel.alpha.coreos.com/backend-type: vxlan
                    flannel.alpha.coreos.com/kube-subnet-manager: true
                    flannel.alpha.coreos.com/public-ip: 192.16.90.12
                    kubeadm.alpha.kubernetes.io/cri-socket: unix:///var/run/containerd/containerd.sock
                    node.alpha.kubernetes.io/ttl: 0
                    volumes.kubernetes.io/controller-managed-attach-detach: true
CreationTimestamp:  Mon, 17 Jun 2024 09:29:31 +0000
Taints:             <none>
...
```

### Q. Set Node Affinity to the deployment to place the pods on node01 only.

```bash
controlplane ~ ✖ kubectl edit deployment blue

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: blue
spec:
  replicas: 3
  selector:
    matchLabels:
      run: nginx
  template:
    metadata:
      labels:
        run: nginx
    spec:
      containers:
      - image: nginx
        imagePullPolicy: Always
        name: nginx
      affinity:
        nodeAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
            nodeSelectorTerms:
            - matchExpressions:
              - key: color
                operator: In
                values:
                - blue
:wq

deployment.apps/blue edited
```

### Q. Create a new deployment named red with the nginx image and 2 replicas, and ensure it gets placed on the controlplane node only.


Use the label key - node-role.kubernetes.io/control-plane - which is already set on the controlplane node.

```bash
controlplane ~ ✖ vim red-deploy.yaml

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: red
spec:
  replicas: 2
  selector:
    matchLabels:
      run: nginx
  template:
    metadata:
      labels:
        run: nginx
    spec:
      containers:
      - image: nginx
        imagePullPolicy: Always
        name: nginx
      affinity:
        nodeAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
            nodeSelectorTerms:
            - matchExpressions:
              - key: node-role.kubernetes.io/control-plane
                operator: Exists
:wq

controlplane ~ ✖ kubectl create -f red-deploy.yaml
deployment.apps/red created
```

## Resouce Limits

### Q. A pod called rabbit is deployed. Identify the CPU requirements set on the Pod

```bash
controlplane ~ ➜  kubectl describe pod rabbit
Name:             rabbit
Namespace:        default
Priority:         0
Service Account:  default
Node:             controlplane/192.7.141.9
Start Time:       Tue, 18 Jun 2024 04:35:50 +0000
Labels:           <none>
Annotations:      <none>
Status:           Running
IP:               10.42.0.9
IPs:
  IP:  10.42.0.9
Containers:
  cpu-stress:
    Container ID:  containerd://e5bff6b613cb652462e33290525f74935646bc1d11aa775624513b1f5faa9ffd
    Image:         ubuntu
    Image ID:      docker.io/library/ubuntu@sha256:2e863c44b718727c860746568e1d54afd13b2fa71b160f5cd9058fc436217b30
    Port:          <none>
    Host Port:     <none>
    Args:
      sleep
      1000
    State:          Waiting
      Reason:       CrashLoopBackOff
    Last State:     Terminated
      Reason:       StartError
      Message:      failed to create containerd task: failed to create shim task: OCI runtime create failed: runc create failed: unable to start container process: error during container init: error setting cgroup config for procHooks process: failed to write "200000": write /sys/fs/cgroup/cpu,cpuacct/kubepods/burstable/pod0604153b-d337-443e-8f9c-1e571c491b25/e5bff6b613cb652462e33290525f74935646bc1d11aa775624513b1f5faa9ffd/cpu.cfs_quota_us: invalid argument: unknown
      Exit Code:    128
      Started:      Thu, 01 Jan 1970 00:00:00 +0000
      Finished:     Tue, 18 Jun 2024 04:36:09 +0000
    Ready:          False
    Restart Count:  2
    Limits:
      cpu:  2
    Requests:
      cpu:        1
  ...
```

> A. 1

### Q. Another pod called elephant has been deployed in the default namespace. It fails to get to a running state. Inspect this pod and identify the Reason why it is not running.

```bash
controlplane ~ ➜  kubectl describe pod elephant | grep -A5 State:
    State:          Waiting
      Reason:       CrashLoopBackOff
    Last State:     Terminated
      Reason:       OOMKilled
      Exit Code:    1
      Started:      Tue, 18 Jun 2024 04:40:14 +0000
      Finished:     Tue, 18 Jun 2024 04:40:14 +0000
    Ready:          False
```

> A. OOMKilled (Out of Memory)

### Q. The elephant pod runs a process that consumes 15Mi of memory. Increase the limit of the elephant pod to 20Mi.

Delete and recreate the pod if required. Do not modify anything other thant teh required fields.

```bash
controlplane ~ ✖ kubectl get pod elephant -o yaml > elephant.yaml

---
apiVersion: v1
kind: Pod
metadata:
  name: elephant
  namespace: default
spec:
  containers:
  - args:
    - --vm
    - "1"
    - --vm-bytes
    - 15M
    - --vm-hang
    - "1"
    command:
    - stress
    image: polinux/stress
    name: mem-stress
    resources:
      limits:
        memory: 20Mi
      requests:
        memory: 5Mi
:wq

controlplane ~ ➜  kubectl replace -f elephant.yaml --force
pod "elephant" deleted
pod/elephant replaced
```

## DaemonSets

## Static PODs

## Multiple Schedulers
