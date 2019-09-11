# 安装protobuf

1. 下载源码

   ```shell
   wget  https://github.com/protocolbuffers/protobuf/releases/download/v3.9.0/protobuf-cpp-3.9.0.zip
   ```

2. 安装

   ```shell
   yum install -y unzip
   unzip protobuf-cpp-3.9.0.zip
   cd ./protobuf-3.9.0/
   ./configure --prefix=/usr/local/protobuf
   # 编译
   make -j4
   # 测试
   make check -j4
   # 安装
   make install -j4
   # refresh shared library cache.
   ldconfig
   ```

3. 设置环境变量

   ```shell
   #vim /etc/profile
   #export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/protobuf/lib
   #export LIBRARY_PATH=$LIBRARY_PATH:/usr/local/protobuf/lib
   #export PATH=$PATH:/usr/local/protobuf/bin
   
   echo "export LD_LIBRARY_PATH=\$LD_LIBRARY_PATH:/usr/local/protobuf/lib" >> /etc/profile
   echo "export LIBRARY_PATH=\$LIBRARY_PATH:/usr/local/protobuf/lib" >> /etc/profile
   echo "export PATH=\$PATH:/usr/local/protobuf/bin" >> /etc/profile
   echo "export CPLUS_INCLUDE_PATH=\$CPLUS_INCLUDE_PATH:/usr/local/protobuf/include" >> /etc/profile
   
   # 执行以下命令使配置生效
   source /etc/profile
   ```

4. 查看版本

   ```shell
   protoc --version
   ```

   