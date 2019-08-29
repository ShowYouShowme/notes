# 1.安装Tars前的准备

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
   yum install wget
   # 备份
   mv /etc/yum.repos.d/CentOS-Base.repo /etc/yum.repos.d/CentOS-Base.repo.backup
   wget -O /etc/yum.repos.d/CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-7.repo
   yum makecache
   ```

6. 安装git 并配置代理

   ```shell
   yum install git 
   #配置http和https代理
   git config --global http.proxy http://10.10.10.23:8090
   git config --global https.proxy http://10.10.10.23:8090
   ```
   

# 2.开始安装Tars

## 安装依赖

### 依赖软件

```shell
yum install -y git vim net-tools telnet glibc-devel gcc-c++ gcc ncurses-devel zlib-devel perl perl-Module-Install.noarch flex bison
```

### cmake

```shell
wget -e "https_proxy=http://10.10.10.23:8090" https://github.com/Kitware/CMake/archive/v2.8.8.tar.gz

tar -zxvf  v2.8.8.tar.gz
cd ./CMake-2.8.8/
./bootstrap
make -j5
make install
```



### MySQL安装

1. 配置安装目录

   ```shell
   cd /usr/local
   mkdir mysql-5.6.26
   chown ${普通用户}:${普通用户} ./mysql-5.6.26 # root用户可以忽略
   ln -s /usr/local/mysql-5.6.26 /usr/local/mysql
   ```

2. 编译MySQL

   ```shell
   cd /root
   wget https://dev.mysql.com/get/Downloads/MySQL-5.6/mysql-5.6.26.tar.gz
   tar -zxvf mysql-5.6.26.tar.gz
   cd ./mysql-5.6.26
   cmake . -DCMAKE_INSTALL_PREFIX=/usr/local/mysql-5.6.26 -DWITH_INNOBASE_STORAGE_ENGINE=1 -DMYSQL_USER=mysql -DDEFAULT_CHARSET=utf8 -DDEFAULT_COLLATION=utf8_general_ci
   make -j4
   make install
   ```

3. 配置MySQL

   ```shell
   cd /usr/local/mysql
   useradd mysql
   rm -rf /usr/local/mysql/data
   mkdir -p /data/mysql-data
   ln -s /data/mysql-data /usr/local/mysql/data
   chown -R mysql:mysql /data/mysql-data /usr/local/mysql/data
   cp support-files/mysql.server /etc/init.d/mysql
   #如果/etc/目录下有my.cnf存在，需要把这个配置删除了
   rm -rf /etc/my.cnf
   perl scripts/mysql_install_db --user=mysql
   vim /usr/local/mysql/my.cnf
   ```

   + 启动MySQL

     ```shell
     service mysql start
     chkconfig mysql on # 这个命令是做什么的
     ```

   + 添加MySQL的bin路径 重启系统生效

     ```shell
     vim /etc/profile
     PATH=$PATH:/usr/local/mysql/bin
     export PATH
     ```

   + 修改root密码

     ```shell
     ./bin/mysqladmin -u root password 'root@appinside'
     ```

   + 添加MySQL库路径 动态链接库查找路径

     ```
     vim /etc/ld.so.conf
     /usr/local/mysql/lib/
     ldconfig
     ```

   + 修改centOS时区

     ```shell
     timedatectl set-timezone Asia/Shanghai
     ```

   + my.cnf 配置文件
   
     ```
     [mysqld]
     
     # Remove leading # and set to the amount of RAM for the most important data
     # cache in MySQL. Start at 70% of total RAM for dedicated server, else 10%.
     innodb_buffer_pool_size = 128M
     
     # Remove leading # to turn on a very important data integrity option: logging
     # changes to the binary log between backups.
     log_bin
     
     # These are commonly set, remove the # and set as required.
     basedir = /usr/local/mysql
     datadir = /usr/local/mysql/data
     # port = .....
     # server_id = .....
     socket = /tmp/mysql.sock
     
     bind-address={$your machine ip}
     
     # Remove leading # to set options mainly useful for reporting servers.
     # The server defaults are faster for transactions and fast SELECTs.
     # Adjust sizes as needed, experiment to find the optimal values.
     join_buffer_size = 128M
     sort_buffer_size = 2M
     read_rnd_buffer_size = 2M
     
     sql_mode=NO_ENGINE_SUBSTITUTION,STRICT_TRANS_TABLES
     default-time-zone = '+8:00'
     ```
   
     vim 粘贴前先设置 `set paste`，粘贴完成后再设置`set nopaste`

