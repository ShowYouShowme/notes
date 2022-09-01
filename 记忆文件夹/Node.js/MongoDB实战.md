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

官方安装文档：https://mongodb.net.cn/manual/tutorial/install-mongodb-on-red-hat/

### centos7

***

1. 创建repo文件

   ```shell
   vim /etc/yum.repos.d/mongodb-org-4.0.repo
   
   [mongodb-org-4.0]
   name=MongoDB Repository
   baseurl=https://repo.mongodb.org/yum/redhat/$releasever/mongodb-org/4.0/x86_64/
   gpgcheck=1
   enabled=1
   gpgkey=https://www.mongodb.org/static/pgp/server-4.0.asc
   ```

2. 安装

   ```shell
   yum install -y mongodb-org
   ```

3. 修改配置文件

   ```shell
   vim /etc/mongod.conf
   ```

   ```shell
   # mongod.conf
   
   # for documentation of all options, see:
   #   http://docs.mongodb.org/manual/reference/configuration-options/
   
   # where to write logging data.
   systemLog:
     destination: file
     logAppend: true
     path: /var/log/mongodb/mongod.log
   
   # Where and how to store data.
   storage:
     dbPath: /var/lib/mongo
     journal:
       enabled: true
   #  engine:
   #  wiredTiger:
   
   # how the process runs
   processManagement:
     fork: true  # fork and run in background
     pidFilePath: /var/run/mongodb/mongod.pid  # location of pidfile
     timeZoneInfo: /usr/share/zoneinfo
   
   # network interfaces
   net:
     port: 27017
   # 修改为0.0.0.0 否则远程无法连接
     bindIp: 0.0.0.0  # Enter 0.0.0.0,:: to bind to all IPv4 and IPv6 addresses or, alternatively, use the net.bindIpAll setting.
   
   # 配置为启用认证（创建账号/密码用户登录）
   security:
     authorization: enabled
   
   #operationProfiling:
   
   #replication:
   
   #sharding:
   
   ## Enterprise-Only Options
   
   #auditLog:
   
   #snmp:
   ```

4. 开启服务

   ```shell
   systemctl enable mongod
   systemctl start mongod
   ```

5. 客户端

   ```shell
   mongo --host 127.0.0.1:27017
   
   # 或者
   mongo --port 27017 -u "adminUser" -p "adminPass" --authenticationDatabase "admin"
   ```

   

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





### 查询数据

+ 查询表里的全部记录

  ```javascript
  import Mongodb = require("mongodb");
  import {MongoClient, MongoError} from "mongodb";
  
  let url = "mongodb://localhost:27017/testdb";
  
  // 连接数据库
  Mongodb.MongoClient.connect(url, (err : MongoError, db : MongoClient):void=>{
      if (err) throw err;
  
      let dbase = db.db("testdb");
  
      dbase.collection("user").find({}).toArray((error: MongoError, result: any[]): void=>{
          if (error) throw err;
  
          console.log(result);
          db.close();
      })
  });
  ```

+ 指定条件查询

  ```javascript
  import Mongodb = require("mongodb");
  import {MongoClient, MongoError} from "mongodb";
  
  let url = "mongodb://localhost:27017/testdb";
  
  Mongodb.MongoClient.connect(url, (err : MongoError, db : MongoClient):void=>{
      if (err) throw err;
  
      let dbase = db.db("testdb");
  
  	// 指定查询条件
      dbase.collection("user").find({name:'Tom'}).toArray((error: MongoError, result: any[]): void=>{
          if (error) throw err;
  
          console.log(result);
          db.close();
      })
  });
  ```

  ```javascript
  import Mongodb = require("mongodb");
  import {MongoClient, MongoError} from "mongodb";
  
  let url = "mongodb://localhost:27017/testdb";
  
  
  Mongodb.MongoClient.connect(url, (err : MongoError, db : MongoClient):void=>{
      if (err) throw err;
  
      let dbase = db.db("testdb");
  
  	// 查询条件
      let condition = {name : 'lucy'};
      dbase.collection("user").find(condition).toArray((error: MongoError, result: any[]): void=>{
          if (error) throw err;
  
          console.log(result);
          db.close();
      })
  });
  
  ```

