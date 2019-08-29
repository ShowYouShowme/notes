# centOS源码安装gcc和g++

1. 下载源码

   ```shell
   wget https://github.com/gcc-mirror/gcc/archive/gcc-8_2_0-release.tar.gz
   ```

2. 安装依赖库

   ```shell
   tar -zxvf gcc-8_2_0-release.tar.gz
   cd ./gcc-gcc-8_2_0-release
   yum -y install bzip2
   # 必须设置代理，否则下载速度非常慢
   export ftp_proxy=http://192.168.0.100:8090
   ./contrib/download_prerequisites 
   ```

3. 配置

   ```shell
   mkdir build
   cd build
   # 仅支持C/C++
   ../configure  --prefix=/usr --enable-multilib --enable-languages=c,c++ -disable-multilib
   ```

4. 编译安装

   ```shell
   # top 命令下按下数字1显示CPU个数,内存建议8G以上，否则容易内存不足导致编译失败
   make -j8
   make install
   ```

   