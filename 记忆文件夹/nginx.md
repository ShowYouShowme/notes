# 第一章 负载均衡



## 1.1 负载均衡策略

| 策略             | 说明            |
| ---------------- | --------------- |
| 轮询             | 默认方式        |
| weight           | 权重方式        |
| ip_hash          | 根据ip分配方式  |
| least_conn       | 最少连接方式    |
| fair(第三方)     | 响应时间方式    |
| url_hash(第三方) | 根据URL分配方式 |



## 1.2 TCP负载均衡

```nginx
# 默认使用轮询的策略
# 如果server只有一个，就变成了TCP反向代理
stream {
  upstream test_mysql {
    server 192.168.0.68:8080;
    server 192.168.0.72:80;
  }
  server {
    listen 10086 so_keepalive=on;				# 开启 TCP 存活探测
    proxy_connect_timeout 10s;					# 连接超时时间
    proxy_timeout 300s;							# 端口保持时间
    proxy_pass test_mysql;
  }
}

```



## 1.3 haproxy TCP负载均衡

1. 安装

   ```shell
   # ubuntu 20.04
   sudo apt install software-properties-common
   sudo add-apt-repository ppa:vbernat/haproxy-2.5
   sudo apt update
   sudo apt install haproxy
   ```

2. 配置

   ```shell
   # 管理后台：http://192.168.0.66:8888/haproxy?stats
   # 配置文件haproxy.cfg 最后加上
   # 如果server 只配置一个就是TCP反向代理了
   frontend http_front
      bind *:8888
      stats uri /haproxy?stats
      default_backend http_back
   
   backend http_back
      balance roundrobin
      server web_server_1 192.168.0.68:8080 check
      server web_server_2 192.168.0.72:80 check
   ```




## 1.4 lvs 负载均衡

配置复杂，推荐使用nginx或者haproxy。

### 模式

1. LVS-DR：直接路由。Director和RealServer都在同一个局域网内
2. LVS-TUN：隧道模式
3. LVS-NAT：地址转换。 使用NAT模式将需要两个不同网段的IP，一个IP接受外部请求服务，一般为外网ip，此IP称为VIP，一个IP与后realserver同一地址段，负责相互通信，称为DIP。后端realserver的网关地址需指向DIP。同时需开启linux内核的数据包转发功能



### 调度算法

1. 轮叫调度 rr

2. 加权轮叫 wrr

3. 最少链接 lc

4. 加权最少链接 wlc

5. 基于局部性的最少连接调度算法 lblc

6. 复杂的基于局部性最少的连接算法 lblcr

7. 目标地址散列调度算法 dh

8. 源地址散列调度算法 sh



### DR模式配置

1. 机器ip

   > 三台server的ip
   >
   > direct_server:192.168.0.66
   >
   > real_server1:192.168.0.68
   >
   > real_server2:192.168.0.72
   >
   > vip:192.168.0.166 （Virtual ip）

2. 配置direct_server

   ```shell
   #! /bin/bash
   echo 1 > /proc/sys/net/ipv4/ip_forward
   ipv=/sbin/ipvsadm
   vip=192.168.0.166 # 虚拟IP
   rs1=192.168.0.68
   rs2=192.168.0.72
   ifconfig ens32:0 $vip broadcast $vip netmask 255.255.255.255 up
   route add -host $vip dev ens32:0
   
   ipvsadm -C
   ipvsadm -A -t $vip:8080 -s rr 
   ipvsadm -a -t $vip:8080 -r $rs1:8080 -g
   ipvsadm -a -t $vip:8080 -r $rs2:8080 -g
   ```

3. 配置real_server

   ```shell
   #! /bin/bash
   vip=192.168.0.166
   ifconfig lo:0 $vip broadcast $vip netmask 255.255.255.255 up
   route add -host $vip lo:0
   echo "1" >/proc/sys/net/ipv4/conf/lo/arp_ignore
   echo "2" >/proc/sys/net/ipv4/conf/lo/arp_announce
   echo "1" >/proc/sys/net/ipv4/conf/all/arp_ignore
   echo "2" >/proc/sys/net/ipv4/conf/all/arp_announce
   ```

