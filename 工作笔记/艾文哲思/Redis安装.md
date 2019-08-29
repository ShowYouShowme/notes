# 安装Redis服务器

## 下载文件

```shell
wget https://github.com/antirez/redis/archive/4.0.8.tar.gz
```

## 安装

```shell
tar -zxvf 4.0.8.tar.gz
yum install -y tcl 
cd ./redis-4.0.8/
# 编译
make -j4
# 测试
make test -j4

# 安装
mkdir redis-4.0.8
ln -s /usr/local/redis-4.0.8/ /usr/local/redis
make install PREFIX=/usr/local/redis 

# 配置环境变量
echo "PATH=\$PATH:/usr/local/redis/bin" >> /etc/profile
echo "export PATH" >> /etc/profile
source /etc/profile
```



# 安装C++开发库

## 下载文件

```shell
wget https://github.com/redis/hiredis/archive/v0.14.0.tar.gz
```

## 安装

```shell
tar -zxvf v0.14.0.tar.gz
cd ./hiredis-0.14.0/
make -j4
make install
ldconfig /usr/local/lib
```

