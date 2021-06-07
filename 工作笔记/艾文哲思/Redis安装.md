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
make PREFIX=/usr install   # 安装到指定目录,开发时直接能找到
ldconfig
ldconfig -v | grep hiredis # 不知道是否需要ldconfig,可以用此命令测试一下

# 如果第三方SDK 安装到/usr目录下依然找不到so(编译或者运行时),可以用命令
# ldconfig -v | grep hiredis 查看一下,或者试试 ldconfig 即可
```