4. 查看虚拟ip

   ```shell
   ifconfig





# 第二章 初识Nginx

配置https

```shell
server {
        listen 443 ssl;
        root /var/www/html;
        index index.html index.htm index.nginx-debian.html;
    
        ssl_certificate     keys/server.crt;#配置证书位置
        ssl_certificate_key keys/server.key;#配置秘钥位置
        location / { 
                proxy_pass  http://127.0.0.1:8080;
        }   

}
```

证书

1. 自签名

1. 申请免费证书

   ```ini
   url = https://manage.sslforfree.com/
   
   ; 没有域名就填写机器的公网IP
   ```
   
   
   
   



# 第三章 Nginx架构基础



## 3.1 冲突配置指令

```nginx
server{
	listen 8080;
	root /home/geek/nginx/html;
	access_log logs/geek.access.log main;
	
	location /test{
		root /home/geek/nginx/test;
		access_log logs/access.test.log main;
	}
	
	location /dlib{
		alias dlib/;
	}

	location / {
	}
}
```



## 3.2 Listen指令

```shell
listen unix:/var/run/nginx.sock;
listen 127.0.0.1:8000;
listen 127.0.0.1;
listen 8000;
listen *:8000;
listen localhost:8000 bind;
listen [::]:8000 ipv6only=on;
listen [::1];
```





# 第四章 详解HTTP模块



```flow
st=>start: 接收URI
op1=>operation: 分配请求内存池
op2=>operation: 状态机解析请求行
op3=>operation: 分配大内存
op4=>operation: 状态机解析请求行
op5=>operation: 标识URI

st->op1->op2->op3->op4->op5
```

```flow
st=>start: 接收header
op2=>operation: 状态机解析header
op3=>operation: 分配大内存
op4=>operation: 标识header
op5=>operation: 移除超时定时器
op6=>operation: 开始11个阶段的http请求处理

