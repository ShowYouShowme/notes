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



选项卡

```ini
[监测]
仪表板 	= 1
问题   	 = 2 
概览   	 = 3
Web监测	 = 4
最新数据	=5
图形   	 = 6
聚合图形	= 7
拓补图 	 = 8
自动发现	= 7
服务   	 = 8

[资产记录]
概览 = 1
主机 = 2

[报表]
系统信息   = 1
可用性报表 = 2
触发器    = 3
审计      = 4
动作日志   = 5
警报      = 6

[配置]
主机群组 = 1
模板    = 2
主机    = 3
维护    = 4
动作    = 5
关联事件 = 6
自动发现 = 7
服务    = 8

[管理]
一般         = 1
agent代理程序 = 2
认证         = 3
用户群组      = 4
用户         = 5
报警媒介类型   = 6
脚本         = 7
队列         = 8
```



安装zabbix取值工具

```ini
yum install -y zabbix-get

;取值
cmd     = zabbix_get -s ${HOST} -p ${PORT} -k ${KEY}
example = zabbix_get -s 127.0.0.1 -p 10050 -k system.cpu.util[,idle]
```



修改密码

1. 点击右上角人头
2. 切换到用户选项卡，然后点击修改密码





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

```INI
[配置文件]
path = vim /etc/zabbix/zabbix_agentd.conf

[格式]
;可以写多个,key不能重复
UserParameter=<key>,<shell command>

;监控tps
example = UserParameter=tps,iostat | awk '$1~/^vda$/{print $2}'
;重启zabbix-agent
cmd = systemctl restart zabbix-agent
;测试是否生效
cmd = zabbix_get -s 127.0.0.1 -p 10050 -k tps

[在web页面上增加监控项]
; 配置 --> 主机 --> 选择一台主机(点击主机名称) --> 切换到监控项选项卡 --> 创建监控项
名称    = 硬盘的tps
键值    = tps
;数据类型一定要正确,否则查看最新数据显示感叹号
;修改不支持的监控项的刷新时间:  管理 --> 一般 --> 其它 --> 刷新不支持的项目 --> 10s
信息类型 = 浮点数
更新间隔 = 5s

[查看数据]
; 监测 --> 最新数据 --> 主机(点击那个选择按钮) -->应用


[查看统计图表]
; 监测 --> 最新数据 --> 主机(点击那个选择按钮) -->应用 --> 图形(每一行数据最右边)
自从 = now-24h
到   = now
```



监控TCP连接数

```ini
;配置netstat的权限 chmod +s /bin/netstat
UserParameter=tcp_established_num,netstat -apnt | grep ESTABLISHED -c
```





## 2.3 自定义触发器

作用：某个指标达到一定值时，触发事件！常见的就是报警，比如磁盘空间不足！



### 2.3.1 创建触发器

1. 配置

2. 主机

3. 在名称这一列选择一个主机

4. 点击触发器选项卡

5. 点击右边的 创建触发器  按钮

6. 填写信息

   ```ini
   
   名称   = 硬盘读写太频繁
   严重性 = 警告
   ; {web01:tps.last()}>5
   表达式 = 
   		监控项 = 
   		;一般选择last(磁盘使用率大于指定值), avg(),不同(比如/etc/passwd 被修改),nodate(ping收不到数据)
   		功能   =
   		;一般选择 >
   		结果   =
   		
   ;填写完上面信息再点击添加
   ```

7. 配置报警时播放音效

   1. 点击Admin
   2. 切换到正在发送消息
   3. 勾选前端信息中
   4. 点击更新

   

### 2.3.2 入侵时报警

1. 点击配置

2. 点击主机

3. 在名称这一列，点击一个主机

4. 点击触发器

5. 点击右边的 “创建触发器”

6. 配置触发器

   ```ini
   名称 = 你的服务器可能被黑客入侵了
   严重性 = 灾难
   ;点击添加
   ;监控项 选择 Checksum of /etc/passwd
   ;功能 选择 diff
   ;结果 选择 1, 1 表示不同
   表达式 =
   
   
   ;更新 监控项的更新时间 为 10 s
   
   ; 重启zabbix-server
   systemctl restart zabbix-server
   ```

   






# 第三章 报警



## 3.1 配置邮件报警

1. 点击管理

2. 点击告警媒介类型

3. 在名称这列点击Email

4. 配置发件人Email信息

   ```ini
   SMTP服务器    = smtp.126.com
   SMTP服务器端口 = 465
   SMTP HELO    = 126.com
   SMTP电邮      = wzc_0618@126.com
   ;SSL验证对端 和 SSL验证主机不需要勾选
   安全链接       = SSL/TLS
   认证          = 用户名和密码
   用户名称       = wzc_0618@126.com
   ; 密码是申请到的授权码
   密码          = SAGJEOZIYUNKVLLH
   ```

5. 配置收件人信息

   ```ini
   1 = 点击Admin
   2 = 点击报警媒介
   3 = 点击添加
   4 = 填写收件人的邮件地址
   5 = 点击 添加按钮, 再点击 带下划线的添加文字 , 最后点击更新
   ```

   

6. 开启邮件报警

   ```ini
   1 = 点击配置
   2 = 点击动作
   3 = 点击停用的,就会开启邮件报警
   ```

   





**查看报警信息**

1. 点击报表
2. 点击动作日志

## 3.2 配置微信报警





# 第四章 grafana自定义图形



## 4.1 zabbix自定义图形



### 4.1.1 定义图形

1. 点击配置

2. 点击主机

3. 在名称这一列点击主机

4. 点击图形

5. 点击右边的创建图形

6. 填写信息

   ```ini
   名称 = tcp连接数
   ; 正常 = 折线图
   ; 层积 = 柱状图
   ; Pie = 饼状图
   ; 爆发 很少用
   图形类别 = 正常
   
   ; 可以添加多个监控项,比如监控TCP的十一种状态, 并且配置不同的颜色
   监控项 = 
   ```

   



### 4.1.2 查看图形

1. 点击监测
2. 点击图形
3. 选择群组，选择主机，再选择图形



### 4.1.3 zabbix 乱码修复

1. 将windows的字体复制到桌面，字体路径C:\Windows\Fonts，这里我们选择--> 简体字(华文宋体 常规)
2. zabbix 的字体路径：/usr/share/zabbix/assets/fonts
3. \mv STSONG.TTF  graphfont.ttf



### 4.1.4 应用集

用于把监控项分组的标签。创建监控项的时候可以选择应用集。



#### 创建应用集

1. 点击配置
2. 点击主机
3. 点击名称这列的某个主机
4. 点击应用集
5. 点击右边的创建应用集按钮





## 4.2 安装配置grafana



## 4.3 使用grafana自定义图形







# 第五章 自定义模板



## 5.1 监控tcp的十一种状态



## 5.2 创建自定义模板







# 第六章 常用服务监控

