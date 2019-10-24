# netstat

1. 列出所有端口情况

   > ```shell
   > [root@xiesshavip002 ~]# netstat -a      # 列出所有端口
   > [root@xiesshavip002 ~]# netstat -at     # 列出所有TCP端口
   > [root@xiesshavip002 ~]# netstat -au     # 列出所有UDP端口
   > ```

2. 列出所有处于监听状态的 Sockets

   > ```shell
   > [root@xiesshavip002 ~]# netstat -l   # 只显示监听端口
   > [root@xiesshavip002 ~]# netstat -lt  # 显示监听TCP端口
   > [root@xiesshavip002 ~]# netstat -lu  # 显示监听UDP端口
   > [root@xiesshavip002 ~]# netstat -lx  # 显示监听UNIX端口
   > ```

3. 显示每个协议的统计信息

   > ```shell
   > [root@xiesshavip002 ~]# netstat -s     # 显示所有端口的统计信息
   > [root@xiesshavip002 ~]# netstat -st    # 显示所有TCP的统计信息
   > [root@xiesshavip002 ~]# netstat -su    # 显示所有UDP的统计信息
   > ```

4. 显示 PID 和进程名称

   > ```shell
   > [root@xiesshavip002 ~]# netstat -p
   > ```

5. 查看端口和服务

   > ```shell
   > [root@xiesshavip002 ~]# netstat -antp | grep ssh
   > [root@xiesshavip002 ~]# netstat -antp | grep 22
   > ```
   
6. 部分参数介绍

   > + -n： Local Address这列的host和port均用数字表示
   >
   > + -p：显示PID/Programe name 这列
   > + -a：列出全部端口
   > + -t：列出TCP端口
   > + -u：列出UDP端口
   > + -l：列出监听端口



# tar

1. 打包制定文件

   ```shell
   tar -cf archive.tar foo bar
   ```

2. 打包文件夹

   ```shell
   tar -cf Test.tar ./test/*
   ```

3. 打包+压缩文件夹

   ```shell
   tar -zcvf Tars_1.6.tar.gz ./Tars/*
   ```

4. 解压文件

   ```shell
   # 解压tar.gz
   tar -zxvf mysql-5.6.26.tar.gz
   ```

5. 参数

   > -v：显示处理的文件
   >
   > -x：解压
   >
   > -c：创建新文档，打包时用



# 防火墙

```shell
firewall-cmd --state # 查看防火墙状态
systemctl stop firewalld.service # 停止防火墙
systemctl disable firewalld.service  # 禁止防火墙开机启动
```



# SELinux

```shell
# 查看SELinux状态
getenforce

# 临时关闭SELinux
setenforce 0

# 永久关闭SELinux
vim /etc/selinux/config 
SELINUX=permissive
```



# SCP

格式：

```shell
scp [命令参数] [源路径] [目的路径]
```



### 操作

***

1. 将本地文件复制到远程

   ```shell
   scp -r /home/administrator/ root@192.168.6.129:/etc/squid
   ```

2. 将远程文件复制到本地

   ```
   scp remote@www.abc.com:/usr/local/sin.sh /home/administrator
   ```




### 免密码复制

***

```shell
# 生成公钥和私钥
ssh-keygen -t rsa -P ""
# 拷贝公钥到远程主机
scp ~/.ssh/id_rsa.pub root@10.10.10.61:/root/.ssh
# 登录远程主机，将公钥id_rsa.pub输入到authorized_keys文件中
cd ~/.ssh
cat id_rsa.pub >> authorized_keys 

# 秘钥文件权限全部设置为600
id_rsa、id_rsa.pub和authorized_keys
```



# ssh秘钥登录

1. 生成密钥（公钥和私钥）
2. 放置公钥(Public Key)到服务器~/.ssh/authorized_key文件中
3. 配置ssh客户端使用密钥登录





# 开机启动服务或脚本

1. 编写脚本，在脚本前加入下面三行

   ```shell
   #!/bin/bash
   # chkconfig:   2345 90 10
   # description:  myservice
   ```

2. 给脚本赋予执行权限，并移动至**/etc/rc.d/init.d**

   ```shell
   chmod u+x ./autostart.sh
   mv  ./autostart.sh /etc/rc.d/init.d
   ```

3. 添加脚本至开机启动项目

   ```shell
   cd /etc/rc.d/init.d
   chkconfig --add autostart.sh
   chkconfig autostart.sh on
   ```




# uname -r

查看当前使用的内核





# trap

捕获系统信号，并打印提示信息

```shell
# 捕获Ctrl+C
trap "echo sig 2" 2
```



# tree

以目录树的方式显示指定目录下全部文件

```shell
yum install tree -y
```



# screen

1. 显示正在运行的screen 会话

   ```shell
   screen -ls
   ```

2. 进入指定的screen会话

   ```shell
   screen -r ${sessionID}
   ```

3. screen会话与终端分离(detached)

   + 进入指定的screen会话

     ```shell
      screen -r ${sessionID}
     ```

   + 按如下键盘

   ```shell
   Ctrl + A,D
   ```

4. 创建Screen会话

   ```shell
   screen
   ```

5. 关闭screen会话

   + 进入指定的screen会话

     ```shell
     screen -r ${sessionID}
     ```

   + 关闭会话

     ```shell
     exit
     ```

     

   





# grep

功能：文本查找

1. 查找指定名称的进程

   ```shell
   ps -ef | grep tarsnode
   ```

2. 在文件中查找指定文本，并显示所在行号

   ```shell
   grep -n 'home' mount_wzc.sh
   ```

3. 正则表达式查找

   ```shell
   # -E 选项指定使用正则表达式
   grep -n -E '[0-9]{2}\.[0-9]{2}\.[0-9]{2}\.[0-9]{2}' mount_wzc.sh
   ```

   

# 下载软件包及其依赖

```shell
# 安装下载工具
yum -y install yum-utils

#下载依赖包
yumdownloader --resolve ${packageName} --destdir=${DESTDIR}
```



