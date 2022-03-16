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

   

# windows查看端口占用

```shell
# 查看指定端口被谁占用
netstat -aon|findstr "8081"


  TCP    172.18.80.183:6396     172.18.80.183:8888     ESTABLISHED     27068
  TCP    172.18.80.183:8888     0.0.0.0:0              LISTENING       12052   # 这个
  TCP    172.18.80.183:8888     172.18.80.183:6396     ESTABLISHED     12052
  

# 查看指定PID 的进程
tasklist|findstr "12052"


# 强行杀死进程
taskkill /T /F /PID 12052  
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
   # 如果公钥copy过去了,用户名不需要指定(root@ 可以省略)
   
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
   ssh-copy-id -i ~/.ssh/id_rsa.pub slzg@192.168.0.10
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

2. 从第五行开始打印到末尾

   ```shell
   tail -n +5 redis-server.log
   ```

3. docker 删除全部镜像

   ```shell
   docker rmi $(docker images | tail -n +2 | awk '{print $3}')
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



# 





# 解决RPM包依赖问题

1. 如上下载软件包及其依赖

2. 进入目录安装

   ```shell
   rpm -Uvh *
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
     curl -o thatpage.html http://www.netscape.com/ -L -v
     ```

   + 下载文件并用远程文件名存储

     ```shell
     curl -O http://www.netscape.com/index.html -L -v
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
  > 6. 替代telnet 连接服务
  >
  >    ```shell
  >    # 输入时,按下回车数据才会发送;Telnet 按下任意键都会发送数据
  >    nc ${host} ${port}
  >    ```
  >    
  > 7. 连接unix 域套接字
  >
  >    ```shell
  >    nc -U ./sample-socket
  >    ```
  >
  >    
  >
  > 
  >
  > 

# chown

+ 作用：修改文件属主

+ 示例

  ```shell
  chown ${user}[:${group}] ${file}
  
  chown -R nfsnobody:nfsnobody /data/share/
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

firewall是iptables的封装，推荐使用它替代iptables

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

8. 端口转发

   + 本机内部转发

     ```shell
     firewall-cmd --add-forward-port=port=7777:proto=tcp:toport=8888
     ```

   + 转发到其他机器

     ```shell
     firewall-cmd --add-forward-port=port=9000:proto=tcp:toport=8000:toaddr=192.168.1.102
     ```

9. 允许指定ip的全部流量

   ```shell
   firewall-cmd --zone=public --add-source=192.168.172.32 
   ```

10. 开启nat

    ```shell
    firewall-cmd --permanent --zone=public --add-masquerade
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

   ```shell
   ssh-copy-id -i ~/.ssh/id_rsa.pub slzg@192.168.0.10
   ```

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
   ssh  -p 12008 root@dna3.viewdao.com "bash /root/remote.sh"
   ```

2. 执行本地脚本

   ```shell
   # 执行本地脚本
   ssh  -p 12008 root@dna3.viewdao.com < local.sh
   
   # 执行本地脚本,并且传入参数
   ssh  -p 12008 root@dna3.viewdao.com "bash -s " < local.sh 66778
   ```
   
3. 命令远程机器执行命令

   ```shell
   # 先把公钥copy 过去
   ssh 192.168.0.1 "ls -l"
   ```

   



## 8 公钥拷贝到远程机器

```shell
ssh-copy-id -p ${port} ${user}@${host}

ssh-copy-id -p 22 root@192.168.1.2
```





# 查看文件夹大小

```shell
du -sh ./protobuf/
```





# rsync

***



## 选项和功能

***

