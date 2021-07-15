# 制作证书



## 步骤

```shell
# 产生rsa私钥
openssl genrsa -out server.key 2048

# 产生证书请求
openssl req -new -key server.key -out server.csr
#Country Name : cn
#State or Province Name : jiangsu
#Locality Name : nanjing
#Organization Name : tencent
#Organizational Unit Name : guangzi
#Common Name : 127.0.0.1 --> 注意： 这里填写 域名或者 IP地址
#Email Address :wzc_0618@126.com
#A challenge password : 直接按下回车
#An optional company name ： 直接按下回车


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


## 产生rsa秘钥

+ 产生私钥

  ```shell
  # 产生长度为1024的私钥
  openssl genrsa -out rsa_private_key.pem 1024
  ```

+ 根据私钥产生公钥

  ```shell
  openssl rsa -in rsa_private_key.pem -pubout -out rsa_public_key.pem
  ```

+ 加密和解密

  ```shell
  # 使用公钥加密
  openssl rsautl -encrypt -in ${加密文件} -inkey ${公钥} -pubin -out ${加密后的文件}
  openssl rsautl -encrypt -in hey.c -inkey rsa_public_key.pem -pubin -out hey.en
  
  # 使用私钥解密
  openssl rsautl -decrypt -in ${被加密的文件} -inkey ${私钥文件} -out ${解密后的文件}
  openssl rsautl -decrypt -in hey.en -inkey rsa_private_key.pem -out hey.de
  ```

  



# 非对称加密的原理

+ 保证发送的内容已经加密

+ 保证内容是某人发送的，比如是google发送的

+ 例子

  ```shell
  # 牛郎给织女发送邮件
  
  1. 牛郎用织女的 公钥 加密,确保只能织女才能解密
  2. 牛郎用自己的私钥做签章， 织女收到后用牛郎的公钥验证，确保信件是牛郎发出来的
  ```

+ 公钥和私钥的作用

  > 1. 公钥
  >    + 加密数据，加密后的数据用私钥解密
  >    + 校验签名
  > 2. 私钥
  >    + 解密用公钥加密后的数据
  >    + 制作签名，签名可以用公钥来校验