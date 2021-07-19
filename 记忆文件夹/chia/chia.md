# 第一章 安装



## 1.1 Centos

```shell
sudo yum install epel-release -y
sudo yum update -y

# Compiling python 3.7 is generally required on CentOS 7.7 and newer
sudo yum install gcc openssl-devel bzip2-devel zlib-devel libffi libffi-devel -y
sudo yum install libsqlite3x-devel -y
# possible that on some RHEL based you also need to install
sudo yum groupinstall "Development Tools" -y
sudo yum install python3-devel gmp-devel  boost-devel libsodium-devel -y

sudo yum install wget -y
sudo wget https://www.python.org/ftp/python/3.7.7/Python-3.7.7.tgz
sudo tar -zxvf Python-3.7.7.tgz ; cd Python-3.7.7
./configure --enable-optimizations; sudo make -j$(nproc) altinstall; cd ..

# Download and install the source version
git clone https://github.com/Chia-Network/chia-blockchain.git -b latest
cd chia-blockchain

sh install.sh
. ./activate
```





## 1.2 Ubuntu

```shell
# Ubuntu 18.04 LTS 增加以下命令
sudo apt-get install python3.7-venv python3.7-distutils python3.7-dev git lsb-release -y

# Ubuntu 20.04 LTS
sudo apt-get update
sudo apt-get upgrade -y

# Install Git
sudo apt install git -y

# Checkout the source and install
git clone https://github.com/Chia-Network/chia-blockchain.git -b latest --recurse-submodules
cd chia-blockchain

sh install.sh

. ./activate
```





# 第二章 常用命令



## 2.1 查看帮助

```shell
chia --help
```



## 2.2 命令一览

```shell
  configure   Modify configuration
  farm        Manage your farm
  init        Create or migrate the configuration
  keys        Manage your keys
  netspace    Estimate total farmed space on the network
  plots       Manage your plots
  run_daemon  Runs chia daemon
  show        Show node information
  start       Start service groups
  stop        Stop services
  version     Show chia version
  wallet      Manage your wallet
```



## 2.3 停止运行

```shell
chia stop -d all
deactivate
```





## 2.4 初始化

1. 命令

   ```shell
   chia init
   ```

2. 作用

   > 检查~/.chia目录里是否安装旧版本的chia，如果有，将这些旧文件迁移到新版本

   

## 2.5 开启服务

```shell
chia start ${service}

chia start node # 启动全节点

chia start farmer
```



## 2.6 P盘

1. 命令

   ```shell
   chia plots create
   ```

2. 参数

   ```shell
   -k [size]。定义绘图的大小。不同系统上的k大小和创建时间列表请查看：k大小对应的P盘文件规格
   
   -n [绘图数量]。按顺序进行的绘图数量。一旦一个绘图完成，它将被移动到最终位置-d，然后再开始下一个绘图序列。
   
   -b [内存缓冲区大小MiB]。定义内存/RAM使用量。默认值是2048 (2GiB)。更多的内存将略微提高绘图的速度。请记住，这只是分配给绘图算法的内存。运行钱包等将需要你的系统提供额外的内存。
   
   -f [farmer 公钥]: 这是你的 "农民公钥". 当你想在其他机器上创建P盘文件时，如果你不想给chia账户完整的访问权限，就可以使用这个密钥。要找到你的 Chia 农民公钥，请使用以下命令： chia keys show
   
   -p [pool 公钥]。这是你的 "池公钥". 当你想在其他机器上创建P盘文件时，如果你不想给chia账户完整的访问权限时，就可以使用它。要找到你的 Chia Pool 公钥，请使用下面的命令： chia keys show
   
   -a [fingerprint]。这是用来选择农夫公钥和池子公钥的指纹。当你想从钥匙链中的多个钥匙中选择一个时，请使用这个命令。要找到你的 Chia 密钥指纹，请使用以下命令： chia keys show
   
   -t [tmp dir]。定义P盘时的临时目录。这里是P盘的第一阶段和第二阶段需要使用。-t 路径需要最大的工作空间：通常是最终plot文件大小的 4 倍左右。
   
   -2 [tmp dir 2]: 定义一个次要的临时目录，用于存放P盘临时文件。这是绘图阶段3（压缩）和阶段4（检查）发生的地方。根据您的操作系统，-2可能默认为-t或-d的相同路径。因此，如果-t或-d的空间不足，建议手动设置-2。-2 路径需要的工作空间与绘图的最终大小相等。
   
   -d [final dir]: 定义存储plot文件的最终位置。当然，-d 应该有足够的可用空间作为Plot文件的最终大小。这个目录会自动添加到 ~/.chia/VERSION/config/config.yaml 文件中。你可以使用 chia plots remove -d 从配置中删除一个最终目录。
   
   -r [线程数]: 2线程通常是最佳的。多线程目前只在P盘第一阶段使用。
   
   -u [buckets数量]。更多的数据包可以减少对内存的需求，但需要更多的随机磁盘搜索。对于机械磁盘，你需要设置更少的buckets，而对于NVMe固态硬盘，你可以设置更多的buckets。一般来说，你可以设置32、64或128（默认）
   
   -s [stripe size]。这是在第一阶段进行并行工作负载时，交给每个线程的数据量。默认的64K似乎是整体的最佳选择。32K往往是小损失，128K也是小损失。
   
   -e [bitfield plotting]。使用-e标志将禁用bitfield P盘算法，并恢复到旧的b17的P盘格式。它降低了对内存的要求，但在P盘时时也会多写12%的数据。它通常被认为是一个更快的选项，适用于更快的驱动器，如SSD。
   ```



