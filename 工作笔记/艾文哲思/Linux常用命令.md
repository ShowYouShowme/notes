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
   > 
   > netstat -ltpnae  #显示对应用户
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
   
   
   # 使用lsof
   lsof -i:3000  # 查看3000端口是否处于listening状态
   ```
   



# SS

类似netstat的一个工具，但是性能非常高，当服务器连接数或者time_wait过多是，netstat的运行速度会非常慢



帮助信息

```ini
Usage: ss [ OPTIONS ]
       ss [ OPTIONS ] [ FILTER ]
   -h, --help           this message
   -V, --version        output version information
   -n, --numeric        don't resolve service names
   -r, --resolve       resolve host names
   -a, --all            display all sockets
   -l, --listening      display listening socket
   -o, --options       show timer information
   -e, --extended      show detailed socket information
   -m, --memory        show socket memory usage
   -p, --processes      show process using socket
   -i, --info           show internal TCP information
   -s, --summary        show socket usage summary
 
   -4, --ipv4          display only IP version 4 sockets
   -6, --ipv6          display only IP version 6 sockets
   -0, --packet display PACKET sockets
   -t, --tcp            display only TCP sockets
   -u, --udp            display only UDP sockets
   -d, --dccp           display only DCCP sockets
   -w, --raw            display only RAW sockets
   -x, --unix           display only Unix domain sockets
   -f, --family=FAMILY display sockets of type FAMILY
 
   -A, --query=QUERY, --socket=QUERY
       QUERY := {all|inet|tcp|udp|raw|unix|packet|netlink}[,QUERY]
 
   -D, --diag=FILE      Dump raw information about TCP sockets to FILE
   -F, --filter=FILE   read filter information from FILE
       FILTER := [ state TCP-STATE ] [ EXPRESSION ]
```



查看统计信息

```shell
ss -s
```



统计TCP的状态

```ini
; 建立链接的数量
ss -s | sed -n "2p" | awk -F, '{print $1}' | awk '{print $4}'

; time_wait 的个数
ss -s | sed -n "2p" | awk -F, '{print $5}' | awk '{print $2}' | awk -F/ '{print $1}'

; syn_recv 的个数
 ss -o state syn-recv | wc -l
 
; 列出全部监听的端口
ss -lnt

; TCP 的全部状态 established, syn-sent, syn-recv, fin-wait-1, fin-wait-2, time-wait, closed, close-wait, last-ack, listening and closing
; 统计某个状态的TCP链接
ss -o state syn-recv | wc -l
```





# Linux上查看不可见字符

1.  windows上用\r\n作为换行，linux上用\n。shell脚本必须用\n换行，否则执行出错

2. 查看换行符

   ```shell
   # \r 用^M表示   \n用$表示
   cat -A vm-key.pri
   ```

3. 换行符转换

   ```shell
   # 单个文件
   sed -i 's/\r//'  filename
   
   # 多个文件
   sed -i 's/\r//'  filename1 filename2 ...
   ```




# 搜索路径

```shell
vim /etc/profile
export PATH=$PATH:/opt/bin
```





# 列出文件

```shell
ls -lh

#自动显示颜色,比如文件夹颜色,软连接颜色,docker里面默认全是白色
ls --color=auto -lh
```





# ansible

作用：批量操作机器

安装

```shell
yum install epel-release -y
yum install -y ansible
```

配置

```shell
vim /etc/ansible/hosts

# 加入以下内容
[www_jfedu]
192.168.1.88
```

执行shell命令

```shell
ansible www_jfedu  -m shell -a "pwd"

# ping
ansible www_jfedu  -m ping

# 拷贝文件
ansible www_jfedu -m copy -a 'src=/root/install.log dest=/tmp/
```





# 压测ab

命令

```shell
# 500并发，发起10000个请求
ab -n 10000 -c 500 http://192.168.1.159:5000/

