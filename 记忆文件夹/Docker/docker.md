
# 第一章 docker 配置



## 1.1 安装docker

```shell
# 参考官方文档
# https://docs.docker.com/engine/install/centos/

# centos7 安装docker
sudo yum remove docker \
                  docker-client \
                  docker-client-latest \
                  docker-common \
                  docker-latest \
                  docker-latest-logrotate \
                  docker-logrotate \
                  docker-engine

sudo yum install -y yum-utils
sudo yum-config-manager \
    --add-repo \
    https://download.docker.com/linux/centos/docker-ce.repo

# 安装最新版本
sudo yum install docker-ce docker-ce-cli containerd.io docker-compose-plugin -y

# 启动docker
sudo systemctl enable docker
sudo systemctl start docker


# 测试docker是否可用
sudo docker run hello-world
```



## 1.2 配置



### 1.2.1 打开配置文件

```shell
vim /etc/docker/daemon.json
```



### 1.2.2 配置内容

```shell
{
"registry-mirrors": ["http://hub-mirror.c.163.com"],
"dns" : [ "223.5.5.5","223.6.6.6" ]
}
```



### 1.2.3 重启服务

```shell
systemctl restart docker
```



## 1.3 启动失败

> 1. 查看日志
>
>    ```shell
>    systemctl status docker.service
>    ```
>
> 2. 错误日志
>
>    ```shell
>    # 日志里面的错误信息 -- SELinux未关闭
>    Error starting daemon: SELinux is not supported
>    ```
>
> 3. 解决方案
>
>    ```shell
>    关闭SELinux,重启电脑
>    ```

## 1.4 启动docker容器

```shell
# 方法一： 交互式启动 ubuntu 20.04 启动并且挂载目录
sudo docker run --name mysql --hostname master-node -it -v /data:/data centos:centos7.9.2009 /bin/bash



# 方法二： 后台启动 服务必须在前台运行的方式
sudo docker run --name test3  --hostname test3  -d  centos:centos7.9.2009 /path/to/yourapp

# 方法三： 命令如果执行完毕了，或者叫指定的应用终结时，容器会自动停止，加上-t 后阻止容器终止
sudo docker run --name test3  --hostname test3  -td  centos:centos7.9.2009 /bin/bash

#将端口映射到环回网卡
docker run -it -d -p 127.0.0.1:5000:5000 docker.io/centos:latest /bin/bash
```



## 1.5 启动参数

```shell
-a stdin: 指定标准输入输出内容类型，可选 STDIN/STDOUT/STDERR 三项；

-d: 后台运行容器，并返回容器ID；

-i: 以交互模式运行容器，通常与 -t 同时使用；

-P: 随机端口映射，容器内部端口随机映射到主机的端口

-p: 指定端口映射，格式为：主机(宿主)端口:容器端口

-t: 为容器重新分配一个伪输入终端，通常与 -i 同时使用；

--name="nginx-lb": 为容器指定一个名称；

--dns 8.8.8.8: 指定容器使用的DNS服务器，默认和宿主一致；

--dns-search example.com: 指定容器DNS搜索域名，默认和宿主一致；

-h "mars": 指定容器的hostname；

-e username="ritchie": 设置环境变量；

--env-file=[]: 从指定文件读入环境变量；

--cpuset="0-2" or --cpuset="0,1,2": 绑定容器到指定CPU运行；

-m :设置容器使用内存最大值；

--net="bridge": 指定容器的网络连接类型，支持 bridge/host/none/container: 四种类型；

--link=[]: 添加链接到另一个容器；

--expose=[]: 开放一个端口或一组端口；

--volume , -v: 绑定一个卷
```





# 第二章 常见操作



## 2.1 查看日志

```shell
docker logs -f ${容器名}

docker logs -f ${容器ID}

# 只显示最后100行
docker logs -f --tail=100 e9badb669c52
```



## 2.2 镜像导入导出

1. 导出镜像

   ```shell
   docker save -o nginx.tar nginx:latest
   
   # 或者
   docker save > nginx.tar nginx:latest
   ```

