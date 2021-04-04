

# 安装gcc-7.3

1. 下载源码

   ```shell
   wget http://ftp.gnu.org/gnu/gcc/gcc-7.3.0/gcc-7.3.0.tar.xz
   
   tar xvf gcc-7.3.0.tar.xz
   
   cd ./gcc-7.3.0
   ```

2. 安装gcc和g++

   ```shell
   yum -y install bzip2.x86_64
   
   yum -y gcc gcc-c++
   ```

3. 下载依赖

   ```shell
   ./contrib/download_prerequisites
   
   # 会下载并解压,如果成功打印 "All prerequisites downloaded successfully"
   
   # 如果下载慢,可以加入下面的代理
   export http_proxy=http://10.10.10.23:8090
   export http_proxys=http://10.10.10.23:8090
   ```

4. 编译

   ```shell
   ./configure --enable-checking=release --enable-languages=c,c++ --disable-multilib
   
   make -j10
   ```

5. 安装

   ```shell
   #STEP-1 卸载之前的gcc
   yum remove gcc-c++
   yum remove gcc
   
   #STEP-2 安装
   make install
   
   #STEP-3 重新登录
   su - root
   ```

   