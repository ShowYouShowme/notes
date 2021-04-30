# 制作证书



## 步骤

```shell
# 产生rsa私钥
openssl genrsa -out server.key 2048

# 产生证书请求
openssl req -new -key server.key -out server.crt

# 签名
openssl x509 -req -days 365 -in server.csr -signkey server.key -out server.crt
```



## 证书格式

1. PEM 格式

   > 以-----BEGIN CERTIFICATE-----开头，-----END CERTIFICATE-----结尾，中间是base64编码的内容。apache和nginx需要的就是这种证书
   >
   > 查看证书信息：
   >
   > openssl x509 -noout -text -in server.crt

2. DER格式

   > 二进制格式证书
   >
   > 查看证书信息：
   >
   > openssl x509 -noout -text -informder  -in server.der