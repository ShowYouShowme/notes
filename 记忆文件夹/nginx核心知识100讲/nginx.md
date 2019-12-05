## 跨域配置

```nginx
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

