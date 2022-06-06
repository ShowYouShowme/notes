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

   

