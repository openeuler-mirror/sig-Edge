# Env

## Hardware

* Rockchip Rk3588s LP4X EVB

## Software

* 镜像需要自己移植

# Install

## kubeedge

### 使用k3s 搭建集群

* 安装 k3s 相关软件

```bash
curl -sfL https://get.k3s.io | sh -

```

* 修改关于k3s配置将`/etc/rancher/k3s/k3s.yaml`中的`server:` 修改为本机ip。

* 详细请查[文档](https://rancher.com/docs/k3s/latest/en/quick-start/)

* 查看本机安装的k3s环境

```bash
sudo k3s kubectl version
```

```result
Client Version: version.Info{Major:"1", Minor:"24", GitVersion:"v1.24.4+k3s1", GitCommit:"c3f830e9b9ed8a4d9d0e2aa663b4591b923a296e", GitTreeState:"clean", BuildDate:"2022-08-25T03:46:35Z", GoVersion:"go1.18.1", Compiler:"gc", Platform:"linux/arm64"}
Kustomize Version: v4.5.4
Server Version: version.Info{Major:"1", Minor:"24", GitVersion:"v1.24.4+k3s1", GitCommit:"c3f830e9b9ed8a4d9d0e2aa663b4591b923a296e", GitTreeState:"clean", BuildDate:"2022-08-25T03:46:35Z", GoVersion:"go1.18.1", Compiler:"gc", Platform:"linux/arm64"}
```

### 部署云端(KebeEdge主节点)

* 下载`keadm` `wget https://github.com/kubeedge/kubeedge/releases/download/v1.11.1/keadm-v1.11.1-linux-arm64.tar.gz`
* 加压缩到当前目录 `tar zxvf keadm-v1.11.1-linux-arm64.tar.gz`
* 切换到`keadm`目录
* 开始部署 `sudo ./keadm init --kube-config /etc/rancher/k3s/k3s.yaml`
* 查看coludcore节点`sudo k3s kubectl get pod -A`
  ![cloudcore](image/cloudcore.png)
* 查看cloudcore节点log `sudo k3s kubectl logs  cloudcore-5f48f6bcc6-kxg64 -n kubeedge`
  ![cloudcore_log](image/cloudcore_logs.png)

### 部署边缘端(KubeEdge工作节点)  

#### 从云端获取令牌

* 在云端运行 keadm gettoken 将返回token令牌，该令牌将在加入边缘节点时使用。

```bash
sudo ./keadm gettoken --kube-config /etc/rancher/k3s/k3s.yaml
07af921b2ba8737611a1d9bf4b7c5592ceae4770fc597f36d23ccba14f92df07.eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2NjI3OTQyNDh9.IP81UXvaJO_Cs3l-ZTE2YOLiH66sovtnaxCqs8Wx7f8
```

![edgecore](image/edgecore.png)

#### 加入边缘节点

* 寻找一台新机器，并在机器上，配置好`keadm`的环境, 确认该环境中不存在相关的`k8s`,`microk8s`,`k3s`等环境。
* keadm join 将安装 edgecore 和 mqtt。它还提供了一个命令行参数，通过它可以设置特定的版本。 其中`--cloudcore-ipport=`为服务器端ip。

```bash
sudo ./keadm join --cloudcore-ipport=10.0.20.145:10000 --token=07af921b2ba8737611a1d9bf4b7c5592ceae4770fc597f36d23ccba14f92df07.eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2NjI3OTQyNDh9.IP81UXvaJO_Cs3l-ZTE2YOLiH66sovtnaxCqs8Wx7f8

```

![edgecore_service](image/edgecore_service.png)

#### 通过`cloudcore`向设备端`edgecore`部署`nginx`容器

##### 创建新的命名空间`ns-test`

* 保存文件到`cloudcore` `nginx-namespace.yaml`

```yaml
apiVersion: v1 #类型为Namespace
kind: Namespace  #类型为Namespace
metadata:
  name: ns-test  #命名空间名称
  labels:
    name: label-test  #pod标签
```

* `sudo k3s kubectl apply -f nginx-namespace.yaml`
* 查看命名空间`sudo k3s kubectl get namespace`
  ![ns-test](image/namespace.png)

###### 部署多个nigix服务，添加下面yaml文件到本地`nginx-deployment.yaml`

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  namespace: ns-test
  name: nginx-deployment
spec:
  selector:
    matchLabels:
      app: nginx
  replicas: 5
  template:
    metadata:
      labels:
        app: nginx
    spec:
      containers:
      - name: nginx
        image: nginx:alpine
        ports:
        - containerPort: 80
```

* 启动该deployment `sudo k3s kubectl apply -f nginx-deployment.yaml`
* 查看启动的`pod` `sudo k3s kubectl get pod -n ns-test`
  ![pods](image/nginx.png)

##### 在`edgecore`查看启动的`nginx`

`docker ps`

![nvidia_nginx](image/nvida_nginx.png)

# Q&A

* 当kubeedge `cloudecore`状态一直是`Pending`时，查看下node的状态，以及对应pods的log

```bash
sudo k3s kubectl describe node node-name

sudo k3s kubectl logs pods-name -n namesapce
```
