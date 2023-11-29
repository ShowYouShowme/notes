# 第一章  环境搭建

1. 安装nginx

   ```shell
   # 系统  ubuntu20.04
   sudo apt install -y nginx
   ```

2. 安装php-fpm

   + ubuntu

     ```shell
     sudo apt install php php-cli php-fpm php-json php-pdo php-mysql php-zip php-gd  php-mbstring php-curl php-xml php-pear php-bcmath
     
     # 启动php-fpm
     systemctl status php7.4-fpm.service
     ```

   + centos7

     ```ini
     [php5.4.16]
     yum -y install php php-fpm php-gd php-mysql php-common php-pear php-mbstring php-mcrypt
     systemctl status php-fpm
     systemctl start php-fpm
     systemctl enable php-fpm
     
     [启动命令]
     ; 后台启动
     /usr/sbin/php-fpm --daemonize
     ; 前台启动
     /usr/sbin/php-fpm --nodaemonize
     
     [配置文件]
     ;路径
     /etc/php-fpm.d/www.conf
     
     ;配置启动用户
     ;编译安装的nginx，以运行命令的用户启动，比如roglic
     ;如果要让php文件能被正常访问，需要
     ;1、资源文件放在nginx的html目录
     ;2、将php-fpm的启动用户设置为nginx的启动用户
     
     ;nginx配置
             location / {
                 root   html;
                 index  index.html index.htm index.php;
             }
     
             location ~ \.php$ {
                     root           html;
                     fastcgi_pass   127.0.0.1:9000;
                     fastcgi_param  SCRIPT_FILENAME  $document_root$fastcgi_script_name;
                     include        fastcgi_params;
             }
     
     [php7.4]
     
     ```
     
     

3. 配置nginx

   ```shell
   # php-fpm 默认使用unix domain socket 通信，可以修改配置用TCP通信
   cd /etc/nginx/conf.d && touch app.conf
   server {
       listen       8011;
       location ~ \.php$ {
           root           /var/www/html;
           #fastcgi_pass   127.0.0.1:9000;
           fastcgi_pass unix:/run/php/php7.4-fpm.sock;
   	fastcgi_param  SCRIPT_FILENAME  $document_root$fastcgi_script_name;
           include        fastcgi_params;
       }
   }
   ```

4. 增加php文件

   ```shell
   # step-1 创建php文件
   cd /var/www/html && touch index.php
   
   # step-2 编辑文件
   <!DOCTYPE html>
   <html>
   <body>
   
   <?php
   phpinfo();
   ?>
   
   </body>
   </html>
   
   # step-3 重新加载nginx配置
   sudo nginx -s reload
   ```

