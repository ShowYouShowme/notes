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

;模板选项卡, 必须链接一个模板,否则 可用性 ZBX为灰色
链接指示 = 输入Linux,然后点击 底下的文字 添加，最后点击添加按钮

[修改防火墙]
防火墙开放 10050端口, zabbix-server 通过10050端口从zabbix-agent获取数据
```





## 2.2 创建自定义监控项

```INI
[配置文件]
; 自定义配置文件的路径 = /etc/zabbix/zabbix_agentd.d
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

;自定义的监控项放在 某些自定义的应用集里面
应用集  =

[查看数据]
; 监测 --> 最新数据 --> 主机(点击那个选择按钮) -->应用


[查看统计图表]
; 监测 --> 最新数据 --> 主机(点击那个选择按钮) -->应用 --> 图形(每一行数据最右边)
自从 = now-24h
到   = now
```



监控TCP连接数

```ini
; netstat 监控进程TCP状态时不要加上参数p,那个必须得有root权限
; netstat -ant | grep -c ESTABLISHED
UserParameter=UserParameter=ESTABLISHED,ss -s | sed -n "2p" | awk -F, '{print $1}' | awk '{print $4}'

;主要用于监控dos攻击
UserParameter=SYN_RECV, ss -o state syn-recv | wc -l

; 监控timewait的连接数
UserParameter=TIME_WAIT,ss -s | sed -n "2p" | awk -F, '{print $5}' | awk '{print $2}' | awk -F/ '{print $1}'

; 监控磁盘TPS, queryTps 可以设置为参数
UserParameter=TPS,curl -s http://127.0.0.1:3004/queryTps


;可变key
;获取值 zabbix_get -s 127.0.0.1 -p 10050 -k tcp[ESTABLISHED]
;web界面的key要改成tcp[ESTABLISHED]
UserParameter=tcp[*],netstat -ant | grep -c "$1"
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

1. 将windows的字体复制到桌面，字体路径C:\Windows\Fonts，这里我们选择--> 简体字(推荐微软雅黑)
2. zabbix 的字体路径：/usr/share/zabbix/assets/fonts
3. \mv STSONG.TTF  graphfont.ttf
4. 字体github地址：https://github.com/chengda/popular-fonts



### 4.1.4 应用集

用于把监控项分组的标签。创建监控项的时候可以选择应用集。



#### 创建应用集

1. 点击配置
2. 点击主机
3. 点击名称这列的某个主机
4. 点击应用集
5. 点击右边的创建应用集按钮





## 4.2 安装配置grafana

grafana图形稍微好看一点，但是没有必要安装！

流程

1. 安装grafana的服务

2. 安装zabbix的插件

3. 添加zabbix的数据源

   ```ini
   ; 填写zabbix的地址
   URL = http://localhost:8000/zabbix/api_jsonrpc.php
   
   ; 填写zabbix管理后台账号密码
   Username = 
   Password = 
   ```

   

```ini
wget https://dl.grafana.com/enterprise/release/grafana-enterprise-9.3.6-1.x86_64.rpm
yum localinstall ./grafana-enterprise-9.3.6-1.x86_64.rpm
systemctl start grafana-server.service
;grafana 监听的端口是3000
systemctl enable grafana-server.service
```





登录

```ini
;默认账号 admin
;默认密码 admin
http://${host}:3000/
```





## 4.3 使用grafana自定义图形

不需要







## 4.4 聚合图形

作用：将多张图展示到一个页面当中。



创建：点击监测 --> 聚合图形-->创建聚合图形





# 第五章 自定义模板

模板

1. 打开模板

   ```ini
   1 = 点击配置
   2 = 点击主机
   3 = 点击 模板 这一列的某一个
   ```

2. 模板的内容

   ```ini
   [模板的字段]
   ;给应用集分组的标签
   应用集 	= 
   ;重点
   监控项 	= 
   触发器 	= 
   图形   	 =
   ;多张图形放到一起
   聚合图形 	= 
   自动发现规则 = 
   Web场景 	  = 
   ```

   



## 5.1 监控tcp的十一种状态



## 5.2 创建自定义模板

```ini
; cd /etc/zabbix/zabbix_agentd.d
; vim tcp_status.conf
UserParameter=ESTABLISHED,netstat -apnt | grep ESTABLISHED -c
UserParameter=SYN_SENT,netstat -apnt | grep SYN_SENT -c
UserParameter=SYN_RECV,netstat -apnt | grep SYN_RECV -c
UserParameter=FIN_WAIT1,netstat -apnt | grep FIN_WAIT1 -c
UserParameter=FIN_WAIT2,netstat -apnt | grep FIN_WAIT2 -c
UserParameter=TIME_WAIT,netstat -apnt | grep TIME_WAIT -c
UserParameter=CLOSE,netstat -apnt | grep CLOSE -c
UserParameter=CLOSE_WAIT,netstat -apnt | grep CLOSE_WAIT -c
UserParameter=LAST_ACK,netstat -apnt | grep LAST_ACK -c
UserParameter=LISTEN,netstat -apnt | grep LISTEN -c
UserParameter=CLOSING,netstat -apnt | grep CLOSING -c


;重启agent服务
systemctl restart zabbix-agent

;测试获取值
zabbix_get -s 127.0.0.1 -p 10050 -k TIME_WAIT
```