| OPTION选项        | 功能                                                         |
| ----------------- | ------------------------------------------------------------ |
| -a                | 这是归档模式，表示以递归方式传输文件，并保持所有属性，它等同于-r、-l、-p、-t、-g、-o、-D 选项。-a 选项后面可以跟一个  --no-OPTION，表示关闭 -r、-l、-p、-t、-g、-o、-D 中的某一个，比如-a --no-l 等同于  -r、-p、-t、-g、-o、-D 选项。 |
| -r                | 表示以递归模式处理子目录，它主要是针对目录来说的，如果单独传一个文件不需要加 -r 选项，但是传输目录时必须加。 |
| -v                | 表示打印一些信息，比如文件列表、文件数量等。                 |
| -l                | 表示保留软连接。                                             |
| -L                | 表示像对待常规文件一样处理软连接。如果是 SRC 中有软连接文件，则加上该选项后，将会把软连接指向的目标文件复制到 DEST。 |
| -p                | 表示保持文件权限。                                           |
| -o                | 表示保持文件属主信息。                                       |
| -g                | 表示保持文件属组信息。                                       |
| -D                | 表示保持设备文件信息。                                       |
| -t                | 表示保持文件时间信息。                                       |
| --delete          | 表示删除 DEST 中 SRC 没有的文件。                            |
| --exclude=PATTERN | 表示指定排除不需要传输的文件，等号后面跟文件名，可以是通配符模式（如 *.txt）。 |
| --progress        | 表示在同步的过程中可以看到同步的过程状态，比如统计要同步的文件数量、 同步的文件传输速度等。 |
| -u                | 表示把 DEST 中比 SRC 还新的文件排除掉，不会覆盖。            |
| -z                | 加上该选项，将会在传输过程中压缩。                           |

记住最常用的几个即可，比如 -a、-v、-z、--delete 和 --exclude



## 示例

***

1. test1备份到test2

   ```shell
   rsync -av test1/ test2/
   ```

2. test1备份到test2，且删除test2中test1不存在的文件

   ```shell
   rsync -av --delete test1/ test2/
   ```

3. 拷贝本地机器内容到远程机器

   ```shell
   rsync -av /home/coremail/ 192.168.11.12:/home/coremail/
   ```

4. 远程机器内容拷贝到本地

   ```shell
   rsync -av 192.168.11.11:/home/coremail/ /home/coremail/
   ```

5. 显示远程机器的文件列表

   ```shell
   rsync -v rsync://192.168.11.11/data
   ```



# iptable

1. 安装

   ```shell
   yum install -y iptables
   ```

2. 只允许指定ip的数据进来

3. 端口映射

4. 只允许指定目的地的流量出去

5. **开启内核转发**

   ```shell
   # 跨主机端口转发必须开启
   # 本机转发不需要
   vim /etc/sysctl.conf
   net.ipv4.ip_forward = 1
   
   sysctl -p
   ```

   

6. 显示规则

   ```shell
   iptables -nL --line-number -t nat
   
   # nat表和input 之类的不是一个，所以要显式指出
   
   # 或者
   iptables -t nat -L -n
   ```

7. 删除规则

   ```shell
   # 删除FORWARD链的第二条规则
   iptables -D FORWARD 2
   
   
   # 删除PREROUTING的规则，POSTROUTING类似
   iptables -t nat -D PREROUTING 1
   iptables -t nat -D POSTROUTING 1
   
   # 删除全部规则
   iptables -t nat -F
   iptables -F
   ```

8. 只允许指定IP访问某个端口

   ```shell
   iptables -A INPUT -p tcp --dport 22 -s 47.106.120.244 -j ACCEPT
   iptables -A INPUT -p tcp --dport 22 -j DROP
   ```

9. 端口转发

   + 本机转发

     ```shell
     # 把发送到8000端口的流量转发到80
     iptables -t nat -A PREROUTING -s 192.168.1.0/24 -p tcp --dport 8000 -j REDIRECT --to 80
     ```

   + 跨主机转发[必须开启内核转发]

     ```shell
     #TCP转发
     iptables -t nat -A PREROUTING -p tcp --dport [端口号] -j DNAT --to-destination [目标IP]:[端口号]
     iptables -t nat -A POSTROUTING -p tcp -d [目标IP] --dport [端口号] -j SNAT --to-source [本地服务器IP]
     
     iptables -t nat -A PREROUTING -p tcp --dport 80 -j DNAT --to-destination 192.168.1.102:9090
     iptables -t nat -A POSTROUTING -p tcp -d 192.168.1.102 --dport 9090 -j SNAT --to-source 192.168.1.159
     
     #UDP转发
     iptables -t nat -A PREROUTING -p udp --dport [端口号] -j DNAT --to-destination [目标IP]:[端口号]
     iptables -t nat -A POSTROUTING -p udp -d [目标IP] --dport [端口号] -j SNAT --to-source [本地服务器IP]
     
     iptables -t nat -A PREROUTING -p udp --dport 53 -j DNAT --to-destination 192.168.1.1:53
     iptables -t nat -A POSTROUTING -p udp -d 192.168.1.1 --dport 53 -j SNAT --to-source 192.168.1.159
     ```

   + 多端口转发

     ```shell
     #将本地服务器的50000~65535转发至目标IP为1.1.1.1的50000~65535端口
     -A PREROUTING -p tcp -m tcp --dport 50000:65535 -j DNAT --to-destination 1.1.1.1
     -A PREROUTING -p udp -m udp --dport 50000:65535 -j DNAT --to-destination 1.1.1.1
     -A POSTROUTING -d 1.1.1.1/32 -p tcp -m tcp --dport 50000:65535 -j SNAT --to-source [本地服务器IP]
     -A POSTROUTING -d 1.1.1.1/32 -p udp -m udp --dport 50000:65535 -j SNAT --to-source [本地服务器IP]
     ```

