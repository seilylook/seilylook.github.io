# Certified Kubernetes Administrator


# Introduction 

CKA 자격증은 쿠버네티스 클러스터를 설치, 구성, 관리하는 데 필요한 지식과 경험을 입증하는 자격증이다. 

## 문제

### 1. Question

Use context: `kubectl config use-context k8s-c2-AC`

The cluster admin asked you to find out the following information about etcd runngin on cluster2-controlplane1:

- Server private key location

- Server certificate expiration date

- Is client certificate authentication enabled

Write these information into `/opt/course/p1/etcd-info.txt`

Finally you're asked to save an etcd snapshot at `/etc/etcd-snapshot.db` on cluster2-controlplane1 and display its status

#### Answer

**Find out etcd information**

check the nodes:

```bash 
k get nodes

NAME                     STATUS   ROLES           AGE    VERSION
cluster2-controlplane1   Ready    control-plane   89m   v1.30.1
cluster2-node1           Ready    <none>          87m   v1.30.1

ssh cluster2-controlplane1
```

First we check how etcd is setup in this cluster:

```bash
k get pods -n kube-system

NAME                                                READY   STATUS    RESTARTS   AGE
coredns-66bff467f8-k8f48                            1/1     Running   0          26h
coredns-66bff467f8-rn8tr                            1/1     Running   0          26h
etcd-cluster2-controlplane1                         1/1     Running   0          26h
kube-apiserver-cluster2-controlplane1               1/1     Running   0          26h
kube-controller-manager-cluster2-controlplane1      1/1     Running   0          26h
kube-proxy-qthfg                                    1/1     Running   0          25h
kube-proxy-z55lp                                    1/1     Running   0          26h
kube-scheduler-cluster2-controlplane1               1/1     Running   1          26h
weave-net-cqdvt                                     2/2     Running   0          26h
weave-net-dxzgh                                     2/2     Running   1          25h
```

We see it's running as a Pod, more specific a static Pod. So we check for the default kubelet directory for static manifests:

```bash
find /etc/kubernetes/manifests/

/etc/kubernetes/manifests/
/etc/kubernetes/manifests/kube-controller-manager.yaml
/etc/kubernetes/manifests/kube-apiserver.yaml
/etc/kubernetes/manifests/etcd.yaml
/etc/kubernetes/manifests/kube-scheduler.yaml

cat /etc/kubernetes/manifests/etcd.yaml
```

So we look at the yaml and parameter with which etcd is started:

```yaml
# /etc/kubernetes/manifests/etcd.yaml

apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  labels:
    component: etcd
    tier: control-plane
  name: etcd
  namespace: kube-system
spec:
  containers:
  - command:
    - etcd
    - --advertise-client-urls=https://192.168.102.11:2379
    - --cert-file=/etc/kubernetes/pki/etcd/server.crt              # server certificate
    - --client-cert-auth=true                                      # enabled
    - --data-dir=/var/lib/etcd
    - --initial-advertise-peer-urls=https://192.168.102.11:2380
    - --initial-cluster=cluster2-controlplane1=https://192.168.102.11:2380
    - --key-file=/etc/kubernetes/pki/etcd/server.key               # server private key
    - --listen-client-urls=https://127.0.0.1:2379,https://192.168.102.11:2379
    - --listen-metrics-urls=http://127.0.0.1:2381
    - --listen-peer-urls=https://192.168.102.11:2380
    - --name=cluster2-controlplane1
    - --peer-cert-file=/etc/kubernetes/pki/etcd/peer.crt
    - --peer-client-cert-auth=true
    - --peer-key-file=/etc/kubernetes/pki/etcd/peer.key
    - --peer-trusted-ca-file=/etc/kubernetes/pki/etcd/ca.crt
    - --snapshot-count=10000
    - --trusted-ca-file=/etc/kubernetes/pki/etcd/ca.crt
...
```

We see that client authentication is enalbed and also the requested path to the server private key, now let's find out the expiration of the server certificate:

```bash 
openssl x509 -noout -text -in /etc/kubernetes/pki/etcd/server.crt 

        Validity
            Not Before: Sep 13 13:01:31 2021 GMT
            Not After : Sep 13 13:01:31 2022 GMT
```

