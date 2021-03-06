# netstat[按字母排序]

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
   
6. 查看指定ip的TCP连接

   > ```shell
   > # 可以查看到TCP连接的状态,TIME_WAIT  FIN_WAIT2 等等
   > netstat -at | grep "${ip}"
   > 
   > netstat -at | grep "10.10.10.23"
   > ```

7. 列出全部TCP监听的端口

   > ```shell
   > netstat -ltnp
   > ```

8. 部分参数介绍

   > + -n： Local Address这列的host和port均用数字表示
   >+ -p：显示PID/Programe name 这列
   > + -a：列出全部端口
   > + -t：列出TCP端口
   > + -u：列出UDP端口
   > + -l：列出监听端口
   
9. mac上面的用法[与centOS有差异]

   ```shell
   # 查询全部监听的tcp端口
   netstat -f inet -n | grep tcp4
   ```

   



# alias

***

+ 作用：设置指令的别名

+ 配置

  1. 给所有用户使用

     ```shell
     # /etc/bashrc
     
     alias ll='ls -lh'  # 等号两边不要有空格,某些平台不支持比如mac
     ```

     

  2. 给指定用户使用

     ```shell
     # ~/.bashrc
     
     alias ll='ls -lh'
     ```

     

  

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

4. 忽略部分打包文件

   ```shell
   tar -zcvf dna-explorer-api.tar.gz --exclude=dna-explorer-api/.idea/ --exclude=dna-explorer-api/.git/ dna-explorer-api/
   ```

1. 解压文件

   ```shell
   # 解压tar.gz
   tar -zxvf mysql-5.6.26.tar.gz
   ```

2. 参数

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

## 1 命令格式

```shell
scp [命令参数] [源路径] [目的路径]

# 文件夹的话先打包,再传输,速度快很多
```

## 2 常见操作

1. 将本地文件复制到远程[发布和部署时用到]

   ```shell
   scp -r /home/administrator/ root@192.168.6.129:/etc/squid
   ```

2. 将远程文件复制到本地

   ```shell
   scp remote@www.abc.com:/usr/local/sin.sh /home/administrator
   
   # 例子
   scp root@10.10.10.168:/usr/local/tars/cpp/makefile/makefile.tars ./
   ```
   
3. 免密码复制

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
   
4. 指定端口`-P`

   ```shell
   # P 是大写的
   scp -P 12008 ./dna-explorer-api.tar.gz root@dna3.viewdao.com:/tmp
   ```

5. 指定私钥`-i`

   ```shell
   
   ```

   





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





# tail

