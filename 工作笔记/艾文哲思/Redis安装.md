# 安装Redis服务器



## 安装

```shell
docker pull redis:6.2.3

docker run -d -p 6379:6379 redis:6.2.3
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
make PREFIX=/usr install  # 安装到指定目录
ldconfig
```

