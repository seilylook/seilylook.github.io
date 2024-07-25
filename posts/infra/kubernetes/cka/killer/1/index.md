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

Create a single Pod of image `httpd:2.4.41-alpine` in Namespace `default`. The Pod should be named `pod1` and the container should be named `pod1-container`. This Pod should only be scheduled on controlplane nodes. Do not add new labels to any nodes.

#### Answer

```bash
k describe node cluster1-controlplane | grep Taint
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
