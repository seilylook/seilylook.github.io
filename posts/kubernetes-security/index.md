# Kubernetes Security


## [What is SSL](https://www.notion.so/f21c4e51bc63459cacf9df894b99ec89?pvs=4#01dc08d0a59642b49567b68233e6e89d)

## Word Convention

|Public key|Private key|
|:--------:|:---------:|
|*.crt / *.pem|*.key / *-key.pem|
|server.crt|server.key|
|server.pem|server-key.pem|
|client.crt|client.key|
|client.pem|client-key.pem|

## View Certificate Details

### Q. Indentify the certificate file used for the kube-api server

```bash
controlplane ~ ➜  cat /etc/kubernetes/manifests/kube-apiserver.yaml

    - --tls-cert-file=/etc/kubernetes/pki/apiserver.crt

```

### Q. Identify the Certificate file used to authenticate kube-apiserver as a client to ETCD server

```bash
controlplane ~ ➜  cat /etc/kubernetes/manifests/kube-apiserver.yaml

    - --etcd-certfile=/etc/kubernetes/pki/apiserver-etcd-client.crt
```

### Q. Identify the key used to authenticate kubeapi-server to the kubelet server

```bash
controlplane ~ ➜  cat /etc/kubernetes/manifests/kube-apiserver.yaml

    - --kubelet-client-key=/etc/kubernetes/pki/apiserver-kubelet-client.key
```

### Q. Identify the ETCD Server Certificate used to host ETCD server

```bash
controlplane ~ ➜  cat /etc/kubernetes/manifests/etcd.yaml

    - --cert-file=/etc/kubernetes/pki/etcd/server.crt
```

### Q. Identify the ETCD Server CA Root Certificate used to serve ETCD Server

ETCD can have its own CA. So this may be a different CA certificate than the one used by kube-api server.

```bash
controlplane ~ ➜  cat /etc/kubernetes/manifests/etcd.yaml

    - --trusted-ca-file=/etc/kubernetes/pki/etcd/ca.crt
```

### Q. What is the Common Name(CN) configured on the Kube API Server Certificate?

OpenSSL Syntax: `openssl x509 -in file-path.crt -text -noout`

```bash
controlplane ~ ✖ openssl x509 -in /etc/kubernetes/pki/apiserver.crt -text

        Subject: CN = kube-apiserver
```

### Q. What is the name of the CA who issued the Kube API Server Certificate?

```bash
controlplane ~ ✖ openssl x509 -in /etc/kubernetes/pki/apiserver.crt -text

        Issuer: CN = kubernetes
```

### Q. Which of the below alternate names is not configured on the Kube API Server Certificate?

```bash
controlplane ~ ✖ openssl x509 -in /etc/kubernetes/pki/apiserver.crt -text

        X509v3 Subject Alternative Name: 
                        DNS:controlplane, DNS:kubernetes, DNS:kubernetes.default, DNS:kubernetes.default.svc, DNS:kubernetes.default.svc.cluster.local, IP Address:10.96.0.1, IP Address:192.12.87.9
```

### Q. What is the Common Name(CN) configured on the ETCD Server certificate?

```bash
controlplane ~ ➜  openssl x509 -in /etc/kubernetes/pki/etcd/server.crt -text

        Subject: CN = controlplane
```

### Q. How long, from the issued date, is the Kube-API Server Certificate valid for?

```bash
controlplane ~ ➜  openssl x509 -in /etc/kubernetes/pki/apiserver.crt -text

        Validity
            Not Before: Jun 25 06:30:33 2024 GMT
            Not After : Jun 25 06:35:33 2025 GMT
```

### Q. How long, from the issued date, is the Root CA Certificate valid for?

```bash
controlplane ~ ➜  openssl x509 -in /etc/kubernetes/pki/ca.crt -text

        Validity
            Not Before: Jun 25 06:30:33 2024 GMT
            Not After : Jun 23 06:35:33 2034 GMT
```

### Q. Kubectl suddenly stops responding to your commands. Check it out! Someone recently modified the /etc/kubernetes/manifests/etcd.yaml file

You are asked to investigate and fix the issue. Once you fix the issue wait for sometime for kubectl to respond. Check the logs of the ETCD container.

```bash
controlplane ~ ➜  vim /etc/kubernetes/manifests/etcd.yaml

    - --cert-file=/etc/kubernetes/pki/etcd/server.crt
:wq!

controlplane ~ ➜  ls -l /etc/kubernetes/pki/etcd/server* | grep .crt
-rw-r--r-- 1 root root 1208 Jun 25 06:35 /etc/kubernetes/pki/etcd/server.crt
```

### Q. The kube-api server stopped again! Check it out. Inspect the kube-api server logs and identify the root cause and fix the issue.

Run crictl ps -a command to identify the kube-api server container. Run crictl logs container-id command to view the logs.

```bash
root@controlplane:~# crictl ps -a | grep kube-apiserver
1fb242055cff8       529072250ccc6       About a minute ago   Exited              kube-apiserver            3                   ed2174865a416       kube-apiserver-controlplane

root@controlplane:~# crictl logs --tail=2 1fb242055cff8  
W0916 14:19:44.771920       1 clientconn.go:1331] [core] grpc: addrConn.createTransport failed to connect to {127.0.0.1:2379 127.0.0.1 <nil> 0 <nil>}. Err: connection error: desc = "transport: authentication handshake failed: x509: certificate signed by unknown authority". Reconnecting...
E0916 14:19:48.689303       1 run.go:74] "command failed" err="context deadline exceeded"
```

This indicates an issue with the ETCD CA certificate used by the `kube-apiserver`. Correct it to use the file `/etc/kubernetes/pki/etcd/ca.crt`.

