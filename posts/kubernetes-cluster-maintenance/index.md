# Kubernetes Cluster Maintenance


# Introduction

Kubernetes의 `drain`, `cordon`, `uncordon` 명령어는 노트 상태를 관리하고 워크로드의 배포와 관리를 최적화하는데 사용한다. 

## Drain

`drain` 명령어는 Node에서 모든 POD를 안전하게 제거해 Node를 비운다. `drain`은 `cordon` 명령어를 내부적으로 호출해 Node를 먼저 cordon 상태로 만든 후, Node에서 실행중인 모든 POD를 삭제하거나 다른 Node로 이동시킨다.

```bash
kubectl drain <node-name> --ignore-daemonsets --delete-local-data
```

주요 특징

- Node를 비워서 점검하거나, Node 종료 및 식제 시 사용한다.

- `--ignore-daemonsets` 옵션을 사용해 DaemonSet POD는 무시한다.

- `--delete-local-data` 옵션을 사용해 로컬 데이터가 있는 POD도 삭제한다.

- POD가 안전하게 종료되고, 가능한 경우 다른 Node로 이동한다.

- Node가 비워지기 때문에 서비스 중단을 최소화할 수 있다.

## Cordon

`cordon` 명령어는 Node를 `cordon` 상태로 만들어서, 새로운 POD가 해당 Node에 스케줄링되지 않도록 한다. 이미 실행 중인 POD는 영향을 받지 않지만, 새로 생성되거나 재스케줄링되는 POD는 다른 Node로 이동한다.

```bash
kubectl cordon <node-name>
```

주요 특징

- Node가 `cordon` 상태가 되면 새 POD는 해당 Node에 스케줄되지 않는다.

- 기존 POD는 영향을 받지 않고 계속 실행된다.

- 주로 Node를 점검하거나 유지보수할 때 사용한다.

## Uncordon

`uncordon` 명령어는 cordon 상태의 Node를 다시 사용할 수 있게 풀어준다. 이 명령어를 사용하면 새로운 POD가 해당 Node에 스케줄링 될 수 있다.

```bash
kubectl uncordon <node-name>
```

주요 특징

- cordon 상태의 Node를 다시 정상 상태로 되돌린다.

- 새 POD가 해당 Node에 스케줄링 될 수 있다.

- Node 점검이나 유지보수가 완료된 후 사용한다.

### 요약

`Drain`: Node를 비우기 위해 모든 POD를 안전하게 제거합니다. 내부적으로 cordon 상태로 전환한 후 POD를 삭제하거나 이동시킵니다.

`Cordon`: Node를 cordon 상태로 만들어 새로운 POD가 스케줄링되지 않도록 합니다.

`Uncordon`: cordon 상태의 Node를 정상 상태로 되돌려서 새로운 POD를 스케줄링할 수 있게 합니다.

## OS Upgrades

### Q. We need to take `node01` out for maintenance. Empty the node of all applications and mark it unshedulable.

Node node01 Unschedulable

Pods evicted from node01

```bash
controlplane ~ ✖ k drain node01 --ignore-daemonsets
node/node01 cordoned
Warning: ignoring DaemonSet-managed Pods: kube-flannel/kube-flannel-ds-lfwv8, kube-system/kube-proxy-77vqk
evicting pod default/blue-fffb6db8d-cjl6s
evicting pod default/blue-fffb6db8d-bfkvx
pod/blue-fffb6db8d-cjl6s evicted
pod/blue-fffb6db8d-bfkvx evicted
node/node01 drained
```

### Q. What nodes are the apps on now?

```bash
controlplane ~ ➜  k get pods -o wide
NAME                   READY   STATUS    RESTARTS   AGE     IP           NODE           NOMINATED NODE   READINESS GATES
blue-fffb6db8d-26pnb   1/1     Running   0          54s     10.244.0.6   controlplane   <none>           <none>
blue-fffb6db8d-6k7c2   1/1     Running   0          54s     10.244.0.5   controlplane   <none>           <none>
blue-fffb6db8d-lkjjs   1/1     Running   0          4m32s   10.244.0.4   controlplane   <none>           <none>
```

> A. controlplane

### Q. The maintenance tasks have been completed. Configure the node `node01` to be schedulable again.

Node01 is schedulable