There we have it. 

```txt
# /opt/course/p1/etcd-info.txt

Server private key location: /etc/kubernetes/pki/etcd/server.key
Server certificate expiration date: Sep 13 13:01:31 2022 GMT
Is client certificate authentication enabled: yes
```

**Create etcd snapshot**

```bash
ETCDCTL_API=3 etcdctl snapshot save /etc/etcd-snapshot.db
```

We get the endpoint also from the yaml. But we need to specify more parameters, all of which we can find the yaml declaration abobe:

```bash
ETCDCTL_API=3 etcdctl snapshot save /etc/etcd-snapshot.db \
--cacert /etc/kubernetes/pki/etcd/ca.crt \
--cert /etc/kubernetes/pki/etcd/server.crt \
--key /etc/kubernetes/pki/etcd/server.key
```

This wored, Now we can output the status of the backup file:

```bash
ETCDCTL_API=3 etcdctl snapshot status /etc/etcd-snapshot.db
4d4e953, 7213, 1291, 2.7 MB
```

### 2. Question

Use context: `kubectl config use-context k8s-c1-H`

You're asked to confirm that kube-proxy is running correctly on all nodes. For this preform the following in *Namespace* `project-hamster`:

Create a new Pod names `p2-pod` with two containers, one of image `nginx:1.21.3-alpine` and one of image `busybox:1.31`. Make sure the busybox container keeps running for some time.

Create a new Service named `p2-service` which exposes that pod internally in the cluster on port 3000 -> 80.

Find the kube-proxy container on all nodes `clutser1-controlplane1`, `cluster1-node1` and `clutser1-node2` and make sure that it's using iptables. Use command `crictl` for this.

Write the iptables rules of all nodes belonging the created service `p2-service` into file `/opt/course/p2/iptables.txt`

Finally delete the Service and confirm that the iptables rules are gone from all nodes.

#### Answer

**Create the Pod**

```bash
kubectl run p2-pod --image=nginx:1.21.3-alpine -o yaml > p2.yaml

vim p2.yaml
```

Next we add the requested second container

```yaml
# p2.yaml
apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  labels:
    run: p2-pod
  name: p2-pod
  namespace: project-hamster             # add
spec:
  containers:
  - image: nginx:1.21.3-alpine
    name: p2-pod
  - image: busybox:1.31                  # add
    name: c2                             # add
    command: ["sh", "-c", "sleep 1d"]    # add
    resources: {}
  dnsPolicy: ClusterFirst
  restartPolicy: Always
status: {}
```

And we create the Pod:

```bash
k crete -f p2.yaml
```

**Create the Service**

Next we create the Service:

```bash
k expose pod p2-pod --name p2-service --port 3000 --target-port 80 -n project-hamster
```

This will create a yaml file:

```yaml
apiVersion: v1
kind: Service
metadata:
  creationTimestamp: "2020-04-30T20:58:14Z"
  labels:
    run: p2-pod
  managedFields:
...
    operation: Update
    time: "2020-04-30T20:58:14Z"
  name: p2-service
  namespace: project-hamster
  resourceVersion: "11071"
  selfLink: /api/v1/namespaces/project-hamster/services/p2-service
  uid: 2a1c0842-7fb6-4e94-8cdb-1602a3b1e7d2
spec:
  clusterIP: 10.97.45.18
  ports:
  - port: 3000
    protocol: TCP
    targetPort: 80
  selector:
    run: p2-pod
  sessionAffinity: None
  type: ClusterIP
status:
  loadBalancer: {}
```

We should confirm Pods and Services are connected, hence the Service should have endpoints.

```bash
k get pod,svc,ep -n project-hamster
```

**Confirm kube-proxy is running and is using iptables**

First we get nodes in the cluster:

```bash
k get node

NAME                     STATUS   ROLES           AGE   VERSION
cluster1-controlplane1   Ready    control-plane   98m   v1.30.1
cluster1-node1           Ready    <none>          96m   v1.30.1
cluster1-node2           Ready    <none>          95m   v1.30.1
```

The idea here is to log into every node, find the kube-proxy container and check its logs:

```bash
ssh cluster1-controlplane1

crictl ps | grep kube-proxy
27b6a18c0f89c       36c4ebbc9d979       3 hours ago         Running             kube-proxy

crictl logs 27b6a18c0f89c
...
I0913 12:53:03.096620       1 server_others.go:212] Using iptables Proxier.
...
```

This should be repeated on every node and result in the same output `Using iptables Proxier`

**Check kube-proxy is creating iptables rules**

New we check the iptables rules on every node first manullay:

```bash
ssh cluster1-controlplane1 iptables-save | grep p2-service

-A KUBE-SEP-6U447UXLLQIKP7BB -s 10.44.0.20/32 -m comment --comment "project-hamster/p2-service:" -j KUBE-MARK-MASQ
-A KUBE-SEP-6U447UXLLQIKP7BB -p tcp -m comment --comment "project-hamster/p2-service:" -m tcp -j DNAT --to-destination 10.44.0.20:80
-A KUBE-SERVICES ! -s 10.244.0.0/16 -d 10.97.45.18/32 -p tcp -m comment --comment "project-hamster/p2-service: cluster IP" -m tcp --dport 3000 -j KUBE-MARK-MASQ
-A KUBE-SERVICES -d 10.97.45.18/32 -p tcp -m comment --comment "project-hamster/p2-service: cluster IP" -m tcp --dport 3000 -j KUBE-SVC-2A6FNMCK6FDH7PJH
-A KUBE-SVC-2A6FNMCK6FDH7PJH -m comment --comment "project-hamster/p2-service:" -j KUBE-SEP-6U447UXLLQIKP7BB

ssh cluster1-node1 iptables-save | grep p2-service

-A KUBE-SEP-6U447UXLLQIKP7BB -s 10.44.0.20/32 -m comment --comment "project-hamster/p2-service:" -j KUBE-MARK-MASQ
-A KUBE-SEP-6U447UXLLQIKP7BB -p tcp -m comment --comment "project-hamster/p2-service:" -m tcp -j DNAT --to-destination 10.44.0.20:80
-A KUBE-SERVICES ! -s 10.244.0.0/16 -d 10.97.45.18/32 -p tcp -m comment --comment "project-hamster/p2-service: cluster IP" -m tcp --dport 3000 -j KUBE-MARK-MASQ
-A KUBE-SERVICES -d 10.97.45.18/32 -p tcp -m comment --comment "project-hamster/p2-service: cluster IP" -m tcp --dport 3000 -j KUBE-SVC-2A6FNMCK6FDH7PJH
-A KUBE-SVC-2A6FNMCK6FDH7PJH -m comment --comment "project-hamster/p2-service:" -j KUBE-SEP-6U447UXLLQIKP7BB

ssh cluster1-node2 iptables-save | grep p2-service

-A KUBE-SEP-6U447UXLLQIKP7BB -s 10.44.0.20/32 -m comment --comment "project-hamster/p2-service:" -j KUBE-MARK-MASQ
-A KUBE-SEP-6U447UXLLQIKP7BB -p tcp -m comment --comment "project-hamster/p2-service:" -m tcp -j DNAT --to-destination 10.44.0.20:80
-A KUBE-SERVICES ! -s 10.244.0.0/16 -d 10.97.45.18/32 -p tcp -m comment --comment "project-hamster/p2-service: cluster IP" -m tcp --dport 3000 -j KUBE-MARK-MASQ
-A KUBE-SERVICES -d 10.97.45.18/32 -p tcp -m comment --comment "project-hamster/p2-service: cluster IP" -m tcp --dport 3000 -j KUBE-SVC-2A6FNMCK6FDH7PJH
-A KUBE-SVC-2A6FNMCK6FDH7PJH -m comment --comment "project-hamster/p2-service:" -j KUBE-SEP-6U447UXLLQIKP7BB
```

Now let's write these logs into the requested file:

```bash
ssh cluster1-controlplane1 iptables-save | grep p2-service >> /opt/course/p2/iptables.txt

ssh cluster1-node1 iptables-save | grep p2-service >> /opt/course/p2/iptables.txt

ssh cluster1-node2 iptables-save | grep p2-service >> /opt/course/p2/iptables.txt
```

