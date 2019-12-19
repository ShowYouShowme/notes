## 什么是MongoDB

> MongoDB将数据存储为文档，数据结构有键值对组成。MongoDB文档类似于JSON对象。字段值可以包含其他文档，数组和文档数组。
>
> ```json
> {
>     name : "sue",
>     age: 26,
>     status: "A",
>     groups: ["news", "sports"]
> }
> ```



## MongonDB的特点

> + Map和Reduce：用于遍历集合中的所有记录
> + GridFS：用于存放大量小文件
> + 允许在服务端执行脚本，类似redis可以直接执行lua



## 安装

> + [MongoDB下载地址](https://www.mongodb.com/)
> + [Robo下载地址](https://robomongo.org/)



## 启动

> 1. 设置环境变量
>
> 2. 创建存储数据的文件夹
>
>    ```shell
>    mkdir mdb
>    ```
>
> 3. 启动mongonDB
>
>    ```shell
>    mongod --dbpath D:\MyCode\mdb
>    ```