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
