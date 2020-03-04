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

   