10. 保存规则

    ```shell
    # 安装服务
    yum install iptables-services -y
    
    # 保存
     service iptables save
     
     # 设置服务开机启动
     systemctl enable iptables
    ```

11. nat转发，充当路由器角色

    ```shell
    #需要开启内核转发
    iptables -t nat -A POSTROUTING -s 192.168.1.0/24 -j SNAT --to-source 192.168.1.159
    
    ## 如果公网ip不固定， 下面的做法应该总是第一选择
    iptables -t nat -A POSTROUTING -s 192.168.1.0/24 -j MASQUERADE
    
    # dns查询数据包转发，这样内网可以设置dns server为nat服务器
    iptables -t nat -A PREROUTING -p udp --dport 53 -j DNAT --to-destination 192.168.1.1:53
    iptables -t nat -A POSTROUTING -p udp -d 192.168.1.1 --dport 53 -j SNAT --to-source 192.168.1.159
    ```

    

12. 常见使用案例

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



# top

1. 查看CPU个数

   ```shell
   按下Q上的数字1
   ```

2. 按CPU使用率排序

   ```shell
   P  [daxie]
   ```

3. 按内存使用排序

   ```shell
   M [daxie]
   ```

4. 存储单位修改

   ```shell
   shift + e
   ```
   
5. 查看指定进程

   ```shell
   top -p ${pid}
   ```

6. 查看指定多个进程

   ```shell
    top -p ${pid1},${pid2}
   ```

7. 监控指定进程

   ```shell
   top -p 3595782  -b -n 1 -d 3 > kvm.txt
   
   # -b: batch模式，可以重定向到文件中
   
   # -n 1: 一共取1次top数据
   
   # -d 3: 每次top时间间隔是3秒钟
   ```

8. 获取某个进程数据

   ```shell
   # c++ 可以执行此命令来获取标准输出 得到CPU 使用率
   top -p 3462371  -n 1
   ```

   






# 源码编译软件

1. 建议安装在/usr目录，这样可以直接搜索到include和so和bin文件（比如protobuf，openssl，libevent之类）
2. 安装在自定义路径,可以直接删除整个软件，方便删除







# 代理配置



## http代理

1. squid（性能好，推荐）

   ```shell
   # 支持connect 方法
   yum install squid
   
   # 启动服务
   systemctl start squid
   
   # 设置服务开机启动
   systemctl enable squid
   
   # 配置文件 一般不需要配置
   /etc/squid/squid.conf
   
   
   # 配置监听本地地址[可选]
   sed -i "s/3128/127.0.0.1:8888/g" /etc/squid/squid.conf
   ```

   

2. nginx(性能好，推荐)

   ```shell
   # nginx 性能特别高
   
   $ wget http://nginx.org/download/nginx-1.9.2.tar.gz
   $ tar -xzvf nginx-1.9.2.tar.gz
   $ cd nginx-1.9.2/
   $ patch -p1 < /path/to/ngx_http_proxy_connect_module/patch/proxy_connect.patch
   $ ./configure --add-module=/path/to/ngx_http_proxy_connect_module
   $ make && make install
   
   
   # 配置文件
    server {
        listen                         3128;
   
        # dns resolver used by forward proxying
        resolver                       8.8.8.8;
   
        # forward proxy for CONNECT request
        proxy_connect;
        proxy_connect_allow            443 563;
        proxy_connect_connect_timeout  10s;
        proxy_connect_read_timeout     10s;
        proxy_connect_send_timeout     10s;
   
        # forward proxy for non-CONNECT request
        location / {
            proxy_pass http://$host;
            proxy_set_header Host $host;
        }
    }
   ```

   

3. tinyproxy（性能差，不推荐）



## socks5代理





# 续行符

1. 符号："\\"当命令过长时使用

