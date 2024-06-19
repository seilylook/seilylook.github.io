# Kubernetes Logging & Monitoring


## Monitoring Cluster Components

### Q. Identify the POD that comsume the most Memory(bytes) in default namespace.

```bash
controlplane kubernetes-metrics-server on  master ➜  kubectl top pod
NAME       CPU(cores)   MEMORY(bytes)   
elephant   14m          32Mi            
lion       1m           18Mi            
rabbit     97m          252Mi 

controlplane kubernetes-metrics-server on  master ➜  kubectl top pod --sort-by='memory' --no-headers | head -1
rabbit     99m   232Mi   
```

> A. rabbit

### Q. Identify the POD that consumes the least CPU(cores) in default namespace.

```bash
controlplane kubernetes-metrics-server on  master ➜  kubectl top pod
NAME       CPU(cores)   MEMORY(bytes)   
elephant   14m          32Mi            
lion       1m           18Mi            
rabbit     100m         252Mi           

controlplane kubernetes-metrics-server on  master ➜  kubectl top pod --sort-by='cpu' --no-headers | tail -1
lion       1m    18Mi
```

> A. lion

## Managing Application Logs

### Q. A user - USER5 - has expressed concerns accessing the application. Identify the cause of the issue.

```bash
controlplane ~ ➜  kubectl get pods
NAME       READY   STATUS    RESTARTS   AGE
webapp-1   1/1     Running   0          13s

controlplane ~ ✖ kubectl logs webapp-1
[2024-06-19 04:16:41,715] INFO in event-simulator: USER4 is viewing page2
[2024-06-19 04:16:42,716] INFO in event-simulator: USER1 logged in
[2024-06-19 04:16:43,717] INFO in event-simulator: USER1 is viewing page3
[2024-06-19 04:16:44,719] INFO in event-simulator: USER3 is viewing page3
[2024-06-19 04:16:45,720] INFO in event-simulator: USER1 is viewing page2
[2024-06-19 04:16:46,721] WARNING in event-simulator: USER5 Failed to Login as the account is locked due to MANY FAILED ATTEMPTS.
```

### Q. A user is reporting issues while trying to purchase an item. Identify the user and the cause of the issue.

```bash
controlplane ~ ➜  kubectl get pods
NAME       READY   STATUS    RESTARTS   AGE
webapp-1   1/1     Running   0          3m27s
webapp-2   2/2     Running   0          11s

controlplane ~ ➜  kubectl logs webapp-2
Defaulted container "simple-webapp" out of: simple-webapp, db
[2024-06-19 04:19:55,002] INFO in event-simulator: USER2 is viewing page3
[2024-06-19 04:19:56,003] INFO in event-simulator: USER2 is viewing page1
[2024-06-19 04:19:57,004] INFO in event-simulator: USER2 is viewing page3
[2024-06-19 04:19:58,005] INFO in event-simulator: USER3 logged in
[2024-06-19 04:19:59,007] INFO in event-simulator: USER1 logged in
[2024-06-19 04:20:00,008] WARNING in event-simulator: USER5 Failed to Login as the account is locked due to MANY FAILED ATTEMPTS.
[2024-06-19 04:20:00,008] INFO in event-simulator: USER3 logged in
[2024-06-19 04:20:01,010] INFO in event-simulator: USER3 logged in
[2024-06-19 04:20:02,010] INFO in event-simulator: USER1 is viewing page1
[2024-06-19 04:20:03,012] WARNING in event-simulator: USER30 Order failed as the item is OUT OF STOCK.
[2024-06-19 04:20:03,012] INFO in event-simulator: USER4 is viewing page3
[2024-06-19 04:20:04,013] INFO in event-simulator: USER4 is viewing page2
[2024-06-19 04:20:05,014] WARNING in event-simulator: USER5 Failed to Login as the account is locked due to MANY FAILED ATTEMPTS.
[2024-06-19 04:20:05,015] INFO in event-simulator: USER1 logged in
[2024-06-19 04:20:06,016] INFO in event-simulator: USER1 is viewing page2
[2024-06-19 04:20:07,016] INFO in event-simulator: USER2 logged out
[2024-06-19 04:20:08,017] INFO in event-simulator: USER1 is viewing page2
[2024-06-19 04:20:09,018] INFO in event-simulator: USER1 is viewing page2
```
