# Mock Test 2


### 1. Question

Take a backup of the etcd cluster and save it to `/opt/etcd-backup.db`.

#### Answer

```bash
export ETCDCTL_API=3

etcdctl snapshot save --endpoints https://[127.0.0.1]:2379 --cacert=/etc/kubernetes/pki/etcd/ca.crt --cert=/etc/kubernetes/pki/etcd/server.crt --key=/etc/kubernetes/pki/etcd/server.key  /opt/etcd-backup.db
```

### 2. Question

Create a Pod called `redis-storage` with image: `redis:alpine` with a Volume of type `emptyDir` that lasts for the life of the Pod.

#### Answer

Use the command `kubectl run` and create a pod definition file for `redis-storage` pod and add volume.

```bash
kubectl run redis-storage --image=redis:alpine --dry-run=client -o yaml > redis-storage.yaml
```

add the volume `emptyDir` in it.

```yaml
---
apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  labels:
    run: redis-storage
  name: redis-storage
spec:
  containers:
  - image: redis:alpine
    name: redis-storage
    volumeMounts:
    - mountPath: /data/redis
      name: temp-volume
  volumes:
  - name: temp-volume
    emptyDir: {}
```

### 3. Question

Create a new pod called `super-user-pod` with image `busybox:1.28`. Allow the pod to be able to set `system_time`.

The container should sleep for 4800 seconds.

#### Answer

```yaml
---
apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  labels:
    run: super-user-pod
  name: super-user-pod
spec:
  containers:
  - command:
    - sleep
    - "4800"
    image: busybox:1.28
    name: super-user-pod
    securityContext:
      capabilities:
        add: ["SYS_TIME"]
  dnsPolicy: ClusterFirst
  restartPolicy: Always
```

### 4. Question

A pod definition file is created at `/root/CKA/use-pv.yaml`. Make use of this manifest file and mount the persistent volume called `pv-1`. Ensure the pod is running and the PV is bound.

mountPath: `/data`

persistentVolumeClaim Name: `my-pvc`

#### Answer

Add a `persistentVolume` definition to pod definition file.

```yaml
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: my-pvc
spec:
  accessModes:
  - ReadWriteOnce
  resources:
    requests:
       storage: 10Mi
```

Update the pod definition file

```yaml
apiVersion: v1
kind: Pod
metadata:
  creationTimestamp: null
  labels:
    run: use-pv
  name: use-pv
spec:
  containers:
  - image: nginx
    name: use-pv
    volumeMounts:
    - mountPath: "/data"
      name: mypd
  volumes:
    - name: mypd
      persistentVolumeClaim:
        claimName: my-pvc
```

### 5. Question

Create a new deployment called `nginx-deploy`, with image `nginx:1.16` and `1` replica. Next upgrade the deployment to version `1.17` using rolling update.

#### Answer

```bash
k create deployment nginx-deploy --image=nginx:1.16 --replicas=1

k edit deployment nginx-deploy
```

### 6. Question

Create a new user called `john`. Grant him access to the cluster. John should have permission to `create, list, get, update and delete pods` in the `development` namespace . The private key exists in the location: `/root/CKA/john.key` and csr at `/root/CKA/john.csr`.

Important Note: As of kubernetes 1.19, the CertificateSigningRequest object expects a `signerName`.

#### Answer

```bash
ls /CKA
john.csr    john.key    use-pv.yaml

cat john.csr | base64 | tr -d "\n"
```

```yaml
---
apiVersion: certificates.k8s.io/v1
kind: CertificateSigningRequest
metadata:
  name: john-developer
spec:
  signerName: kubernetes.io/kube-apiserver-client
  request: <PASTE_IT_HERE>
  usages:
  - digital signature
  - key encipherment
  - client auth
```

To approve this certificate,

`kubectl certificate approve john-developer`

Create a role `developer` and rolebinding `developer-role-binding`

```bash
$ kubectl create role developer --resource=pods --verb=create,list,get,update,delete --namespace=development

$ kubectl create rolebinding developer-role-binding --role=developer --user=john --namespace=development
```

Verify the permission

```bash
$ kubectl auth can-i update pods --as=john --namespace=development
```


### 7. Question

Create a nginx pod called `nginx-resolver` using image `nginx`, expose it internally with a service called `nginx-resolver-service`. 

Test that you are able to look up the service and pod names from within the cluster. Use the image: `busybox:1.28` for dns lookup. Record results in `/root/CKA/nginx.svc` and `/root/CKA/nginx.pod`

#### Answer

Use the command kubectl run and create a nginx pod and busybox pod. Resolve it, nginx service and its pod name from busybox pod.

To create a pod nginx-resolver and expose it internally:

```bash
kubectl run nginx-resolver --image=nginx
kubectl expose pod nginx-resolver --name=nginx-resolver-service --port=80 --target-port=80 --type=ClusterIP
```
To create a pod test-nslookup. Test that you are able to look up the service and pod names from within the cluster:

```bash
kubectl run test-nslookup --image=busybox:1.28 --rm -it --restart=Never -- nslookup nginx-resolver-service
kubectl run test-nslookup --image=busybox:1.28 --rm -it --restart=Never -- nslookup nginx-resolver-service > /root/CKA/nginx.svc
```

Get the IP of the nginx-resolver pod and replace the dots(.) with hyphon(-) which will be used below.

```bash
kubectl get pod nginx-resolver -o wide
kubectl run test-nslookup --image=busybox:1.28 --rm -it -
```


### 8. Question

Create a static pod on `node01` called `nginx-critical` with image `nginx` and make sure that it is recreated/restarted automatically in case of a failure.

Use `/etc/kubernetes/manifests` as the Static Pod path for example.

#### Answer

To create a static pod called nginx-critical by using below command:

```bash
kubectl run nginx-critical --image=nginx --dry-run=client -o yaml > static.yaml
```

Copy the contents of this file or use scp command to transfer this file from controlplane to node01 node.

```bash
root@controlplane:~# scp static.yaml node01:/root/
```

To know the IP Address of the node01 node:

```bash
root@controlplane:~# kubectl get nodes -o wide

# Perform SSH
root@controlplane:~# ssh node01
OR
root@controlplane:~# ssh <IP of node01>
```

On node01 node:

Check if static pod directory is present which is /etc/kubernetes/manifests, if it's not present then create it.

```bash
root@node01:~# mkdir -p /etc/kubernetes/manifests
```

Add that complete path to the staticPodPath field in the kubelet config.yaml file.

```bash
root@node01:~# vi /var/lib/kubelet/config.yaml
```

now, move/copy the static.yaml to path /etc/kubernetes/manifests/.

```bash
root@node01:~# cp /root/static.yaml /etc/kubernetes/manifests/
```

Go back to the controlplane node and check the status of static pod:

```bash
root@node01:~# exit
logout
root@controlplane:~# kubectl get pods 
```