2. 导入镜像

   ```shell
   docker load -i nginx.tar
   
   # 或者
   docker load < nginx.tar
   ```




## 2.3 文件复制

1. 宿主机文件复制到docker内部

   ```shell
   docker cp /path/filename 容器id或名称:/path/filename
   ```

2. docker内部文件复制到宿主机

   ```shell
   docker cp 容器id或名称:/path/filename /path/filename
   ```




## 2.4 挂载目录

1. 目录不能是root或者其子目录，否则无法读写，除非加`--privileged`



## 2.5 查看容器占用资源

```shell
docker stats -a
```



## 2.6 列出本地镜像

```shell
docker images
```



## 2.7 查看容器

```shell
# 查看所有容器
docker ps -a

# 查看正在运行的容器
docker ps
```



## 2.8 进入docker容器

### 2.8.1 docker attach

```shell
# 所有窗口同步显示,不推荐此方法
docker attach ${容器ID}  

docker attach 44fc0f0582d9  
```



### 2.8.2 ssh

```shell
# 需要安装ssh服务
```



### 2.8.3 nsenter

1. 安装

   ```shell
   wget https://www.kernel.org/pub/linux/utils/util-linux/v2.24/util-linux-2.24.tar.gz
   tar -xzvf util-linux-2.24.tar.gz
   cd util-linux-2.24/
   ./configure --without-ncurses
   make nsenter
   cp nsenter /usr/local/bin
   ```

2. 使用

   > 1. 获取容器的进程ID
   >
   >    ```shell
   >    # 命令格式
   >    docker inspect -f {{.State.Pid}} ${容器ID}
   >    
   >    # 示例
   >    docker inspect -f {{.State.Pid}} 44fc0f0582d9
   >    ```
   >
   > 2. 访问容器
   >
   >    ```shell
   >    # 命令格式
   >    nsenter --target ${PID} --mount --uts --ipc --net --pid
   >                                                                
   >    # 示例
   >    nsenter --target 3326 --mount --uts --ipc --net --pid
   >    ```
   >
   >    



### 2.8.4 docker exec

```shell
# 会另外启一个进程[推荐此方法]
docker exec -it 775c7c9ee1e1 /bin/bash
```





## 2.9 退出docker容器

***

1. 退出并关闭容器

   ```shell
   exit
   ```

   

2. 退出不关闭容器

   ```shell
   # 按住ctrl,然后按下P,然后再按下Q 注意是大写字母
   Ctrl+P+Q
   ```

   

## 2.10 查看docker内进程

***

```shell
# 可以查看docker 内正在运行的进程
top
```



## 2.11 screen

> 要保持docker容器处于活跃状态，运行的进程不能中断，某个app默认以后台启动时，此时用screen包裹docker
>
> 1. 让服务前台运行
> 2. 在screen里面启动docker
> 3. 带参数-ti启动，执行完命令后在xshell里把窗口关闭



## 2.12 启动停止容器

```shell
docker stop ${containerID}
```



## 2.13 启动容器

```shell
# 启动被stop的容器
docker start ${containerID}

# 或者
docker restart ${containerID}
```



## 2.14 指定镜像名

```shell
--name mysql
```



## 2.15 指定主机名

```shell
--hostname master-node
```



## 2.16 容器执行命令

+ 查看容器进程

  ```shell
  sudo docker exec test3 ps -ef
  ```

+ 杀死容器中某个进程

  ```shell
  # 先用sudo docker exec test3 ps -ef 查看进程ID
  sudo docker exec test3 kill -9 39
  ```

+ 容器服务更新流程

  ```shell
  # step-1 停止容器服务
  sudo docker exec  powell ps -ef  # 查看容器服务PID
  sudo docker exec  powell kill -9 58 # 停止服务
  
  # step-2 更新代码
  
  # step-3 启动服务
  sudo docker exec -td powell python3 /data/test.py
  
  ## 缺点：容器的日志无法通过docker logs查看，可以将日志目录挂载出来
  ```

  