```bash
controlplane ~ ➜  k uncordon node01
node/node01 uncordoned
```

### Q. How many pods are scheduled on `node01` now in the default namepace?

```bash
controlplane ~ ➜  k get pods -o wide
NAME                   READY   STATUS    RESTARTS   AGE     IP           NODE           NOMINATED NODE   READINESS GATES
blue-fffb6db8d-26pnb   1/1     Running   0          4m35s   10.244.0.6   controlplane   <none>           <none>
blue-fffb6db8d-6k7c2   1/1     Running   0          4m35s   10.244.0.5   controlplane   <none>           <none>
blue-fffb6db8d-lkjjs   1/1     Running   0          8m13s   10.244.0.4   controlplane   <none>           <none>
```

> A. 0

### Q. Why are there no pods on `node01`?

> A. Running the `uncordon` command on a node will not automatically schedule pods on the node. When new pods are creatd, they will be placed on node01.

### Q. Why are the pods placed on the `controlplane` node? 

```bash
root@controlplane:~# kubectl describe node controlplane | grep -i  taint
Taints:             <none>
root@controlplane:~#
```

> A. Since there are no taints on the controlplace node, all the pods were started on it when we ran the `kubectl drain node01` command.

### `hr-app` is a critical app and we do not want it to be removed and we do not want to schedule any more pods on `node01`. Mark `node01` as `unschedulable` so that no new pods are scheduled on this node.

Make sure that hr-app is not affected.

> Do not drain `node01`, instead use the `kubectl cordon node01` command. This will ensure that no new pods are scheduled on this node and the existing pods will not be affected by this operation.

## Cluster Upgrade

### Q. What is the current version of the cluster?

```bash
controlplane ~ ➜  k get nodes -o wide
NAME           STATUS   ROLES           AGE   VERSION   INTERNAL-IP    EXTERNAL-IP   OS-IMAGE             KERNEL-VERSION   CONTAINER-RUNTIME
controlplane   Ready    control-plane   59m   v1.28.0   192.7.153.9    <none>        Ubuntu 20.04.6 LTS   5.4.0-1106-gcp   containerd://1.6.6
node01         Ready    <none>          58m   v1.28.0   192.7.153.11   <none>        Ubuntu 20.04.6 LTS   5.4.0-1106-gcp   containerd://1.6.6
```

> A. 1.28.0

### Q. How many nodes can host workloads in this cluster?

Inspect the application and taints set on the nodes.

```bash
root@controlplane:~# kubectl describe nodes  controlplane | grep -i taint
Taints:             <none>
root@controlplane:~# 
root@controlplane:~# kubectl describe nodes  node01 | grep -i taint
Taints:             <none>
root@controlplane:~#
```

> A. Both nodes have the ability to schedule workloads on them.

### Q. What is the latest version available for an upgrade with the current version of the kubeadm tool installed?

```bash
controlplane ~ ➜  kubeadm upgrade plan
[upgrade/config] Making sure the configuration is correct:
[upgrade/config] Reading configuration from the cluster...
[upgrade/config] FYI: You can look at this config file with 'kubectl -n kube-system get cm kubeadm-config -o yaml'
[preflight] Running pre-flight checks.
[upgrade] Running cluster health checks
[upgrade] Fetching available versions to upgrade to
[upgrade/versions] Cluster version: v1.28.0
[upgrade/versions] kubeadm version: v1.28.0
I0624 01:43:01.970184   18248 version.go:256] remote version is much newer: v1.30.2; falling back to: stable-1.28
[upgrade/versions] Target version: v1.28.11
[upgrade/versions] Latest version in the v1.28 series: v1.28.11

Components that must be upgraded manually after you have upgraded the control plane with 'kubeadm upgrade apply':
COMPONENT   CURRENT       TARGET
kubelet     2 x v1.28.0   v1.28.11

Upgrade to the latest version in the v1.28 series:

COMPONENT                 CURRENT   TARGET
kube-apiserver            v1.28.0   v1.28.11
kube-controller-manager   v1.28.0   v1.28.11
kube-scheduler            v1.28.0   v1.28.11
kube-proxy                v1.28.0   v1.28.11
CoreDNS                   v1.10.1   v1.10.1
etcd                      3.5.9-0   3.5.9-0

You can now apply the upgrade by executing the following command:

        kubeadm upgrade apply v1.28.11
```