st->op2->op3->op4->op5->op6
```



## 4.4 正则表达式

1. 元字符

   | 代码 | 说明                         |
   | ---- | ---------------------------- |
   | .    | 匹配除换行外的任意单个字符   |
   | \w   | 匹配字母或数字或下划线或汉字 |
   | \s   | 匹配任意空白符               |
   | \d   | 匹配数字                     |
   | \b   | 匹配单词的开始或者结束       |
   | ^    | 匹配字符串开始               |
   | $    | 匹配字符串的结束             |

   

2. 重复

   | 代码  | 说明              |
   | ----- | ----------------- |
   | *     | 重复零次或多次    |
   | +     | 重复一次或多次    |
   | ?     | 重复零次或一次    |
   | {n}   | 重复n次           |
   | {n,}  | 重复n此或者更多次 |
   | {n,m} | 重复n到m次        |

   

3. 测试

   ```shell
   # 使用pcretest 工具测试
   ```



## 4.5 处理请求的server指令块



## rewrite阶段的rewrite模块

1. return指令语法

   ```shell
   return code [text];
   return code URL;
   return URL;
   
   Context: server,location,if
   ```

2. 返回状态码

   ```shell
   Nginx自定义：
   	444：关闭链接
   HTTP1.0标准：
   	301：http1.0永久重定向
   	302：临时重定向，禁止被缓存
   HTTP1.1标准：
   	303：临时重定向，允许改变方法，禁止被缓存
   	307：临时重定向，不允许改变方法，禁止被缓存
   	308：永久重定向，不允许改变方法
   ```

3. error_page指令

   ```shell
   error_page code uri;
   
   Context http,server,location, if in location;
   ```

   ```nginx
   error_page 404 /404.html;
   error_page 500 502 503 504 /50x.html;
   error_page 404 =200 /empty.gif;
   error_page 404 = /404.php;
   
   location / {
       error_page 404= @fallback;
   }
   ```

4. rewrite指令

   ```nginx
   rewrite regrex replacement [flag];
   
   Context: server, location,if
   
   # flag 取值
   last: 用replacement这个URI进行新的location匹配
   break: 停止当前脚本指令的执行
   redirect：返回302 重定向
   permanent：返回301 重定向
   ```

5. if指令

   ```nginx
   if (condition) {...}
   
   Context: server, location
   
   1. 检查变量为空或者值是否为0
   2. 将变量与字符串做匹配，使用=或者!=
   3. 将变量与正则表达式匹配
   	大小写敏感 ~或者!~
   	大小写不敏感 ~*或者!~*
   4. 检查文件是否存在 -f或者!-f
   5. 检查目录是否存在 -d或者!-d
   6. 检查文件，目录，软连接是否存在 -e或者-e!
   7. 检查是否为可执行文件 使用-x或者!-x
   ```
   
   ```nginx
   if($http_user_agent ~ MSIE){
       return 405;
   }
   
   if($request_method = POST){
       return 404;
   }
   
   if($slow){
       limit_rate 10k;
   }
   
   if($invalid_referer){
       return 403;
   }
   ```
   



## find_config阶段

1. location指令

   ```nginx
   Syntax: location [=|~|~*|^~] uri {...}
   Context: server, location
   
   Syntax: merge_slashes on| of
   Default: merge_slashes on;
   Context: http, server
   ```

2. location 匹配规则

   + 常规
   + = 精确匹配
   + ^~ 匹配上后则不再进行正则表达式匹配

3. 正则表达式

   + ~ 大小写敏感
   + ~* 忽略大小写

4. 内部跳转的命名location: @

5. **重点是匹配规则**



## preaccess阶段

1. limit_conn_zone指令

   ```nginx
   limit_conn_zone key zone=name:size;
   Context: http
   ```

2. limit_conn指令

   ```nginx
   limit_conn zone number;
   Context: http,server,location  
   ```

3. limit_conn_log_level 指令

   ```nginx
   limit_conn_log_level info|notice|warn|error;
   Default: limit_conn_log_level error;
   Context: http,server,location
   ```

4. limit_conn_status指令

   ```nginx
   limit_conn_status code;
   Default: limit_conn_status 503;
   Context: http,server,location
   ```

5. 示例配置

   ```nginx
   limit_conn_zone $binary_remote_addr zone=addr:10m;
   
   server {
       server_name limit.taohui.tech;
       root html/;
       error_log logs/myerror.log info;
       
       location / {
           limit_conn_status 500;
           limit_conn_log_level warn;
           limit_rate 50;
           limit_conn addr 1;
       }
   }
   ```

6. limit_req模块：限制一个链接上每秒处理的请求数，在limit_conn之前处理

7. limit_req_zone指令

   ```nginx
   limit_req_zone key zone=name:size rate=rate;
   Context: http
   
   # rate 单位为r/s 或者  r/m
   
   limit_req zone=name [burst=number][nodelay];
   Context: http, server,location
   # burst 默认为0 ---> 盆里可以容纳的请求数量
   # nodelay 对burst里面的请求不再采用延时处理的做法，而是立刻处理
   
   
   limit_req_log_level info|notice|warn|error;
   Default: limit_req_log_level error;
   Context: http,server,location
   
   limit_req_status code;
   Default limit_req_status 503;
   Context: http,server,location
   ```



## access 阶段

+ access模块

  ```ini
  [allow]
  Syntax  = allow address | CIDR | unix:| all;
  Context = http,server,location,limit_except 
  
  [deny]
  Syntax  = deny address | CIDR | unix:| all;
  Context = http,server,location,limit_except 
  ```

  示例

  ```nginx
  location / {
      deny 192.168.1.1;
      allow 192.168.1.0/24;
      allow 10.1.1.0/16;
      allow 2001:0db8::/32;
      deny all;
  }
  ```

  

+ auth_basic模块

  ```ini
  [auth_basic]
  Syntax  = auth_basic string | off;
  Default = auth_basic off;
  Context = http,server,location,limit_except;
  
  [auth_basic_user_file]
  Syntax  = auth_basic_user_file file;
  Context = http,server,location,limit_except;
  ```

  生成工具

  ```ini
  [httpd-tools]
  htpasswd -c file -b user pass
  ```

  示例

  ```nginx
  location / {
      satisfy any;
      auth_basic "test auth_basic";
      auth_basic_user_file examples/auth.pass;
      deny all;
  }
  ```

  

+ auth_request模块

  ```ini
  [编译]
  option = --with-http_auth_request_module
  
  [auth_request]
  Syntax  = auth_request uri | off;
  Default = auth_request off;
  Context = http,server,location
  
  [auth_request_set]
  Syntax = auth_request_set $variable value;
  Context = http,server,location
  ```

  功能

  向上游服务转发请求，若上有服务返回的响应码是2xx，则继续执行，若上游服务返回的是401或者403，则将响应返回给客户端。

  示例

  ```nginx
  server {
      location / {
          auth_request /test_auth;
      }
      
      location = /test_auth{
          proxy_pass http://127.0.0.1:8090/auth_upstream;
          proxy_pass_request_body off; # 没有请求body
          proxy_set_header Content-Length "";
          proxy_set_header X-Original-URI $request_uri;
      }
  }
  
  
  # 8090 的配置
  
  server {
      listen 8090;
      location /auth_upstream { 
          return 200 "auth success!";
          # return 403 "auth failed!";
      }
  }
  ```

+ satisfy指令

  ```ini
  [satisfy]
  Syntax  = satisfy all | any;
  Default = satisfy all;
  Context = http,server,location;
  
  ; all  access,auth_basic,auth_request 模块均要放行请求，该请求才能继续往下执行
  ; any  access,auth_basic,auth_request 任意一个模块放行请求即可
  ```



## precontent阶段

1. try_files模块

   ```ini
   [try_files]
   Syntax = try_files file ... uri;
   Syntax = try_files file ... =code;
   
   Context = server, location
   
   ; 依次访问多个url对应的文件,如果所有文件都不存在则按最后一个URL或者code返回。
   ```

   示例

   ```nginx
   server{
       error_log logs/myerror.log info;
       root html/;
       default_type text/plain;
       
       location /first{
           try_files /system/maintenance.html
               $uri $uri/index.html $uri.html
               @lasturl;
       }
       
       location @lasturl {
           return 200 'lasturl!\n';
       }
       
       location /second {
           try_files $uri $uri/index.html $uri.html =404;
       }
   }
   ```

   

2. ngx_http_mirror_module

   ```ini
   ; 处理请求时，生成子请求访问其他服务，对子请求的返回值不做处理
   ; 主要用于流量拷贝
   [mirror]
   Syntax  = mirror uri | off;
   Default = mirror off;
   Context = http,server,location
   
   [mirror_request_body]
   Syntax  =  mirror_request_body on | off;
   Default =  mirror_request_body on;
   Context = http,server,location;
   ```

   示例

   ```nginx
   server{
       error_log logs/error.log debug;
       
       location / {
           mirror /mirror;
           mirror_request_body off;
       }
       
       location = /mirror{
           internal; # 指定只允许来自本地 Nginx 的内部调用
           proxy_pass http://127.0.0.1:10020$request_uri;
           proxy_pass_request_body off;
           proxy_set_header Content-Length "";
           proxy_set_header X-Original-URI $request_uri;
       }
   }
   
   server{
       listen 10020;
       location / {
           return 200 'mirror response!';
       }
   }
   ```



## content 阶段

1. static模块

   ```ini
   ;将url映射为文件路径，以返回静态文件内容
   [alias]
   Syntax  = alias path;
   Content = location; 
   
   [root]
   Syntax  = root path;
   Default = root html;
   Context = http,server,location,if in location
   
   ; root会将完整url映射进文件路径中
   ; alias只会将location后的URL映射到文件路径
   
   ; root处理结果: root路径 + location路径
   ; alias处理结果: alias路径替换location路径
   ```

   三个变量

   + request_filename：待访问的文件的完整路径

   + document_root：由URI和root/alias规则生成的文件夹路径

   + realpath_root：将document_root中的软链接换成真实路径

     示例

     ```nginx
     server {
         location /RealPath{
             alias html/realpath/;
             return 200 '$request_filename:$document_root;$realpath_root';
         }
     }
     ```

     其它指令

     ```ini
     [types]
     Syntax  = types {...}
     Default = types {text/html html; image/gif gif; image/jpeg jpg;}
     Context = http,server,location
     
     [default_type]
     Syntax  = default_type mime-type;
     Default = default_type text/plain;
     Context = http,server,location;
     
     [types_hash_bucket_size]
     Syntax  = types_hash_bucket_size size;
     Default = types_hash_bucket_size 64;
     Context = http,server,location;
     
     [types_hash_max_size]
     Syntax  = types_hash_max_size size;
     Default =  types_hash_max_size 1024;
     Context = http,server,location;
     
     
     [log_not_found]
     Syntax  = log_not_found on | off;
     Default = log_not_found on;
     Context = http,server,location;
     ```

     重定向跳转的域名

     ```ini
     ; 访问目标为目录,但是URL末尾未加/返回301重定向,重定向相关的指令如下
     [server_name_in_redirect]
     ; 响应头的Location用server_name中的域名
     Syntax  = server_name_in_redirect on | off;
     Default = server_name_in_redirect off;
     Context = http,server,location;
     
     [port_in_redirect]
     Syntax  = port_in_redirect on | off;
     Default = port_in_redirect on;
     Context = http,server,location;
     
     [absolute_redirect]
     ; 响应头的Location字段是否填写域名
     ; 如果请求头没有Host字段,使用请求的域名
     ; 如果有Host字段,使用Host的域名
     ; 如果server_name_in_redirect on 使用 server_name
     Syntax  = absolute_redirect on | off;
     Default = absolute_redirect off;
     Context = http,server,location;
     ```

     

1. concat模块

2. random_index模块

3. index模块

   ```ini
   ; 优先于auto_index模块
   ; 用于设置网站的默认首页
   [index]
   Syntax = index file ...
   Default = index index.html
   Context = http,server,location
   ```

   示例

   ```nginx
   server {
       location / {
           root /usr/local/nginx/html;
           index index.html index.htm;
       }
   }
   ```

   

4. auto_index模块

   ```ini
   [autoindex]
   ; 用于显示目录结构
   Syntax  = autoindex on | off;
   Default = autoindex off;
   Context = http,server,location;
   
   [autoindex_exact_size]
   Syntax  = autoindex_exact_size on | off;
   Default = autoindex_exact_size on;
   Context = http,server,location;
   
   [autoindex_formt]
   Syntax  = autoindex_formt html | xml | json | jsonp;
   Default = autoindex_formt html;
   Context = http,server,location;
   
   [autoindex_localtime]
   Syntax  = port_in_redirect on | off;
   Default = port_in_redirect off;
   Context = http,server,location;
   ```

   



# 第五章 反向代理与负载均衡



# 第六章 性能优化



# 第七章 Nginx与Openresty

