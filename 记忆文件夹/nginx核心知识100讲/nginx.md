## 跨域配置

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



## 利用反向代理解决跨域

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





## 利用websocket 解决跨域

1. websocket支持跨域通信





## 利用jsonp解决跨域