### Q. We will be upgrading the controlplane node first. Drain the controlplane node of workloads and mark it `UnSchedulable`.

Controlplane Node: SchedulingDisabled

```bash
controlplane ~ ➜  k drain controlplane --ignore-daemonsets
node/controlplane cordoned
Warning: ignoring DaemonSet-managed Pods: kube-flannel/kube-flannel-ds-x7ljk, kube-system/kube-proxy-jd6st
evicting pod kube-system/coredns-5dd5756b68-vchp5
evicting pod default/blue-667bf6b9f9-lnprm
evicting pod default/blue-667bf6b9f9-2ppcf
evicting pod kube-system/coredns-5dd5756b68-mxnht
pod/blue-667bf6b9f9-2ppcf evicted
pod/blue-667bf6b9f9-lnprm evicted
pod/coredns-5dd5756b68-mxnht evicted
pod/coredns-5dd5756b68-vchp5 evicted
node/controlplane drained
```

### Q. Upgrade the `controlplane` components to exact version `v1.29.0`

Upgrade the kubeadm tool (if not already), then the controlplane components, and finally the kubelet. Practice referring to the Kubernetes documentation page.

Controlplane Node Upgraded to v1.29.0

Controlplane Kubelet Upgraded to v1.29.0

1. On the `controlplane` node:

   Use any text editor you prefer to open the file that defines the Kubernetes apt repository.

    ```bash
    vim /etc/apt/sources.list.d/kubernetes.list
    ```

2. Update the version in the URL to the next available minor release, i.e v1.29.

    ```bash
    deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.29/deb/ /
    ```

3. After making changes, save the file and exit from your text editor. Proceed with next instruction.

    ```bash
    root@controlplane:~# apt update
    root@controlplane:~# apt-cache madison kubeadm
    ```

4. Based on the version information displayed by `apt-cache madison`, it indicates that for Kubernetes version `1.29.0`, the available package version is `1.29.0-1.1`. Therefore, to install kubeadm for kubernetes `v1.29.0`, use the following command:

    ```bash
    root@controlplane:~# apt-get install kubeadm=1.29.0-1.1
    ```

5. Run the following command to upgrade the kubernetes cluster.

    ```bash
    root@controlplane:~# kubeadm upgrade plan v1.29.0
    root@controlplane:~# kubeadm upgrade apply v1.29.0
    ```

6. Now, upgrade the version and restart Kubelet. Also, mark the node(in this case, the "controlplane" node) as schedulable.

    ```bash
    root@controlplane:~# apt-get install kubelet=1.29.0-1.1
    root@controlplane:~# systemctl daemon-reload
    root@controlplane:~# systemctl restart kubelet
    root@controlplane:~# kubectl uncordon controlplane
    ```

### Q. Upgrade the worker node to the exact version `v.1.29.0`.

Worker Node Upgraded to v1.29.0

Worker Node Ready

On the node01 node, run the following commands:

If you are on the controlplane node, run ssh node01 to log in to the node01.

Use any text editor you prefer to open the file that defines the Kubernetes apt repository.

```bash
vim /etc/apt/sources.list.d/kubernetes.list
```

Update the version in the URL to the next available minor release, i.e v1.29.

```bash
deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.29/deb/ /
```

After making changes, save the file and exit from your text editor. Proceed with the next instruction.

```bash
root@node01:~# apt update
root@node01:~# apt-cache madison kubeadm
```

Based on the version information displayed by apt-cache madison, it indicates that for Kubernetes version 1.29.0, the available package version is 1.29.0-1.1. Therefore, to install kubeadm for Kubernetes v1.29.0, use the following command:

```bash
root@node01:~# apt-get install kubeadm=1.29.0-1.1
# Upgrade the node 
root@node01:~# kubeadm upgrade node
```

Now, upgrade the version and restart Kubelet.

```bash
root@node01:~# apt-get install kubelet=1.29.0-1.1
root@node01:~# systemctl daemon-reload
root@node01:~# systemctl restart kubelet
```

Type exit or logout or enter CTRL + d to go back to the controlplane node.

## Backup and Restore Methods I

### Q. What is the version of ETCD running on the cluster?