5. 访问php文件

   ```SHE
   http://192.168.0.72:8011/index.php

6. 附录

   ```shell
   # 配置php-fpm 使用tcp通信
   listen = 127.0.0.1:9000
   ```



# 第二章  nginx配置鉴权



## 2.1 使用数据库鉴权

1. 增加配置

   ```SHEll
   server {
       auth_basic "Please input password!";               # 增加的配置
       auth_basic_user_file /etc/nginx/conf.d/auth_pwd;   # 增加的配置
       listen       8011;
       location ~ \.php?.*$ {
           root           /var/www/html;
           #fastcgi_pass   127.0.0.1:9000;
           fastcgi_pass unix:/run/php/php7.4-fpm.sock;
   	fastcgi_param  SCRIPT_FILENAME  $document_root$fastcgi_script_name;
           include        fastcgi_params;
       }
   }
   
   ```

2. 生成密码

   ```shell
   # 创建密码文件
   touch /etc/nginx/conf.d/auth_pwd
   
   # 使用openssl 加密密码
   openssl passwd hello    # 输出为 m1267HhWihWTQ
   
   # 存放账号和加密后的密码
   echo -n "nash:m1267HhWihWTQ" > auth_pwd
   ```




## 2.2 使用接口鉴权

1. 源码编译nginx并且开启ngx_http_auth_request_module模块

   ```shell
   wget  http://nginx.org/download/nginx-1.10.2.tar.gz
   
   # 配置
     ./configure --prefix=/opt/nginx \
                 --with-http_dav_module \
                 --with-http_ssl_module \
                 --with-http_realip_module \
                 --with-http_gzip_static_module \
                 --with-http_stub_status_module \
                 --with-http_degradation_module \
                 --with-http_auth_request_module
     make && make install
   ```

2. 配置

   ```shell
       server {
           listen       80;
           server_name  localhost;
   
           location / {
               auth_request /auth;    # 添加此行
               root   html;
               index  index.html index.htm;
           }
   
   		# 配置鉴权接口
       	location = /auth {
               proxy_pass http://192.168.0.72:8011/HttpBasicAuthenticate.php;
               proxy_pass_request_body off;
               proxy_set_header Content-Length "";
               proxy_set_header X-Original-URI $request_uri;
       	}
      }
      
      
   server {
       listen       8011;
       location ~ \.php$ {
           root           html;
           fastcgi_pass unix:/run/php/php7.4-fpm.sock;  # 设置文件权限为666,否则普通用户无法读写
           fastcgi_param  SCRIPT_FILENAME  $document_root$fastcgi_script_name;
           include        fastcgi_params;
       }
   }
   
   
   ```

3. 鉴权的php代码

   ```php
   <?php
   
   if(isset($_SERVER['PHP_AUTH_USER'], $_SERVER['PHP_AUTH_PW'])){
       $username = $_SERVER['PHP_AUTH_USER'];
       $password = $_SERVER['PHP_AUTH_PW'];
   
       if ($username == 'wang' && $password == '123456'){
           return true;
       }   
   }
   
   header('WWW-Authenticate: Basic realm="Git Server"');
   header('HTTP/1.0 401 Unauthorized');
   
   ?>
   ```




# 第三章 源码安装php7.4

源码包：php-7.4.30.tar.gz



## 3.1 安装步骤

1. 安装依赖

   ```shell
   #先安装第三方源,其它的可以一起安装
   sudo yum install epel-release -y
   sudo yum install -y gcc gcc-c++
   sudo yum install -y libxml2-devel
   sudo yum install -y openssl-devel
   sudo yum install -y sqlite-devel libcurl-devel libpng-devel
   sudo yum install oniguruma-devel -y
   ```

2. 安装libzip

   ```shell
   #安装libzip
   #依赖于cmake root或者有sudo权限的用户
   wget https://github.com/Kitware/CMake/releases/download/v3.25.0/cmake-3.25.0-linux-x86_64.tar.gz
   
   #解压后可以直接使用
   tar -zxvf cmake-3.25.0-linux-x86_64.tar.gz
   
   wget https://libzip.org/download/libzip-1.8.0.tar.gz && tar -zxf libzip-1.8.0.tar.gz && cd libzip-1.8.0
   
   mkdir build && cd build \
   && ../../cmake-3.25.0-linux-x86_64/bin/cmake -DCMAKE_INSTALL_PREFIX=$HOME/usr .. \
   && make \
   && make install
   ```

3. 编译安装php

   ./configure --prefix=$HOME/local/php7 --bindir=$HOME/local/php7/bin --with-config-file-path=$HOME/local/php7/etc --enable-fpm --with-openssl --with-curl --with-pdo-mysql --with-zip --enable-mbstring --with-zlib --enable-gd --with-zlib 

   make -j20    	//使用20个核心
   make install


   给php执行文件加软连接到bin

   	ln -s $HOME/local/php7/bin/php $HOME/bin/php

   创建 php-fpm 执行文件

   	cp $HOME/tmp/php-7.4.30/sapi/fpm/init.d.php-fpm $HOME/local/php7/bin/php-fpm

   给执行文件 执行权限

   	chmod +x $HOME/local/php7/bin/php-fpm

   创建软连接

   	ln -s $HOME/local/php7/bin/php-fpm $HOME/bin/php-fpm


   测试php-fpm 

   	php-fpm configtest												
   	//报错 failed to open configuration file '/usr/local/php7/etc/php-fpm.conf': No such file or directory


   由于安装时指定了配置路径 --with-config-file-path=/home/li/local/php7/etc ， 所以需要拷贝php.ini到对应目录

   	cp $HOME/tmp/php-7.4.30/php.ini-development $HOME/local/php7/etc/php.ini


   创建 php-fpm 配置文件 

   	cd $HOME/local/php7/etc/
   	cp ./php-fpm.conf.default ./php-fpm.conf
   	
   	cd php-fpm.d
   	cp www.conf.default www.conf

   













## 3.2 操作命令

```ini
[启动]
cmd  = php-fpm start

