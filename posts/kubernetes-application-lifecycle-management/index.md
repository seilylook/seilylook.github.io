# Kubernetes Application Lifecycle Management


## Rolloing Updates and Roll Back

### Q. Let us try that. Upgrade the application by setting the image on the deployment to kodekloud/webapp-color:v2

Do not delete and re-create the deployment. Only set the new image name for the existing deployment.

Deployment Name: frontend

Deployment Image: kodekloud/webapp-color:v2

```bash
controlplane ~ ➜  kubectl edit deployment frontend

apiVersion: apps/v1
kind: Deployment
metadata:
  annotations:
    deployment.kubernetes.io/revision: "1"
  creationTimestamp: "2024-06-19T04:55:08Z"
  generation: 1
  name: frontend
  namespace: default
  resourceVersion: "897"
  uid: 4b75042c-8a82-42dd-86f9-c4cd41f4a8e8
spec:
  minReadySeconds: 20
  progressDeadlineSeconds: 600
  replicas: 4
  revisionHistoryLimit: 10
  selector:
    matchLabels:
      name: webapp
  strategy:
    rollingUpdate:
      maxSurge: 25%
      maxUnavailable: 25%
    type: RollingUpdate
  template:
    metadata:
      creationTimestamp: null
      labels:
        name: webapp
    spec:
      containers:
      - image: kodekloud/webapp-color:v2
        imagePullPolicy: IfNotPresent
        name: simple-webapp
        ports:
        - containerPort: 8080
          protocol: TCP
        resources: {}
        terminationMessagePath: /dev/termination-log
        terminationMessagePolicy: File
      dnsPolicy: ClusterFirst
      restartPolicy: Always
      schedulerName: default-scheduler
      securityContext: {}
      terminationGracePeriodSeconds: 30
status:
:wq

deployment.apps/frontend edited
```

### Q. Change the deployment strategy to `Recreate`.

Delete and re-create the deployment if neccessary. Only update the strategy type of the existing deployment.

Deployment Name: frontend

Deployment Image: kodekloud/webapp-color:v2

Strategy: Recreate

```bash
controlplane ~ ✖ kubectl edit deployment frontend

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: frontend
  namespace: default
spec:
  replicas: 4
  selector:
    matchLabels:
      name: webapp
  strategy:
    type: Recreate
  template:
    metadata:
      labels:
        name: webapp
    spec:
      containers:
      - image: kodekloud/webapp-color:v2
        name: simple-webapp
        ports:
        - containerPort: 8080
          protocol: TCP
:wq

deployment.apps/frontend edited
```