#常见错误 apr_socket_recv: Connection reset by peer (104)
vim /etc/sysctl.conf
##此参数是为了防止洪水DOS的，但对于大并发系统，要禁用此设置
net.ipv4.tcp_syncookies = 0
sysctl -p
```



# 查看网卡信息



## 全部网卡

```shell
ip a
```



## 指定网卡

```shell
# ifconfig ${网卡名}
ifconfig ens32
```







# 自动化部署流程

作用：常用于开发阶段



## 传统部署

```shell
# step-1 打包源码
tar -zcvf ebin.tar.gz ebin/*

# step-2 上传到服务器 注意配置ssh免密码登录
scp ebin.tar.gz dev:/data/hmyxz_code/v220228/server

# step-3 远程执行脚本
ssh dev "cd /data/hmyxz_code/v220228/server && source ./restart_server.sh"


# STEP-4 MAKEFILE
# make file 里面有 build, deploy 和 test[测试接口] 三个target 基本就够了

```



## jenkins部署

```shell
# step-1 在开发机上配置jenkins

# step-2 提交代码

# step-3 使用jenkins自动构建和发布
```





# sudo

作用：以root身份执行命令，主要在Debian的发行版上。



## Ubuntu

### 加入sudo用户组

```shell
usermod -aG sudo $username
```



### 查看是否拥有sudo权限

```shell
sudo whoami

# 你会被提示输入密码。如果用户有 sudo 权限，这个命令将会打印“root”
```



### 免密码执行sudo

```shell
# 使用vim编辑 visudo
export EDITOR=vim; 

sudo visudo

# 将以下行添加到文件最后, 替换用户名
$username  ALL=(ALL) NOPASSWD:ALL
```





## centos7

1. 修改配置文件

   ```shell
   vim /etc/sudoers
   
   # 注释掉这行
   %wheel ALL=(ALL)       ALL
   
   # 去掉这行的注释
   %wheel  ALL=(ALL)       NOPASSWD: ALL
   ```

2. 将用户加入组wheel

   ```shell
   # 以后每次sudo 都不需要输入命令了
   usermod -G wheel ${user}
   ```

3. 将某个用户加入sudo

   ```shell
   #加上NOPASSWD可以免输密码
   roglic ALL=(ALL) NOPASSWD:ALL
   ```

4. 将某个组加入sudo

   ```shell
   %wheel ALL=(ALL)       NOPASSWD: ALL
   ```

   

5. 问题

   > 1. We trust you have received the usual lecture from the local System。有时候会出现这样的提示，输入代码即可。
   >
   > 2. centos7下不可以设置免sudo运行部分命令。
   >
   > 3. 文件/etc/sudoers是只读的，需要用wq!来保存





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

  
  
  
  
  
  
  
  # su
  
  切换到指定用户
  
  ```shell
  su - root
  
  # 切换到root[针对ubuntu系统]
  sudo su - root
  ```
  
  
  
  切换到非登录用户shell
  
  ```shell
  #创建非登录用户
  useradd -s /sbin/nologin ftp
  # 切换到非登录用户ftp的shell
  su -s /bin/bash ftp
  
  # 进入用户加目录
  cd
  ```
  
  

# history



1. 执行历史命令

   ```shell
   # 56是命令标号
   !56
   ```

2. 搜索历史命令

   ```shell
   Ctrl + R
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

```ini
scp [命令参数] [源路径] [目的路径]

# 文件夹的话先打包,再传输,速度快很多
# 目的路径存在相同文件会直接覆盖

[拷贝目录]
cmd = scp -r test1/ aliyun:~/
tip = 目的目录存在同名文件会直接覆盖

[拷贝文件]
cmd = scp  a.txt aliyun:~/
tip = 目的目录存在同名文件会直接覆盖


[copy文件到win]
desc = win11 自带ssh client和 ssh server
开启ssh server = net start sshd ;管理员身份
cmd  = scp get_env.js  jumbo@192.168.2.108:/Users/jumbo/Desktop
```

## 2 常见操作

1. 将本地文件复制到远程[发布和部署时用到]

   ```shell
   # 如果公钥copy过去了,用户名不需要指定(root@ 可以省略)
   # 1-- 要将公钥copy过去
   # 2-- 在hosts里面配置域名和ip映射关系,这样就不用写ip地址了
   
   scp -r /home/administrator/ root@192.168.6.129:/etc/squid
   
   # ssh 配置一下, 这样更加简单
   scp aws:/home/ubuntu/erl-socks5/socks5.erl .
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

4. windows 可以使用git bash,也具有tail的功能

   ```shell
   tail -f C://Users//jumbo//project//hall_ts//tigerTraining.log
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

8. 显示行的数量

   ```shell
   netstat -apnt | grep ESTABLISHED -c
   ```

   




# lsof

作用：列出打开的文件，正常情况超过1024程序就会报错



```shell
# 列出打开的TCP链接，从1开始排序
lsof -p 1252164 | grep IPv4 | grep  IPv4 -n
```



```shell
# 查看某个端口的服务的全部链接
lsof -i:3000
```





# unlink

删除软连接



# rz 上传二进制文件

```shell
# 可以一次性选择多个文件的 ==此方式可以替代SFTP客户端上传
rz -be ${fileName}

# -y 选项可以替换-be
rz -y ${fileName}


# 也可以使用ftp服务,然后利用win的资源管理器上传和下载
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

3. 断点续传

   ```shell
   wget -c url
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
     
     # 或者
     curl  -H "Content-Type: application/json" -X POST -d '{"user_id": "123", "coin":100, "success":1, "msg":"OK!" }' "http://www.baidu.com/"
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
     
     # 或者
     curl -LO http://www.netscape.com/index.html
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
     
     
     #或者
     curl http://192.168.2.117:3001/ --cookie "someCookie"
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

9. 打印响应头 和响应码

   ```shell
   curl -I  http://127.0.0.1:3000/ 
   ```

10. 不显示进度条或者错误信息，只显示结果

   ```shell
   # 通常用于zabbix的监控
   curl -s http://127.0.0.1:3004/queryTps
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
  
  3. 根据CNAME查询IP
  
     ```shell
     nslookup -type=cname _cf07c7093e563600816ff2bb9c829f6f.zrvsvrxrgs.acm-validations.aws.
     ```
  
  4. 查询TXT信息
  
     ```shell
     #主要用于LetsEncrypt申请证书
     nslookup -query=txt  _acme-challenge.dev.icashflow.cc
     ```
  
     




# telnet 

tcp的客户端，测试端口是否处于监听状态。



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
  >    
  >    nc -l 127.0.0.1 5900
  >    
  >    nc -l 172.31.2.68 5900
  >    
  >    nc -l 0.0.0.0 5900
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
  >



# watch

作用：监控命令运行结果，省得你一遍遍手动运行



参数

| 选项 | 作用                                 |
| ---- | ------------------------------------ |
| -n   | 缺省每2秒运行一下程序                |
| -d   | 高亮显示变化的区域                   |
| -t   | 会关闭watch命令在顶部的时间间隔,命令 |

示例

+ 监控网络连接数

  ```shell
  watch -n 1 -d netstat -ant
  
  # 或者 会显示time-out剩余时间
  watch -n 1 -d netstat -ant
  ```

+ 监控http连接数

  ```shell
  watch -n 1 -d 'pstree|grep http'
  ```

+ 查看指定客户机连接数

  ```shell
  watch 'netstat -an | grep:21 | \ grep<模拟攻击客户机的IP>| wc -l' 
  ```

+ 查看目录中文件变化

  ```shell
  watch -d 'ls -l|grep scf'
  ```

+ 10s一次输出系统负载

  ```shell
  watch -n 10 'cat /proc/loadavg'
  ```

+ 配合tail查看日志

  ```shell
  # 每一秒显示后3行
  watch -n 1 tail -n 3 name.txt
  ```

+ watch和grep配合使用

  ```shell
  watch 'netstat -nat | grep 22'
  ```

+ 监控cpu使用情况

  ```shell
  watch -n 1 'top -n 1 -d 1 -b  | sed -n 3p'
  ```

  



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
  >    nmap -p 8000-10000 15.228.42.79 -Pn
  >    ```
  >
  > 2. 扫描一个网段的主机存活数
  >
  >    ```shell
  >    nmap -sP 10.10.10.1/24
  >    ```
  >
  > 3. 扫描指定端口
  >
  >    ```shell
  >    time nmap -p 1234 47.112.251.164
  >    ```
  >
  > 
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

11. 安装防火墙

    ```shell
    #aws的centos7默认未安装
    yum install firewalld firewall-config
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



## 1 远程隧道

```shell
# 让家里的电脑能访问公司内网的电脑

ssh -Nf -R 2222:127.0.0.1:22 47.112.162.19  # 公司内网机器执行

ssh -p 2222 127.0.0.1 # 机器47.112.162.19 执行,此时即可在家里访问公司内网的服务器

# 命令讲解
ssh -Nf -R ${中间服务器端口}:${局域网IP}:${局域网端口} ${中间服务器IP}

ssh -p ${局域网映射的端口} 127.0.0.1
```



## 2 密钥登陆

1. 配置服务器权限

   ```ini
   [.ssh]
   ;服务器的.ssh 目录的权限必须是700,执行命令ssh-keygen会自动生成该文件夹并且配置好权限
   cmd = chmod 700 .ssh
   
   [authorized_keys]
   ;authorized_keys 的权限是600
   cmd = chmod 600 authorized_keys
   
   [config]
   ;config 权限是600
   
   [秘钥文件]
   ;公钥和私钥的权限都必须是600,否则会出错
   ```

   

2. 生成密钥

   ```shell
   # 指定加密类型和注释，rsa长度默认为2048位
   ssh-keygen -t rsa -C "myname@163.com"
   
   # 更简单的方案
   ssh-keygen
   ```

3. ssh-keygen 用法

   ```ini
   [参数]
   -b = 指定密钥长度
   -e = 读取已有私钥或者公钥文件
   -f = 指定用来保存密钥的文件名
   -t = 指定要创建的密钥类型
   -C = 添加注释
   
   [EXAMPLE]
   ;默认方式创建秘钥
   cmd-1 = ssh-keygen
   
   ;指定参数
   cmd-2 = ssh-keygen -t rsa -b 2048 -f aliyun
   
   ;移动到秘钥目录
   cmd = mv aliyun aliyun.pub $HOME/.ssh
   ```

   

4. 放置公钥(Public Key)到服务器~/.ssh/authorized_key文件中

   ```shell
   ssh-copy-id -i ~/.ssh/id_rsa.pub slzg@192.168.0.10
   
   # 或者 打开服务器 ~/.ssh/authorized_keys , 把你的公钥复制进去
   # 服务器的.ssh 目录的权限必须是700, authorized_keys 的权限是600
   # 推荐先在服务器生成公私钥,然后再将私钥copy到客户端使用
   ```

5. 登陆

   ```shell
   # 登陆命令
   ssh -i ${密钥名} -p ${port} ${user}@${host}
   
   # 例子
   ssh -i your_key -p 12008 root@dna2.viewdao.com
   ```



## 3 长时间无操作，ssh自动断开

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



## 4 远程服务器执行脚本

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

   

## 5 多机器免密钥配置

1. 创建文件

   ```shell
   ~/.ssh/config
   
   # 证书的权限必须是600
   ```

2. 写入如下内容

   ```shell
   Host aliyun
       HostName 120.25.248.58
       User root
       Port 22
       IdentityFile ~/.ssh/aliyun.pem
   
   Host aws
       HostName 120.25.248.58
       User ubuntu
       Port 8000
       IdentityFile ~/.ssh/hk.pem
   ```

## 6 常用配置

1. 配置文件：/etc/ssh/sshd_config

2. 禁止root登录

   ```shell
   PermitRootLogin no
   ```

3. 禁止密码登录

   ```shell
   AuthorizedKeysFile   .ssh/authorized_keys   //公钥公钥认证文件
   PubkeyAuthentication yes   //可以使用公钥登录
   PasswordAuthentication no  //不允许使用密码登录
   ```

4. 限制用户只能执行sftp连接，不能ssh登录

   ```shell
   Subsystem sftp internal-sftp
   Match User fu           # 匹配用户
   X11Forwarding no        # 禁止X11转发
   AllowTcpForwarding no   # 禁止tcp转发
   ForceCommand internal-sftp
   
   
   # ChrootDirectory  不需要配置,配置这个需要copy大量的动态链接库，非常麻烦
   ```

   





# 查看文件夹大小

```shell
du -sh ./protobuf/
```





# rsync

***

主要是用来备份数据，rsync 的最大特点是会检查发送方和接收方已有的文件，仅传输有变动的部分。配合python脚本就可以定时备份了，不建议使用cron。和scp的区别：scp会拷贝全部文件，如果目的路径存在同名文件直接覆盖。



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

1. 安装

   ```shell
   sudo apt-get install rsync
   ```

2. 命令语法

   ```shell
    rsync -r source destination
   ```

1. test1备份到test2

   ```shell
   rsync -av test1/ test2/
   ```

2. test1备份到test2，且删除test2中test1不存在的文件

   ```shell
   rsync -av --delete test1/ test2/
   ```



## 远程同步



### ssh协议

1. 拷贝本地机器内容到远程机器

   ```shell
   rsync -av /home/coremail/ 192.168.11.12:/home/coremail/
   ```

2. 远程机器内容拷贝到本地

   ```shell
   rsync -av 192.168.11.11:/home/coremail/ /home/coremail/
   ```

3. 显示远程机器的文件列表

   ```shell
   rsync -v rsync://192.168.11.11/data
   ```



### rsync协议

必须在服务器部署rsync守护程序

1. 查看module列表

   ```shell
   rsync rsync://192.168.122.32
   ```

2. 同步数据

   ```shell
   rsync -av source/ rsync://192.168.122.32/module/destination
   ```



## 增量备份

```shell
rsync -a --delete --link-dest /compare/path /source/path /target/path

# --link-dest参数用来指定同步时的基准目录
# --link-dest参数指定基准目录/compare/path，然后源目录/source/path跟基准目录进行比较，找出变动的文件，将它们拷贝到目标目录/target/path。那些没变动的文件则会生成硬链接。这个命令的第一次备份时是全量备份，后面就都是增量备份了。
```

```shell
# 示例脚本

#!/bin/bash

# A script to perform incremental backups using rsync

set -o errexit
set -o nounset
set -o pipefail

readonly SOURCE_DIR="${HOME}"
readonly BACKUP_DIR="/mnt/data/backups"
readonly DATETIME="$(date '+%Y-%m-%d_%H:%M:%S')"
readonly BACKUP_PATH="${BACKUP_DIR}/${DATETIME}"
readonly LATEST_LINK="${BACKUP_DIR}/latest"

mkdir -p "${BACKUP_DIR}"

rsync -av --delete \
  "${SOURCE_DIR}/" \
  --link-dest "${LATEST_LINK}" \
  --exclude=".cache" \
  "${BACKUP_PATH}"

rm -rf "${LATEST_LINK}"
ln -s "${BACKUP_PATH}" "${LATEST_LINK}"
```





# iptables

1. 简介

   ```ini
   [安装]
   cmd = yum install -y iptables
   
   [说明]
   desc1 = iptables包含4个表，5个链。
   desc2 = 4个表:filter,nat,mangle,raw，默认表是filter
   desc3 = 5个链：PREROUTING,INPUT,FORWARD,OUTPUT,POSTROUTING
   
   [命令格式]
   cmd-1 = iptables -L [-t 表名] 如果没有指定表名,默认查看filter
   cmd-1-default = iptables -L -t filter
   
   cmd-2 = iptables -L [-t 表名] [链名]
   查看INPUT的规则 = iptables -L INPUT -n
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
   # 列出nat规则
   iptables -nL --line-number -t nat
   
   # nat表和input 之类的不是一个，所以要显式指出
   
   # 或者
   iptables -t nat -L -n
   
   # 列出规则, 非nat
   iptables -Ln
   
   # 列出INPUT链的规则
   iptables -L INPUT -n --line-number
   
   # 列出FORWARD的规则
   iptables -L FORWARD -n
   
   # 列出OUTPUT的规则
   iptables -L OUTPUT -n
   ```

7. 删除规则

   ```shell
   # 删除INPUT的第一条规则
   iptables -D INPUT 1
   
   # 删除FORWARD链的第二条规则
   iptables -D FORWARD 2
   
   
   # 删除PREROUTING的规则，POSTROUTING类似
   iptables -t nat -D PREROUTING 1
   iptables -t nat -D POSTROUTING 1
   
   # 删除全部规则
   iptables -t nat -F
   iptables -F
   ```

8. **只允许指定IP访问某个端口**

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
     
     
     
     # ubuntu
     sudo apt install iptables-persistent # 安装服务
     
     sudo netfilter-persistent  save
    ```

11. nat转发，充当路由器角色

    ```shell
    # 台式机里装虚拟机，虚拟机装centos7做nat，必须使用网线，测试无线网卡不可用
    
    #需要开启内核转发
    iptables -t nat -A POSTROUTING -s 192.168.1.0/24 -j SNAT --to-source 192.168.1.159
    
    ## 如果公网ip不固定， 下面的做法应该总是第一选择
    iptables -t nat -A POSTROUTING -s 192.168.1.0/24 -j MASQUERADE
    
    # dns查询数据包转发，这样内网可以设置dns server为nat服务器
    iptables -t nat -A PREROUTING -p udp --dport 53 -j DNAT --to-destination 192.168.1.1:53
    iptables -t nat -A POSTROUTING -p udp -d 192.168.1.1 --dport 53 -j SNAT --to-source 192.168.1.159
    ```

12. 丢弃数据包

    ```shell
    # 只允许管理员从202.13.0.0/16网段使用SSH远程登录防火墙主机
    
    iptables -A INPUT -p tcp --dport 22 -s 202.13.0.0/16 -j ACCEPT
    
    iptables -A INPUT -p tcp --dport 5600 -j DROP
    ```

13. DROP 和 RESET 对比

    1. iptables -A INPUT -p tcp -m tcp --dport 4444 -j DROP：对方会不断发送syn，直到超时，可以模拟断开网线的情况
    2. iptables -A INPUT -p tcp -m tcp --dport 5555 -j REJECT --reject-with icmp-port-unreachable：对方会发两次syn
    3. iptables -A INPUT -p tcp -m tcp --dport 5566 -j REJECT --reject-with tcp-reset ： 效果和4一样，返回reset
    4. \# 未被使用的 5568 端口作为参照

14. 常见使用案例

    + 模拟网线突然被掐断的情况[TCP连接,网络被掐断,而双方都不知道]





# iostat

0. 功能

     ```shell
     输出CPU和磁盘I/O相关的统计信息，主要关注TPS
     
     # 测试命令
     dd if=/dev/zero of=/opt/test2 bs=1k count=10240000
     ```

1. 安装

   ```shell
   yum install sysstat -y
   ```

2. 示例

   ```shell
   # 每两秒采样一次,共采样3次
   iostat -d 2 3
   
   # 每两秒采样一次,不断采样
   iostat -d 2 
   
   #以MB为单位显示
   iostat -d 1 -m
   
   #以kB为单位显示
   iostat -d 1 -k
   ```

3. 列解释

   | Device   | tps            | kB_read/s | kB_wrtn/s | kB_read  | kB_wrtn  |
   | -------- | -------------- | --------- | --------- | -------- | -------- |
   | 磁盘名称 | 每秒钟的io请求 | 读取速率  | 写入速率  | 总共读取 | 总共写入 |

4. 磁盘监控

   ```ini
   ;如果传输的数据非常多,可以把-k改为-m,用MB作为单位
   monitorCmd = iostat -d 1 -k
   
   ;监控工具 zabbix
   ```

   




# iotop

+ 功能

  > 查看磁盘使用情况
  
+ 信息说明

  ```ini
  
  [概览]
  Total DISK READ   = 从磁盘中读取的总速率
  Total DISK WRITE  = 往磁盘里写入的总速率
  
  ;监控该值
  Actual DISK READ  = 从磁盘中读取的实际速率
  
  ;监控该值
  Actual DISK WRITE = 往磁盘里写入的实际速率
  
  [列]
  TID 		= 线程ID，按p可转换成进程ID
  PRIO 		= 优先级
  USER 		= 线程所有者
  ;监控该值
  DISK READ 	= 从磁盘中读取的速率
  ;监控该值
  DISK WRITE 	= 往磁盘里写入的速率
  ;监控该值
  SWAPIN 		= swap交换百分比
  ;监控该值
  IO> 		= IO等待所占用的百分比
  COMMAND 	= 具体的进程命令
  ```
  
  



# **dstat**

+ 介绍：性能监控工具，可以用来替换iostat，netstat之类的工具，监控磁盘用iostat

+ 安装

  ```shell
  yum install -y dstat
  ```

+ 使用

  ```shell
  dstat
  ```
  
+ 信息说明

  ```ini
  ;CPU使用率
  [----total-cpu-usage----]
  usr  = 用户空间的程序所占百分比
  sys  = 系统空间程序所占百分比
  idel = 空闲百分比
  wai  = 等待磁盘I/O所消耗的百分比
  hiq  = 硬中断次数
  siq  = 软中断次数
  
  ;磁盘统计
  [-dsk/total-]
  read = 读的字节总数
  writ = 写的字节总数
  
  ;网络统计
  [-net/total-]
  recv = 网络收包总数
  send = 网络发包总数
  
  ;内存分页统计
  [---paging--]
  in = pagein（换入）
  out =page out（换出）
  
  ;系统信息
  [---system--]
  int = 中断次数
  csw = 上下文切换
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
       
       #选取第二行到最后一行
       docker ps -a | sed -n "2,$"p | awk '{print "rm -f " $1}'
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
       
     + 从第二行到最后一行
  
       ```shell
       sed -n "2, $"p test.lua 
       ```
  
     + 选取第二行
  
       ```shell
       ss -s | sed -n "2p"
       ```
  
       
  
  5. 批量删除docker镜像
  
     ```shell
     docker images | sed -n "2,6p" | awk '{print "docker rmi " $3}' | sh
     ```
  
  6. 指定分隔符
  
     ```shell
     # 分隔符紧跟在-F参数后面（中间没有空格）
     awk -F, '{print $2}' test.txt
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




# 清除history记录

```shell
rm -rf ~/.bash_history
history -c
```





# shutdown

1. 重启

   ```shell
   shutdown -r now
   
   # 或者
   reboot
   ```
   
2. 关机

   ```shell
   shutdown -h now
   
   # 或者
   poweroff
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
   # 查找java相关的包
   yun list java*
   
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
   
5. 安装本地rpm包

   ```shell
   # 会自动解决依赖问题
   yum localinstall grafana.rpm -y
   
   # 或者
   yum localinstall *.rpm -y
   ```
   
6. 查看已安装的包

   ```shell
   rpm -qa| grep nginx
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
   
   #查看全部可用时区
   timedatectl list-timezones
   ```

2. 修改时区

   ```shell
   timedatectl set-timezone "Asia/ShangHai"
   ```
   
3. 再次查看时间

   ```shell
   data -R
   ```
   
4. 文件备份

   ```shell
   mv ebin ebin-`date  +%Y-%m-%d-%H-%M-%S`
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

1. 选项

   | 选项 | 作用                                         |
   | ---- | -------------------------------------------- |
   | -d   | 更新间隔，默认3s                             |
   | -b   | 批处理模式，用于将输出重定向到文件，避免乱码 |
   | -n   | 执行次数，默认一直执行                       |
   | -p   | 进程pid                                      |
   | -u   | 指定用户                                     |
   | -s   | 安全模式                                     |

   

2. 查看CPU个数

   ```shell
   按下Q上的数字1
   ```

3. 按CPU使用率排序

   ```shell
   P  [daxie]
   ```

4. 按内存使用排序

   ```shell
   M [daxie]
   ```

5. 存储单位修改

   ```shell
   shift + e
   ```

6. 查看指定进程

   ```shell
   top -p ${pid}
   ```

7. 查看指定多个进程

   ```shell
    top -p ${pid1},${pid2}
   ```

8. 监控指定进程

   ```shell
   top -p 3595782  -b -n 1 -d 3 > kvm.txt
   
   # -b: batch模式，可以重定向到文件中
   
   # -n 1: 一共取1次top数据
   
   # -d 3: 每次top时间间隔是3秒钟
   ```

9. 获取某个进程数据

   ```shell
   # c++ 可以执行此命令来获取标准输出 得到CPU 使用率
   top -p 3462371  -n 1
   ```




# 查看进程信息

```shell
# 可以看到进程包含的线程数，内存，uid等等
cat /proc/{pid}/status
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
# root用户执行此命令，ubuntu 用 sudo su - 切换到root
adduser ${user}  # 只需要设置密码，其它的全部直接按回车

# 创建.ssh目录
su - powell && cd ~ && mkdir .ssh
cd .ssh && touch authorized_keys  # 把公钥粘贴到里面即可

#创建用户并指定其家目录
mkdir /home/second
useradd fuck -d /home/second/fuck
```



## 删除用户

```shell
userdel -r nash
```



## 修改密码

```shell
passwd ${user}
```





# 用户组

1. 查看用户所在组

   ```shell
   groups ${user}
   ```

2. 将用户加入指定组

   ```shell
   # -a append
   usermod -a -G groupA user
   
   
   # 注意 会使你离开其他用户组，仅仅做为 这个用户组 groupA 的成员
   usermod -G groupA user
   ```

3. 创建用户组

   ```shell
   groupadd groupname
   ```

4. 删除用户组

   ```shell
   groupdel groupname
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




# 进程状态



| 进程状态 | 含义                                                         | 对应ps命令的状态码                            |
| -------- | ------------------------------------------------------------ | --------------------------------------------- |
| 运行     | 正在运行或在运行队列中等待                                   | R 运行 runnable (on run queue)                |
| 中断     | 休眠中, 受阻, 在等待某个条件的形成或接受到信号               | S 中断 sleeping                               |
| 不可中断 | 收到信号不唤醒和不可运行, 进程必须等待直到有中断发生         | D 不可中断 uninterruptible sleep (usually IO) |
| 僵死     | 进程已终止, 但进程描述符存在, 直到父进程调用wait4()系统调用后释放 | Z 僵死 a defunct (”zombie”) process           |
| 停止     | 进程收到SIGSTOP, SIGSTP, SIGTIN, SIGTOU信号后停止运行运行    | T 停止 traced or stopped                      |

只需要关注运行R和中断S两种。



查看进程状态

```shell
# top 或者 ps -aux
```



统计处于R状态的进程数

```shell
ps -aux | sed -n "2, $"p | awk '{print  $8}' | grep R | wc -l
```



系统负载分析

```shell
# STEP-1 查看负载
uptime
00:44:22 up  1:17,  3 users,  load average: 8.13, 5.90, 4,94

# load average:    8.13,5.90,4,94
# 显示的是过去的1,5,15分钟内进程队列中的平均进程数量

# 系统负载这个指标表示的是系统中当前正在运行的进程数量，它等于running状态的进程数 + uninterrupt状态的进程数 
# load = runing tasks num + uninterrupt tasks num


# STEP-2 查看负载是否过高

如果每个cpu(可以按CPU核心的数量计算)上当前活动进程数不大于3，则系统性能良好
不大于4，表示可以接受
如大于5，则系统性能问题严重
上面例中的8.13,如果有2个cpu核心,则8.13/2=4.065,  此系统性能可以接受

# STEP-3 CPU 核心数查看

## 方法一  top命令按下1
## 方法二  lscpu
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

4. 查看指定用户进程

   ```shell
   # 生产机器上全部业务服务都用一个非root帐号启动，此方式可以快速查看全部进程
   ps -u ubuntu -f
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



# fio



测试磁盘的随机读写和顺序读写性能





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

5. 替换

   ```shell
   # 间隔符可以自定义,比如用/ 或者 # 或者@
   :%s#${原字符串}#${新字符串}#g
   ```

   






# centos7安装第三方仓库

```shell
yum install -y epel-release
```



# Rsyslog

Rsyslog可以简单的理解为syslog的超集，系统日志工具。类似Logstash、ElasticSearch、Kibana



## 作用

1. 把不同节点的日志收集到一台节点上
2. 同一节点，systemctl管理的服务的日志收集到一个文件夹下，方便查看



# 分界符

以<<EOF开始，EOF结束

1. 多行内容输入文件，当你需要输入多行内容到配置文件就有用了

   ```shell
   cat <<EOF >>name.txt
   this is your name
   second day!
   EOF
   ```

   

2. 多行内容输出到控制台

   ```shell
   cat <<EOF
   echo "hello"
   echo " world"
   EOF
   ```



# centos7 源码编译gcc9.2

```shell
cd /home/build
GCC_VERSION=9.2.0
wget https://ftp.gnu.org/gnu/gcc/gcc-${GCC_VERSION}/gcc-${GCC_VERSION}.tar.gz
tar xzvf gcc-${GCC_VERSION}.tar.gz
mkdir obj.gcc-${GCC_VERSION}
cd gcc-${GCC_VERSION}
./contrib/download_prerequisites
cd ../obj.gcc-${GCC_VERSION}
../gcc-${GCC_VERSION}/configure --disable-multilib --enable-languages=c,c++
make -j $(nproc)
make install

#卸载已经安装的gcc和g++
yum remove gcc gcc-c++
#用户重新登录即可
```







# Windows常用命令

1. 列出目录下的全部文件

   ```shell
   dir
   ```

2. 创建目录

   ```shell
   md ${dirName}
   ```

3. 显示当前目录

   ```shell
   pwd
   ```

4. 创建文件

   ```ini
   cmd     = fsutil file createnew ${fileName} ${fileSize}
   example = fsutil file createnew filename.txt 0
   
   ;必须是cmd,不支持powershell
   CMD = TYPE NUL > ${fileName}
   EXAMPLE = TYPE NUL > hello.txt
   ```

5. 删除文件

   ```shell
   del ${fileName}
   ```

6. 删除文件夹

   ```ini
   [删除空文件夹]
   cmd     = rmdir ${folderName}
   example = rmdir Rubbish
   
   
   [删除非空文件夹]
   cmd-1 = rm -r ${folderName}
   example = rm -r Rubbish
   
   cmd-2 = rmdir  /S /Q  ${folderName}
   example = rmdir  /S /Q  Rubblish
   ```

7. 查看帮助信息

   ```ini
   [查看全部命令]
   ;必须是cmd,不是powershell
   cmd = help
   
   [查看单个命令的帮助信息]
   cmd = rmdir /?
   ```

8. 清屏

   ```ini
   cmd = cls
   ```

9. 进程管理

   ```ini
   ;查看指定端口被谁占用
   cmd = netstat -aon|findstr "8081"
   
   ;查看监听的端口
   cmd = netstat -aon|findstr "TCP" | findstr "LISTENING"
   
     TCP    172.18.80.183:6396     172.18.80.183:8888     ESTABLISHED     27068
     TCP    172.18.80.183:8888     0.0.0.0:0              LISTENING       12052   # 这个
     TCP    172.18.80.183:8888     172.18.80.183:6396     ESTABLISHED     12052
     
   
   ;查看指定PID 的进程
   cmd = tasklist|findstr "12052"
   
   
   ; 强行杀死进程
   cmd = taskkill /T /F /PID 12052  
   ```

10. 复制文件

    ```ini
    CMD     = copy ${src} ${dst}
    EXAMPLE = copy index.txt index.txt.bak 
    ```

11. 复制文件夹

    ```ini
    CMD-1 = Xcopy /E /I C:\dir1\sourcedir D:\data\destinationdir
    
    ;目的目录加上后缀\就不需要/I,建议原目录和目的目录都加上\
    CMD-2 = Xcopy /E C:\dir1\sourcedir D:\data\destinationdir\
    ```

12. 移动目录

    ```ini
    ;文件重命名
    CMD = MOVE ${srcFile} ${dstFile}
    
    ;文件夹重命名
    CMD = MOVE ${name1} ${name2}
    
    ;移动文件夹
    CMD     = MOVE ${srcPath} ${dstPath}
    EXAMPLE =  move .\tt\tmp3 .\
    ```

13. 环境变量

    ```ini
    [设置环境变量]
    CMD = SET varName=Value
    
    [打印环境变量]
    CMD = echo %MyName%
    ```

14. 运行程序

    ```ini
    ;启动一个单独的命令提示符窗口来运行指定的程序或者命令
    CMD = start
    
    ;打开画图工具
    EXAMPLE-1 = start mspaint 
    
    ;打开注册表
    EXAMPLE-2 = start regedit
    
    ;打开控制面板
    EXAMPLE-3 = start control
    
    ;打开记事本
    EXAMPLE-4 = start notepad
    
    ;打开notepad++
    EXAMPLE-5 = start notepad++
    
    ;打开vscode
    EXAMPLE-5 = start code
    ```

15. 查看可执行文件路径，类似linux的which命令

    ```ini
    ;在默认情况下，搜索是在当前目录和 PATH 环境变量指定的路径中执行的。
    CMD = where
    
    ;查询regedit.exe
    EXAMPLE = where regedit
    
    [常见参数]
    /R = 从指定目录开始，递归性搜索并显示符合指定模式的文件。
    
    EXAMPLE = where /R C:\Windows  hosts
    ```

    