**Delete the Service and confirm iptables rules are gone**

Delete the Service:

```bash
k delete svc p2-service -n project-hamster
```

Confirm the iptables rules are gone:

```bash
ssh cluster1-controlplane1 iptables-save | grep p2-service

ssh cluster1-node1 iptables-save | grep p2-service

ssh cluster1-node2 iptables-save | grep p2-service
```

### 3. Question

Use context: `kubectl config use-context k8s-c2-AC`

Create a Pod names `check-ip` in Namespace `default` using image `httpd:2.4.41-alpine`. Expose it on port 80 as a ClusterIP Service named `check-ip-service`. Remember/output the IP of that Service.

Change the service CIDR to `11.96.0.0/12` for the cluster.

Then create a second Service named `check-ip-service2` pointing to the same Pod to check if your settings did take effect. Finally check if the IP of the first Service has changed

#### Answer

Create the Pod and expose it:

```bash
k run check-ip --image=httpd:2.4.41-alpine

k expose pod check-ip --name check-ip-service --port 80
```

Check the Pod and Service ips:

```bash
k get svc,ep -l run=check-ip

NAME                       TYPE        CLUSTER-IP    EXTERNAL-IP   PORT(S)   AGE
service/check-ip-service   ClusterIP   10.104.3.45   <none>        80/TCP    8s

NAME                         ENDPOINTS      AGE
endpoints/check-ip-service   10.44.0.3:80   7s
```

Now we change the Service CIDR on the kube-apiserver:

```bash
ssh cluster2-controlplane1

vim /etc/kubernetes/manifests/kube-apiserver.yaml
```

```yaml
# /etc/kubernetes/manifests/kube-apiserver.yaml

apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  labels:
    component: kube-apiserver
    tier: control-plane
  name: kube-apiserver
  namespace: kube-system
spec:
  containers:
  - command:
    - kube-apiserver
    - --advertise-address=192.168.100.21
...
    - --service-account-key-file=/etc/kubernetes/pki/sa.pub
    - --service-cluster-ip-range=11.96.0.0/12             # change
    - --tls-cert-file=/etc/kubernetes/pki/apiserver.crt
    - --tls-private-key-file=/etc/kubernetes/pki/apiserver.key
...
```

**Give it a bit for the kube-apiserver and controller-manager to restart**

Wait for the api to be up again:

```bash
kubectl get pod -n kube-system | grep api

kube-apiserver-cluster2-controlplane1            1/1     Running   0              49s
```

Now we do the same for the controller manager:

```bash
vim /etc/kubernetes/manifests/kube-controller-manager.yaml
```

```yaml
# /etc/kubernetes/manifests/kube-controller-manager.yaml

apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  labels:
    component: kube-controller-manager
    tier: control-plane
  name: kube-controller-manager
  namespace: kube-system
spec:
  containers:
  - command:
    - kube-controller-manager
    - --allocate-node-cidrs=true
    - --authentication-kubeconfig=/etc/kubernetes/controller-manager.conf
    - --authorization-kubeconfig=/etc/kubernetes/controller-manager.conf
    - --bind-address=127.0.0.1
    - --client-ca-file=/etc/kubernetes/pki/ca.crt
    - --cluster-cidr=10.244.0.0/16
    - --cluster-name=kubernetes
    - --cluster-signing-cert-file=/etc/kubernetes/pki/ca.crt
    - --cluster-signing-key-file=/etc/kubernetes/pki/ca.key
    - --controllers=*,bootstrapsigner,tokencleaner
    - --kubeconfig=/etc/kubernetes/controller-manager.conf
    - --leader-elect=true
    - --node-cidr-mask-size=24
    - --requestheader-client-ca-file=/etc/kubernetes/pki/front-proxy-ca.crt
    - --root-ca-file=/etc/kubernetes/pki/ca.crt
    - --service-account-private-key-file=/etc/kubernetes/pki/sa.key
    - --service-cluster-ip-range=11.96.0.0/12         # change
    - --use-service-account-credentials=true
```

**Give it a bit for the scheduler to restart**

We can check if it was restarted using `crictl`:

