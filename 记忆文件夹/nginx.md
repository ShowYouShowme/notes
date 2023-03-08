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
    # proxy_timeout 300s;							# 300s内没有数据可读写则关闭，默认10m
    proxy_timeout 60m;
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



## 2.0 常见配置项

```ini
[配置启动用户]
user  nobody;

[配置工作进程数]
worker_processes  1;

[配置最大连接数]
;生产服务一般配置为65536,同时得修改ulimit
worker_connections  1024;
```





## 2.1 配置https

```shell
#ssl_certificate 和 ssl_certificate_key 的 Context是http、server,因此只有一个域名或者泛域名证书，# 可以在 http模块里面配置 
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
   Let’s-Encrypt 来申请
   ```
   
   
   
   
   
   配置案例
   
   ```nginx
   #nginx 是编译安装
   #域名在godaddy购买
   #keys目录和html同级
   http{
   
       server{
           listen 8300;
           root         html/;
       }
   
   server {
           listen 4430 ssl;
           root html/;
           index index.html index.htm index.nginx-debian.html;
       
           ssl_certificate     ../keys/certificate.crt;#配置证书位置
           ssl_certificate_key ../keys/private.key;#配置秘钥位置
           location / { 
                   proxy_pass  http://127.0.0.1:8300;
           }   
   
   }
   }
   ```
   
   
   
   
   

## 2.2 基本http服务配置

```nginx
# 如果是非root用户编译安装Nginx,打算监听80端口,必须用sudo 启动,同时配置 user 为 该用户而不是nobody
#user  nobody;
worker_processes  1;

#error_log  logs/error.log;
#error_log  logs/error.log  notice;
#error_log  logs/error.log  info;

#pid        logs/nginx.pid;


events {
    worker_connections  1024; # 最大连接数配置  同时链接超过后会链接失败,生产上要改大
							  # 同时还要修改ulimit 的参数 和  Mysql的最大连接数
}

http{
    server{
        listen 8100;
        root         /usr/share/nginx/html;
    }

}
```



## 2.3 文件服务器配置

```nginx
http{
    server{
	  listen 8200;
          location / {
		alias dlib/;
		autoindex on;		
		}
    }
}
```



## 2.4 http反向代理

```nginx

worker_processes  1;
events {
    worker_connections  1024;
}

http {
    include       mime.types;
    default_type  application/octet-stream;
    sendfile        on;
    keepalive_timeout  65;
    
    #这里是关键
    server {
        listen       9901;
		location / {
				proxy_pass  http://192.168.2.102:9901;
		}
    }
}
```



## 2.5 前台启动nginx

```nginx
#全局作用域
daemon off;
```



## 2.6 ws反向代理 + wss配置

```nginx
http{
    
map $http_upgrade $connection_upgrade {
    default upgrade;
    '' close;
}

upstream websocket {
    server 192.168.2.228:8080; # appserver_ip:ws_port
}

server {
     server_name dev.icashflow.cc;
     listen 8283 ssl;
     location / { 
         proxy_pass http://websocket:8000;
         # 超时配置
         proxy_read_timeout 300s; # 默认60s,游戏开发的话,使用默认值即可
         proxy_send_timeout 300s; # 默认60s,游戏开发的话,使用默认值即可

         proxy_set_header Host $host;
         proxy_set_header X-Real-IP $remote_addr;
         proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;

         proxy_http_version 1.1;
         proxy_set_header Upgrade $http_upgrade;
         proxy_set_header Connection $connection_upgrade;
     }
     ssl_certificate     ../keys/certificate.crt;#配置证书位置
     ssl_certificate_key ../keys/private.key;#配置秘钥位置
}

}
```



简化版配置

```nginx
http{
    server {
         	 listen 8000;
             location / { 
                 proxy_http_version 1.1;
                 proxy_set_header Upgrade $http_upgrade;
                 proxy_set_header Connection "upgrade";
                 proxy_pass http://websocket:8000;
             }
    }
}
```





## 2.7 多域名配置