## 2.17 无法使用systemctl

描述：使用centos7的镜像的容器，使用systemctl会报错Failed to get D-Bus connection: Operation not permitted



解决方案

```shell
# step-1 使用特权模式运行容器
docker run -d --name centos7 --privileged=true centos:7 /usr/sbin/init

# step-2 进入容器
docker exec -it centos7 /bin/bash

# step-3 安装和启动服务
yum install vsftpd
systemctl start vsftpd
```



## 2.18 保存容器为镜像

构建开发或者运行环境时，需要安装很多依赖，有些情况下使用dockerfile很难处理，安装完成后可以保存容器为镜像，下次部署只需要挂载目录然后执行命令即可。



保存步骤

1. 退出容器

   ```shell
   exit
   
   # 确保容器已经关闭
   docker ps -a
   ```

2. 保存容器为新镜像

   ```shell
    docker commit 23c18d958279 nginx:v0.2
   ```

3. 导出镜像为压缩包

   ```shell
   docker save -o nginx.tar nginx:v0.2
   ```




## 2.19 服务更新



### 更新步骤

1. 停止容器

   ```shell
   docker stop ${containerID}
   ```

2. 更新挂载目录的代码

3. 启动容器

   ```shell
   docker start ${containerID}
   ```



### 示例

```shell
# Dockerfile
FROM centos:centos7.9.2009
RUN yum install -y python3
WORKDIR /data
CMD ["/usr/bin/python3", "test.py"] # 服务启动命令,必须前台运行
```

启动命令

```shell
sudo docker run --name biden --hostname biden -d -v /home/nash/tmp:/data main-network:v1
```





## 2.20 删除容器

1. 删除一个容器

   ```shell
   docker rm ${containerID}
   ```

2. 删除全部容器

   ```shell
   docker ps -a | sed -n "2,$"p | awk '{print "docker rm " $1}' | sh
   ```

   





# 第三章 常用官方镜像

## 3.1 MySQL

1. 下载镜像

   ```shell
   docker pull mysql:5.6.47
   ```

2. 启动镜像

   > + 从宿主机挂载数据目录
   >
   >   ```shell
   >   docker run --name mysql -e MYSQL_ROOT_PASSWORD=tars2015 -d -p 3306:3306 -v /home/wzc/mysql-data:/var/lib/mysql mysql:5.6.47
   >   ```
   >
   > + 使用自定义配置文件
   >
   >   ```shell
   >   docker run --name some-mysql -v /my/custom:/etc/mysql/conf.d -e MYSQL_ROOT_PASSWORD=my-secret-pw -d mysql:tag
   >   ```

3. 链接mysql

   ```ini
   docker run -it --rm mysql:5.7 mysql -h192.168.2.110 -uroot -ptars2015
   ```

   



## 3.2 Redis

1. 下载镜像

   ```shell
   docker pull redis
   ```

2. 启动容器

   ```shell
   docker run --name some-redis -d redis
   ```

3. 连接

   ```ini
   ;redis-cl
   docker run -it --link some-redis --rm redis redis-cli -h some-redis
   ```



## 3.3 mongodb







# 第四章 镜像制作

文件名：Dockerfile

## 4.1 nginx



### 4.1.1 dockerfile

```dockerfile
FROM centos:7

# 修改这一行可以禁用Docker build cache
ENV REFRESHED_AT 2020-03-04
RUN yum install -y wget
# 类似CD命令
WORKDIR /home  
RUN wget http://nginx.org/download/nginx-1.16.1.tar.gz
RUN tar -zxvf nginx-1.16.1.tar.gz
WORKDIR ./nginx-1.16.1

# nginx配置文件在VIM中高亮
RUN mkdir ~/.vim/
RUN cp -r ./contrib/vim/* ~/.vim/

RUN yum install gcc pcre pcre-devel zlib zlib-devel openssl openssl-devel -y


RUN ./configure --prefix=/usr/local/nginx/

RUN make -j4


RUN make install
```



### 4.1.2 制作镜像

