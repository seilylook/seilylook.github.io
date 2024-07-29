# Past Exam Questions


## 기출 문제 목록


### Pod에서 특정 log만 추출하여 파일로 저장

```bash
k logs Pod이름 | grep 에러메시지 > 저장 경로
```

- ServiceAccount 생성, Role 생성, Role Binding 생성 후 확인


### ETCD snapshot save & restore

#### Save ETCD

```bash
export ETCDCTL_API=3

etcdctl snapshot save --cacert=/etc/kubernetes/pki/etcd/ca.crt --cert=/etc/kubernetes/pki/etcd.server.crt --key=/etc/kubernetes/pki/etcd/server.key /opt/snapshot-pre-boot.db
```

#### Restore ETCD

```bash
export ETCDCTL_API=3

etcdutl snapshot restore /opt/snapshot-pre-boot.db --data-dir=/var/lib/etcd-from-backup
```

snapshot을 다른 디렉토리에 복원만 한 상태이다.

ETCD snapshot을 /var/lib/etcd-from-backup으로 복원했으므로 ETCD라는 볼륨에 대한 호스트 경로를 변경해야 한다.

```yaml
# /etc/kubernetes/manifests/etcd.yaml

volumes:
- name: etcd-data
  hostPath:
    path: /var/lib/etcd-from-backup
    type: DirectoryOrCreate
```

### Pod에 nodeSelector (disktype=ssd) 추가

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: nginx
spec:
  containers:
    - name: nginx
      image: nginx
  nodeSelector:
    disktype: ssd
```

### Pod를 생성하고 포트는 80, NodePort는 30020인 서비스를 배포

```bash
k run nginx-resolver --image=nginx

k expose pod nginx-resolver --name=nginx-resolver-service --port=80 --target-port=80 --type=NodePort
```

### Taint가 없는 Node의 개수를 파일로 저장

```bash
k get node # 노드 개수 3개 확인

k describe node | grep -i taint

echo '2' > 저장 경로
```

### Node의 상태가 ready 개수를 파일로 저장

[Kubectl Quick Reference](https://kubernetes.io/docs/reference/kubectl/quick-reference/)

**ready**로 검색을 하면 다음과 같은 json path를 알 수 있다.

```bash
# Check which nodes are ready
JSONPATH='{range .items[*]}{@.metadata.name}:{range @.status.conditions[*]}{@.type}={@.status};{end}{end}'

kubectl get nodes -o jsonpath="$JSONPATH" | grep "Ready=True" > 저장 경로

# Check which nodes are ready with custom-columns
kubectl get node -o custom-columns='NODE_NAME:.metadata.name,STATUS:.status.conditions[?(@.type=="Ready")].status' > 저장 경로
```

### 사용률이 가장 높은 Pod를 특정 label로만 조회해서 파일로 저장

```bash
# 특정 namespace에 control-plane label로 필터링해서 cpu로 정렬
k top pod -l tier=control-plane --sort-by=cpu -n kube-system

echo 노드 이름 > 저장 위치
```

### 특정 Node를 Pod를 다른 Node로 Reschedule하고 해당 Node는 SchedulingDisabled

```bash
# 특정 노드 이름 조회
k get node --show-labels | grep k8s-node-0

# Drain
k drain k8s-node-0 --ignore-daemonsets

k get node -o wide

k get pod -o wide
```

### 특정 Node가 NotReady 상태인데 Ready가 되도록 TroubleShooting

```bash
k get node

ssh node01

sudo -i

systemctl status kubelet 
# ... inactivate 상태 확인

systemctl restart kubelet

systemctl status kubelet
# ... active 상태 확인
```

### 특정 Deployment에 대해 replicas 수정

```bash
k scale deployment nginx-deployment --replicas=10
```

### 기존에 배포된 Pod에 새로운 Container 추가 (Sidecar 패턴)

```bash
# 기존 컨테이너에서 yaml 복사, 문제 번호 + log.yaml
k get pod eshop-cart-app -o yaml > 9-log.yaml

# yaml 검증
k apply -f 9-log.yaml --dry-run=server
# ... 문법 오류가 발생하지 않으면 Pod container의 추가 수정은 불가라고 뜬다.

# 적용을 위한 기존 Pod 제거
# delete 시 시간이 소요되어 즉시 삭제 옵션 추가 --force --grace-period 0
k delete pod eshop-cart-app --force --grace-period 0

k apply -f 9-log.yaml

# 로그 확인
k logs eshop-cart-app count-log-1
```

### 이미지 nginx 1.16으로 Deployment 생성 후 이미지를 nginx 1.17로 업그레이드 하기

```bash
k create deployment deploy-1 --image=nginx:1.16

k set image deployment deploy01 nginx=nginx:1.17
```
