# 第一章 制作证书

***



## 1.1 步骤

***

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



## 1.2 证书格式

***

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



## 1.3 产生rsa秘钥

***

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

  



# 第二章 非对称加密的原理

***

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



# 第三章  签名和验证

***



## 3.1 生成数据文件，私钥和公钥

***

```shell
#Create a file containing all lower case alphabets
$ echo abcdefghijklmnopqrstuvwxyz > myfile.txt
 
#Generate 512 bit Private key
$ openssl genrsa -out myprivate.pem 512
 
#Separate the public part from the Private key file.
$ openssl rsa -in myprivate.pem -pubout > mypublic.pem
 
#Cat the contents of private key
$ cat myprivate.pem
 
-----BEGIN RSA PRIVATE KEY-----
MIIBOwIBAAJBAMv7Reawnxr0DfYN3IZbb5ih/XJGeLWDv7WuhTlie//c2TDXw/mW
914VFyoBfxQxAezSj8YpuADiTwqDZl13wKMCAwEAAQJAYaTrFT8/KpvhgwOnqPlk
NmB0/psVdW6X+tSMGag3S4cFid3nLkN384N6tZ+na1VWNkLy32Ndpxo6pQq4NSAb
YQIhAPNlJsV+Snpg+JftgviV5+jOKY03bx29GsZF+umN6hD/AiEA1ouXAO2mVGRk
BuoGXe3o/d5AOXj41vTB8D6IUGu8bF0CIQC6zah7LRmGYYSKPk0l8w+hmxFDBAex
IGE7SZxwwm2iCwIhAInnDbe2CbyjDrx2/oKvopxTmDqY7HHWvzX6K8pthZ6tAiAw
w+DJoSx81QQpD8gY/BXjovadVtVROALaFFvdmN64sw==
-----END RSA PRIVATE KEY-----
```





## 3.2 签名

***

```shell
# Sign the file using sha1 digest and PKCS1 padding scheme
$ openssl dgst -sha1 -sign myprivate.pem -out sha1.sign myfile.txt
 
# Dump the signature file
$ hexdump sha1.sign
 
0000000 91 39 be 98 f1 6c f5 3d 22 da 63 cb 55 9b b0 6a
0000010 93 33 8d a6 a3 44 e2 8a 42 85 c2 da 33 fa cb 70
0000020 80 d2 6e 7a 09 48 37 79 a0 16 ee bc 20 76 02 fc
0000030 3f 90 49 2c 2f 2f b8 14 3f 0f e3 0f d8 55 59 3d0000040
```





## 3.3 验证

***

```shell
# Verify the signature of file
$ openssl dgst -sha1 -verify mypublic.pem -signature sha1.sign myfile.txt
Verified OK
```







# 第四章 免费证书申请网站

```ini
[info]
url  = https://manage.sslforfree.com/
直接用DNS 验证即可, 推荐用godaddy 来购买域名.
```