```shell
docker build -t nginx:v1 .
```



### 4.1.3 启动命令

> 1. 前台启动
>
>    ```shell
>    docker run -t -i -p 4444:80 nginx:v1 /bin/bash
>    ```
>
> 2. 后台启动
>
>    1. screen里面启动docker
>    2. 执行命令`/usr/local/nginx/sbin/nginx`
>    3. xshell里把窗口关闭





## 4.2 nginx V2



### 4.2.1 dockerfile

```dockerfile
FROM centos:7 

RUN yum install gcc pcre pcre-devel zlib zlib-devel openssl openssl-devel -y
```



### 4.2.2 制作镜像

```shell
docker build -t nginx:v1 .
```



### 4.2.3 启动

```shell
# 必须有编译好的nginx
docker run -t -i -p 4444:80 -v ${PWD}/nginx:/usr/local/nginx nginx:v1 /bin/bash
```






## 4.3 sinatra



### 4.3.1 dockerfile

```dockerfile
FROM centos:7
ENV REFRESHED_AT 2020-03-05
WORKDIR /home
COPY ruby-2.5.7.tar.gz /home
RUN yum install -y gcc gcc-c++ make openssl-devel zlib-devel readline-devel gdbm-devel
RUN tar -zxvf ./ruby-2.5.7.tar.gz
WORKDIR ./ruby-2.5.7
RUN ./configure --prefix=/usr/local/ruby
RUN make
RUN make install
ENV PATH=$PATH:/usr/local/ruby/bin
RUN gem source -r https://rubygems.org/
RUN gem sources --add https://gems.ruby-china.com/
RUN gem sources -u
RUN gem install --no-rdoc --no-ri sinatra json redis
RUN mkdir -p /opt/webapp
EXPOSE 4567
RUN ln -s /usr/local/ruby/bin/ruby /usr/bin/ruby
RUN ls /usr/bin/ruby
```



### 4.3.2 启动命令

```shell
docker run -t -i -p 4567:4567 --privileged -v /home/yourDoom/sinatra/webapp:/opt/webapp sinatra:v5 /opt/webapp/bin/webapp
```



## 4.4 apache



### 4.4.1 dockerfile

```dockerfile
FROM centos:7

RUN yum install -y httpd

CMD ["/usr/sbin/httpd", "-DFOREGROUND"] # 从httpd.service里面拿出来的
```



### 4.4.2 启动命令

```shell
docker run -d -p 80:80 -v /home/xman/apache/html:/var/www/html apacher:v123
```



## 4.5 rummy服务

1. Dockerfile放在rummy项目的根目录

2. Dockerfile

   ```dockerfile
   FROM golang:1.21.1
   
   # COPY 目录到docker容器里
   # COPY 只复制目录中的内容而不包含目录自身
   COPY . /home/rummy
   RUN /bin/bash -c 'ls -l /home/rummy'
   WORKDIR /home/rummy
   RUN go mod tidy
   
   # 编译golang最好禁用CGO
   RUN CGO_ENABLED=0 go build
   RUN echo "build end!"
   RUN /bin/bash -c 'ls -l /home/rummy'
   ```

4. 构建命令

   ```shell
    # 加上 --progress=plain 可以看到执行shell命令后的输出
    docker build -t rummy:v1 . --no-cache --progress=plain
   ```
   





## 4.6 使用代理构建golang项目

golang下载依赖时经常失败，配置代理即可解决问题

```shell
docker build --build-arg HTTPS_PROXY=http://192.168.180.43:3128 -t rummy:v2 .
```



# 第五章 Dockerfile命令

1. **COPY**：复制目录/文件到容器；如果复制的是目录，只复制目录中的内容而不包含目录自身

   ```
   COPY . /home/rummy
   
   
   COPY rummy/ /home/rummy
   ```

   

2. ADD

   + 复制目录/文件到容器；如果复制的是目录，只复制目录中的内容而不包含目录自身

   + 解压压缩文件并把它们添加到镜像中

     ```dockerfile
     WORKDIR /app
     
     # 可以是gitee打出的包
     ADD nickdir.tar.gz .
     ```