```bash
root@controlplane:~# kubectl -n kube-system logs etcd-controlplane | grep -i 'etcd-version'
"caller":"embed/etcd.go:306","msg":"starting an etcd server","etcd-version":"3.5.7","git-sha":"215b53cf3"

root@controlplane:~# 

root@controlplane:~# kubectl -n kube-system describe pod etcd-controlplane | grep Image:
    Image:         registry.k8s.io/etcd:3.5.12-0
root@controlplane:~#
```

### Q. At what address can you reach the ETCD cluster from the controlplane node?

Check the ETCD Service configuration in the ETCD POD

```bash
root@controlplane:~# kubectl -n kube-system describe pod etcd-controlplane | grep '\--listen-client-urls'
      --listen-client-urls=https://127.0.0.1:2379,https://10.2.43.11:2379
root@controlplane:~#
```

> A. 

### Q. Where is the ETCD server certificate file located?

Note this path down as you will need to use it later.

```bash
controlplane ~ ✖ kubectl -n kube-system describe pod etcd-controlplane | grep '\--cer
t-file'
      --cert-file=/etc/kubernetes/pki/etcd/server.crt
```

> A. /etc/kubernetes/pki/etcd/server.crt

### Q. Where is the ETCD CA Certificate file located?

Note this path down as you will need to use it later

```bash
root@controlplane:~# kubectl -n kube-system describe pod etcd-controlplane | grep '\--trusted-ca-file'
      --trusted-ca-file=/etc/kubernetes/pki/etcd/ca.crt
root@controlplane:~#
```

Check the ETCD pod configuration with dommand: `kubectl describe pod etcd-controlplane -n kube-system` and look for the value --

> A. /etc/kubernetes/pki/etcd/server.crt

### Q. Take a snapshot of the ETCD database using the built-inn snapshot functionality.

Store the backup file at location `/opt/snapshot-pre-boot.db`

```bash
controlplane ~ ➜  ETCDCTL_API=3 etcdctl --endpoints=https://[127.0.0.1]:2379 \
--cacert=/etc/kubernetes/pki/etcd/ca.crt \
--cert=/etc/kubernetes/pki/etcd/server.crt \
--key=/etc/kubernetes/pki/etcd/server.key \
snapshot save /opt/snapshot-pre-boot.db
Snapshot saved at /opt/snapshot-pre-boot.db
```

### Q. Restore the original state of the cluster using the backup file.

Deployments: 2

Services: 3

First restore the snapshot:

```bash
root@controlplane:~# ETCDCTL_API=3 etcdctl  --data-dir /var/lib/etcd-from-backup \
snapshot restore /opt/snapshot-pre-boot.db


2022-03-25 09:19:27.175043 I | mvcc: restore compact to 2552
2022-03-25 09:19:27.266709 I | etcdserver/membership: added member 8e9e05c52164694d [http://localhost:2380] to cluster cdf818194e3a8c32
```

Note: In this case, we are restoring the snapshot to a different directory but in the same server where we took the backup(the controlplane node) As a result, the only required option for the restore command is the `--data-dir`.

Next, update the `/etc/kubernetes/manifests/etcd.yaml`

We have now restored the etcd snapshot to a new path on the controlplane - `/var/lib/etcd-from-backup`, so, the only change to be made in the YAML file, is to change the hostPath for the volume called `etcd-data` from old directory (`/var/lib/etcd`) to the new directory (`/var/lib/etcd-from-backup`)

```bash
  volumes:
  - hostPath:
      path: /var/lib/etcd-from-backup
      type: DirectoryOrCreate
    name: etcd-data
```

With this change, `/var/lib/etcd` on the container points to `/var/lib/etcd-from-backup` on the `controlplane` (which is what we want)

When this file is updated, the `ETCD` pod is automatically re-created as that is a static pod placed under the `/etc/kubernetes/manifests` directory

Note 1: As the ETCD pod has changed it will automatically restart, and also `kube-controller-manager` and `kube-scheduler`. Wait 1-2 to mins for this pods to restart. You can run the command: `watch "crictl ps | grep etcd"` to see when the ETCD pod is restarted.

Note 2: If the etcd pod is not getting `Ready 1/1`, then restart it by `kubectl delete pod -n kube-system etcd-controlplane` and wait 1 minute.

