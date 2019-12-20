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





## 数据库基本概念

| SQL术语     | MongoDB术语 | 说明                                 |
| ----------- | ----------- | ------------------------------------ |
| database    | database    | 数据库                               |
| table       | collection  | 表/集合                              |
| row         | document    | 行/文档                              |
| column      | field       | 字段/域                              |
| index       | index       | 索引                                 |
| table joins |             | 表连接，mongoDB不支持                |
| primary key | primary key | 主键，MongoDB自动将_id字段设置为主键 |



## 数据类型

| 数据类型           | 描述                                                         |
| ------------------ | ------------------------------------------------------------ |
| String             | 字符串                                                       |
| Integer            | 整型数值                                                     |
| Boolean            | 布尔值                                                       |
| Double             | 双精度浮点数                                                 |
| Min/Max keys       | 将一个值与BSON元素的最低值和最高值相对比。                   |
| Array              | 数组                                                         |
| Timestamp          | 时间戳                                                       |
| Object             | 用于内嵌文档                                                 |
| Null               | 用于创建空值                                                 |
| Symbol             | 符号。基本等同于字符串，用于采用特殊符号类型的语言。[基本不使用] |
| Date               | 日期时间                                                     |
| Object ID          | 对象ID。用于创建文档的ID                                     |
| Binary Data        | 二进制数据。用于存储二进制数据。                             |
| Code               | 代码类型。用于存储JavaScript代码。                           |
| Regular Expression | 正则表达式类型。用于存储正则表达式。                         |



## Robo 3T的使用

> ### 图形化操作
>
> ***
>
> + 创建db
>
>   > 操作步骤
>   >
>   > ```shell
>   > 选中连接-->右键选择Create Database
>   > ```
>   >
>   > Collections：表结构
>   >
>   > Users：用户权限
>
> + 创建表
>
>   ```shell
>   选中Collections-->右键选择Create Collection
>   ```
>
> + 表的操作菜单
>
>   > 1. 查看：view Doc
>   >
>   >    > + 树模式
>   >    > + 表模式
>   >
>   > 2. 插入：insert Doc
>   >
>   > 3. 更改：update Doc
>   >
>   > 4. 删除：Remove Doc
>   >
>   > 5. 删除全部：Remove All Doc
>
> + 执行命令
>
>   > 1. 选中数据库
>   > 2. 右键 open shell
>   > 3. 输入命令后
>   > 4. 点击工具栏的三角符号执行命令





## Node.js操作MongoDB

### 驱动安装

***

```shell
npm install mongodb --save

npm install @types/mongodb
```





### 创建数据库和表

***

```javascript
import Mongodb = require("mongodb");
import {MongoClient, MongoError} from "mongodb";

let url = "mongodb://localhost:27017/testdb";

// 连接数据库,不存在则创建
Mongodb.MongoClient.connect(url, (err : MongoError, db : MongoClient):void=>{
    if (err) throw err;
    console.log("数据库已创建!");

    let dbase = db.db("testdb");
    dbase.createCollection('user',(error: MongoError, result: Mongodb.Collection<any>):void=>{
        if (err) throw err;
        console.log("创建集合!");
        db.close();
    })
});
```



### 插入数据

***

> + 插入一条数据
>
>   ```javascript
>   import Mongodb = require("mongodb");
>   import {MongoClient, MongoError} from "mongodb";
>   
>   let url = "mongodb://localhost:27017/testdb";
>   
>   // 连接数据库,不存在则创建
>   Mongodb.MongoClient.connect(url, (err : MongoError, db : MongoClient):void=>{
>       if (err) throw err;
>   
>       let dbase = db.db("testdb");
>   
>       let myInfo  = {name : "Tom", age : "18"};
>       dbase.collection("user").insertOne(myInfo, (err, res):void=>{
>           if (err) throw err;
>           console.log("文档插入成功!");
>           db.close();
>       })
>   });
>   ```
>
> + 插入多条记录
>
>   ```javascript
>   import Mongodb = require("mongodb");
>   import {MongoClient, MongoError} from "mongodb";
>   
>   let url = "mongodb://localhost:27017/testdb";
>   
>   // 连接数据库,不存在则创建
>   Mongodb.MongoClient.connect(url, (err : MongoError, db : MongoClient):void=>{
>       if (err) throw err;
>   
>       let dbase = db.db("testdb");
>   
>       let myInfo  = [
>           {name:"jim", age:18},
>           {name:"lilei", age:26},
>           {name:'lucy', age:16}
>       ]
>       dbase.collection("user").insertMany(myInfo, (err, res):void=>{
>           if (err) throw err;
>           console.log("插入的文档数量为:" + res.insertedCount);
>           db.close();
>       })
>   });
>   
>   ```
>
>   