自定义模板

```ini
1 = 点击配置
2 = 点击模板
3 = 点击右边的创建模板按钮
4 = 
	4.1  模板名称 = TcpState
		 群组    = Templates
		 描述    = TCP的十一种状态的模板
5 = 点击添加
```



为模板创建监控项

```ini
1 = 点击配置
2 = 点击模板
3 = 在名称这一列, 点击某个模板
4 = 点击监控项

; 也可以将已有的监控项复制到模板 [选择某个监控项,点击下面的复制, 目标类型选择模板, 目标这行选择一个模板]
5 = 点击创建监控项

; 选择全部监控项,点击批量更新, 勾上 添加新的或者已经存在的应用, 在里面选择一个应用集
6 = 将模板里面的监控项配置到指定应用集
```





为主机添加模板

```ini
1 = 点击配置
2 = 点击主机
3 = 名称这一列点击某个主机
4 = 点击模板选项卡
5 = 链接指示器 这里选择一个模板, 在点击添加，最后点击更新
```



模板的导入和导出



# 第六章 常用服务监控



**监控步骤**

1. 开启监控页面

   ```ini
   1 = 点击配置
   2 = 点击模板
   3 = 导入模板
   ```

2. 导入模板

3. 上传配置文件到zabbix-agent目录，上传脚本到指定目录，重启zabbix-agent

   > 配置文件通过执行shell脚本来获取监控项

4. 用zabbix-get测试能否正确获取到监控项

5. 链接模板，可能需要手动配置宏



## 6.1 监控Nginx

1. 开启状态页面

   ```nginx
   location = /basic_status {
       stub_status;
   }
   ```

2. 查看状态

   ```shell
   curl -s http://127.0.0.1:9000/basic_status
   ```

3. 配置监控项

   ```shell
   UserParameter=NGINX_ActiveConnections,curl -s http://127.0.0.1:9000/basic_status | sed -n "1p" | awk '{print $3}'
   UserParameter=NGINX_AcceptConnections, curl -s http://127.0.0.1:9000/basic_status | sed -n "3p" | awk '{print $1}'
   UserParameter=NGINX_HandledConnections,curl -s http://127.0.0.1:9000/basic_status | sed -n "3p" | awk '{print $2}'
   UserParameter=NGINX_Requests,curl -s http://127.0.0.1:9000/basic_status | sed -n "3p" | awk '{print $3}'
   UserParameter=NGINX_Reading,curl -s http://127.0.0.1:9000/basic_status | sed -n "4p" | awk '{print $2}'
   UserParameter=NGINX_Writing,curl -s http://127.0.0.1:9000/basic_status | sed -n "4p" | awk '{print $4}'
   UserParameter=NGINX_Waiting,curl -s http://127.0.0.1:9000/basic_status | sed -n "4p" | awk '{print $6}'
   ```

   



## 6.2 监控php-fpm

1. 开启状态页面

   ```ini
   ;pm.status_path = /status
   ; 改成下面这样
   pm.status_path = /php_status
   ```

2. 配置nginx

   ```ini
   location / {
       proxy_set_header X-Real-IP $remote_addr;
       proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
       proxy_pass  http://127.0.0.1:9002;
   
   }
   ```

   

3. 请求数据

   ```shell
   curl http://127.0.0.1:9002/php_status
   ```

4. 各种常用监控项

   ```ini
   startSince 			= curl -s http://127.0.0.1:9002/php_status | grep 'start since' | awk -F: '{print $2}'
   acceptedConn 		= curl -s http://127.0.0.1:9002/php_status | grep 'accepted conn' | awk -F: '{print $2}'
   listenQueue  		= curl -s http://127.0.0.1:9002/php_status | grep '^listen queue:' | awk -F: '{print $2}'
   maxListenQueue 		= curl -s http://127.0.0.1:9002/php_status | grep '^max listen queue:' | awk -F: '{print $2}'
   listenQueueLen 		= curl -s http://127.0.0.1:9002/php_status | grep '^listen queue len:' | awk -F: '{print $2}'
   idleProcesses  		= curl -s http://127.0.0.1:9002/php_status | grep '^idle processes:'| awk -F: '{print $2}'
   activeProcesses 	= curl -s http://127.0.0.1:9002/php_status | grep '^active processes'| awk -F: '{print $2}'
   totalProcesses 		= curl -s http://127.0.0.1:9002/php_status | grep '^total processes'| awk -F: '{print $2}'
   maxActiveProcesses 	= curl -s http://127.0.0.1:9002/php_status | grep '^max active processes'| awk -F: '{print $2}'
   maxChildrenReached 	= curl -s http://127.0.0.1:9002/php_status | grep '^max children reached'| awk -F: '{print $2}'
   slowRequests 		= curl -s http://127.0.0.1:9002/php_status | grep '^slow requests'| awk -F: '{print $2}'
   ```

   



