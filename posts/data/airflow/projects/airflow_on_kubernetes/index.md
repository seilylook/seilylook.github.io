# Airflow_on_kubernetes


## Install Helm chart

```bash
brew install helm
```

## Install the Chart

```bash
 {seilylook} 💎minikube start

 {seilylook} 💎helm repo add apache-airflow https://airflow.apache.org

"apache-airflow" has been added to your repositories

 {seilylook} 💎 helm repo list
NAME          	URL
apache-airflow	https://airflow.apache.org
```

## Upgrade the Chart

```bash
 {seilylook} 💎 helm upgrade --install airflow apache-airflow/airflow --namespace airflow --create-namespace

 {seilylook} 💎   ~/Development/Devlog   main ±  kubectl get pods -n airflow -o wide
NAME                                READY   STATUS    RESTARTS      AGE     IP            NODE       NOMINATED NODE   READINESS GATES
airflow-postgresql-0                1/1     Running   0             9m10s   10.244.0.9    minikube   <none>           <none>
airflow-redis-0                     1/1     Running   0             9m10s   10.244.0.8    minikube   <none>           <none>
airflow-scheduler-d4f745f94-bb8f6   2/2     Running   0             9m10s   10.244.0.5    minikube   <none>           <none>
airflow-statsd-b45f54fb4-5crk8      1/1     Running   0             9m10s   10.244.0.4    minikube   <none>           <none>
airflow-triggerer-0                 2/2     Running   0             9m10s   10.244.0.11   minikube   <none>           <none>
airflow-webserver-5664c7c9-sld8x    0/1     Running   1 (13s ago)   9m10s   10.244.0.6    minikube   <none>           <none>
airflow-worker-0                    2/2     Running   0             9m10s   10.244.0.10   minikube   <none>           <none>
```

To access the Airflow UI in browser we now need to port forward the `airflow-webserver`. We will use port `8080` 

### Forward the service 

```bash
 {seilylook} 💎   ~/Development/Devlog   main ±  kubectl get svc -n airflow         
NAME                    TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)             AGE
airflow-postgresql      ClusterIP   10.107.100.22   <none>        5432/TCP            10m
airflow-postgresql-hl   ClusterIP   None            <none>        5432/TCP            10m
airflow-redis           ClusterIP   10.110.71.17    <none>        6379/TCP            10m
airflow-statsd          ClusterIP   10.99.35.197    <none>        9125/UDP,9102/TCP   10m
airflow-triggerer       ClusterIP   None            <none>        8794/TCP            10m
airflow-webserver       ClusterIP   10.97.221.13    <none>        8080/TCP            10m
airflow-worker          ClusterIP   None            <none>        8793/TCP            10m
```

```bash
✘ {seilylook} 💎   ~/Development/Devlog   main ±  kubectl port-forward svc/airflow-webserver 8080:8080 -n airflow
Forwarding from 127.0.0.1:8080 -> 8080
Forwarding from [::1]:8080 -> 8080
```

Now head into browser to `localhost:8080` and we can see the **Airflow UI**.

## Load code/Dags to Airflow

Now we have Airflow running locally on Kubernetes, it is time to add your user code(a collection of python defined data pipeline). We are going to use a common methodology known as **Gitsync** which allows us to define a git repository that will be sync periodically with our application

### Add a test python DAG to github

1. Add test python DAG code in git repo: https://github.com/rarup1/airflow-demo-dags.git

2. Load `values.yaml` and change the `gitSync`

```bash
# Enter to the test dags folder
 {seilylook} 💎 cd airflow_demo_dags

# GET the values.yaml using Helm chart
 {seilylook} 💎 helm show values apache-airflow/airflow > values.yaml
```

```yaml
# airflow-demo-dags/values.yaml

  gitSync:
    enabled: true

    # git repo clone url
    # ssh example: git@github.com:apache/airflow.git
    # https example: https://github.com/apache/airflow.git
    repo: https://github.com/seilylook/Airflow_Demo_DAGS.git
    branch: main
    rev: HEAD
    # The git revision (branch, tag, or hash) to check out, v4 only
    ref: v2-2-stable
    depth: 1
    # the number of consecutive failures allowed before aborting
    maxFailures: 0
    # subpath within the repo where dags are located
    # should be "" if dags are at repo root
    subPath: ""
```

**enabled: true**

**repo: <DEMO_DAG_REPOSITRY>**

**subPath: ""** (if python code in in /root/)

### Synchronize to Github

```bash
 {seilylook} 💎 helm upgrade --install airflow apache-airflow/airflow -n airflow -f values.yaml --debug
```

### Check the Airflow webserver

```bash
 {seilylook} 💎 kubectl port-forward svc/airflow-webserver 8080:8080 --namespace airflow
```

### Add dependencies to airflow image

1. Add arequirements.txt file with the Airflow provider for dbt (as an example):

```text
apache-airflow-providers-dbt-cloud==3.6.0
```

2. Add a `Dockerfile` file:

```yaml
FROM apache/airflow:2.7.1-python3.11

COPY requirements.txt .

RUN pip install -r requirements.txt
```

3. Build the docker image and add to minikube:

```bash
 {seilylook} 💎 docker build -t my-airflow:1.0.0 .

 {seilylook} 💎 minikube image load my-airflow:1.0.0
```

4. Update `values.yaml`:

In order to our minikube k8s Airflow deployment to pick up the change in image(including our dbt provider) we need to amend our `values.yaml`:

```yaml
# Default airflow repository -- overridden by all the specific images below
defaultAirflowRepository: my-airflow

# Default airflow tag to deploy
defaultAirflowTag: "1.0.0"
```

**Push to Git**

5. ``helm upgrade`

```bash
 {seilylook} 💎 helm upgrade --install airflow apache-airflow/airflow -n airflow -f values.yaml --debug

 {seilylook} 💎 kubectl port-forward svc/airflow-webserver 8080:8080 --namespace airflow
```
