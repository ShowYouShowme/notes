# 第一章 centos内核编译



## 1.1 内核版本

内核版本为5.8





## 1.2 编译过程

1. 安装依赖

   ```shell
   yum install gcc gcc-c++ make ncurses-devel openssl-devel elfutils-libelf-devel bison flex -y
   ```

2. 编译

   ```shell
   # STEP-1 配置 进入UI 界面,方向键切换到save直接保存
   make menuconfig
   
   
   # STEP-2 修改配置文件
   CONFIG_DEBUG_INFO_BTF=n
   CONFIG_SYSTEM_TRUSTED_KEYS=""
   
   # STEP-3 编译
   make
   make modules
   make modules_install
   make install
   ```

3. 查看内核版本

   ```shell
   uname -r
   ```

   





# 第二章 qemu编译



## 2.1 qemu版本

开发选用5.2版本



## 2.2 安装依赖

```shell
yum install python3

# 安装ninja 和 meson
pip3 install ninja
pip3 install meson

# 用法 生成build目录
meson build

cd ./build

# 编译
ninja 

# 安装
ninja install
```







# 第三章 安装Tesla T4 显卡驱动

1. 下载显卡驱动

   ```shell
   https://www.nvidia.cn/Download/index.aspx?lang=cn
   ```

2. 屏蔽系统自带显卡驱动`nouveau`

   ```shell
   vim /lib/modprobe.d/dist-blacklist.conf
   
   # 注释
   #blacklist nvidiafb
   
   # 增加以下两行
   blacklist nouveau
   options nouveau modeset=0
   ```

3. 重建`initramfs image`

   ```shell
   mv /boot/initramfs-$(uname -r).img /boot/initramfs-$(uname -r).img.bak
   dracut /boot/initramfs-$(uname -r).img $(uname -r)
   ```

4. 修改运行级别

   ```shell
   systemctl set-default multi-user.target
   ```

5. 重启，用root登录

   ```shell
   reboot
   ```

6. 查看 nouveau 是否已经禁用

   ```shell
   # 没有信息则已经禁用
   lsmod | grep nouveau
   ```

7. 安装驱动

   ```shell
   # 安装依赖
   yum install -y libglvnd-devel
   
   # 安装驱动
   ./NVIDIA-Linux-x86_64-460.73.01.run  --kernel-source-path=/root/linux-5.8 -k $(uname -r)
   
   # 错误 --> 据说 BIOS中禁用Security BOOT选项即可,我当时重启再装一次就好了
    Unable to load the 'nvidia-drm' kernel module
    
    
   # 重启 驱动装好后要重启才能生效,因为重启会加载模块
   reboot
   ```

8. 查看显卡驱动是否成功安装

   ```shell
   nvidia-smi
   
   lshw -c video
   ```

9. 卸载驱动

   ```shell
   ./NVIDIA-Linux-x86_64-460.73.01.run --uninstall
   ```

   