3. FROM：设置基础镜像

4. RUN：执行shell命令

5. WORKDIR：设定工作目录

6. MAINTAINER：设置Dockerfile的作者

   ```shell
   CMD=MAINTAINER ${NAME}
   
   # 比如
   MAINTAINER nash
   ```

7. **[一般用不到]**USER：指令设置用户名或（UID）和可选用户组（或GID），用于运行`Dockerfile`中接下来的`RUN`、`CMD`、`ENTRYPOINT`指令

   ```
    USER <user>[:<group>]
    USER <UID>[:<GID>]
   ```

8. **[一般用不到]**SHELL：设置默认shell，Linux上默认shell是`["/bin/sh","-c"]`

9. **[一般用不到]**HEALTHCHECK：健康检查

   ```ini
   [命令形式]
   
   ; 禁用从基础镜像继承的任何健康检查
   cmd = HEALTHCHECK NONE
   
   ; 通过容器内运行命令来检查容器健康状况
   cmd = HEALTHCHECK [OPTIONS] CMD command
   返回值 = 0  success  容器是健康的
   返回值 = 1  unhealthy 容器没有正常工作
   返回值 = 2  reserved  没有使用退出状态
   
   [OPTIONS]
   --interval=DURATION：检查间隔，default: 30s
   --timeout=DURATION：检查超时时间，超出此范围认为检查失败，default: 30s
   --start-period=DURATION：容器初始化阶段的时间，此阶段健康检查失败不计入最大重试次数，如果检查成功则认为容器已启动，default: 0s
   --retries=N：健康检查连续失败次数，default: 3
   
   [EXAMPLE]
    HEALTHCHECK --interval=5m --timeout=3s \
      CMD curl -f http://localhost/ || exit 1
   ```

10. 设置容器退出时唤起的系统调用信号,用于让容器内的程序在接收到signal之后可以先处理些未完成的事务，实现优雅结束进程后退出容器

    ```
     STOPSIGNAL signal
    ```

11. ENTRYPOINT：`ENTRYPOINT`和`CMD`一样，都是在指定容器启动程序以及参数，不会它不会被`docker run`的命令行指令所覆盖。如果要覆盖的话需要通过`docker run --entrypoint`来指定

    ```
     ENTRYPOINT ["exec","param1","param1"]
     ENTRYPOINT command param1 param2
    ```

12. ARG：构建时使用的命令，docker build 可以传入参数，这个参数只会在构建时存在，不会保留在镜像中

    ```shell
    ARG <name>[=<default value>]
    
    docker build --build-arg <varname>=<value>
    
    
    # 预定义的环境变量
    HTTP_PROXY  http代理
    http_proxy
    HTTPS_PROXY https代理
    https_proxy
    FTP_PROXY
    ftp_proxy
    NO_PROXY
    no_proxy
    
    # 配置https代理
     docker build --build-arg HTTPS_PROXY=https://my-proxy.example.com .
    ```

13. ENV：设置环境变量，在后续任何RUN命令中使用，并在容器运行时保持。一般用于软件更便捷的运行

    ```
     ENV PATH=/usr/local/nginx/bin:$PATH
     CMD ["nginx"]
    ```

14. EXPOSE：通知容器在运行时监听某个端口，可以指定TCP或UDP，如果不指定协议，默认为TCP端口；正常除了网关和登录服，其它服务都映射到127.0.0.1即可

    ```shell
     EXPOSE 80/tcp
     EXPOSE 80/udp
     
     
     docker run -P：将所有端口发布到主机接口，每个公开端口绑定到主机上的随机端口
     docker run -p ：显式映射单个端口或端口范围
    ```

15. CMD：指令来指示`docker run`命令运行镜像时要执行的命令。Dockerfile只允许使用一次`CMD`命令。使用多个`CMD`会抵消之前所有的命令，只有最后一个命令生效

    ```
     FROM ubuntu
     CMD ["/usr/bin/wc","--help"]
    ```