## 2.7 校验

```shell
chia plots check -n [num checks] -l -g [substring] 
```



## 2.8 查看公私钥

```shell
chia keys show #只显示公钥

chia keys show --show-mnemonic-seed #连助记词一起显示
```



## 2.9 日志

***

1. 日志路径

   ```shell
   /home/nash/.chia/mainnet/log
   ```

   



# 第三章 chia-plotter



## 3.1 安装

***

```shell
#Ubuntu 20.04
sudo apt install -y libsodium-dev cmake g++ git build-essential
#Checkout the source and install
git clone https://github.com/madMAx43v3r/chia-plotter.git 
cd chia-plotter

git submodule update --init
./make_devel.sh
./build/chia_plot --help
```



## 3.2 P图

***

```shell
# P图命令
./chia_plot \
-n -1 \
-r {CPU核数} \
-u 7 \
-t {SSD缓存目录} \
-2 {SSD缓存或内存盘目录} \
-d {Plot文件存放位置} \
-p {矿池公钥} \
-f {农夫公钥}
```

```shell
# 示例
/home/slzg/chia-plotter/build/chia_plot -n -1 -r 8 -u 128 -b 30000 \ 
-t /home/slzg/ssd/tmp/ \
-d /home/slzg/ssd/plot/ \
-p b4c4e0364464a06a78579ad14ea3bab207671f5ba491fd83b2b136cf82677820b9b37515c68b140c72c94a46f6c679c1 \
-f b7a5f31efd753681c5866969400a9806173c7ef2c04406086b00b3c2c0fe8cf00dea8677bc2e30c578ca963f6705350b
```





# 第四章 多节点部署



## 4.1  复制证书文件

***

```shell
cd ~/.chia/mainnet/config/ssl
tar -zcvf ca.tar.gz ./ca/*
scp ./ca.tar.gz slzg@192.168.0.10:/home/slzg
```



## 4.2 修改全节点的日志等级

***

```shell
#~/.chia/mainnet/config/config.yaml
log_level: INFO

#或者执行命令
chia configure --log-level DEBUG

#重启服务
chia start -r farmer
```



## 4.3 启动全节点

***

```shell
chia start farmer

#查看日志,观察收割机是否已经连上
tail -f debug.log | grep 192.168.0.10

#断开收割机后收到看到如下日志
2021-07-16T18:39:49.089 farmer farmer_server              : INFO     Connection closed: 192.168.0.10, node id: 303c69afc4521dbef380bb2eba2efbc53005e46d6a883b7edf36973ef6d8641e
2021-07-16T18:39:49.090 farmer chia.farmer.farmer         : INFO     peer disconnected {'host': '192.168.0.10', 'port': 8448}

#或者用如下命令
chia farm summary
```



## 4.4  初始化收割机

***

```shell
chia init -c  ~/ca
```



## 4.5 设置farmer的地址

```shell
harvester:
  chia_ssl_ca:
    crt: config/ssl/ca/chia_ca.crt
    key: config/ssl/ca/chia_ca.key
  farmer_peer:
    host: Main.Machine.IP#修改这里
    port: 8447
```



## 4.6 启动收割机

```shell
chia start harvester
```



