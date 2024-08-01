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



# 配置方式一  最简单

1. 修改网卡配置`vi /etc/sysconfig/network-scripts/ifcfg-ens32`

   ```shell
   # 自动获取ip地址,DHCP方式
   ONBOOT=yes # 将no改为yes
   ```

2. 重启网卡

   ```shell
   service network restart
   ```

3. 查看ip地址

   ```shell
   ip a
   ```

# 配置方式二  稍微麻烦

1. 修改网卡配置`vi /etc/sysconfig/network-scripts/ifcfg-ens32`；配置网卡静态地址或者dhcp时，最好先设置ONBOOT=no，然后重启机器（此时网卡处于关闭状态）；最后配置ONBOOT=yes和其他选项，然后service start nework 或者 ifup ens32

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
   ONBOOT=yes # 开机是否启动网卡, 将no改为yes
   
   
   IPADDR=10.10.10.129 #ip
   GATEWAY=10.10.10.1 # 网关 VMvare Nat模式,网关地址为 xxx.xxx.xxx.2
   NETMASK=255.255.255.0#子网掩码
   DNS1=223.6.6.6#dns 这个配置文件的key和value与'='之间不能有空格
   ```

2. 重要选项说明

   ```ini
   [ONBOOT]
   value = yes | no
   ; 开机是否启动该网卡,一般设置为yes
   ;如果开机未启动,需要手动启动网卡.网卡启动和关闭命令 ifup ens32 ; ifdown ens32
   
   ; 网卡未启动时的信息ip a
   ; 2: ens32: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP ; group default qlen 1000
   ;    link/ether 00:0c:29:9e:de:5e brd ff:ff:ff:ff:ff:ff
   
   ; 网卡已经启动的信息, 多了inet inet6
   ; 2: ens32: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP group default qlen 1000
   ;    link/ether 00:0c:29:9e:de:5e brd ff:ff:ff:ff:ff:ff
   ;    inet 192.168.135.128/24 brd 192.168.135.255 scope global noprefixroute ;dynamic ens32
   ;       valid_lft 1634sec preferred_lft 1634sec
   ;    inet6 fe80::75c1:39c4:b006:49e8/64 scope link noprefixroute 
   ;       valid_lft forever preferred_lft forever
   
   
   [BOOTPROTO]
   ; none : 系统启动时不配置网卡信息
   ; static : 系统启动时用静态地址
   ; dhcp : 系统启动时查询路由器获取ip地址
   
   ; 当配置centos7静态ip地址失败时,设置ONBOOT=no; 重启机器，系统启动后不会自动启动网卡，然后手动配置 ONBOOT=yes; 并且配置ip信息,最后重启网卡  service network restart 即可
   value = none | static | dhcp
   ```

   

3. 重启网卡

   ```shell
   service network restart
   ```

4. 配置ssh允许root远程登录

   ```shell
   vi /etc/ssh/sshd_config
   #PermitRootLogin yes # 将前面的'#'删掉
   #重启 ssh
   service sshd restart
   用xshell远程连接
   ```

5. 配置网易源

   ```shell
   yum install wget net-tools -y
   # 备份
   mv /etc/yum.repos.d/CentOS-Base.repo /etc/yum.repos.d/CentOS-Base.repo.backup
   wget -O /etc/yum.repos.d/CentOS-Base.repo http://mirrors.163.com/.help/CentOS7-Base-163.repo
   yum makecache
   ```

6. 配置阿里源：默认的Centos源不可用

   ```shell
   mv /etc/yum.repos.d/CentOS-Base.repo /etc/yum.repos.d/CentOS-Base.repo-bak
   curl -o /etc/yum.repos.d/CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-7.repo
   yum makecache
   ```

   



# centos8 

不建议使用，现在都是使用centos7.9

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