[停止]
cmd  = php-fpm stop

[重启]
cmd  = php-fpm restart

[命令全部用法]
cmd  = php-fpm {start|stop|force-quit|restart|reload|status|configtest}
```



## 3.3 Dockerfile

```dockerfile
# 构建好image,启动container后,设置Php的启动user = root  group = root, 前台运行 daemonize = no
# 将端口9000暴露出去, 启动Php-fpm 后, 按住 Ctrl 再按P、Q退出不关闭容器
FROM centos:centos7.9.2009

# 修改这一行可以禁用Docker build缓存
ENV REFRESH_DATE 2018-01-07
ENV PATH=$HOME/bin:$PATH
RUN export PATH
ENV TOOLS_HOST=http://192.168.2.105:2000
WORKDIR /opt
RUN mkdir $HOME/bin $HOME/local
RUN yum install -y wget
RUN yum install -y vim
RUN yum install -y net-tools
RUN yum install epel-release -y
RUN yum install -y gcc gcc-c++
RUN yum install -y libxml2-devel
RUN yum install -y openssl-devel
RUN yum install -y sqlite-devel libcurl-devel libpng-devel
RUN yum install oniguruma-devel -y
RUN yum install -y make
RUN wget $TOOLS_HOST/cmake-3.25.0-linux-x86_64.tar.gz
RUN wget $TOOLS_HOST/libzip-1.8.0.tar.gz
RUN tar -zxf libzip-1.8.0.tar.gz
RUN tar -zxvf cmake-3.25.0-linux-x86_64.tar.gz
WORKDIR /opt/libzip-1.8.0/build
RUN /opt/cmake-3.25.0-linux-x86_64/bin/cmake  -DCMAKE_INSTALL_PREFIX=/usr ..
RUN make
RUN make install

WORKDIR /opt
RUN wget $TOOLS_HOST/php-7.4.30.tar.gz
RUN tar -zxvf php-7.4.30.tar.gz
WORKDIR /opt/php-7.4.30
RUN ./configure --prefix=$HOME/local/php7 --bindir=$HOME/local/php7/bin --with-config-file-path=$HOME/local/php7/etc --enable-fpm --with-openssl --with-curl --with-pdo-mysql --with-zip --enable-mbstring --with-zlib --enable-gd --with-zlib 

RUN make -j20
RUN make install


RUN cp /opt/php-7.4.30/sapi/fpm/init.d.php-fpm  $HOME/local/php7/bin/php-fpm
RUN chmod +x $HOME/local/php7/bin/php-fpm
RUN ln -s $HOME/local/php7/bin/php-fpm $HOME/bin/php-fpm
RUN cp /opt/php-7.4.30/php.ini-development $HOME/local/php7/etc/php.ini

WORKDIR /root/local/php7/etc
RUN cp ./php-fpm.conf.default ./php-fpm.conf
WORKDIR /root/local/php7/etc/php-fpm.d
RUN cp www.conf.default www.conf
RUN /root/bin/php-fpm configtest	

```



#  第四章 搭建Lamp

1. 安装apache

   ```shell
   yum install -y httpd
   ```

2. 安装MySQL

   ```shell
   wget -i -c http://dev.mysql.com/get/mysql57-community-release-el7-10.noarch.rpm
   yum -y install mysql57-community-release-el7-10.noarch.rpm
   yum -y install mysql-community-server
   yum -y install  mysql-devel
   ```

3. 安装Php服务

   ```shell
   yum install -y php php-mysql
   ```

4. 在`/var/www/html` 目录下编辑生成index.php文件

   ```php
   <html>
           <title>This is a PHP page.</title>
           <body>
                   <h1>PHP Info Page</h1>
                   <?php
                           phpinfo();
                   ?>
           </body>
   </html>
   ```

5. 启动httpd服务并访问响应页面`http://10.10.10.126`

   ```shell
   systemctl start httpd  
   firewall-cmd --state # 查看防火墙状态
   systemctl stop firewalld.service # 停止防火墙
   systemctl disable firewalld.service  # 禁止防火墙开机启动
   
   #临时关闭SELinux
   setenforce 0
   #永久关闭SELinux
   vim /etc/selinux/config 
   SELINUX=permissive
   ```
   
   
   