```bash
crictl ps | grep scheduler

3d258934b9fd6    aca5ededae9c8    About a minute ago   Running    kube-scheduler ...
```

checking our existing Pod and Service aganin:

```bash
k get pod,svc -l run=check-ip
NAME           READY   STATUS    RESTARTS   AGE
pod/check-ip   1/1     Running   0          21m

NAME                       TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)   AGE
service/check-ip-service   ClusterIP   10.99.32.177   <none>        80/TCP    21m
```

Nothing changed so far. Now we create another Service like before:

```bash
k expose pod check-ip --name check-ip-service2 --port 80
```

Check again:

```bash
k get svc, ep -l run=check-ip

NAME                        TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)   AGE
service/check-ip-service    ClusterIP   10.109.222.111   <none>        80/TCP    8m
service/check-ip-service2   ClusterIP   11.111.108.194   <none>        80/TCP    6m32s

NAME                          ENDPOINTS      AGE
endpoints/check-ip-service    10.44.0.1:80   8m
endpoints/check-ip-service2   10.44.0.1:80   6m13s
```

### 4. Question

Upgrade the current version of kubernetes from `1.29.0` to `1.30.0` exactly using the `kubeadm` utility. Make sure that the upgrade is carried out one node at a time starting with the controlplane node. 

To minimiza downtime, the deployment `gold-nginx` should be rescheduled on an alternate node before upgrading each node.

Upgrade `controlplane` node first and drain node `node01` before upgrading it. Pods for `gold-nginx` should run on the `controlplane` node subsequently.

#### Answer

**On the Controlplane node**

```bash
vim /etc/apt/sources.list.d/kubernetes.list
```

Update the version in the URL to the next available minor release, v1.30

```bash
deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.30/deb/ /
```

```bash
kubectl drain controlplane --ignore-daemonsets

apt update

apt-cache madison kubeadm
```

Based on the version information displayed by `apt-cache madison`, it indicates that for kubernetes version `1.30.0`, the available package version is `1.30.0-1.-1`. Therefore, to install kubeadm for kubernetes, `v1.30.0`, use the following command:

```bash
apt-get install kubeadm=1.30.0-1.1
```

Upgrade the kubernetes cluster:

```bash
kubeadm upgrade plan v1.30.0

kubeadm upgrade apply v1.30.0
```

Now, upgrade the version and restart Kubelet. Also, mark the node (in this case, the "controlplane" node) as schedulable.

```bash
apt-get install kubelet=1.30.0-1.1

systemctl daemon-reload

systemctl restart kubelet

kubectl uncordon controlplane
```

Before draining `node01`, if the controlplane gets taint during an upgrade, we have to remove it.

```bash
# Identify the taint first. 
kubectl describe node controlplane | grep -i taint

# Remove the taint with help of "kubectl taint" command.
kubectl taint node controlplane node-role.kubernetes.io/control-plane:NoSchedule-

# Verify it, the taint has been removed successfully.  
kubectl describe node controlplane | grep -i taint
```

**On the node01 node**

`SSH` to the `node01` and perform the below steps as follows: -

Use any text editor you prefer to open the file that defines the Kubernetes apt repository.

```bash
vim /etc/apt/sources.list.d/kubernetes.list
```

Update the version in the URL to the next available minor release, i.e v1.30.

```bash
deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.30/deb/ /
```

After making changes, save the file and exit from your text editor. Proceed with the next instruction.

```bash
apt update

apt-cache madison kubeadm
```

Based on the version information displayed by apt-cache madison, it indicates that for Kubernetes version 1.30.0, the available package version is 1.30.0-1.1. Therefore, to install kubeadm for Kubernetes v1.30.0, use the following command:

```bash
apt-get install kubeadm=1.30.0-1.1

# Upgrade the node 
kubeadm upgrade node
```

Now, upgrade the version and restart Kubelet.

```bash
apt-get install kubelet=1.30.0-1.1

systemctl daemon-reload

systemctl restart kubelet
```

To exit from the specific node, type exit or logout on the terminal.

Back on the controlplane node:

```bash
kubectl uncordon node01

kubectl get pods -o wide | grep gold # make sure this is scheduled on a node
```

### 5. Question

