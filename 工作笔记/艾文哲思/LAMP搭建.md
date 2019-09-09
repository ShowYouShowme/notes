#  在CentOS上搭建Lamp

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
   </html
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
   
   

