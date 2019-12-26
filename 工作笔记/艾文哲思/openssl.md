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

  