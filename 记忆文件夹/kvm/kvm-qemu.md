# 第一章 安装



## 1.0 开启虚拟化支持

```shell
处理器 --> 虚拟化引擎 -->  虚拟化inter VT-x/EPT或AMD-V/RVI(V)
```



## 1.1 检查CPU是否支持硬件虚拟化

```shell
grep -E '(vmx|svm)' /proc/cpuinfo
```



## 1.2 安装kvm和相关的依赖

```shell
yum install qemu-kvm qemu-img virt-manager libvirt libvirt-python libvirt-client virt-install virt-viewer bridge-utils
```



## 1.3 启动libvirtd服务，并设置开机启动

```shell
systemctl start libvirtd
systemctl enable libvirtd
```



## 1.4 检查KVM模块是否加载

```shell
lsmod | grep kvm

# 输出
kvm_intel             188740  0 
kvm                   637289  1 kvm_intel
irqbypass              13503  1 kvm
```



## 1.5 启动virt-manager

```shell
# virt-manager 底层用libvirt实现，用来管理虚拟机
virt-manager
```



# 第二章 Virsh



## 2.1 安装

```shell
# 命令合起来会报错
yum install qemu-kvm -y
yum install libvirt -y
yum install virt-install -y
yum install bridge-utils -y
```



## 2.2 命令



### 2.2.1 帮助命令

***

> 1. 查看帮助信息
>
>    ```shell
>    virsh help
>    ```
>
> 2. 查看一组帮助信息
>
>    ```shell
>    virsh help volume
>    ```
>
> 3. 查看某个命令的用法
>
>    ```shell
>    virsh help vol-clone
>    ```



### 2.2.2 管理虚拟机命令

***

> 1. 列出虚拟机
>
>    ```shell
>    virsh list
>
>    virsh list --all # 列出全部
>    ```
>
> 2. 创建虚拟机并运行
>
>    ```shell
>    # 从XML文件创建虚拟机
>    virsh create ${file}
>    ```
>
> 3. 创建虚拟机但不运行
>
>    ```shell
>    virsh define ${file}
>    ```
>
> 4. 连接虚拟机的控制台
>
>    ```shell
>    virsh console ${domain}
>
>    virsh console c2
>    ```
>
> 5. 关闭虚拟机
>
>    ```shell
>    virsh shutdown ${domain}
>    ```
>
> 6. 强制关机
>
>    ```shell
>    # 类似kill -9,kvm 的虚拟机在宿主机上就是一个进程
>    virsh destroy ${domain}
>    ```
>
> 7. 启动虚拟机
>
>    ```shell
>    virsh start ${domain}
>    ```
>
> 8. 挂起虚拟机
>
>    ```shell
>    # 把运行状态的虚拟机暂停，并把当前运行状态保存到内存，有点类似时间停止的感觉，外部客户端对它访问它也不会响应；如果此时宿主机掉电，那么之前保存在内存的运行状态数据也将随之丢失
>    virsh suspend ${domain}
>    ```
>
> 9. 恢复被挂起的虚拟机
>
>    ```shell
>    virsh resume ${domain}
>    ```
>
> 10. 保存虚拟机运行状态到指定文件
>
>     ```shell
>     # 类似vmware 中的挂起操作，vmware的挂起操作是把运行状态保存到磁盘，宿主机掉电，它不会的丢失数据
>     virsh save ${domain} ${file} --paused
>     ```
>
> 11. 从指定文件恢复虚拟机
>
>     ```shell
>     virsh restore ${file}
>     ```
>
> 12. 重启虚拟机
>
>     ```shell
>     virsh reboot ${domain}
>     ```
>
> 13. 强制重启，类似按下机箱重置按钮
>
>     ```shell
>     virsh reset ${domain}
>     ```
>
> 14. 输出虚拟机的详细配置
>
>     ```shell
>     virsh dumpxml ${domain}
>     ```
>
> 15. 删除指定虚拟机
>
>     ```shell
>     # 连同配置文件一起删除,存储卷需要自己删除
>     virsh undefine ${domain}
>     ```
>
> 16. 设置虚拟机随着宿主机启动而启动
>
>     ```shell
>     virsh autostart ${domain}
>
>     virsh autostart ${domain} --disable # 禁止自动启动
>     ```
>



## 2.3 快速创建虚拟机

1. 用virt-manager 安装系统

2. 基于模板创建虚拟机

   > 1. 复制卷
   >
   >    ```shell
   >    cp /var/lib/libvirt/images/centos7.0.qcow2 /kvm/images/c2.qcow2
   >    ```
   >
   > 2. 复制配置文件
   >
   >    ```shell
   >    cd /etc/libvirt/qemu
   >    
   >    cp centos7.0.xml c2.xml
   >    ```
   >
   > 3. 修改配置文件
   >
   >    ```shell
   >    # 修改虚拟机名称
   >    <name>
   >    
   >    # 修改UUID
   >    <uuid>
   >    
   >    # 修改卷
   >    <source file='/kvm/images/c2.qcow2'/>
   >    
   >    # 修改网卡地址
   >    <mac address='52:54:00:e3:8d:11'/>
   >    ```
   >
   > 4. 创建并启动虚拟机
   >
   >    ```shell
   >    virsh create c2.xml
   >    ```
   >
   > 5. 启动图形界面virt-manager，查看c2是否已经启动





# 第三章 qemu-img



## 3.1 常见命令

1. 创建磁盘

   ```shell
   # 磁盘最大空间为40G
   qemu-img create -f qcow2 base.qcow2 40G
   ```

2. 查看磁盘信息

   ```shell
   qemu-img info base.qcow2
   ```

3. 磁盘扩容

   ```shell
   qemu-img resize base.qcow2 +2G
   ```






# 第四章 qemu

1. 安装虚拟机

   ```shell
   # 创建磁盘镜像
   qemu-img create -f qcow2 fedora.img 10G
   
   # 安装系统
   qemu-system-x86_64 -m 2048 -enable-kvm fedora.img -cdrom ./Fedora-Live-Desktop-x86_64-20-1.iso
   ```

2. 启动虚拟机

   ```shell
   qemu-system-x86_64 -m 2048 -enable-kvm fedora.img
   

   # 启动虚拟机,同时暴露端口给spice client
   /mnt/server/opt/qemu/build/bin/qemu-system-x86_64 -m 4096 -enable-kvm /mnt/images/5ffdf526b0321206714888c7_518df33b-684d-4457-a3f0-4e7f99c8f441.qcow2 -spice port=5902,image-compression=off,playback-compression=off,disable-ticketing
   ```
   
   