Note 3: This is the simplest way to make sure that ETCD uses the restored data after the ETCD pod is recreated. You don't have to change anything else.

If you do change `--data-dir` to `/var/lib/etcd-from-backup` in the ETCD YAML file, make sure that the `volumeMounts` for `etcd-data` is updated as well, with the mountPath pointing to `/var/lib/etcd-from-backup` (THIS COMPLETE STEP IS OPTIONAL AND NEED NOT BE DONE FOR COMPLETING THE RESTORE)

## Backup and Restore Methods II

### Q. How many clusters are defined in the kubeconfig on the student-node?

```bash
student-node ~ ✖ k config view
apiVersion: v1
clusters:
- cluster:
    certificate-authority-data: DATA+OMITTED
    server: https://cluster1-controlplane:6443
  name: cluster1
- cluster:
    certificate-authority-data: DATA+OMITTED
    server: https://192.14.89.17:6443
  name: cluster2
contexts:
- context:
    cluster: cluster1
    user: cluster1
  name: cluster1
- context:
    cluster: cluster2
    user: cluster2
  name: cluster2
current-context: cluster1
kind: Config
preferences: {}
users:
- name: cluster1
  user:
    client-certificate-data: REDACTED
    client-key-data: REDACTED
- name: cluster2
  user:
    client-certificate-data: REDACTED
    client-key-data: REDACTED
```

> A. 2

### Q. How many nodes(both controlplane and worker) are part of cluster1?

Make sure to switch the context to `cluster1`:

```bash
student-node ~ ➜  kubectl config use-context cluster1
Switched to context "cluster1".

student-node ~ ➜  k get nodes
NAME                    STATUS   ROLES           AGE   VERSION
cluster1-controlplane   Ready    control-plane   64m   v1.24.0
cluster1-node01         Ready    <none>          64m   v1.24.0
```

### Q. How is ETCD configured for cluster1?

Remeber, you can access the clusters from `student-node` using the `kubectl` tool. You can also `ssh` to the cluster nodes from the `student-node`.

Make sure to switch the context to `cluster`:

```bash
student-node ~ ➜  kubectl config use-context cluster1
Switched to context "cluster1".

student-node ~ ➜  kubectl get pods -n kube-system | grep etcd
etcd-cluster1-controlplane                      1/1     Running   0              9m26s
```

This means that ETCD is set up as a `Stacked ETCD Topolofy` where the distributed data storage cluster provided by `etcd` is stacked on top of the cluster formed by the nodes managed by kubeadm that run control plane components.

### Q. How is ETCD configured for cluster2?

Remeber, you can access the clusters from `student-node` using the `kubectl` tool. You can also `sssh` to the cluster nodes from the `student-node`.

Make sure to switch the context to `cluster2`:

If you check out the pods running in the `kube-system` namespace in `cluster2`, you will notice that there are NO `etcd` pods running in this cluster!

```bash
student-node ~ ➜  kubectl config use-context cluster2
Switched to context "cluster2".

student-node ~ ➜  kubectl get pods -n kube-system  | grep etcd
```

Also, there is NO static pod configuration for `etcd` under the static pod path:

```bash
student-node ~ ✖ ssh cluster2-controlplane
Welcome to Ubuntu 18.04.6 LTS (GNU/Linux 5.4.0-1086-gcp x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage
This system has been minimized by removing packages and content that are
not required on a system that users do not log into.

To restore this content, you can run the 'unminimize' command.
Last login: Wed Aug 31 05:05:04 2022 from 10.1.127.14

cluster2-controlplane ~ ➜  ls /etc/kubernetes/manifests/ | grep -i etcd
```

However, if you inspect the process on the controlplane for cluster2, you will see that that the process for the `kube-apiserver` is referencing an external etcd datastore:

