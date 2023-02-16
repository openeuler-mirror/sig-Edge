1. 安装gdm，wayland

    `yum install -y gdm wayland`
2. 拷贝文件和固件

    将所有.so文件放到/user/lib64下

    将mali_csffw.bin文件放在/usr/lib/firmware目录下
3. 更改配置

    /etc/gdm/custom.conf中的WaylandEnable=false字段注释掉，便可从X11转为wayland
4. 启动桌面

    `systemctl restart gdm`