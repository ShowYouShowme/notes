# 安装步骤

1. 用UltraISO制作U盘启动盘
2. 在BIOS里面设置Boot Mode为Legacy Only
3. 从U盘启动系统，在grub界面选择Install CentOS 7
4. 在系统-->安装位置里删掉原来的分区，再重新分区最后设置分区大小
   + /boot ：存放与系统启动相关的程序，建议大小100~1024M
   + / ：根目录，尽量多分配空间
   + /home 目录，存放用户数据，多分配空间
   + swap：交换分区，比内存大
5. 开始安装



# 镜像

CentOS-7-x86_64-Minimal-1810.iso





# 配置

1. 修改网卡配置`vi /etc/sysconfig/network-scripts/ifcfg-ens32`

   ```shell
   TYPE=Ethernet
   PROXY_METHOD=none
   BROWSER_ONLY=no
   BOOTPROTO=static #将dhcp 改为static
   DEFROUTE=yes
   IPV4_FAILURE_FATAL=no
   IPV6INIT=yes
   IPV6_AUTOCONF=yes
   IPV6_DEFROUTE=yes
   IPV6_FAILURE_FATAL=no
   IPV6_ADDR_GEN_MODE=stable-privacy
   NAME=ens33
   UUID=40dcd0dd-bed3-41dc-8b09-f5ecf20c486f
   DEVICE=ens33
   ONBOOT=yes # 将no改为yes
   
   
   IPADDR=10.10.10.129 #ip
   GATEWAY=10.10.10.1 # 网关
   NETMASK=255.255.255.0#子网掩码
   DNS1=223.6.6.6#dns 这个配置文件的key和value与'='之间不能有空格
   ```

2. 重启网卡

   ```shell
   service network restart
   ```

3. 配置ssh允许root远程登录

   ```shell
   vi /etc/ssh/sshd_config
   #PermitRootLogin yes # 将前面的'#'删掉
   #重启 ssh
   service sshd restart
   用xshell远程连接
   ```

5. 配置阿里源

   ```shell
   # 阿里云有个域名无法解析,直接删掉即可
   yum install wget net-tools -y
   # 备份
   mv /etc/yum.repos.d/CentOS-Base.repo /etc/yum.repos.d/CentOS-Base.repo.backup
   wget -O /etc/yum.repos.d/CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-7.repo
   yum makecache
   ```



# centos8 

1. 更换阿里源

   ```shell
   cd /etc/yum.repos.d
   
   mkdir back
   mv ./*.repo ./back
   wget -O /etc/yum.repos.d/CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-8.repo
   yum clean all
   yum makecache
   ```

2. 重启网卡

   ```shell
   # 和 centos7 不一样
   systemctl restart NetworkManager
   ```

   