2. 例子

   ```shell
   # ls \
   > -lh   # 此时按下回车即可
   
   drwxrwxr-x.  4 root root 4.0K Apr 29 06:57 hiredis-1.0.0
   -rw-r--r--.  1 root root  96K May 28  2021 hiredis-1.0.0.tar.gz
   drwx------. 15 nash nash 4.0K Apr 28 04:12 nash
   drwxr-xr-x.  2 root root  12K May 28  2021 shared_dir
   -rw-r--r--.  1 root root  444 May  4 11:16 test.js
   ```
   
3. 注意：命令很长时，一般先在文本编辑器里面写好，再粘贴到terminal里面，此时续行符后面只能带换行



# 用户管理



## 添加用户

```shell
adduser ${user}
```



## 修改密码

```shell
passwd ${user}
```



# 赋予root权限

```shell

vim /etc/passwd

#用户名:密码:UID:GID:描述信息:主目录:默认shell
nash:x:1002:1002:nash:/home/nash:/bin/bash

# 修改为如下
nash:x:0:0:nash:/home/nash:/bin/bash
```





# 环境变量

1. 用指定环境变量启动程序

   ```shell
   myName=Nash ./a.out
   ```



# 查看命令帮助信息

```shell
killall --help

或者

killall -h
```





# 守护进程

1. 命令：daemonize

2. 作用：关闭终端后进程依然运行，用来替换nohup cmd & 和 screen；并且可以将控制台输出重定向

3. 参数

   ```shell
   -a             Append to, instead of overwriting, output files. Ignored 
                  unless -e and/or -o are specified.
   -c <dir>       Set daemon's working directory to <dir>.
   -e <stderr>    Send daemon's stderr to file <stderr>, instead of /dev/null.
   -E var=value   Pass environment setting to daemon. May appear multiple times.
   -o <stdout>    Send daemon's stdout to file <stdout>, instead of /dev/null.
   -p <pidfile>   Save PID to <pidfile>.
   -u <user>      Run daemon as user <user>. Requires invocation as root.
   -l <lockfile>  Single-instance checking using lockfile <lockfile>.
   -v             Issue verbose messages to stdout while daemonizing.
   ```
   
4. 示例

   ```shell
   daemonize -a -e  watch-dog.err -o watch-dog.out -p watch-dog.pid -c `pwd` /usr/bin/python3 /home/slzg/watch-dog/main.py /home/slzg/test 
   ```

   




# ps

1. 查看全部进程信息

   ```shell
   ps -ef
   ```

2. 查看指定进程信息

   ```shell
   ps -p ${pid} -f
   ```

3. 根据进程名查看信息

   ```shell
   ps -C ${procName} -f
   
   ps -C lock-free -f
   ```

   

# lsblk

作用：查看所有可用块设备的信息



示例

```shell
lsblk

NAME   MAJ:MIN rm   SIZE RO type mountpoint
sda      8:0    0 232.9G  0 disk 
├─sda1   8:1    0  46.6G  0 part /
├─sda2   8:2    0     1K  0 part 
├─sda5   8:5    0   190M  0 part /boot
├─sda6   8:6    0   3.7G  0 part [SWAP]
├─sda7   8:7    0  93.1G  0 part /data
└─sda8   8:8    0  89.2G  0 part /personal
sr0     11:0    1  1024M  0 rom

# type
disk: 磁盘

part: 分区
```



# 产生大文件

***

```shell
#产生20G的文件
dd if=/dev/zero of=file bs=1M count=20000
```



# 挂载

***



## 内存挂载为文件

***

```shell
sudo mount tmpfs /path/to/data -t tmpfs -o size=100G
```



## 内存挂载为目录

```shell
mount -t tmpfs -o size=1024m tmpfs /mnt/ram
```



## 系统自带内存目录

```shell
/dev/shm
```





## 取消挂载

***

```shell
sudo umount /dev/hda2
```





# Linux释放缓存

***

```shell
#将缓存写入文件
sync
#释放缓存
echo 1 > /proc/sys/vm/drop_caches
#由操作系统管理内存
echo 0 > /proc/sys/vm/drop_caches
```





# fdisk

***



功能：显示或者操作磁盘分区表



常用命令：

```shell
sudo fdisk -l
```





# dd

***

 作用：把文件/设备的内容 按字节复制到 另一个文件/设备



## 磁盘备份

```shell
dd if=/dev/sda of=/root/sda.img
```



