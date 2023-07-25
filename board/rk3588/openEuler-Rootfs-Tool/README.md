# openEuler-rk-rootfs

## 介绍
openEuler rootfs tool  
用来构建openEuler在Rockchip平台上的rootfs以及docker镜像

## 使用说明

### 编译环境说明

#### Debian或Ubuntu


```
  sudo apt install git dnf python3 qemu-user-static
```
 **注意：** Debian系OS在编译时会出现rpmlist被破坏的问题，详见后文【目前已知的问题】

#### CentOS或Openeuler

  脚本在运行过程中会生成 yum repo文件，并 **破坏系统中原有的 yum repo配置**   
  如果Host系统为CentOS等使用yum包管理器的系统，则建议使用Dokcer环境进行编译，以防止原本的repo遭到破坏

### Rootfs构建

1.  编辑配置文件config.json   


-  **TargetVersion** : 目标openEuler rootfs版本
-  **SourceFile** : rootfs基础软件包列表，需要一个rpmlist文件  
-  **ImageName** : 生成的镜像名称  
-  **RootPassword** : root账户的登录密码
-  **CustomRepoEnable** ：启用用户自定义repo源，如果开启了此配置，TargetVersion配置和MirrorRepo配置均会失效
-  **CustomRepoFile** ：用户自定义repo源文件
-  **MirrorRepoEnable** ：启用yum镜像源
-  **MirrorRepoSource** ：yum镜像源repo地址
-  **RemovePackage** ：从rpmlist移除的软件包列表，默认会移除kernel与grub2相关的软件包  
-  **ExtraPackage** : 添加至rootfs中的额外软件包  


    
2.  以root权限运行脚本 main.py  


```
    sudo ./main.py
```

### Docker镜像构建

    cd docker/ 
    ./build.sh 

    执行 run.sh 运行docker image


## 其他说明

1. 默认启动了北京yum repo镜像源，可以根据网络情况替换为合适的repo源
2. 生成的rootfs镜像默认登录的用户名为 root / 123   
3. 镜像默认使能了网口及DHCP， 可以使用ssh或者串口进行登录调试  
4. 镜像适配了RK平台的adb功能(需要硬件支持usb调试)

## 依赖软件包说明
1. gdisk ： GPT分区工具，系统服务 resize-disk.service依赖
2. dpkg : Debian 包管理工具，系统服务 adbd.service依赖

## 目前已知的问题
1. 如果Host主机与目标Rootfs中的dnf不一致，编译后的roofs中无法正确读取已安装的rpmlist列表；  
  **为避免此问题，请使用与目标rootfs一致的HostOS进行编译；例如目标版本为openEuler-22.03-lts，则主机也应该使用openEuler-22.03-lts进行编译** 