1. 查看倒数200行日志

   ```shell
   tail -n 200 redis-server.log
   ```

   





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
   # 方式一
   screen
   
   # 方式二 用指定名称创建会话
   screen -S ${sessionName}
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
   
   + 不进入screen关闭

     ```shell
     screen -X -S ${SessionID} quit
     screen -X -S 11584 quit
     ```
   
   + 删除状态为dead的会话
   
     ```shell
     screen -wipe ${SessionID}
     screen -wipe 17005
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

5. 反选

   ```shell
   # 显示不匹配"aaa"的内容
   grep -v "aaa" mount_wzc.sh
   ```

6. 当前目录下的全部文件和文件夹里查找内容

   ```shell
   grep ${CONTENT} -r ./*
   
   grep 192.168.2.131 -r ./*
   ```

7. 只显示文件名

   ```shell
   grep ${CONTENT} -l ./*
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
   
2. 指定http代理

   + 目的地址是https

     ```shell
     wget -e "https_proxy=http://10.10.10.23:8090" https://github.com/ShowYouShowme/SwitchyOmega/archive/v2.5.20.tar.gz
     ```

   + 目的地址是http

     ```shell
     wget -e "http_proxy=http://127.0.0.1:8087" http://www.subversion.org.cn/svnbook/1.4/
     ```

     



# curl

1. post请求

   + json数据

     ```shell
     curl -X POST -H "Content-Type:application/json" \
     http://127.0.0.1:2375/containers/create \
     -d \
     " \
     { \
     \"Image\":\"centos:7.6.1810\" \
     }"
     ```

   + url编码的数据

     ```shell
     curl -d "name=Rafael%20Sagula&phone=3320780" http://www.where.com/guest.cgi
     ```

     

2. GET请求

   1. 基本请求

      ```shell
      curl http://www.weirdserver.com:8000/
      ```

   2. 标准请求

      ```shell
      curl -X GET --header 'Accept: application/json' 'http://127.0.0.1:5000/api/v1/accounts/statistics'
      ```

      

3. 下载文件

   + 下载并用指定名称存储

     ```shell
     curl -o thatpage.html http://www.netscape.com/
     ```

   + 下载文件并用远程文件名存储

     ```shell
     curl -O http://www.netscape.com/index.html
     ```

4. 使用代理

   + http代理

     ```shell
     # https的网站用connect 方法,必须增加-L选项自动跟踪重定向,否则容易出错
     curl -x http://10.10.10.23:8090 -v -L -o a.tar.gz https://github.com/ShowYouShowme/SwitchyOmega/archive/v2.5.20.tar.gz
     ```

5. 打印调试信息

   + 打印交互细节

     ```shell
     curl -v ftp://ftp.upload.com/
     ```

   + 打印二进制信息到文件

     ```shell
     curl --trace trace.txt www.baidu.com
     ```

6. <font color="red" style="font-weight:bold">跟踪重定向`-L`</font>

   > 建议请求加上此选项，有些下载链接会重定向，无此选项会失败

7. <font color="red">设置头部信息`-H`</font>

8. Coockies

   + 发请求时添加Cookies信息

     ```shell
     curl -b "name=Daniel" www.sillypage.com
     ```

   + 存放响应的Cookies

     1. 方式一

        ```shell
        curl --dump-header headers www.example.com
        ```

     2. 方式二

        ```shell
        curl -c cookies.txt www.example.com
        ```

        

   + 使用存放在文件里面的Cookies信息访问网站

     ```shell
     curl -b headers www.example.com
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

  



# nc

+ nc是netcat的简写

+ 功能

  > 1. 监听TCP/UDP端口
  > 2. 端口扫描
  > 3. 文件传输
  > 4. 网络测速

+ 安装

  ```shell
  yum install -y nc
  ```

+ 用法

  > 1. 监听TCP端口
  >
  >    ```shell
  >    nc -l 9999
  >    ```
  >
  > 2. 监听UDP端口
  >
  >    ```shell
  >    nc -ul 9998
  >    ```
  >
  > 3. 文件传输
  >
  >    1. 在目的机器文件监听端口
  >
  >       ```shell
  >       nc -l ${port} > ${file}
  >       
  >       # 示例
  >       nc -l 9900 > nc.txt
  >       ```
  >
  >    2. 在源机器发送文件
  >
  >       ```shell
  >       nc ${dst_host} ${port} < ${file}
  >       
  >       # 示例
  >       nc 10.10.10.190 9900 < anaconda-ks.cfg
  >       ```
  >
  > 4. 测试网速
  >
  >    1. 在目的机器监听，并将数据丢弃
  >
  >       ```shell
  >       nc -l 9991 > /dev/null
  >       ```
  >
  >    2. 在源机器上发起请求
  >
  >       ```shell
  >       nc 10.10.10.190 9991 < /dev/zero
  >       ```
  >
  >    3. 查看网速
  >
  >       ```shell
  >       # 安装
  >       yum install -y dstat
  >       
  >       # 注意recv 和 send 两列
  >       dstat
  >       ```
  >
  > 5. 测试端口是否开启
  >
  >    ```shell
  >    # 可以替代telnet
  >    nc -zv 192.168.3.79 22
  >    ```
  >
  >    

# chown

+ 作用：修改文件属主

+ 示例

  ```shell
  chown ${user} ${file}
  ```



# nmap

+ 作用 => 网络发现和安全审核工具

+ 示例

  > 1. 端口扫描
  >
  >    ```shell
  >    nmap -p 1-65535 47.112.251.164
  >    ```
  >
  > 2. 扫描一个网段的主机存活数
  >
  >    ```shell
  >    nmap -sP 10.10.10.1/24
  >    ```
  >
  >    

  


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

 ## 1 使用代理

```shell
# xshell 里面的'连接'有个代理的选项;可以设置http tunnel 或者 socket5 代理
```

## 2 本地隧道

```shell
#1--隧道仅转发流量[端口映射],此方法可以通过跳板机连接测试机和线上的服务器,防止被攻击

ssh -N -f -L 0.0.0.0:2121:47.75.37.140:22 47.112.162.19

ssh -N -f -L ${本地IP}:${本地端口}:${目的服务器IP}:${目的服务器端口} ${中间服务器IP}


#2--不经过跳板机的映射
# 本机2121端口映射到47.112.251.164:1081
ssh -N -f -L 0.0.0.0:2121:47.112.251.164:1081 127.0.0.1 

#3--本地1089端口映射到172.18.29.247:1082,公网1082未对外暴露
# 47.112.251.164 是公网地址,172.18.29.247是机器网卡地址,1082端口不对外开放
# 此方法可以让服务器只对外暴露22端口,其它服务端口均通过映射的方式,安全性极高
ssh -N -f -L 0.0.0.0:1089:172.18.29.247:1082 47.112.251.164

ssh -N -f -L ${局域网IP}:${局域网端口}:${线上服务器内网IP}:${线上服务器端口,不对外暴露} ${线上服务器公网IP}
```

## 3 远程隧道

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



## 5 密钥登陆

1. 生成密钥

   ```shell
   # 指定加密类型和注释，rsa长度默认为2048位
   ssh-keygen -t rsa -C "myname@163.com"
   
   # 更简单的方案
   ssh-keygen
   ```

2. 放置公钥(Public Key)到服务器~/.ssh/authorized_key文件中

3. 登陆

   ```shell
   # 登陆命令
   ssh -i ${密钥名} -p ${port} ${user}@${host}
   
   # 例子
   ssh -i your_key -p 12008 root@dna2.viewdao.com
   ```



## 6 长时间无操作，ssh自动断开

1. 修改ssh服务配置[方式一]

   ```shell
   # /etc/ssh/sshd_config
   ClientAliveInterval 60     # 每分钟发送一次心跳，然后客户端响应，从而保持链接                                                     
   ClientAliveCountMax 3      # 客户端3次不响应心跳就断开链接 
   ```

2. 修改ssh客户端配置[方式二]

   ```shell
   # vim /etc/ssh/ssh_config  对所有用户有效
   # vim  ~/.ssh/config 对当前用户有效
   Host *
       ServerAliveInterval 30
       ServerAliveCountMax 3
   ```



## 7 远程服务器执行脚本

1. 执行服务器上的shell脚本

   ```shell
   ssh  -p 12008 root@dna3.viewdao.com bash /root/remote.sh
   ```

2. 执行本地脚本

   ```shell
   # 执行本地脚本
   ssh  -p 12008 root@dna3.viewdao.com < local.sh
   
   # 执行本地脚本,并且传入参数
   ssh  -p 12008 root@dna3.viewdao.com "bash -s " < local.sh 66778
   ```



## 8 公钥拷贝到远程机器

```shell
ssh-copy-id -p ${port} ${user}@${host}

ssh-copy-id -p 22 root@192.168.1.2
```





##8 

# 查看文件夹大小

```shell
du -sh ./protobuf/
```





# rsync

> 文件同步工具




# iptable

1. 安装

   ```shell
   yum install -y iptables
   ```

2. 只允许指定ip的数据进来

3. 端口映射

4. 只允许指定目的地的流量出去

5. 显示规则

   ```shell
   iptables -nL --line-number
   ```

6. 删除规则

   ```shell
   # 删除FORWARD链的第二条规则
   iptables -D FORWARD 2
   ```

7. 只允许指定IP访问某个端口

   ```shell
   iptables -A INPUT -p tcp --dport 22 -s 47.106.120.244 -j ACCEPT
   iptables -A INPUT -p tcp --dport 22 -j DROP
   ```

8. 常见使用案例

   + 模拟网线突然被掐断的情况[TCP连接,网络被掐断,而双方都不知道]





# iostat

0. 功能

   ```
   输出CPU和磁盘I/O相关的统计信息
   ```

1. 安装

   ```shell
   yum install sysstat -y
   ```

2. 示例

   ```shell
   # 每两秒采样一次,共采样3次
   iostat -d 2 
   
   # 每两秒采样一次,不断采样
   iostat -d 2 
   ```




# iotop

+ 功能

  > 查看磁盘使用情况



# **dstat**

+ 介绍：性能监控工具，可以用来替换iostat，netstat之类的工具

+ 安装

  ```shell
  yum install -y dstat
  ```

+ 使用

  ```shell
  dstat
  ```





# 性能监控工具

+ nmon
+ zabbix
+ cacti



# 服务器安全相关

1. 禁止root登录，只能用别的用户登录，再切换到root
2. 只有业务端口暴露，其它端口(mysql，redis)用堡垒机映射到内网，并且用iptables限制这些端口只能被堡垒机访问
3. 如果服务器部署在国外，可以映射到国内(用堡垒机)，然后客户端访问，避免被掐断
4. 用vpn，这是最简单的方法





# awk

+ 功能

  ```
  按空白将行分割为单词,并遍历全部行执行任务
  ```

+ 示例

  1. 批量删除任务

     ```shell
     ps -ef | grep python3 | grep -v grep | awk '{print "kill -9 " $2}' |sh
     ```

  2. 查找进程pid
  
     ```shell
     # 查找进程rsync的PID
     bin="rsync"
     PID=`ps -eopid,cmd | grep "$bin" |  grep -v "grep" |awk '{print $1}'`
     # 进程存在则杀死
     if [ "$PID" != "" ]; then
             kill -9 $PID
             echo "kill -9 $PID"
     fi
     ```
  
  3. 递归删除当前目录下全部日志文件
  
     ```shell
     find ./ -name *.log |  awk '{print "rm -f " $1}' | sh
     ```
  
  4. 选取指定行
  
     + 选取2到6行
  
       ```shell
       docker images | sed -n "${n1},${n2}p" | awk '{print "rm -f " $1}'
       
       docker images | sed -n "2,6p"
       ```
  
     + 选取1,2,5行
  
       ```shell
       docker images | sed -n "${n1}p;${n2}p;${n3}p"
       
       docker images | sed -n "1p;2p;5p"
       ```
  
     + 选取1，2，3，4和6行
  
       ```shell
       docker images | sed -n "${n1},${n2}p;${n3}p"
       
       docker images | sed -n "1,2p;6p"
       ```
  
  5. 批量删除docker镜像
  
     ```shell
     docker images | sed -n "2,6p" | awk '{print "docker rmi " $3}' | sh
     ```
  
     

# nl

## 显示行号

1. 打印文件，并显示行号

   ```shell
   nl sources.list
   ```

2. 和管道结合

   ```shell
   netstat -lntp | nl
   ```



# wc

统计行数

1. 统计正在运行的容器数量

   ```shell
   docker ps | wc -l
   ```

   



# shutdown

1. 重启

   ```shell
   shutdown -r now
   ```




# which

作用：查找可执行文件的路径

示例

```shell
which bash
```





# systemctl 配置

```shell
[Unit]
Description=The Apache HTTP Server  # 描述
After=network.target remote-fs.target nss-lookup.target #在network.target,remote-fs.target和nss-lookup.target后启动
Documentation=man:httpd(8)
Documentation=man:apachectl(8)

[Service]
Type=notify
EnvironmentFile=/etc/sysconfig/httpd
ExecStart=/usr/sbin/httpd $OPTIONS -DFOREGROUND # 启动服务的命令, $OPTIONS 在EnvironmentFile文件里面
ExecReload=/usr/sbin/httpd $OPTIONS -k graceful # 重启命令
ExecStop=/bin/kill -WINCH ${MAINPID}		# 停止命令
# We want systemd to give httpd some time to finish gracefully, but still want
# it to kill httpd after TimeoutStopSec if something went wrong during the
# graceful stop. Normally, Systemd sends SIGTERM signal right after the
# ExecStop, which would kill httpd. We are sending useless SIGCONT here to give
# httpd time to finish.
KillSignal=SIGCONT
PrivateTmp=true  # 非服务分配独立的临时空间

[Install]
WantedBy=multi-user.target # 多用户模式下需要
```


# yum

1. 查找软件包是否存在

   ```shell
   # List a package or groups of packages
   yum list | grep redis
   
   # 建议用下面这个
   # Search package details for the given string
   yum search openssl
   ```

2. 安装epel仓库

   ```shell
   # 安装EPEL(额外的软件包)
   yum install epel-release
   ```
   
3. 虚拟机阿里源连接超时

   ```shell
   # step1：在阿里云ECS上查询IP地址
   nslookup mirrors.aliyun.com
   
   # step2: 逐个在虚拟机上测试速度
   ping 110.80.139.243
   
   # step3: 找出速度最快的,写到虚拟机的hosts文件里
   110.80.139.249    mirrors.aliyun.com
   ```

4. `CentOS7`切换为阿里源

   ```shell
   # 深圳阿里云速度慢,可以换成网易云
   # step1:备份
   mv /etc/yum.repos.d/CentOS-Base.repo /etc/yum.repos.d/CentOS-Base.repo.backup
   
   # step2:下载阿里源的repo
   wget -O /etc/yum.repos.d/CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-7.repo
   
   
   # step3:更新缓存
   yum makecache
   ```






# 堡垒机的web后台搭建

[jumpserver](https://www.jumpserver.org/)







# 增加swap的大小

***

```shell
# 操作系统为ubuntu
mkdir swapfile
cd ./swapfile/
sudo dd if=/dev/zero of=swap bs=1G count=5 # 大小为5G

# 文件类型转换为swap
sudo mkswap -f swap

# 挂载
sudo swapon swap

# 卸载
sudo swapoff swap

# 开机挂载
vim /etc/fstab
/root/swapfile/swap none swap defaults 0 0
```





# 时间

***



## 更改时区

***

1. 查看系统当前时间

   ```shell
   date -R
   ```

2. 修改配置文件`/etc/profile`

   ```shell
   # 增加一行 ubuntu 18.04 的做法
   TZ='Asia/Shanghai'; export TZ
   ```

3. 再次查看时间

   ```shell
   data -R
   ```




## 同步时间

***

1. 安装**ntpdate**工具

   ```shell
   sudo apt-get install ntpdate
   ```

2. 将系统时间和网络时间同步

   ```shell
   ntpdate cn.pool.ntp.org
   ```

3. 将时间写入硬件<font color="blue">[可选]</font>

   ```shell
   hwclock --systohc
   
   # 时钟分为两种
   ## 1 硬件时钟
   ## 2 系统时钟，由Linux内核的时钟保持的时间
   ```

   

4. 查看时间

   ```shell
   date
   ```





# chmod

***

+ 作用：修改文件，目录的权限

+ 操作对象

  1. u：用户user，文件或目录所有者
  2. g：用户组group，文件或者目录所属的用户组
  3. o：其它用户other
  4. a：所有用户all

+ 操作符

  1. +：添加权限
  2. -：减少权限
  3. =：直接给定权限

+ 权限

  1. r：读取
  2. w：写入
  3. x：执行

+ 例子

  1. 给其它用户增加写入权限

     ```shell
     chmod o+w 1.txt
     ```

  2. 给文件属主增加执行权限

     ```shell
     chmod u+x 1.txt
     ```

  3. 递归设置权限

     ```shell
     chmod o+w -R ./share
     ```

  4. 用数字设置权限

     ```shell
     # rwx r-x r-x
     chmod 755 1.txt
     ```

     



# htop

***

+ top的替代产品

+ 安装

  ```shell
  yum install -y htop
  ```

+ 操作

  1. F1 --> 帮助
  2. F2 -->配置界面显示信息
  3. F3 --> **进程搜索**
  4. F4 --> **进程过滤**
  5. F5 --> 显示进程树
  6. F6 --> 排序
  7. F7 --> 减少nice值
  8. F8 --> 增加nice值
  9. F9 --> **杀掉指定进程**
  10. F10 --> 退出htop