16. RUN：执行shell命令

    ```
     RUN /bin/bash -c 'echo $HOME'
     
     RUN echo $HOME
     
     默认在Linux上使用/bin/sh -c，在Windows上使用cmd /S /C
    ```
    
    



# 第五章  Docker网络

处于一个docker网络内的容器，可以用容器名称访问其它的容器[访问其它服务比如mysql，redis非常方便]。也可以隐藏db，后端业务服的端口号。使用docker网络后，只需要对外暴露给客户端访问的端口，数据库和内部服务端口不需要暴露。



命令

| 命令       | 功能                                                 |
| ---------- | ---------------------------------------------------- |
| connect    | Connect a container to a network                     |
| create     | Create a network                                     |
| disconnect | Disconnect a container from a network                |
| inspect    | Display detailed information on one or more networks |
| ls         | List networks                                        |
| prune      | Remove all unused networks                           |
| rm         | Remove one or more networks                          |



## 5.1 使用案例

+ 创建网络

  ```shell
  docker network create simple-network
  ```

+ 创建容器

  ```shell
  docker run -itd --name=test11 busybox
  
  docker run -itd --name=test22 busybox
  ```

+ 容器加入网络

  ```shell
  sudo docker network connect simple-network test11
  sudo docker network connect simple-network test22
  ```

+ 查看网络中的容器

  ```shell
  sudo docker network inspect simple-network
  ```

  

+ 测试容器是否能ping通

  ```shell
  sudo docker exec -it test 11 /bin/bash
  
  ping test22
  ```

+ 测试容器telnet是否成功

  ```shell
  # step-1 在test22 里监听端口
  nc -l 123
  
  # step-2 在test11 里面telnet测试
  telnet test22 123
  ```

  

# 第六章 Docker Compose

作用：单个节点上定义和运行多个容器的工具



## 6.1 安装

```shell
curl -L https://github.com/docker/compose/releases/download/1.25.4/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# 名字是docker-compose-Linux-x86_64
```



## 6.2 示例应用





# 第七章 Docker Swarm

Docker集群管理工具，简易版的k8s，适用于中小型项目（几个~几十个节点），对比k8s更加简单。



# 第八章 Docker machine

作用：快速帮助我们搭建 Docker 主机环境





# 第九章 Docker API

+ Registry API：存储docker镜像
+ Docker Hub API：与docker Hub集成的功能
+ Docker Remote API：与docker守护进程集成的API，本章重点介绍





## 9.1 访问docker API

1. 修改配置文件`/usr/lib/systemd/system/docker.service`

   ```shell
   变量ExecStart增加选项-H tcp://0.0.0.0:2375
   ```

2. 重新加载和启动docker守护进程

   ```shell
   systemctl --system daemon-reload
   ```

3. 访问

   ```shell
   docker -H 127.0.0.1:2375 info
   ```



## 9.2 测试API



## 9.2.1 管理docker镜像

1. 获取镜像列表

   ```shell
   curl http://127.0.0.1:2375/images/json | python3 -m json.tool
   ```

2. 查看docker信息

   ```shell
   curl http://127.0.0.1:2375/info | python3 -m json.tool
   ```

3. 查询指定镜像的信息

   ```shell
   curl http://127.0.0.1:2375/images/f1cb7c7d58b7/json | python3 -m json.tool
   ```

4. 在Docker Hub上面查找镜像

   ```shell
   curl http://127.0.0.1:2375/images/search?term=nginx | python3 -m json.tool
   ```



## 9.2.2 管理docker容器

1. 列出正在运行的容器

   ```shell
   curl http://127.0.0.1:2375/containers/json | python3 -m json.tool
   ```

2. 列出全部容器

   ```shell
   curl http://127.0.0.1:2375/containers/json?all=1 | python3 -m json.tool
   ```

