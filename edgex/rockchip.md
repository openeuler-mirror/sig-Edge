# Env
## Hardware
* Rockchip Rk3588s LP4X EVB 
## Software
* 镜像需要自己移植
# Install


## install
* 采用docker的方案去部署整个edgex的服务

### Docker Install
* 因为openEuler提供的repo源中，docker的版本过低，导致Edgex无法顺利运行，所以需要手动安装docker二进制包，并配置daemon 服务。
```
# 通过二进制包的方式安装docker
wget https://download.docker.com/linux/static/stable/aarch64/docker-20.10.17.tgz
dnf install tar -y
tar zxvf docker-20.10.17.tgz
cp -p docker/* /usr/local/bin

# 配置docker服务
sudo cat > /usr/lib/systemd/system/docker.service <<EOF
[Unit]
Description=Docker Application Container Engine
Documentation=http://docs.docker.com
After=network.target docker.socket
[Service]
Type=notify
EnvironmentFile=-/run/flannel/docker
WorkingDirectory=/usr/local/bin
ExecStart=/usr/local/bin/dockerd -H tcp://0.0.0.0:4243 -H unix:///var/run/docker.sock --selinux-enabled=false --log-opt max-size=1g
ExecReload=/bin/kill -s HUP $MAINPID
# Having non-zero Limit*s causes performance problems due to accounting overhead
# in the kernel. We recommend using cgroups to do container-local accounting.
LimitNOFILE=infinity
LimitNPROC=infinity
LimitCORE=infinity
# Uncomment TasksMax if your systemd version supports it.
# Only systemd 226 and above support this version.
#TasksMax=infinity
TimeoutStartSec=0
# set delegate yes so that systemd does not reset the cgroups of docker containers
Delegate=yes
# kill only the docker process, not all processes in the cgroup
KillMode=process
Restart=on-failure
[Install]
WantedBy=multi-user.target
EOF


groupadd docker
chgrp docker /var/run/docker.sock

systemctl enable docker
systemctl start docker

# 验证docker是否成功安装
docker run hello-world

```
* 运行`docker run hello-world`,无法启动，使用`dockerd`命令可获得下面的错误提示
![运行报错](image/run_error.png)
```
#可以尝试关闭防火墙
systemctl stop firewalld
systemctl disable firewalld
```
* 安装docker-compose
```
wget https://github.com/docker/compose/releases/download/v2.7.0/docker-compose-linux-aarch64
mv docker-compose-linux-aarch64 docker-compose
chmod +x docker-compose
sudo mv docker-compose /usr/local/bin

```
# Demo

```
# 拉取相关仓库
dnf install git -y

git clone https://github.com/edgexfoundry/edgex-compose.git
# 切换到版本2.1.0
git checkout v2.1.0
# 启动demoe
docker-compose -f docker-compose-no-secty-with-app-sample-arm64.yml up -d

# 检查状态
docker-compose ps
```
![state](image/state.png)