1. 不定义default_server

   ```nginx
   http {
       # 如果没有显式声明 default server 则第一个 server 会被隐式的设为 default server
       server {
           listen 80;
           server_name _; # _ 并不是重点 __ 也可以 ___也可以
           return 403; # 403 forbidden
       }
       
       server {
           listen 80;
           server_name www.a.com;
           ...
       }
       
       server {
           listen 80;
           server_name www.b.com;
           ...
       }
       
       # 443端口禁止 直接用ip地址访问
       server {
           listen 443 ssl default_server;
           server_name _;
           return 403;
   	}
   
   }
   
   # 在没有显式定义 default server 时，nginx 会将配置的第一个 server 作为 default server，即当请求没有匹配任何 server_name 时.此 server 会处理此请求。所以，当我们直接使用 ip 访问时会被交给此处定义的第一个 server 处理，403 forbidden。
   ```

   

2. 显示定义default_server

   ```nginx
   http {
       server {
           listen 80;
           server_name www.a.com;
           ...
       }
       
       server {
           listen 80;
           server_name www.b.com;
           ...
       }
       
       # 显示的定义一个 default server, 用ip访问就会匹配到这里
       server {
           listen 80 default_server;
           server_name _;
           return 403; # 403 forbidden
       }
       
   }
   ```

   

   
   
## 2.8 反向代理路径修改

nginx的proxy_pass配置路径，加与不加“/”差异巨大，加上"/"会去掉匹配的那部分

1. 绝对路径

   ```nginx
   location /proxy {
       proxy_pass http://192.168.137.181:8080/;
   }
   
   # 访问路径    = http://127.0.0.1/proxy/test/test.txt
   # 实际请求路径 = http://10.0.0.1:8080/test/test.txt
   # nginx会去掉匹配的 /proxy
   ```

2. 相对路径

   ```nginx
   location /proxy {
       proxy_pass http://10.0.0.1:8080;
   }
   
   # 访问路径   = http://127.0.0.1/proxy/test/test.txt
   # 实际路径   = http://192.168.137.181:8080/proxy/test/test.txt
   ```

   

3. 增加前缀

   ```nginx
   location /proxy {
       proxy_pass http://10.0.0.1:8080/static01/;
   }
   
   # 访问路径   = http://127.0.0.1/proxy/test/test.txt
   # 实际路径   = http://10.0.0.1:8080/static01/test/test.txt
   ```

