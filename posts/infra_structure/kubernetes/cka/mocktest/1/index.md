# Mock Test 1


### 1. Question

Deploy a pod named `nginx-pod` using the `nginx-alpine` image

#### Answer

```bash
k run nginx-pod --image=nginx:alpine
```

### 2. Question

Deploy a `messagine` pod using the `redis:alpine` image with the labels set to `tier=msg`

#### Answer

```bash
k run messaging --image=redis:alpine -l tier=msg
```

### 3. Question

Create a namespace named `apx-x9984574`

#### Answer

```bash
k create namespace apx-x9984574
```

### 4. Question

Get the list of nodes in JSON format and store it in a file at `/opt/outputs/nodes-z3444kd9.json`

#### Answer

```bash
kubectl get nodes -o json > /opt/outputs/nodes-z3444kd9.json
```

### 5. Question

Create a service `messaging-service` to expose the `messaging` application within the cluster on port `6379`.

#### Answer

```bash
k expose pod messaging --name messaging-service --port 6379
```

### 6. Question

Create a deployment named `hr-web-app` using the image `kodekloud/webapp-color` with `2` replicas.

#### Answer

```bash
k create deployment hr-web-app --image=kodekloud/webapp-color --replicas=2
```

### 7. Question

Create a static pod named `static-busybox` on the controlplane node that uses the `busybox` image and the command `sleep 1000`.

#### Answer

```bash
kubectl run --restart=Never --image=busybox static-busybox --dry-run=client -oyaml --command -- sleep 1000 > /etc/kubernetes/manifests/static-busybox.yaml
```

### 8. Question

Create a POD in the `finance` namespace named `temp-bus` with the image `redis:alpine`.

#### Answer

```bash
k run temp-bus --image=redis:alpine -n finance
```

### 9. Question

A new application `orange` is deployed. There is something wrong with it. Identify and fix the issue.

#### Answer

To know more details of `orange` pod:

```bash
k describe pod orange
```

`initContainers` section, There is an issue with the given command

```bash
k edit pod orange

k replace -f /tmp/kubectl-edit-xxxx.yaml
```

### 10. Question

Expose the `hr-web-app` as service `hr-web-app-service` application on port `30082` on the nodes on the cluster.

The web application listens on port `8080`.

#### Answer

```bash
kubectl expose deployment hr-web-app --type=NodePort --port=8080 --name=hr-web-app-service --dry-run=client -o yaml > hr-web-app-service.yaml
```

In generated service definition file add the `nodePort` field with the given port number under the `ports` section and create a service

### 11. Question

Use JSON PATH query to retrieve the `osImages` of all the nodes and store it in a file `/opt/outputs/nodes_os_x43kj56.txt`.

The `osImages` are under the `nodeInfo` section under `status` of each node.

#### Answer

```bash
kubectl get nodes -o jsonpath='{.items[*].status.nodeInfo.osImage}' > /opt/outputs/nodes_os_x43kj56.txt
```

### 12. Question

Create a `Persistent Volume` with the given specification: -

Volume name: `pv-analytics`

Storage: `100Mi`

Access mode: `ReadWriteMany`

Host path: `/pv/data-analytics`

#### Answer

```bash
vim pv-analytics.yaml
```

```yaml
---
apiVersion: v1
kind: PersistentVolume
metadata:
  name: pv-analytics
spec:
  capacity:
    storage: 100Mi
  volumeMode: Filesystem
  accessModes:
    - ReadWriteMany
  hostPath:
      path: /pv/data-analytics
```
