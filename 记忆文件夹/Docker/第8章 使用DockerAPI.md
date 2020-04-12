# 1 Docker API

+ Registry API：存储docker镜像
+ Docker Hub API：与docker Hub集成的功能
+ Docker Remote API：与docker守护进程集成的API，本章重点介绍





# 2 访问docker API

1. 修改配置文件`/usr/lib/systemd/system/docker.service`

   ```shell
   变量ExecStart增加选项-H tcp://0.0.0.0:2375
   ```

2. 重新加载和启动docker守护进程

   ```shell
   systemctl --system daemon-reload
   ```

3. 访问

   ```shell
   docker -H 127.0.0.1:2375 info
   ```



# 3 测试 API



## 3.1 管理docker镜像

1. 获取镜像列表

   ```shell
   curl http://127.0.0.1:2375/images/json | python3 -m json.tool
   ```

2. 查看docker信息

   ```shell
   curl http://127.0.0.1:2375/info | python3 -m json.tool
   ```

3. 查询指定镜像的信息

   ```shell
   curl http://127.0.0.1:2375/images/f1cb7c7d58b7/json | python3 -m json.tool
   ```

4. 在Docker Hub上面查找镜像

   ```shell
   curl http://127.0.0.1:2375/images/search?term=nginx | python3 -m json.tool
   ```



## 3.2 管理docker容器

1. 列出正在运行的容器

   ```shell
   curl http://127.0.0.1:2375/containers/json | python3 -m json.tool
   ```

2. 列出全部容器

   ```shell
   curl http://127.0.0.1:2375/containers/json?all=1 | python3 -m json.tool
   ```

3. 创建容器

   ```shell
   curl -X POST -H 'Content-Type:application/json' http://127.0.0.1:2375/containers/create -d '{ "Image":"centos:7.6.1810" }'
   ```

   分行的格式

   ```shell
   curl -X POST -H "Content-Type:application/json" \
   http://127.0.0.1:2375/containers/create \
   -d \
   " \
   { \
   \"Image\":\"centos:7.6.1810\" \
   }"
   ```

4. 启动容器

   ```shell
   curl -X POST -H "Content-Type:application/json" http://127.0.0.1:2375/containers/8a4a1fc441ae/start -d {}
   ```

5. 获取指定容器信息

   ```shell
   curl http://127.0.0.1:2375/containers/8a4a1fc441ae/json | python3 -m json.tool
   ```

   