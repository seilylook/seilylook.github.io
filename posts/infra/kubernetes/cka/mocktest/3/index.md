# Mock Test 3


### 1. Question

Create a new service account with the name `pvviewer`. 

Grant this Service account access to `list` all PersistentVolumes in the cluster by creating an appropriate cluster role called `pvviewer-role` and ClusterRoleBinding called `pvviewer-role-binding`.

Next, create a pod called `pvviewer` with the image: `redis` and serviceAccount: `pvviewer` in the default namespace.

#### Answer

Pods authenticate to the API Server using ServiceAccounts. If the serviceAccount name is not specified, the default service account for the namespace is used during a pod creation.

Now, create a service account pvviewer:

```bash
kubectl create serviceaccount pvviewer
```

To create a clusterrole:

```bash
kubectl create clusterrole pvviewer-role --resource=persistentvolumes --verb=list
```

To create a clusterrolebinding:

```bash
kubectl create clusterrolebinding pvviewer-role-binding --clusterrole=pvviewer-role --serviceaccount=default:pvviewer
```

Solution manifest file to create a new pod called pvviewer as follows:

```yaml
---
apiVersion: v1
kind: Pod
metadata:
  name: pvviewer
spec:
  containers:
    - image: redis
      name: pvviewer
  serviceAccountName: pvviewer
```

### 2. Question

List the `InternalIP` of all nodes of the cluster. Save the result to a file `/root/CKA/node_ips`.

Answer should be in the format: `InternalIP of controlplane`<space>`InternalIP of node01` (in a single line)

#### Answer

```bash
k get nodes -o jsonpath='{.items[*].status.addresses[?(@.type=="InternalIP")].address}'
```

### 3. Question

Create a pod called `multi-pod` with two containers.

Container 1: name: `alpha`, image: `nginx`

Container 2: name: `beta`, image: `busybox`, command: `sleep 4800`

Environment Variables:

container 1:
name: `alpha`

Container 2:
name: `beta`

#### Answer

Solution manifest file to create a multi-container pod multi-pod as follows:

```yaml
---
apiVersion: v1
kind: Pod
metadata:
  name: multi-pod
spec:
  containers:
    - name: alpha
      image: nginx
      env:
        - name: name
          value: alpha
    - name: beta
      image: busybox
      env:
        - name: name
          value: beta
      command: ["sleep", "4800"]
```

### 4. Question

Create a Pod called `non-root-pod` , image: `redis:alpine`

runAsUser: 1000

fsGroup: 2000

#### Answer

```yaml
---
apiVersion: v1
kind: Pod
metadata:
  name: non-root-pod
spec:
  containers:
    - name: non-root-pod
      image: redis:alpine
  securityContext:
    runAsUser: 1000
    fsGroup: 2000
```

Verify the user and group IDs by using below command:

```bash
kubectl exec -it non-root-pod -- id
```

### 5. Question

We have deployed a new pod called `np-test-1` and a service called `np-test-service`.

Incoming connections to this service are not working. Troubleshoot and fix it.

Create NetworkPolicy, by the name `ingress-to-nptest` that allows incoming connections to the service over port `80`.

#### Answer

Solution manifest file to create a network policy ingress-to-nptest as follows:

```yaml
---
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: ingress-to-nptest
spec:
  podSelector:
    matchLabels:
      run: np-test-1
  policyTypes:
    - Ingress
  ingress:
    - ports:
      - protocol: TCP
        port: 80
```

### 6. Question

Taint the worker node `node01` to be Unschedulable. 

Once done, create a pod called `dev-redis`, image `redis:alpine`, to ensure workloads are not scheduled to this worker node. 

Finally, create a new pod called `prod-redis` and image: `redis:alpine `with toleration to be scheduled on `node01`.

key: `env_type`, value: `production`, operator: `Equal` and effect: `NoSchedule`

#### Answer

To add taints on the node01 worker node:

```bash
kubectl taint node node01 env_type=production:NoSchedule
```

Now, deploy dev-redis pod and to ensure that workloads are not scheduled to this node01 worker node.

```bash
kubectl run dev-redis --image=redis:alpine
```

To view the node name of recently deployed pod:

```bash
kubectl get pods -o wide
```

Solution manifest file to deploy new pod called prod-redis with toleration to be scheduled on node01 worker node.

```yaml
---
apiVersion: v1
kind: Pod
metadata:
  name: prod-redis
spec:
  containers:
    - name: prod-redis
      image: redis:alpine
  tolerations:
    - key: env_type
      value: production
      operator: Equal
      effect: NoSchedule    
```

To view only prod-redis pod with less details:

```bash
kubectl get pods -o wide | grep prod-redis
```

### 7. Question

Create a pod called `hr-pod` in `hr` namespace belonging to the `production environment` and `frontend tier`, image: `redis:alpine`.

Use appropriate labels and create all the required objects if it does not exist in the system already.

#### Answer

Create a namespace if it doesn't exist:

```bash
kubectl create namespace hr
```

and then create a hr-pod with given details:

```bash
kubectl run hr-pod --image=redis:alpine --namespace=hr --labels=environment=production,tier=frontend
```

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: hr-pod
  labels:
    environment: production
    tier: frontend
spec:
  containers:
    - name: hr-pod
      image: redis:alpine
```

### 8. Question

A kubeconfig file called `super.kubeconfig` has been created under `/root/CKA`. There is something wrong with the configuration. Troubleshoot and fix it.

#### Answer

Verify host and port for kube-apiserver are correct.

Open the super.kubeconfig in vi editor.

Change the 9999 port to `6443` and run the below command to verify:

```bash
kubectl cluster-info --kubeconfig=/root/CKA/super.kubeconfig
```

### 9. Question

We have created a new deployment called `nginx-deploy`. 

scale the deployment to `3 replicas`. Has the replica's increased? 

Troubleshoot the issue and fix it.

#### Answer

Use the command kubectl scale to increase the replica count to 3.

```bash
kubectl scale deploy nginx-deploy --replicas=3
```

The controller-manager is responsible for scaling up pods of a replicaset. 

If you inspect the control plane components in the kube-system namespace, you will see that the controller-manager is not running.

```bash
kubectl get pods -n kube-system
```

The command running inside the controller-manager pod is incorrect.

After fix all the values in the file and wait for controller-manager pod to restart.

```bash
vim /etc/kubernetes/manifests/kube-controller-manager.yaml
```

`kube-contro1ler-manager` -> `kube-controller-manager`

This will fix the issues in controller-manager yaml file.

At last, inspect the deployment by using below command:

```bash
kubectl get deploy
```
