# 镜像制作

## 1 nginx镜像

### 1.1 源码编译

***

1. dockerfile

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

2. 制作镜像

   ```shell
   docker build -t nginx:v1 .
   ```

   

3. 启动命令

   + 前台启动

     ```shell
     docker run -t -i -p 4444:80 nginx:v1 /bin/bash
     ```

   + 后台启动

     ```shell
     # shell 死循环,防止程序退出
     docker run -d -p 4444:80  /bin/bash -c "/usr/local/nginx/sbin/nginx; while true; do echo hello world ; sleep 100; done;"
     ```

     



### 1.2 使用编译的nginx

***

1. dockerfile

   ```dockerfile
   FROM centos:7
   
   RUN yum install gcc pcre pcre-devel zlib zlib-devel openssl openssl-devel -y
   ```

2. 制作镜像

   ```shell
   docker build -t nginx:v1 .
   ```

3. 启动命令

   ```shell
   # 必须有编译好的nginx
   docker run -t -i -p 4444:80 -v ${PWD}/nginx:/usr/local/nginx nginx:v1 /bin/bash
   ```




## 2 sinatra镜像

### 2.1 源码编译

***

1. dockerfile

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

2. 启动命令

   ```shell
   docker run -t -i -p 4567:4567 --privileged -v /home/yourDoom/sinatra/webapp:/opt/webapp sinatra:v5 /opt/webapp/bin/webapp
   ```



## 3 apache

1. dockerfile

   ```dockerfile
   FROM centos:7
   
   RUN yum install -y httpd
   
   CMD ["/usr/sbin/httpd", "-DFOREGROUND"] # 从httpd.service里面拿出来的
   ```

2. 启动命令

   ```shell
   docker run -d -p 80:80 -v /home/xman/apache/html:/var/www/html apacher:v123
   ```

   


# docker 配置

## 1 配置文件路径

```shell
vim /etc/docker/daemon.json
```

## 2 配置内容

```json
{
"registry-mirrors": ["http://hub-mirror.c.163.com"],
"dns" : [ "223.5.5.5","223.6.6.6" ]
}

# 更改配置后必须重启服务 systemctl restart docker
```



# docker与screen

> 要保持docker容器处于活跃状态，运行的进程不能中断
>
> 1. 让服务前台运行
> 2. 在screen里面启动docker
> 3. 带参数-ti启动，执行完命令后再xshell里把窗口关闭





# 常见操作

## 1 查看日志

```shell
docker logs -f ${容器名}

docker logs -f ${容器ID}
```

## 2 镜像导入导出

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




## 3 文件复制

1. 宿主机文件复制到docker内部

   ```shell
   docker cp /path/filename 容器id或名称:/path/filename
   ```

2. docker内部文件复制到宿主机

   ```shell
   docker cp 容器id或名称:/path/filename /path/filename
   ```

   