4. 使用正则重写

   ```nginx
   location /resource {
       rewrite  ^/resource/?(.*)$ /$1 break;
       proxy_pass http://192.168.137.189:8082/; # 转发地址
   }
   
   # 新的路径就是除去/resource/以外的所有，就达到了去除/resource前缀的目的
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





## 4.6 postread阶段

获取用户真实IP

```nginx
location ^~ /your-service/ {
    proxy_set_header        X-Real-IP       $remote_addr; # 这一条配置只需要在最外层的反向代理加,比如CDN
    proxy_set_header        X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_pass http://localhost:60000/your-service/;
}
```





## rewrite阶段的rewrite模块

1. return指令语法

   ```shell
   return code [text];
   return code URL;
   return URL;
   
   Context: server,location,if
   
   #打印请求uri和request
   return 200  'uri = $uri args=$args http_host=$http_host http_user_agent=$http_user_agent http_x_forwarded_for=$http_x_forward    ed_for http_x_real_ip=$http_x_real_ip';
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

   ```nginx
   #利用try_files返回配置文件给client
       server{
            listen 8200;
            root game_config/;
            location /getShopConfig{
                   default_type application/json;
                   try_files /shop.json /error.json;
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

   ```ini
   ; 页面需要访问多个小文件时,把他们的内容合并到一次http响应中返回
   ; 模块: ngx_http_concat_module  阿里巴巴提供的开源模块
   
   [concat]
   ; 是否启用concat模块
   Syntax  = concat on | off
   default = concat off
   Context = http,server,location
   
   [concat_delimiter]
   ; 文件内容分隔符
   Syntax  = concat_delimiter string
   Default = NONE
   Context = http,server,location
   
   [concat_types]
   ; 对哪些文件类型做合并
   Syntax = concat_types MIME types
   Default = concat_types text/css application/x-javascript
   Context = http,server,location
   
   [concat_unique]
   ; 对一种或者多种文件类型进行合并
   Syntax  = concat_unique on | off
   Default = concat_unique on
   Context = http,server,location
   
   [concat_ignore_file_error]
   ; 部分文件出错(比如不存在)继续返回其它文件
   Syntax  = concat_ignore_file_error on | off
   Default = off
   Context = http,server,location
   
   [concat_max_files]
   ; 最多合并多少文件
   Syntax  = concat_max_files numberp
   Default =  concat_max_files 10
   Context = http,server,location
   ```

   示例

   ```nginx
   server {
       server_name concat.taohui.tech;
       
       error_log logs/myerror.log debug;
       concat on;
       root html;
       
       location /concat {
           concat_max_files 20;
           concat_types text/plain;
           concat_unique on;
           concat_delimiter ':::';
           concat_ignore_file_error on;
       }
   }
   
   # curl concat.taohui.tech/concat/??1.txt,2.txt
   ```

   

2. random_index模块

3. index模块

   ```ini
   ; 优先于auto_index模块
   ; 用于设置网站的默认首页
   [index]
   ; 指定/访问时返回index文件的内容
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
   ; 以/访问时返回目录结构
   ; 用于显示目录结构,如果目录下有index.html则不会显示目录结构
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
   Syntax  = autoindex_localtime on | off;
   Default = autoindex_localtime off;
   Context = http,server,location;
   ```

   示例

   ```nginx
   server{
       listen 8080;
       location / {
           alias html/; # 必须以/结尾,使用命令nginx -h查看prefix path
           autoindex on;
           autoindex_exact_size off;
           autoindex_format html;
           autoindex_localtime on;
       }
   }
   ```




## log阶段

模块：nix_http_log_module



# 第五章 反向代理与负载均衡



# 第六章 性能优化

1. 设置最大连接数

   ```shell
   #工作进程数，一般和cpu个数一致
   worker_processes  1;
   
   #一个进程允许最大连接数，可以设置为 65536
   worker_connections  1024;
   
   #查看系统级和用户级最大限制
   cat /proc/sys/fs/file-max
   
   ulimit -n  # 这里默认是1024，要设置为65536
   
   
   #php-fpm最大连接数设置
   pm = static
   pm.max_children = 100  #启动时即生成 100个工作进程，一般来讲可以设置为cpu的个数
   ```

# 第七章 Nginx与Openresty



# 第八章 windows使用nginx

```ini
[启动nginx]
;推荐使用pm2来启动nginx
;使用pm2管理nginx,必须配置前台启动 daemon off;
cmd = start nginx

[重新加载配置文件]
cmd = nginx -s reload

[测试配置文件]
cmd =  nginx -t -c /path/to/nginx.conf

[关闭nginx]
cmd1 = nginx -s stop
cmd2 = nginx -s quit

[pm2管理nginx]
;记得启动前测试配置文件是否有错误
[pm2配置]
 {
    "name"       : "nginx",
    "script"     : "nginx.exe",
    "exec_interpreter": "none",
    "exec_mode"  : "fork_mode",
	"cwd"        : "C:\\Users\\jumbo\\local\\nginx-1.23.2"
 }
```



# 附录

1. 非root测试nginx配置时不能绑定端口

   ```shell
   msg=nginx: [emerg] bind() to 0.0.0.0:80 failed (13: Permission denied)
   
   reason=Linux只有root用户可以使用1024一下的端口
   
   solution=将配置文件中的80端口改为1024以上
   ```

   



# 第九章 安装

源码编译的nginx最好不要用放root里面，应该放普通用户里面，否则启动很可能会失败，因为目录的权限配置不当！

## 9.1 源码编译安装

```ini
wget http://nginx.org/download/nginx-1.16.1.tar.gz
tar -zxvf nginx-1.16.1.tar.gz
cd ./nginx-1.16.1