```bash
cluster2-controlplane ~ ✖ ps -ef | grep etcd
root        1705    1320  0 05:03 ?        00:00:31 kube-apiserver --advertise-address=10.1.127.3 --allow-privileged=true --authorization-mode=Node,RBAC --client-ca-file=/etc/kubernetes/pki/ca.crt --enable-admission-plugins=NodeRestriction --enable-bootstrap-token-auth=true --etcd-cafile=/etc/kubernetes/pki/etcd/ca.pem --etcd-certfile=/etc/kubernetes/pki/etcd/etcd.pem --etcd-keyfile=/etc/kubernetes/pki/etcd/etcd-key.pem --etcd-servers=https://10.1.127.10:2379 --kubelet-client-certificate=/etc/kubernetes/pki/apiserver-kubelet-client.crt --kubelet-client-key=/etc/kubernetes/pki/apiserver-kubelet-client.key --kubelet-preferred-address-types=InternalIP,ExternalIP,Hostname --proxy-client-cert-file=/etc/kubernetes/pki/front-proxy-client.crt --proxy-client-key-file=/etc/kubernetes/pki/front-proxy-client.key --requestheader-allowed-names=front-proxy-client --requestheader-client-ca-file=/etc/kubernetes/pki/front-proxy-ca.crt --requestheader-extra-headers-prefix=X-Remote-Extra- --requestheader-group-headers=X-Remote-Group --requestheader-username-headers=X-Remote-User --secure-port=6443 --service-account-issuer=https://kubernetes.default.svc.cluster.local --service-account-key-file=/etc/kubernetes/pki/sa.pub --service-account-signing-key-file=/etc/kubernetes/pki/sa.key --service-cluster-ip-range=10.96.0.0/12 --tls-cert-file=/etc/kubernetes/pki/apiserver.crt --tls-private-key-file=/etc/kubernetes/pki/apiserver.key
root        5754    5601  0 05:15 pts/0    00:00:00 grep etcd
```

You can see the same information by inspecting the kube-apiserver pod (which runs as a static pod in the kube-system namespace):

```bash
cluster2-controlplane ~ ➜  kubectl -n kube-system describe pod kube-apiserver-cluster2-controlplane 
Name:                 kube-apiserver-cluster2-controlplane
Namespace:            kube-system
Priority:             2000001000
Priority Class Name:  system-node-critical
Node:                 cluster2-controlplane/10.1.127.3
Start Time:           Wed, 31 Aug 2022 05:03:45 +0000
Labels:               component=kube-apiserver
                      tier=control-plane
Annotations:          kubeadm.kubernetes.io/kube-apiserver.advertise-address.endpoint: 10.1.127.3:6443
                      kubernetes.io/config.hash: 9bd4c04b38b27661e9e7f8b0fc1237b8
                      kubernetes.io/config.mirror: 9bd4c04b38b27661e9e7f8b0fc1237b8
                      kubernetes.io/config.seen: 2022-08-31T05:03:28.843162256Z
                      kubernetes.io/config.source: file
                      seccomp.security.alpha.kubernetes.io/pod: runtime/default
Status:               Running
IP:                   10.1.127.3
IPs:
  IP:           10.1.127.3
Controlled By:  Node/cluster2-controlplane
Containers:
  kube-apiserver:
    Container ID:  containerd://cc64f3649222f24d3fd2eb7d5f0f17db5fca76eb72dc4c17295fb4842c045f1b
    Image:         k8s.gcr.io/kube-apiserver:v1.24.0
    Image ID:      k8s.gcr.io/kube-apiserver@sha256:a04522b882e919de6141b47d72393fb01226c78e7388400f966198222558c955
    Port:          <none>
    Host Port:     <none>
    Command:
      kube-apiserver
      --advertise-address=10.1.127.3
      --allow-privileged=true
      --authorization-mode=Node,RBAC
      --client-ca-file=/etc/kubernetes/pki/ca.crt
      --enable-admission-plugins=NodeRestriction
      --enable-bootstrap-token-auth=true
      --etcd-cafile=/etc/kubernetes/pki/etcd/ca.pem
      --etcd-certfile=/etc/kubernetes/pki/etcd/etcd.pem
      --etcd-keyfile=/etc/kubernetes/pki/etcd/etcd-key.pem
      --etcd-servers=https://10.1.127.10:2379
--------- End of Snippet---------
```

### Q. What is the default data directory used the for ETCD datastore used in cluster1?

Remember, this cluster uses a Stacked ETCD topology.

Make sure to switch the context to cluster1:

kubectl config use-context cluster1

```bash
student-node ~ ✖ kubectl -n kube-system describe pod etcd-cluster1-controlplane | grep data-dir
      --data-dir=/var/lib/etcd

student-node ~ ➜ --data-dir=/var/lib/etcd
```

### Q. What is the default data directory used the for ETCD datastore used in clutser2?