+ 多表查询

  ```javascript
  import Mongodb = require("mongodb");
  import {MongoClient, MongoError} from "mongodb";
  
  let url = "mongodb://localhost:27017/testdb";
  
  
  Mongodb.MongoClient.connect(url, (err : MongoError, db : MongoClient):void=>{
      if (err) throw err;
  
      let dbo = db.db("testdb");
  
      dbo.collection('user').aggregate(
          [
              {
                  $lookup:
                      {
                          from:'job',         // 右集合
                          localField:'job_id', // 左集合字段
                          foreignField:"_id",  // 右集合字段
                          as:"user_list"
                      }
              }
          ]
      ).toArray((err, res: any[]):void=>{
          if (err) throw err;
          res.forEach((elem)=>{
              console.log(elem);
          })
          db.close();
      })
  });
  ```

  





### 更新数据

+ 更新单条记录

  ```javascript
  import Mongodb = require("mongodb");
  import {MongoClient, MongoError} from "mongodb";
  
  let url = "mongodb://localhost:27017/testdb";
  
  
  Mongodb.MongoClient.connect(url, (err : MongoError, db : MongoClient):void=>{
      if (err) throw err;
  
      let dbo = db.db("testdb");
  
      let condition = {name:"lucy"};
  
      let updateStatement = {$set:{age:26}};
  
      dbo.collection('user').updateOne(condition, updateStatement,(err, res):void=>{
          if (err) throw err;
  
          console.log("文档更新成功!");
          db.close();
      })
  });
  
  ```

+ 更新多条记录

  ```javascript
  import Mongodb = require("mongodb");
  import {MongoClient, MongoError} from "mongodb";
  
  let url = "mongodb://localhost:27017/testdb";
  
  
  Mongodb.MongoClient.connect(url, (err : MongoError, db : MongoClient):void=>{
      if (err) throw err;
  
      let dbo = db.db("testdb");
  
      let condition = {age:18};
  
      let updateStatement = {$set:{job_id:24}};
  
      dbo.collection('user').updateMany(condition, updateStatement,(err, res):void=>{
          if (err) throw err;
  
          console.log(res.result.nModified + " 条文档被更新!");
          db.close();
      })
  });
  ```

### 删除数据

+ 删除一条数据

  ```javascript
  import Mongodb = require("mongodb");
  import {MongoClient, MongoError} from "mongodb";
  
  let url = "mongodb://localhost:27017/testdb";
  
  Mongodb.MongoClient.connect(url, (err : MongoError, db : MongoClient):void=>{
      if (err) throw err;
  
      let dbase = db.db("testdb");
  
      let condition = {name : "Tom"};
  
      dbase.collection("user").deleteOne(condition,(err, res):void=>{
          if (err) throw err;
  
          console.log("文档删除成功!");
          db.close();
      })
  });
  ```

+ 删除多条数据

  ```javascript
  import Mongodb = require("mongodb");
  import {MongoClient, MongoError} from "mongodb";
  
  let url = "mongodb://localhost:27017/testdb";
  
  Mongodb.MongoClient.connect(url, (err : MongoError, db : MongoClient):void=>{
      if (err) throw err;
  
      let dbase = db.db("testdb");
  
      let condition = {age : 26};
  
      dbase.collection("user").deleteMany(condition,(err, res):void=>{
          if (err) throw err;
  
          console.log(res.result.n + " 条记录被删除!");
          db.close();
      })
  });
  ```

  

+ 删除文档

  ```javascript
  import Mongodb = require("mongodb");
  import {MongoClient, MongoError} from "mongodb";
  
  let url = "mongodb://localhost:27017/testdb";
  
  Mongodb.MongoClient.connect(url, (err : MongoError, db : MongoClient):void=>{
      if (err) throw err;
  
      let dbase = db.db("testdb");
  
      dbase.collection("user").drop((err, delOK)=>{
          if (err) throw err;
          if(delOK) {
              console.log("集合已删除!");
          }
          db.close();
      })
  });
  ```

  