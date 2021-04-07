

# 安装gcc-10.1

1. 下载源码

   ```shell
   wget https://mirrors.aliyun.com/gnu/gcc/gcc-10.1.0/gcc-10.1.0.tar.gz
   
   tar xvf gcc-10.1.0.tar.gz
   
   cd ./gcc-10.1.0
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
   yum remove gcc-c++ -y
   yum remove gcc -y
   
   #STEP-2 安装
   make install
   
   #STEP-3 删除旧的so
   rm -f /usr/lib64/libstdc++.so*
   rm -f /usr/local/lib64/libstdc++.so.6.0.28-gdb.py

   # 重新加载动态库 新的C++ so放/usr/local/lib64
   vim /etc/ld.so.conf
   /usr/local/lib64
   ldconfig
   
   #STEP-4 重新登录
   su - root
   ```
   
   