6. 启动MySQL并测试php与MySQL的连接性

   ```shell
   service mysqld start
   
   # 查看MySQL默认密码
   grep 'password' /var/log/mysqld.log |head -n1
   
   # 用默认密码登录
   mysql -uroot -p${default_password}
   
   # 修改密码
   mysql> ALTER USER '${账号}'@'localhost' IDENTIFIED BY '${密码}';
   ```

   index.php的内容
   
   ```php
   <?php
           $conn = mysql_connect('127.0.0.1','root','Pe4YA4$D2QNB');
           if ($conn)
                   echo "Connected to mysql.";
           else
                   echo "Fail";
   ?>
   ```
   





# 第五章 thinkphp



## 5.0 运行环境搭建

1. 安装nginx

   ```ini
   [CMD]
   sudo yum install -y epel-release
   sudo yum install -y nginx
   
   [配置]
   ;默认网站目录
   WEB_PATH= /usr/share/nginx/html
   
   ;默认配置文件
   CONFIG_PATH=/etc/nginx/nginx.conf
   
   ;自定义配置文件目录, http模块里有 include /etc/nginx/conf.d/*.conf;
   CUSTOM_CONFIG_PATH = /etc/nginx/conf.d/
   
   ;日志目录
   path = /var/log/nginx
   
   ;配置启动用户为apache
   ;nginx.conf
   user apache;
   
   [启动服务]
   docker容器 = /usr/sbin/nginx
   非docker = systemctl start nginx
   ```

2. 安装php-fpm

   ```ini
   [php5.4.16]
   yum -y install php php-fpm php-gd php-mysql php-common php-pear php-mbstring php-mcrypt
   systemctl status php-fpm
   systemctl start php-fpm
   systemctl enable php-fpm
   
   [启动命令]
   ; 后台启动
   /usr/sbin/php-fpm --daemonize
   ; 前台启动
   /usr/sbin/php-fpm --nodaemonize
   
   [配置文件]
   ;路径
   /etc/php-fpm.d/www.conf
   
   
   [日志目录]
   path = /var/log/php-fpm
   ```

3. 创建web root，并且设置权限

   ```shell
   mkdir /data
   chown -R apache:apache /data
   ```

4. 将网站的文件放到web root即可



thinkPHP的资料

```ini
[github]
url = https://github.com/top-think/think/

[开发文档]
; tp5 doc
url = https://static.kancloud.cn/manual/thinkphp5/118003
```

## 5.1 安装

```shell
# thinkphp_5.0.10_full.zip, github上下载的包好像缺少东西
wget https://www.thinkphp.cn/download/1015.html

# 测试是否能跑起来
php ./thinkphp_5.0.10_full/public/index.php 
```





## 5.2 运行

1. 配置nginx

   ```nginx
   # php-fpm的启动用户和nginx要相同
   server {
       listen 8000;
       server_name localhost;
       root   /data/tp5/public;
       index  index.php index.html index.htm;
     
     location ~* ^.+.(jpg|jpeg|gif|css|png|js|thumb) {
          expires 30d;
      }
      location / {
       try_files $uri @default;
   }
   
   location @default {
       fastcgi_pass            127.0.0.1:9000;
       fastcgi_param           SCRIPT_FILENAME $document_root/index.php;
       fastcgi_param           PATH_INFO       $fastcgi_script_name;
       fastcgi_param           PATH_TRANSLATED $document_root/index.php;
       include                 fastcgi_params;
   }
   
   location ~ \.php($|/) {
       fastcgi_pass            127.0.0.1:9000;
       fastcgi_split_path_info ^(.+?\.php)(/.+)$;
       fastcgi_param           SCRIPT_FILENAME $document_root$fastcgi_script_name;
       fastcgi_param           PATH_INFO       $fastcgi_path_info;
       fastcgi_param           PATH_TRANSLATED $document_root$fastcgi_script_name;
       include                 fastcgi_params;
   }
   
   }
   ```

   

2. 将压缩包放到web根目录下的tp5目录，然后解压

3. 接口测试

   ```
   http://127.0.0.1:8000/
   ```

   

   

   

