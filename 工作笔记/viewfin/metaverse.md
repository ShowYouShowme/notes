## 编译

***

1. 安装依赖

   ```shell
   sudo apt-get install -y git cmake autoconf automake libtool pkg-config
   ```

2. 安装第三方包

   + 安装boost

     ```shell
     sudo apt-get install libboost-all-dev
     ```

   + 安装zeromq

     ```shell
     wget https://github.com/zeromq/libzmq/releases/download/v4.2.1/zeromq-4.2.1.tar.gz
     tar -xzvf zeromq-4.2.1.tar.gz
     cd zeromq-4.2.1
     ./autogen.sh
     ./configure
     make -j4 # 内存不够可以make -j1 
     sudo make install && sudo ldconfig
     ```

   + 安装secp256k1

     ```shell
     git clone https://github.com/mvs-live/secp256k1
     cd secp256k1
     ./autogen.sh
     ./configure --enable-module-recovery
     make -j4
     sudo make install && sudo ldconfig
     ```

   + 安装miniupnpc

     ```shell
     wget http://miniupnp.tuxfamily.org/files/miniupnpc-2.0.tar.gz
     tar -xzvf miniupnpc-2.0.tar.gz
     cd miniupnpc-2.0
     make -j4
     sudo INSTALLPREFIX=/usr/local make install && sudo ldconfig
     ```

3. 编译项目

   ```shell
   git clone https://github.com/mvs-org/metaverse.git
   cd metaverse && mkdir build && cd build
   cmake ..
   make -j4 # 内存不足可以make -j1
   sudo make install
   ```

4. 系统要求

   ```shell
   ubuntu18.04
   ```

   