Remember, this cluster uses as `External ETCD` topology.

```bash
student-node ~ ➜  ssh etcd-server
Welcome to Ubuntu 18.04.6 LTS (GNU/Linux 5.4.0-1106-gcp x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage
This system has been minimized by removing packages and content that are
not required on a system that users do not log into.

To restore this content, you can run the 'unminimize' command.

etcd-server ~ ✖ ps -ef | grep etcd
etcd         831       1  0 07:53 ?        00:01:08 /usr/local/bin/etcd --name etcd-server --data-dir=/var/lib/etcd-data --cert-file=/etc/etcd/pki/etcd.pem --key-file=/etc/etcd/pki/etcd-key.pem --peer-cert-file=/etc/etcd/pki/etcd.pem --peer-key-file=/etc/etcd/pki/etcd-key.pem --trusted-ca-file=/etc/etcd/pki/ca.pem --peer-trusted-ca-file=/etc/etcd/pki/ca.pem --peer-client-cert-auth --client-cert-auth --initial-advertise-peer-urls https://192.14.89.6:2380 --listen-peer-urls https://192.14.89.6:2380 --advertise-client-urls https://192.14.89.6:2379 --listen-client-urls https://192.14.89.6:2379,https://127.0.0.1:2379 --initial-cluster-token etcd-cluster-1 --initial-cluster etcd-server=https://192.14.89.6:2380 --initial-cluster-state new
root        1137    1003  0 09:18 pts/0    00:00:00 grep etcd
```

### Q. How many nodes are part of the ETCD cluster that etcd-server is a part of?

```bash
etcd-server ~ ➜  ETCDCTL_API=3 etcdctl \
 --endpoints=https://127.0.0.1:2379 \
 --cacert=/etc/etcd/pki/ca.pem \
 --cert=/etc/etcd/pki/etcd.pem \
 --key=/etc/etcd/pki/etcd-key.pem \
  member list
f0f805fc97008de5, started, etcd-server, https://10.1.218.3:2380, https://10.1.218.3:2379, false
```

### Q. Take a backup of etcd on cluster1 and save it on the student-node at the path /opt/cluster1.db

If needed, make sure to set the context to cluster1

```bash
student-node ~ ➜  kubectl config use-context cluster1
Switched to context "cluster1".
```

Next, inspect the endpoints and certificates used by the `etcd` pod. We will make use of these to take the backup.

```bash
student-node ~ ✖ kubectl describe  pods -n kube-system etcd-cluster1-controlplane  | grep advertise-client-urls
      --advertise-client-urls=https://10.1.218.16:2379

student-node ~ ➜  

student-node ~ ➜  kubectl describe  pods -n kube-system etcd-cluster1-controlplane  | grep pki
      --cert-file=/etc/kubernetes/pki/etcd/server.crt
      --key-file=/etc/kubernetes/pki/etcd/server.key
      --peer-cert-file=/etc/kubernetes/pki/etcd/peer.crt
      --peer-key-file=/etc/kubernetes/pki/etcd/peer.key
      --peer-trusted-ca-file=/etc/kubernetes/pki/etcd/ca.crt
      --trusted-ca-file=/etc/kubernetes/pki/etcd/ca.crt
      /etc/kubernetes/pki/etcd from etcd-certs (rw)
    Path:          /etc/kubernetes/pki/etcd

student-node ~ ➜
```

SSH to the `controlplane` node of `cluster1` and then take the backup using the endpoints and certificates we identified above:

```bash
cluster1-controlplane ~ ➜  ETCDCTL_API=3 etcdctl --endpoints=https://10.1.220.8:2379 --cacert=/etc/kubernetes/pki/etcd/ca.crt --cert=/etc/kubernetes/pki/etcd/server.crt --key=/etc/kubernetes/pki/etcd/server.key snapshot save /opt/cluster1.db
Snapshot saved at /opt/cluster1.db

cluster1-controlplane ~ ➜
```

Finally, copy the backup to the `student-node`. To do this, go back to the `student-node` and use `scp` as shown below:

```bash
student-node ~ ➜  scp cluster1-controlplane:/opt/cluster1.db /opt
cluster1.db                                                                                                        100% 2088KB 112.3MB/s   00:00    

student-node ~ ➜
```
