# 第一章  环境搭建

1. 安装nginx

   ```shell
   # 系统  ubuntu20.04
   sudo apt install -y nginx
   ```

2. 安装php-fpm

   ```shell
   sudo apt install php php-cli php-fpm php-json php-pdo php-mysql php-zip php-gd  php-mbstring php-curl php-xml php-pear php-bcmath
   
   # 启动php-fpm
   systemctl status php7.4-fpm.service
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



安装步骤：

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
   && sudo make install
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

   



