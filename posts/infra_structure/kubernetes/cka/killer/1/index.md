# Killer.sh 1


### 1. Question

You have access to multiple clusters from your main terminal through kubectl contexts. Write all those context names into `/opt/course/1/contexts`.

Next write a command to display the current context into `/opt/course/1/context_default_kubectl.sh`, the command should use kubectl

Finally write a second command doing the same thing into `/opt/course/1/context_default_no_kubectl.sh`, but without the use of kubectl.

#### Answer

```bash
k config get-contexts -o name > /opt/course/1/contexts

echo 'kubectl config current-context' > /opt/course/1/context_default_kubectl.sh

cat ~/.kube/config | grep current | sed -e "s/current-context: //"
```

### 2. Question

Create a single Pod of image `httpd:2.4.41-alpine` in Namespace `default`.

The Pod should be named `pod1` and the container should be named `pod1-container`. 

This Pod should only be scheduled on controlplane nodes. Do not add new labels to any nodes.

#### Answer

```bash
k describe node cluster1-controlplane1 | grep Taint
```

```yaml
# pod1.yaml
apiVersion: v1
kind: Pod
metadata:
  name: pod1
spec:
  containers:
    - name: pod1-container
      image: httpd:2.4.41-alpine
  tolerations:
    - key: "node-role.kubernetes.io/control-plane"
      operator: "Exists"
      effect: "NoSchedule"
```

### 3. Question

There are tow Pods named `o3db` in Namespace `project-c13`.

C13 management asked you to scale the Pods down to one replica to save resources.

#### Answer

```bash
k scale sts o3db --replicas=1 -n project-c13
```

### 4. Question

Do the following in Namespace default.

Create a single Pod named `ready-if-service-ready` of image `nginx:1.16.1-alpine`. 

Configure a LivenessProve which simply executes command true.

Also configure a ReadinessProbe which does check if the url `http://service-am-i-ready:90` is reachable, you can use wget -Y2 -O -https://service-am-i-ready:80 for this. 

Start the pod and confirm it isn't ready because of the ReadinessProbe.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: ready-if-service-ready
  labels:
    run: ready-if-service-ready
spec:
  containers:
    - name: ready-if-service-ready
      image: nginx:1.16.1-apline
      livenessProbe:
        exec:
          command:
            - 'true'
      readinessProbe:
        exec:
          command:
            - sh
            - -c
            - 'wget -T2 -O- http://service-am-i-ready:80'
```

Create a second Pod naemd `am-i-ready` of image `nginx:1.16.1-alpine` with label `id: cross-service-ready`. 

The already existing Service `service-am-i-ready` should now have that second Pod as endpoint.

```bash
k run am-i-ready --image=nginx:1.16.1-alpine --label=id=cross-service-ready
```

### 5. Question

There are various Pods in all namespaces. Write a command into `/opt/course/5/find_pods.sh` which lists all Pods sorted by their `AGE(metadata.creationTimestamp)`

```bash
echo 'kubectl get pods --all-namespaces --sort-by=.metadata.creationTimestamp' > /opt/course/5/find_pods.sh
```

Write a second command into `/opt/course/5/find_pods_uid.sh` which lists all Pods sorted by field `metadata.uid`. Use kubeclt sorting for both commands.

```bash
echo 'kubeclt get pods --all-namespaces --sort-by=.metadata.uid' > /opt/course/5/find_pods_uid.sh
```

### 6. Question

Create a new PersistentVolume named `safari-pv`. It should have a capacity of `2Gi`, accessMode `ReadWrtieOnce`, hostPath `/Volumes/Data` and no storageClassName defined.

```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: safari-pv
spec:
  accessModes:
    - ReadWriteOnce
  capacity:
    storage: 2Gi
  hostPath:
    path: /Volumes/Data
```

Next create a new PersistentVolumeClaim in Namespace `project-tiger` named `safari-pvc`. It should request `2Gi` storage, accessMode `ReadWriteOnce` and should not define a storageClassName. The PVC should bound to the PV correctly.

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: safari-pvc
  namespace: project-tiger
spec:
  accessModes:
    - ReadWrtieOnce
  resources:
    requests:
      storage: 2Gi
```

Finally create a new Deployment `safari` in Namespace `project-tiger` which mounts that volume at `/tmp/safari-data`. The Pods of that Deployment should be of image `httpd:2.4.41-alpine`.

```bash
k create deployment safari --image=httpd:2.4.41-alpine -n project-tiger --dry-run=client -o yaml > safari-deploy.yaml
```

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  creationTimestamp: null
  labels:
    app: safari
  name: safari
  namespace: project-tiger
spec:
  replicas: 1
  selector:
    matchLabels:
      app: safari
  strategy: {}
  template:
    metadata:
      creationTimestamp: null
      labels:
        app: safari
    spec:
      containers:
      - image: httpd:2.4.41-alpine
        name: httpd
        volumeMounts:
          - name: safari-data
            mountPath: /tmp/safari-data
      volumes:
        - name: safari-data
          persistentVolumeClaim:
            claimName: safari-pvc
        resources: {}
status: {}
```

### 7. Question

The metrics-server has been installed in the cluster. Your college would like to know the kubectl commands to:

1. Show Nodes resource usage

2. Show Pods and their containers resource usage

Please write the commands into `/opt/course/7/node.sh` and `/opt/sourse/7/pod.sh`.

```bash
echo 'k top node' > /opt/course/7/node.sh
```
```bash
echo 'k top pod --containers=true' > /opt/course/7/pod.sh
```

### 8. Question

SSH into the controlplane node with `ssh cluster1-controlplane1`. 

Check how the controlplane components `kubelet`, `kube-apiserver`, `kube-scheduler`, `kube-controller-manager` and `etcd` are started/installed on the controlplane node.

Also find out the name of the `DNS application` and how it's started/installed on the controlplane node.

Write the findings into file `/opt/course/8/controlplane-components.txt`. The file should be structured like:

```txt
# /opt/course/8/controlplane-components.txt

kubelet: [TYPE]
kube-apiserver: [TYPE]
kube-scheduler: [TYPE]
kube-controller-manager: [TYPE]
etcd: [TYPE]
dns: [TYPE][NAME]
```

#### Answer

```txt
kubelet: process
kube-apiserver: static-pod
kube-scheduler: static-pod
kube-controller-manager: static-pod
etcd: static-pod
dns: pod coredns
```

### 9. Question

Create a new ServiceAccount `processor` in Namespace `project-hamster`. 

Create a Role and RoleBinding, both named processor as well.

These should allow the new SA to only `create` `Secrets` and `ConfigMaps` in that Namespace.

#### Answer

```bash
k create serviceaccount processor -n project-hamster

k create role processor --verb=create --resources=secret,configmap -n project-hamster

k create rolebinding processor --role=processor --serviceaccount=project-hamster:processor
```