Print the names of all deployments in the `admin2406` namespace in the following format:

DEPLOYMENT   CONTAINER_IMAGE   READY_REPLICAS   NAMESPACE

<deployment name>   <container image used>   <ready replica count>   <Namespace>

The data should be sorted by the increasing order of the deployment name.

Example:

DEPLOYMENT   CONTAINER_IMAGE   READY_REPLICAS   NAMESPACE

deploy0   nginx:alpine   1   admin2406

Write the result to the file `/opt/admin2406_data`.

#### Answer

```bash
kubectl get deployment -o custom-columns=DEPLOYMENT:.metadata.name,CONTAINER_IMAGE:.spec.template.spec.containers[].image,READY_REPLICAS:.status.readyReplicas,NAMESPACE:.metadata.namespace --sort-by=.metadata.name -n admin2406 > /opt/admin2406_data
```

### 6. Question

A kubeconfig file called `admin.kubeconfig` has been created in `/root/CKA`. There is something wrong with the configuration. Troubleshoot and fix it.

#### Answer

Make sure the port for the `kube-apiserver` is correct. So for this change port from `4380` to `6443`. 

```bash
kubectl cluster-info --kubeconfig /root/CKA/admin.kubeconfig
```

### 7. Question

Create a new deployment called `nginx-deploy`, with image `nginx:1.16` and `1` replica. Next upgrade the deployment to version `1.17` using rolling update.

#### Answer

Make use of the kubectl create command to create the deployment and explore the --record option while upgrading the deployment image.

```bash
kubectl create deployment  nginx-deploy --image=nginx:1.16
```

Run the below command to update the new image for nginx-deploy deployment and to record the version:

```bash
kubectl set image deployment/nginx-deploy nginx=nginx:1.17 --record
```

### 8. Question

A new deployment called `alpha-mysql` has been deployed in the `alpha` namespace. However, the pods are not running. Troubleshoot and fix the issue. The deployment should make use of the persistent volume `alpha-pv` to be mounted at `/var/lib/mysql` and should use the environment variable `MYSQL_ALLOW_EMPTY_PASSWORD=1` to make use of an empty root password.

Important: Do not alter the persistent volume.

#### Answer

Use the command kubectl describe and try to fix the issue.

Solution manifest file to create a pvc called mysql-alpha-pvc as follows:

```bash
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: mysql-alpha-pvc
  namespace: alpha
spec:
  accessModes:
  - ReadWriteOnce
  resources:
    requests:
      storage: 1Gi
  storageClassName: slow
```

### 9. Question

Take the backup of ETCD at the location `/opt/etcd-backup.db` on the controlplane node.

#### Answer

```bash
export ETCDCTL_API=3

etcdctl snapshot save --cacert=/etc/kubernetes/pki/etcd/ca.crt --cert=/etc/kubernetes/pki/etcd/server.crt --key=/etc/kubernetes/pki/etcd/server.key --endpoints=127.0.0.1:2379 /opt/etcd-backup.db
```

### 10. Question

Create a pod called `secret-1401` in the `admin1401` namespace using the `busybox` image. The container within the pod should be called `secret-admin` and should `sleep` for `4800` seconds.

The container should mount a `read-only` secret volume called `secret-volume` at the path /`etc/secret-volume`. The secret being mounted has already been created for you and is called dotfile-secret.

#### Answer

Use the command kubectl run to create a pod definition file. Add secret volume and update container name in it.

Alternatively, run the following command:

```bash
kubectl run secret-1401 --image=busybox --dry-run=client -oyaml --command -- sleep 4800 -n admin1401 > admin.yaml
```

Add the secret volume and mount path to create a pod called `secret-1401` in the `admin1401` namespace as follows:

```bash
---
apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  labels:
    run: secret-1401
  name: secret-1401
  namespace: admin1401
spec:
  volumes:
  - name: secret-volume
    # secret volume
    secret:
      secretName: dotfile-secret
  containers:
  - command:
    - sleep
    - "4800"
    image: busybox
    name: secret-admin
    # volumes' mount path
    volumeMounts:
    - name: secret-volume
      readOnly: true
      mountPath: "/etc/secret-volume"
```