### Q. The kube-api server stopped again! Check it out. Inspect the kube-api server logs and identify the root cause and fix the issue.

Run crictl ps -a command to identify the kube-api server container. Run crictl logs container-id command to view the logs.

If we inspect the kube-apiserver container on the controlplane, we can see that it is frequently exiting.

```bash
root@controlplane:~# crictl ps -a | grep kube-apiserver
1fb242055cff8       529072250ccc6       About a minute ago   Exited              kube-apiserver            3                   ed2174865a416       kube-apiserver-controlplane
```

If we now inspect the logs of this exited container, we would see the following errors:

```bash
root@controlplane:~# crictl logs --tail=2 1fb242055cff8  
W0916 14:19:44.771920       1 clientconn.go:1331] [core] grpc: addrConn.createTransport failed to connect to {127.0.0.1:2379 127.0.0.1 <nil> 0 <nil>}. Err: connection error: desc = "transport: authentication handshake failed: x509: certificate signed by unknown authority". Reconnecting...
E0916 14:19:48.689303       1 run.go:74] "command failed" err="context deadline exceeded"
```

This indicates an issue with the ETCD CA certificate used by the kube-apiserver. Correct it to use the file `/etc/kubernetes/pki/etcd/ca.crt`.

```bash
controlplane ~ ➜  vim /etc/kubernetes/manifests/kube-apiserver.yaml

    - --etcd-cafile=/etc/kubernetes/pki/etcd/ca.crt
```

## Certificates API

### Q. Create a CertificateSigningRequest object with the name akshay with the contents of the akshay.csr file

As of kubernetes 1.19, the API to use for CSR is certificates.k8s.io/v1.

Please note that an additional field called signerName should also be added when creating CSR. For client authentication to the API server we will use the built-in signer kubernetes.io/kube-apiserver-client.

Use the command to generate the base64 encoded format on following:

```bash
cat akshay.csr | base64 -w 0
```

```bash
vim akshay-csr.yaml
```

```yaml
apiVersion: certificates.k8s.io/v1
kind: CertificateSigningRequest
metadata:
  name: akshay
spec:
  groups:
  - system:authenticated
  request: LS0tLS1CRUdJTiBDRVJUSUZJQ0FURSBSRVFVRVNULS0tLS0KTUlJQ1ZqQ0NBVDRDQVFBd0VURVBNQTBHQTFVRUF3d0dZV3R6YUdGNU1JSUJJakFOQmdrcWhraUc5dzBCQVFFRgpBQU9DQVE4QU1JSUJDZ0tDQVFFQXhpMG1FbS80OEUwZHRmbCtSajg0R1ZGRHVhdTdOQVpHMGprcUwrU2wxd2o3ClFJQkdQV1l3OHY5YmZvRExpVTBlRnUrTC9NRTduNWlZOHVTRG9Pd3pEQldralZoK1I2SEVEblVkOHZ2eTNSZUsKbk5BV202V0tSVS9JM3A0cmU0dUViYzZ2ajgrVnFlSVhvQ1ZsczJnczBGRGEzL3MzdGxYYU5FTGZ3NjJEdVcxTgpRZ1FoNEh4L1VjWXc0YjU2dzZuREZVTm1TaFA1R0o2cWJWWjlYWndxWDRVMWVNS3N0d0pqemtDZ3libFdmeXdUCmppNmJCMjZzV2VTclV4MVRUOHFCVU1uQWFncVZHVXFyMEdZdFR5NVZrZ3JsSUlCZ2xnMHhwRyszVFZpNUVxWlkKUGl3dkh1RURsUFhhTlBGM2dMYmtHY3E4VHAzOTBnY2w3ZlhOS2tqVVZRSURBUUFCb0FBd0RRWUpLb1pJaHZjTgpBUUVMQlFBRGdnRUJBQ1cwREpSbkxYRmd5VVVjamplQk9qUjdjZjJzemMxK2JpamJmcTJ1SWlwWHJ4VDQ1RWFkCmRpbys0M2pDL0hYekxsQVlEOHNQamdsaTJqZXVjeXBDV05MRzJTRFY2S3NQZXBUbGRQbGo2YmU4R3dCeEl6cUgKVUs5ZkZvSXZPNjVVVE9LQkx0WktJZUd6bXo5SXBjZC9pb3AxT08wTUgyQlpLMGh6MG4vZmhNdWg1SmtoV1ExWgoyZFVFVmEvaGlUV2FNMTY5cVpDY3VYY0dmWnJYZEc4UDRJOVU3WlJxYng4TjlHWldyRUJCdFFOMlJpQXBuV2JLCkUzVHdmbXpEUmYzUHRQYTJXK1krVEtTUEJTTGdwMFJpSy9SUzlrdjFpUDUwNkUyN0owNkl3QlZwcUhETTlQTjYKbzEyVEVnY0c3MmhVMVpHNlk0UWs0R1JSYTJOZVJYMURNL2c9Ci0tLS0tRU5EIENFUlRJRklDQVRFIFJFUVVFU1QtLS0tLQo=
  signerName: kubernetes.io/kube-apiserver-client
  usages:
  - client auth
```

```bash
kubectl apply -f akshay-csr.yaml 

certificatesigningrequest.certificates.k8s.io/akshay created
```

### Q. Approve the CSR Request

```bash
kubectl certificate approve akshay
```

### Q. What groups is this CSR requesting access to?

```bash
kubectl get csr agent-smith -o yaml

  groups:
  - system:masters
  - system:authenticated
```

### Reject the request

```bash
kubectl certificate deny agent-smith
```