3. 创建容器

   ```shell
   curl -X POST -H 'Content-Type:application/json' http://127.0.0.1:2375/containers/create -d '{ "Image":"centos:7.6.1810" }'
   ```

   分行的格式

   ```shell
   curl -X POST -H "Content-Type:application/json" \
   http://127.0.0.1:2375/containers/create \
   -d \
   " \
   { \
   \"Image\":\"centos:7.6.1810\" \
   }"
   ```

4. 启动容器

   ```shell
   curl -X POST -H "Content-Type:application/json" http://127.0.0.1:2375/containers/8a4a1fc441ae/start -d {}
   ```

5. 获取指定容器信息

   ```shell
   curl http://127.0.0.1:2375/containers/8a4a1fc441ae/json | python3 -m json.tool
   ```



## 9.3 认证Docker Remote API



## 9.3.1 建立证书授权中心

1. 创建目录

   ```shell
   mkdir -p /home/docker
   cd /home/docker
   ```

2. 生成序列化记录文件

   ```shell
   echo 01 > ca.srl
   ```

3. 生成私钥

   ```shell
   openssl genrsa -des3 -out ca-key.pem
   
   # 密码暂时指定为:1234
   ```

4. 创建CA证书

   ```shell
   # 信息全部留空
   openssl req -new -x509 -days 365 -key ca-key.pem -out ca.pem
   ```




## 9.3.2 创建服务器证书和密钥

1. 创建服务器密钥

   ```shell
   openssl genrsa -des3 -out server-key.pem
   
   # 密码暂时指定为:5678
   ```

2. 创建服务器证书签名请求(CSR)

   ```shell
   openssl req -new -key server-key.pem -out server.csr
   
   # Common Name 设置为网站域名,其它选项留空
   ```

3. 对CSR签名

   ```shell
   openssl x509 -req -days 365 -in server.csr -CA ca.pem -CAkey ca-key.pem -out server-cert.pem
   ```

4. 清除服务器密钥的密码，否则docker守护进程启动时要输入密码

   ```shell
   openssl rsa -in server-key.pem -out server-key.pem
   ```




## 9.3.3 配置Docker守护进程

1. 复制证书和密钥到指定目录

   ```shell
   cp ./ca.pem server-cert.pem server-key.pem  /etc/docker/
   ```

2. 修改docker配置文件

   ```shell
             # vi /usr/lib/systemd/system/docker.service
             
             --tlsverify \
             --tlscacert=/etc/docker/ca.pem \
             --tlscert=/etc/docker/server-cert.pem \
             --tlskey=/etc/docker/server-key.pem \
   ```

3. 重新加载并启动Docker守护进程

   ```shell
   systemctl --system daemon-reload
   ```




## 9.3.4 创建客户端证书和密钥

1. 创建客户端密钥

   ```shell
   openssl genrsa -des3 -out client-key.pem
   ```

2. 创建客户端CSR

   ```shell
   openssl req -new -key client-key.pem -out client.csr
   ```

3. 添加客户端认证属性

   ```shell
   echo extendedKeyUsage = clientAuth > extfile.cnf
   ```

4. 对客户端CSR签名

   ```shell
   openssl x509 -req -days 365 -in client.csr -CA ca.pem -CAkey ca-key.pem -out client-cert.pem -extfile extfile.cnf
   ```

5. 清除客户端密钥的密码

   ```shell
   openssl rsa -in client-key.pem -out client-key.pem
   ```




## 9.3.5 开启客户端认证功能

1. 复制证书和密钥

   ```shell
   mkdir -p ~/.docker
   cp ca.pem ~/.docker/
   cp client-key.pem  ~/.docker/key.pem
   cp client-cert.pem ~/.docker/cert.pem
   chmod 0600 ~/.docker/key.pem ~/.docker/cert.pem
   ```

2. 测试TLS认证过的连接

   ```shell
   docker -H=docker.example.com:2376 --tlsverify info
   ```

   









# 第十章  常见问题



## 10.1 静态ip

```ini
[创建自定义网络]
docker network create --subnet=172.11.0.0/20 mynetwork

[创建容器]
docker run -itd --name network_test --net mynetwork --ip 172.11.0.3 centos:latest /bin/bash
```

