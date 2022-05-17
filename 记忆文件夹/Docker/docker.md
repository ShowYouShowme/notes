
# 第一章 docker 配置



## 1.1 安装docker

```shell
# centos7
yum install -y docker

# centos8 用以下命令
yum install --allowerasing docker-ce
systemctl start docker # 启动
systemctl status docker # 查看状态
systemctl enable docker.service # 设置服务开机启动

# ubuntu 18.04
sudo apt install curl
curl -fsSL get.docker.com -o get-docker.sh
sudo sh get-docker.sh --mirror Aliyun

# 启动docker
sudo systemctl enable docker
sudo systemctl start docker
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
# ubuntu 20.04 启动并且挂载目录
sudo docker run --name mysql --hostname master-node -it -v /data:/data centos:centos7.9.2009 /bin/bash
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
   # 按住ctrl,然后按下P,然后再按下Q
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



## 3.2 Redis

1. 下载镜像

   ```shell
   docker pull redis:6.2.3
   ```

2. 启动容器

   ```shell
   docker run -d -p 6379:6379 redis:6.2.3
   ```





# 第四章 镜像制作



## 4.1 nginx



### 4.1.1 dockerfile

```dockerfile
FROM centos:7

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



# 第五章  Docker网络

处于一个docker网络内的容器，可以用容器名称访问其它的容器[访问其它服务比如mysql，redis非常方便]。也可以隐藏db，后端业务服的端口号。





# 第六章 Docker Compose

作用：单个节点上定义和运行多个容器的工具



# 第七章 Docker Swarm

Docker集群管理工具，简易版的k8s，适用于中小型项目（几个~几十个节点），对比k8s更加简单。



# 第八章 Docker machine

作用：快速帮助我们搭建 Docker 主机环境