; nginx配置文件在VIM中高亮
mkdir ~/.vim/
cp -r ./contrib/vim/* ~/.vim/

yum install gcc pcre pcre-devel zlib zlib-devel openssl openssl-devel -y


./configure --prefix=$HOME/local/nginx/ --with-stream --with-http_ssl_module

make -j4


make install
```





## 9.2 包管理器安装

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
```





# 第十章 静态资源文件服务

```ini
location / {
      root   html;
      autoindex on;   ## 加上这条即可显示文件夹
      index  index.html index.htm;
}
```



# 第十一章 反向代理



## 11.1 TCP反向代理

TCP反向代理 + 负载均衡配置示例

```ini
; configure 时 加上--with-stream这个参数，以加载ngx_stream_core_module这个模块
; 监听本机的2222端口，实现跳转到192.168.56.12的22号端口
; --with-http_ssl_module 支持https

; 反向代理 + 负载均衡
stream {
    upstream tcp_proxy{
    hash $remote_addr consistent;
    server 178.128.61.189:8399;
    server 178.128.61.190:8399;
    }

    server {
    listen 8399 so_keepalive=on;
    proxy_connect_timeout 10s;  # 链接超时
    proxy_timeout 60m;          # 60分钟无数据传输就关闭链接,默认10分钟
    proxy_pass tcp_proxy;
    }
}
```



TCP 反向代理配置示例

```nginx
stream {
    server {
        listen 3000 so_keepalive=on;
        proxy_connect_timeout 10s;
        proxy_timeout 60m;
        proxy_pass 127.0.0.1:3306;

    # 也支持socket
    # proxy_pass unix:/var/lib/mysql/mysql.socket;
    }
}
```





## 11.2 跨域配置

```nginx
# 这种一般是网页直接在客户浏览器启动(不是从网站下载)，然后请求网站数据
# 如果用python 的flask框架时,直接在响应头加Access-Control-Allow-Origin:*即可解决问题
# 浏览器跨域POST请求时,先发起OPTIONS请求再发起POST请求
location / { 
    #root   html;
    #index  index.html index.htm;
    return 200 'login success!';
    add_header Access-Control-Allow-Origin *;
    add_header Access-Control-Allow-Methods 'GET, POST, OPTIONS';
    add_header Access-Control-Allow-Headers 'DNT,X-Mx-ReqToken,Keep-Alive,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Authorization';

    if ($request_method = 'OPTIONS') {
        return 204;
    }   
}
```

```python
# flask 示例代码
def post_greeting(term: str) -> str:
    # person = {"name" : "wzc","age": 30}
    person = [
  {
    "id": "Falco eleonorae",
    "label": "Eleonora's Falcon",
    "value": "Eleonora's Falcon"
  }
]
    response = make_response(json.dumps(person))
    response.headers["Access-Control-Allow-Origin"] = "*" 
    return response
```

```javascript
//cocos-creator跨域处理
//1--nginx要像上面那样配置
//2--代码要如下面
var xhr = new XMLHttpRequest();
xhr.open('GET', 'http://example.com/', true);
xhr.withCredentials = false; //注意这里
xhr.send(null);
```



## 11.3 利用反向代理解决跨域

```nginx
#user  nobody;
worker_processes  1;

#error_log  logs/error.log;
#error_log  logs/error.log  notice;
#error_log  logs/error.log  info;

#pid        logs/nginx.pid;


events {
    worker_connections  1024;
}


http {
    include       mime.types;
    default_type  application/octet-stream;

    #log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
    #                  '$status $body_bytes_sent "$http_referer" '
    #                  '"$http_user_agent" "$http_x_forwarded_for"';

    #access_log  logs/access.log  main;

    sendfile        on;
    #tcp_nopush     on;

    #keepalive_timeout  0;
    keepalive_timeout  65;

    #gzip  on;

    server {
        listen       80;
        server_name  localhost;

        #charset koi8-r;

        #access_log  logs/host.access.log  main;

        location / {
            root   html;
            index  index.html index.htm;
        }

        #error_page  404              /404.html;

        # redirect server error pages to the static page /50x.html
        #
        error_page   500 502 503 504  /50x.html;
        location = /50x.html {
            root   html;
        }
	location /get_text{
		proxy_pass http://127.0.0.1:81/get_text;
	}
    }
    
        server {
        listen       81;
        server_name  localhost;

        #charset koi8-r;

        #access_log  logs/host.access.log  main;

        location / {
            root   html_81;
            index  index.html index.htm;
        }

        #error_page  404              /404.html;

        # redirect server error pages to the static page /50x.html
        #
        error_page   500 502 503 504  /50x.html;
        location = /50x.html {
            root   html;
        }
	
	location ~ ^/get_text {
    	default_type text/html;
    	return 200 'This is text!';  
}
    }
}
```

```html
<!DOCTYPE html>
<html>
   <body>
	<p1 id = "demo"></p1>
   <button type="button" onclick="loadDoc()">Change Content</button>
      <script>
                  function loadDoc() {
          var xhttp = new XMLHttpRequest();
          xhttp.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
             document.getElementById("demo").innerHTML = this.responseText;
            }
          };
          xhttp.open("GET", "http://10.10.10.123:80/get_text", true);
          xhttp.send();
        }
      </script>
   </body>
</html>

```

思路：本来ajax请求http://10.10.10.123:81/get_text，但是这样会造成跨域（服务器是http://10.10.10.123:80），因此先请求到http://10.10.10.123:80/get_text，然后把http://10.10.10.123:80/get_text 的请求反向代理到http://10.10.10.123:81/get_text







# 第十二章 SSL证书

网站 = https://freessl.cn/，改网站申请的免费证书，一次可以用一年。



## 12.1 申请免费证书

使用Let’s-Encrypt来申请免费证书，一次可以使用3个月，到期后可以再次执行命令更新

```ini
[官网]
url = https://github.com/certbot/certbot
url2= https://certbot.eff.org/

[安装]
;系统  centos7
cmd-1 = yum install epel-release -y
cmd-2 = yum install certbot -y

;必须先启动一个nginx服务,并且防火墙开放80端口,同时要将域名映射到指定的ip地址
[申请证书]
;也可以直接指定webroot: certbot certonly --webroot -w /usr/share/nginx/html -d shop.icashflow.cc
step-1 = sudo certbot certonly --webroot -w /home/centos/local/nginx/html -d dev.icashflow.cc -d stage.icashflow.cc 
;Place files in webroot directory (webroot)
step-2 = 输入2
;输入邮箱地址
step-3 = wzc199088@gmail.com
;You must agree in order to register with the ACME server
step-4 = y
;share your email address with the Electronic Frontier Foundation
step-5 = n
;Input the webroot for shop.icashflow.cc
;输入网站根目录
step-5 = /usr/share/nginx/html


;申请到的证书的路径
certificate = /etc/letsencrypt/live/shop.icashflow.cc/fullchain.pem

;申请到的私钥的路径
private_key = /etc/letsencrypt/live/shop.icashflow.cc/privkey.pem



;证书的有效期只有3个月
[更新证书]
;测试自动更新是否正常,如果看到Congratulations, all simulated renewals succeeded:表示成功
cmd = certbot renew --dry-run

;更新命令
cmd = certbot renew

[配置定时任务自动更新]
crontab = 0 3,19 * * * certbot renew

[使用DNS解析申请证书--不需要启动nginx监听80端口]
cmd = certbot certonly --manual --preferred-challenge dns -d dev.icashflow.cc -d stage.icashflow.cc

;在godaddy里面增加TXT记录

;查询TXT记录是否生效
nslookup -query=txt  _acme-challenge.stage.icashflow.cc

;TXT记录生效后,按Enter就可以生成申请到证书了

;更新证书
cmd = certbot renew
```





## 12.2 证书种类



### 按照验证方式划分

+ DV证书：只需验证域名所有权，无需人工验证申请单位真实身份，几分钟就可颁发的SSL证书。价格一般在百元至千元左右，适用于个人或者小型网站
+ OV证书：需要验证域名所有权以及企业身份信息，证明申请单位是一个合法存在的真实实体，一般在1~5个工作日颁发。价格一般在百元至千元左右，适用于企业型用户申请。
+ EV证书：除了需要验证域名所有权以及企业身份信息之外，还需要提交一下扩展型验证，比如：邓白氏等，通常CA机构还会进行电话回访，一般在2~7个工作日颁发证书。价格一般在千元至万元左右，适用于在线交易网站、企业型网站。EV证书会将公司名称直接显示在浏览器上面。



### 按照域名数量划分

+ 单域名证书：只保护一个域名（包括带www和不带www）的SSL证书，可以是顶级域名可以是二级域名
+ 多域名证书：可以同时保护多个域名，不限制域名类型
+ 通配符证书：只能保护一个域名以及该域名的所有下一级域名，不限制域名数量；例如：[http://anxinssl.com](https://link.zhihu.com/?target=http%3A//anxinssl.com)及它的所有子域，没有数量限制。

