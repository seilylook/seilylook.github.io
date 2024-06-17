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
