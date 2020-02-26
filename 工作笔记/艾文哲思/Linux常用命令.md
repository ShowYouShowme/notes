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



# rm

1. 删除文件夹

   ```shell
   # 把文件夹sofeware 和里面全部内容删除
   rm -rf /sofeware
   ```

2. 删除文件夹里面全部文件和子文件夹

   ```shell
   # 把文件夹sofewae 里面的文件和子文件夹全部删除掉，保留文件夹sofeware
   rm -rf /sofeware/*
   ```

3. 删除文件

   ```shell
   rm -f /a.txt
   ```

   



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



## 操作

***

1. 将本地文件复制到远程

   ```shell
   scp -r /home/administrator/ root@192.168.6.129:/etc/squid
   ```

2. 将远程文件复制到本地

   ```shell
   scp remote@www.abc.com:/usr/local/sin.sh /home/administrator
   
   # 例子
   scp root@10.10.10.168:/usr/local/tars/cpp/makefile/makefile.tars ./
   ```




## 免密码复制

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

   

   
   

# 通配符

1. *(星号)

   ```shell
   # 匹配任意多个字符
   
   ls DBAgent*
   ```

   

2. ?(问号)

   ```shell
   # 匹配一个字符
   
   ls ?[12].txt  # 结果  a1.txt  b2.txt
   
   # [] 是集合,匹配里面的任意的一个字符
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
   
4. 利用通配符查找

   ```shell
   # 查找以"XGame."开头的文件夹的子文件夹bin里面有哪些文件里包含字符串10.10.10.168
   grep "10.10.10.168" "XGame.*/bin/*
   ```

   




# unlink

删除软连接



# rz 上传二进制文件

```shell
# 可以一次性选择多个文件的 ==此方式可以替代SFTP客户端上传
rz -be ${fileName}

# -y 选项可以替换-be
rz -y ${fileName}
```



# 下载软件包及其依赖

```shell
# 安装下载工具
yum -y install yum-utils

#下载依赖包
yumdownloader --resolve ${packageName} --destdir=${DESTDIR}
```



# 保存yum下载的包

```shell
1:修改 /etc/yum.conf 配置文件将keepcache=0 改为keepcache=1
2:下载的包放在路径:/var/cache/yum/x86_64/${centOS版本}/${Repository}/packages 

