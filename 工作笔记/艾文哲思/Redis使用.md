# 关闭保护模式

```shell
> config set protected-mode "no"
```





# 设置密码

```shell
CONFIG SET requirepass ${passwd}

# 示例
CONFIG SET requirepass tars2015
```



# 配置文件

1. 关闭保护模式

   > + protected-mode yes改为protected-mode no
   > + 注释bind 127.0.0.1
   
2. 指定配置文件启动redis



# 连接服务器

```shell
redis-cli -h ${IP} -p ${PORT} -a ${PASSWD}

redis-cli -h 127.0.0.1 -p 6666 -a 123456
```





#  清空数据