## 磁盘恢复

```shell
dd if=/root/sda.img of=/dev/sdb
```



## 把一块磁盘内容复制到另外一块

```shell
#sda --> sdc
dd if=/dev/sda of=/dev/sdc
```



## 备份时压缩

```shell
dd if=/dev/sda | gzip > /root/sda.img.gz

#用bzip2算法
dd if=/dev/sda | bzip2 > disk.img.bz2
bzip2 -dc /root/sda.img.gz | dd of=/dev/sdc
```



## 备份磁盘分区

```shell
dd if=/dev/sda2 of=/root/sda_part1.img
```



## 备份内存

```shell
dd if=/dev/mem of=/root/mem.img
```



## 备份mbr

```shell
dd if=/dev/sda of=/root/sda_mbr.img count=1 bs=512

#恢复
dd if=/root/sda_mbr.img of=/dev/sda
```



## 特殊设备

***

1. /dev/null：任何写入它的数据都会被无情抛弃
2. /dev/zero：可以产生连续不断的 null 的流（二进制的零流），用于向设备或文件写入 null 数据，一般用它来对设备或文件进行初始化
3. /dev/urandom：生成理论意义上的随机数



```shell
#向磁盘上写一个大文件, 来看写性能
[root@roclinux ~]# dd if=/dev/zero bs=1024 count=1048576 of=/dev/shm/1Gb.file
 
#从磁盘上读取一个大文件, 来看读性能
[root@roclinux ~]# dd if=/dev/shm/1Gb.file bs=64k | dd of=/dev/null


#配合 time 命令，可以看出不同的块大小数据的写入时间，从而可以测算出到底块大小为多少时可以实现最佳的写入性能
[root@roclinux ~]# time dd if=/dev/zero bs=1024 count=1000000 of=/dev/shm/1Gb.file
[root@roclinux ~]# time dd if=/dev/zero bs=2048 count=500000 of=/dev/shm/1Gb.file
[root@roclinux ~]# time dd if=/dev/zero bs=4096 count=250000 of=/dev/shm/1Gb.file
[root@roclinux ~]# time dd if=/dev/zero bs=8192 count=125000 of=/dev/shm/1Gb.file

#使用 /dev/urandom 这个随机数生成器来产生随机数据，写到磁盘上，以确保将磁盘原始数据完全覆盖掉
[root@roclinux ~]# dd if=/dev/urandom of=/dev/sda
```





# 显卡

***

1. 查看显卡信息

   ```shell
   nvidia-smi
   ```

2. 安装





# cpu查看

***

```shell
lscpu
```



# 关机，重启

```shell
poweroff # 关机

reboot # 重启

shutdown -h now # 关机，推荐上面那个
```





# head

***

1. 打印文件前几行

   ```shell
   #打印前六行
   head -6 readme.txt
   ```



# hexdump

***

1. 以16进制和相应的ASCII字符显示文件里的字符

   ```shell
   hexdump -C test.txt 
   ```

2. 只格式化前n个字符

   ```shell
   hexdump -C -n 5 test.txt 
   ```

3. 跳过前面n个字符

   ```shell
   hexdump -C -s 5 test.txt 
   ```
   
   
   
   

# sha256sum

***

1. 作用：用sha256算法计算hash

2. 示例

   ```shell
   #不输入换行
   echo -n "hello_world" > file
   
   #计算hash
   sha256sum file
   
   
   #校验hash
   sha256sum file > file.sha256 #生成hash
   sha256sum -c file.sha256     #校验hash
   ```



# apt 使用代理

```shell
# 使用-o 选项执行代理的地址
sudo apt install virtualbox  -y -o Acquire::http::proxy="http://127.0.0.1:8090/"
```



# vim

***

1. 打开目录

   ```shell
   # 方法一
   vim .
   
   # 方法二
   :Ex
   ```

2. 执行命令

   ```shell
   #方法一
   :!${cmd}
   
   #方法二
   :shell 然后执行想要的命令,最后exit回到vim
   ```

3. 修改目录

   ```shell
   :cd /home/nash
   ```

4. 快速进入目录

   ```shell
   # step-1
   vim . 然后选择目录进入
   
   # step-2
   :cd ${target_dir} #目录在界面可以看到
   
   # step-3
   :shell 就直接到目的目录了,执行完命令再exit退回来即可
   ```






# centos7安装第三方仓库

```shell
yum install -y epel-release
```