## 6.3 监控redis

1. 查看redis指标命令

   ```
   redis-cli info
   ```

2. 监控key的数量

   ```shell
   redis-cli info | grep db0 | awk -F, '{print $1}' | awk -F= '{print $2}'
   ```

3. 监控redis使用的内存

   ```shell
   redis-cli info | grep used_memory_rss: | awk -F: '{print $2}'
   ```

4. redis版本

   ```shell
   redis-cli info | grep redis_version | awk -F: '{print $2}'
   ```

5. 运行时间

   ```ini
   运行秒数 = redis-cli info | grep uptime_in_seconds | awk -F: '{print $2}'
   
   运行天数 = redis-cli info | grep uptime_in_days | awk -F: '{print $2}'
   ```

6. 链接客户端数

   ```shell
   redis-cli info | grep connected_clients | awk -F: '{print $2}'
   ```

7. cpu占用

   ```ini
   内核态 = redis-cli info | grep used_cpu_sys: | awk -F: '{print $2}'
   用户态 = redis-cli info | grep used_cpu_user: | awk -F: '{print $2}'
   ```

8. 持久化

   ```ini
   是否开启aof = redis-cli info | grep aof_enabled | awk -F: '{print $2}'
   
   ; #上次保存数据库之后，执行命令的次数
   rdb_changes_since_last_save = redis-cli info | grep rdb_changes_since_last_save | awk -F: '{print $2}'
   
   ; 上次保存的耗时
   rdb_last_bgsave_time_sec = redis-cli info | grep rdb_last_bgsave_time_sec | awk -F: '{print $2}'
   
   ; 上次保存文件的时间戳
   rdb_last_save_time = redis-cli info | grep rdb_last_save_time  | awk -F: '{print $2}'
   ```

9. 持久化相关监控项介绍

   ```ini
   [RDB文件状态]
   rdb_changes_since_last_save = 上次RDB保存以后改变的key次数
   rdb_bgsave_in_progress      = 当前是否在进行bgsave操作。是为1
   rdb_last_save_time          =上次保存RDB文件的时间戳
   rdb_last_bgsave_time_sec    =上次保存的耗时
   rdb_last_bgsave_status      =上次保存的状态
   rdb_current_bgsave_time_sec =目前保存RDB文件已花费的时间
   
   [AOF文件状态]
   aof_enabled               =AOF文件是否启用
   aof_rewrite_in_progress   =表示当前是否在进行写入AOF文件操作
   aof_rewrite_scheduled
   aof_last_rewrite_time_sec =上次写入的时间戳
   aof_current_rewrite_time_sec:-1
   aof_last_bgrewrite_status:ok  = 上次写入状态
   aof_last_write_status:ok      = 上次写入状态
   ```



## 6.4 监控MySQL

1. 查看监控项

   ```shell
   mysql -e "show status\G" -uroot -ptars2015;
   ```

2. 监控

   ```ini
   1 = 利用percona的插件监控
   2 = 利用lepus监控
   ```

   





# 第七章  常见监控项获取

1. 获取进程使用的内存

   ```ini
   ; 从/proc/${pid}/status 里获取
   cat /proc/1716/status | grep VmRSS | awk '{print $2}'
   
   ; 利用top获取
   top -p 1716  -b -n 1 | sed -n "8p" | awk '{print $6}'
   ```

2. 获取进程主动和被动切换次数

   ```ini
   ; 主动切换次数多 属于  IO密集型
   ; 被动切换次数多 属于  cpu密集型
   
   
   ; 主动切换次数, IO阻塞会导致主动切换
   cat /proc/1716/status | grep voluntary_ctxt_switches | sed -n "1p" | awk '{print $2}'
   
   ; 被动切换次数, cpu时间到了会触发被动切换
   cat /proc/1716/status | grep voluntary_ctxt_switches | sed -n "2p" | awk '{print $2}'
   ```

3. 列出进程的TCP连接数。可以监控是否有文件描述符的泄露

   ```ini
   ;查看某个进程的TCP链接
   ; -a 是 AND, 两个条件同时满足
   ; -p ${pid}
   ; -i4 列出全部IPv4链接
   ; -i6 列出全部IPv6链接
   ; -i  列出全部Internet链接
   ; -i:${port}  列出某个端口的InterNet链接
   cmd = sudo lsof -i -a -p 9437
   
   
   ; 列出两个端口的全部网络连接
   ; 一般的服务有一个对外的端口,一个admin调用的端口
   lsof -i:3100,9001
   ```

   

4. 列出进程打开的文件数

   ```shell
   sudo lsof -p 10751 | grep REG
   ```

   