## 5.3 目录介绍

   ```
   project  应用部署目录
   ├─application           应用目录（可设置）
   │  ├─common             公共模块目录（可更改）
   │  ├─index              模块目录(可更改)
   │  │  ├─config.php      模块配置文件
   │  │  ├─common.php      模块函数文件
   │  │  ├─controller      控制器目录
   │  │  ├─model           模型目录
   │  │  ├─view            视图目录
   │  │  └─ ...            更多类库目录
   │  ├─command.php        命令行工具配置文件
   │  ├─common.php         应用公共（函数）文件
   │  ├─config.php         应用（公共）配置文件
   │  ├─database.php       数据库配置文件
   │  ├─tags.php           应用行为扩展定义文件
   │  └─route.php          路由配置文件
   ├─extend                扩展类库目录（可定义）
   ├─public                WEB 部署目录（对外访问目录）
   │  ├─static             静态资源存放目录(css,js,image)
   │  ├─index.php          应用入口文件
   │  ├─router.php         快速测试文件
   │  └─.htaccess          用于 apache 的重写
   ├─runtime               应用的运行时目录（可写，可设置）
   ├─vendor                第三方类库目录（Composer）
   ├─thinkphp              框架系统目录
   │  ├─lang               语言包目录
   │  ├─library            框架核心类库目录
   │  │  ├─think           Think 类库包目录
   │  │  └─traits          系统 Traits 目录
   │  ├─tpl                系统模板目录
   │  ├─.htaccess          用于 apache 的重写
   │  ├─.travis.yml        CI 定义文件
   │  ├─base.php           基础定义文件
   │  ├─composer.json      composer 定义文件
   │  ├─console.php        控制台入口文件
   │  ├─convention.php     惯例配置文件
   │  ├─helper.php         助手函数文件（可选）
   │  ├─LICENSE.txt        授权说明文件
   │  ├─phpunit.xml        单元测试配置文件
   │  ├─README.md          README 文件
   │  └─start.php          框架引导文件
   ├─build.php             自动生成定义文件（参考）
   ├─composer.json         composer 定义文件
   ├─LICENSE.txt           授权说明文件
   ├─README.md             README 文件
   ├─think                 命令行入口文件
   ```



## 5.4 路由配置

1. 开启强制路由

   ```php
   // application/config.php
   'url_route_on'  		=>  true,
   'url_route_must'		=>  true,
   ```

2. 路由定义

   ```php
   // application/route.php
   
   use think\Route;
   // 定义路由, Get请求
   Route::get('hello','great_wall/BlackPerson/hello');
   Route::get('greatWall/sayHello','great_wall/BlackPerson/sayHello');
   
   // 定义Post请求路由规则
   // Route::post('hello','index/demo/hello');
   
   Route::get('showHello',function(){
       return 'my learner, Hello,world!';
   });
   // buyTicket
   Route::post('greatWall/buyTicket','great_wall/BlackPerson/buyTicket');
   
   // 首页的接口
   Route::get('',function(){
       return 'hello, this is our homepage!';
   });
   
   return [
       '__pattern__' => [
           'name' => '\w+',
       ] 
   ];
   ```

3. 控制器编写

   + 创建目录和文件

     ```
     mkdir -p application/great_wall/controller/
     cd application/great_wall/controller/
     touch BlackPerson.php
     ```

   + 编写控制器代码

     ```php
     <?php
     namespace app\great_wall\controller;
     
     use think\Request;
     class BlackPerson
     {
         public function sayHello()
         {
             return 'welcome to great wall!';
         }
     
         public function hello()
         {
             // 这里会直接返回json给client
             return ['name'=>'thinkphp','status'=>1];
         }
     
         public function buyTicket()
         {
             $request = Request::instance();
             echo '请求方法：' . $request->method() . '<br/>';
             echo '资源类型：' . $request->type() . '<br/>';
             echo '访问ip地址：' . $request->ip() . '<br/>';
             echo '是否AJax请求：' . var_export($request->isAjax(), true) . '<br/>';
             echo '请求参数：';
             dump($request->param());
     
             $name = $request->param()['name'];
             $age = $request->param()['age'];
             echo 'name = ' . $name . ' age = ' . $age;
         }
     }
     ```

4. 设置返回json

   ```php
   // config.php 默认的输出类型是html
   'default_return_type'   => 'json',
   
   // 控制器里面采用return语句返回
   return ['name'=>'thinkphp','status'=>1];
   ```

   

   
   
## 5.5 session

 配置文件夹权限，否则会报错

```shell
# session_start() open failed Permission denied
chmod 777 /var/lib/php/session/
```



   