====================
yum安装时会显示安装的Repository
开发机上Repository有：
1:base
2:epel
3:extras
4:updates
```



# 解决RPM包依赖问题

1. 如上下载软件包及其依赖

2. 进入目录安装

   ```shell
   rpm -Uvh *
   ```

   



# 搭建本地yum仓库

1. 安装createrepo

   ```shell
   yum -y install createrepo
   ```

2. 进入本地rpm包目录

   ```shell
   cd /root/packages/gcc
   ```

3. 构建yum仓库

   ```shell
   createrepo  ./
   ```

4. 如果添加或者删除了个人的rpm包，不用重新create，只需--update就可以了

   ```shell
   createrepo --update  ./
   ```

5. 编辑yum源repo文件

   ```shell
   vim /etc/yum.repos.d/local.repo
   
   # 文件内容
   [localrepo]
   name=localrepo
   baseurl=file:///root/packages/gcc
   gpgcheck=0
   enabled=1
   gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-CentOS-7
   ```

6. 备份系统yum源配置文件,只留下local.repo

   ```shell
   cd /etc/yum.repos.d/
   mkdir ~/repos_bak
   cp ./* ~/repos_bak/
   rm -f /etc/yum.repos.d/CentOS*
   ```

7. 更新yum源

   ```shell
   # 清除资源
   yum clean all
   
   # 建立yum资源缓存
   yum makecache
   ```

   

8. 安装软件包时指定yum源名称

   ```shell
   yum install ${packageName} --enablerepo=${yumRepo}
   ```






# wget

1. 下载网站全部资源

   ```shell
   wget -k -r -p -np http://www.cplusplus.com/reference/
   ```




# nslookup

+ 安装

  ```shell
  yum install -y bind-utils
  ```

+ 作用：DNS查询

+ 使用方式

  1. 使用默认DNS服务器

     ```shell
     nslookup ${hostname}
     
     nslookup httpbin.org
     ```

  2. 使用指定DNS服务器

     ```shell
     nslookup ${hostname} ${DNS_SERVER}
     
     nslookup httpbin.org 8.8.8.8
     ```

  



# chown

+ 作用：修改文件属主

+ 示例

  ```shell
  chown ${user} ${file}
  ```




# find

+ 作用：查找文件

+ 示例

  ```shell
  # 用通配符时必须用双引号包含
  find / -name "libcurl*"
  ```

  ```shell
  # 删除找到的文件
  rm -f `find / -name "libcurl*"`
  ```
  



# 强制杀死进程

> 1. 更改可执行文件的名称或者删掉可执行文件
> 2. 用kill命令杀死运行中的进程





# sed

+ 作用：替换文件内容

+ 示例

  ```shell
  # 将文件里面的全部172.17.0.200替换为192.168.1.80
  sed -i "s/172.17.0.200/192.168.1.80/g" ./set_game_room_conf.py  ./start_and_stop.py
  ```

  ```shell
  # 查找存在内容10.10.10.168 的文件，并且把内容10.10.10.168 替换为${TARGET_HOST}
  sed -i "s/10.10.10.168/${TARGET_HOST}/g" `grep 10.10.10.168 -rl XGame.*/bin/*`
  ```




# 打包+COPY

> 文件从CentOS 复制至Windows再复制到CentOS权限和属性信息会丢失，因此如下操作
>
> > 1. tar打包
> > 2. copy至win，再copy至CentOS
> > 3. tar解压，此时文件权限和属性信息则不会丢失





# firewall

1. 查看全部放行的端口

   ```shell
   firewall-cmd --list-all
   ```

2. 放行指定的端口，tcp协议

   ```shell
   firewall-cmd --permanent --add-port=${port}/tcp
   
   firewall-cmd --permanent --add-port=3000/tcp
   
   firewall-cmd --reload
   ```

3. 删除端口

   ```shell
   firewall-cmd  --permanent --remove-port=80/tcp 
   ```

4. 关闭防火墙

   ```shell
   systemctl stop firewalld.service # 停止防火墙
   systemctl disable firewalld.service  # 禁止防火墙开机启动
   ```

5. 查看防火墙状态

   ```shell
   firewall-cmd --state
   ```

6. 开启防火墙

   ```shell
   systemctl start firewalld
   ```

7. 查看防火墙的状态

   ```shell
   # dead 是未开启
   systemctl status firewalld
   ```

   




# rar解压命令[建议用zip替代]

```shell
# 下载源码
wget http://www.rarsoft.com/rar/rarlinux-x64-5.4.0.tar.gz

tar -zxvf rarlinux-x64-5.4.0.tar.gz

cd rar

make

# 解压文件
rar x deploy.rar
```



# zip解压

```shell
# 安装zip
yum -y install zip unzip

# 解压
unzip we.zip

# 压缩
zip -r we.zip we
```



# expect

+ 作用：实现自动的交互，无需人为干预。很多命令，比如ssh的登录命令是交互式的，输入命令，等待程序响应，再输入指令等。

+ 常用命令

  1. send

     > 向进程发送字符串
     
  2. expect
  
     > 等待反馈
  
  3. spawn
  
     > 启动新进程
  
  4. interact
  
     > 退出自动化，进入人工交互

+ 实例

  ```shell
  #!/usr/bin/expect
  set timeout 30
  set host "47.56.112.9"
  set username "root"
  set password "X0xZ2xReP\$qvE%bonY2hVEoU"
  
  spawn ssh $username@$host
  # 判断上次输出结果里是否包含“password”的字符串，如果有则立即返回；否则就等待一段时间后返回，这里
  # 等待时长就是前面设置的30秒；
  expect "*password*" {send "$password\r"}
  interact
  
  ```

  运行

  ```shell
  expect ./login_hk.exp
  ```

  

+ 安装

  ```shell
  yum  install expect
  ```

  



# ssh 

 ### 1 使用代理

```shell
# xshell 里面的'连接'有个代理的选项;可以设置http tunnel 或者 socket5 代理
```

### 2 本地隧道

```shell
# 隧道仅转发流量

ssh -N -f -L 0.0.0.0:2121:47.75.37.140:22 47.112.162.19

ssh -N -f -L ${本地IP}:${本地端口}:${目的服务器IP}:${目的服务器端口} ${中间服务器IP}
```

### 3 远程隧道

```shell
# 让家里的电脑能访问公司内网的电脑

ssh -Nf -R 2222:127.0.0.1:22 47.112.162.19  # 公司内网机器执行

ssh -p 2222 127.0.0.1 # 机器47.112.162.19 执行,此时即可在家里访问公司内网的服务器

# 命令讲解
ssh -Nf -R ${中间服务器端口}:${局域网IP}:${局域网端口} ${中间服务器IP}

ssh -p ${局域网映射的端口} 127.0.0.1
```



## 4 sockets代理服务器

```shell
# ssh 内置了socks5服务

ssh -N -f -D 0.0.0.0:1080 10.10.10.188  # 内网的机器有sshd服务,可以将sshd服务器地址设置为本机

ssh -N -f -D ${本地IP}:${本机端口} ${sshd服务地址}
```





# 查看文件夹大小

```shell
du -sh ./protobuf/
```





# rsync

> 文件同步工具