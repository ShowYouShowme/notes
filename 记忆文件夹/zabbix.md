# 第一章  安装

官网 = https://www.zabbix.com/cn/

```ini
;使用的版本是zabbix4.0
[zabbix-server的安装]
;安装zabbix repo源
rpm -ivh http://repo.zabbix.com/zabbix/4.0/rhel/7/x86_64/zabbix-release-4.0-1.el7.noarch.rpm

;安装zabbix-server 和 zabbix前端
 yum install zabbix-server-mysql zabbix-web-mysql -y
 
 
;安装数据库
yum install -y mariadb-server
systemctl start mariadb
systemctl enable mariadb
mysql_secure_installation



;创建zabbix用户
create user 'zabbix@localhost' identified by 'qhx#2TD3WR+b1sMa';
;创建zabbix数据库
create database zabbix character set utf8 collate utf8_bin;
;授权
grant all privileges on zabbix.* to zabbix@localhost identified by 'qhx#2TD3WR+b1sMa';
;导入数据
zcat /usr/share/doc/zabbix-server-mysql*/create.sql.gz | mysql -uzabbix -p zabbix



;配置数据库
vim /etc/zabbix/zabbix_server.conf
DBHost=localhost
DBName=zabbix
DBUser=zabbix
DBPassword=<password>

;启动zabbix服务,服务的端口是10051
systemctl start zabbix-server
;设置服务开机启动
systemctl enable zabbix-server
;查看日志,zabbix是否正常运行
vim /var/log/zabbix/zabbix_server.log


[zabbix-web的安装]

;配置时区
vim  /etc/httpd/conf.d/zabbix.conf
php_value date.timezone Asia/ShangHai

;启动apache
;安装apache =  yum install httpd php php-mysql mariadb -y
systemctl start httpd
systemctl enable httpd

;登录web管理后台
http://120.25.248.58:8000/zabbix
;一直点击Next step
; Configure DB connection  0表示用3306端口,如果是其它端口需要指定
; 输入数据库密码
; Zabbix server details  --> Name = 监控中心

[初始登录用户]
user   = Admin
passwd = zabbix
```





# 第二章 添加监控主机和自定义监控项



## 2.1 添加监控主机

```ini
[安装agent]
yum install zabbix-agent
;vim /etc/zabbix/zabbix_agentd.conf
;修改Server的地址 Server=127.0.0.1,如果Server和agent在一台机器,不用改

[启动]
systemctl start zabbix-agent
systemctl enable zabbix-agent

[添加主机]
配置 --> 主机 --> 创建主机

;主机选项卡
主机名称 = web01
群主    = Linux servers
接口    = IP地址(agent的IP,如果和server在一台机器,就用127.0.0.1)

;模板选项卡
链接指示 = 输入Linux,然后点击 底下的文字 添加，最后点击添加按钮
```





## 2.2 创建自定义监控项





## 2.3 自定义触发器







# 第三章 报警



## 3.1 配置邮件报警



## 3.2 配置微信报警





# 第四章 grafana自定义图形



## 4.1 zabbix自定义图形



## 4.2 安装配置grafana



## 4.3 使用grafana自定义图形







# 第五章 自定义模板



## 5.1 监控tcp的十一种状态



## 5.2 创建自定义模板







# 第六章 常用服务监控

