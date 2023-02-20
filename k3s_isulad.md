配置K3s使用iSulad作为运行时。

cat /etc/isulad/daemon.json
    "registry-mirrors": [
        "docker.io"
    ],
    "insecure-registries": [
        "rnd-dockerhub.huawei.com"
    ],
    
    # default: rnd-dockerhub.huawei.com/library/pause-${machine}:3.0
    "pod-sandbox-image": "docker.io/rancher/pause:3.1",
        
    # default: "" 表示无网络配置，创建的sandbox只有loop网卡。
    "network-plugin": "cni",
    # default /opt/cni/bin
    "cni-bin-dir": "/var/lib/rancher/k3s/data/current/bin",
    # default /etc/cni/net.d
    "cni-conf-dir": "/var/lib/rancher/k3s/agent/etc/cni/net.d",

# k3s data-dir default: /var/lib/rancher/k3s
$ systemctl cat k3s
 ExecStart=/usr/local/bin/k3s \
    server \
        '--write-kubeconfig-mode' \
        '0644' \
        
        # default: "", 表示用embedded containerd
        '--container-runtime-endpoint' \
        'unix:///var/run/isulad.sock' \
        
        # --pause-image default: docker.io/rancher/pause:3.1
        # networking default: flannel-backend vxlan

kubectl top node
W0822 18:36:37.288653 1109064 top_node.go:119] Using json format to get metrics. Next release will switch to protocol-buffers, switch early by passing --use-protocol-buffers flag
NAME              CPU(cores)   CPU%   MEMORY(bytes)   MEMORY%
openeuleronnuc    82m          2%     4526Mi          61%
openeuleragent2   <unknown>                           <unknown>               <unknown>               <unknown>
# stop / disable firewalld
         
kubectl run --image=nginx nginx-app --port 80

kubectl exec -it nginx-app -- sh
error: unable to upgrade connection: error dialing backend: Unknown scheme: ws

kubectl logs nginx-app

apiVersion: apps/v1
kind: Deployment
metadata:
  name: nginx-deployment
spec:
  selector:
    matchLabels:
      app: nginx
  replicas: 10
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:1.14.2
        ports:
        - containerPort: 80
---        
apiVersion: v1
kind: Service
metadata:
  name: nginx
  labels:
    run: nginx
spec:
  ports:
    - port: 80
      protocol: TCP
  selector:
    app: nginx