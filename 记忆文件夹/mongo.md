# 第一张  安装

参考官网：https://mongodb.net.cn/manual/tutorial/install-mongodb-on-red-hat/



1. 创建仓库文件/etc/yum.repos.d/mongodb-org-4.2.repo

   ```ini
   [mongodb-org-4.2]
   name=MongoDB Repository
   baseurl=https://repo.mongodb.org/yum/redhat/$releasever/mongodb-org/4.2/x86_64/
   gpgcheck=1
   enabled=1
   gpgkey=https://www.mongodb.org/static/pgp/server-4.2.asc
   ```

2. 更新缓存

   ```shell
   yum makecache
   ```

3. 安装软件包

   ```shell
   sudo yum install -y mongodb-org
   
   # /var/lib/mongo （数据目录）
   # /var/log/mongodb （日志目录）
   ```

4. 启动服务

   ```shell
   sudo systemctl start mongod
   ```

5. 使用命令行客户端连接mongod

   ```ini
   mongo
   ```



# 第二章 数据库操作



## 2.1 创建数据库

1. 查看全部数据库

   ```ini
   show dbs
   ```

2. 切换到指定数据库

   ```ini
   ; 如果数据库不存在则创建
   use ${db_name}
   ```

3. 查看当前使用的数据库

   ```ini
   db
   ```



## 2.2 删除数据库

```ini
db.dropDatabase()
```





## 2.3 集合

1. 创建集合

   ```ini
   db.createCollection("runoob")
   ```

2. 查看已有集合

   ```ini
   show collections
   ; 或者
   show tables
   ```

3. 删除集合

   ```ini
   ; mycol2 是集合名
   db.mycol2.drop()
   ```



## 2.4 文档

1. 插入文档

   ```ini
   ; 插入一条文档,collection是集合名称
   db.collection.insertOne({"a": 3})
   
   ; 插入文档,自己指定_id,如果已经存在该_id会导致插入失败,游戏开发可以用uid作为_id
   ; _id是唯一索引
   db.runoob.insertOne({"_id":1, "name": "大刀王五", "age":91230, "height":178})
   
   ; 插入多条文档
   db.collection.insertMany([{"b": 3}, {'c': 4}])
   ```

2. 更新文档

   ```ini
   ; 更新第一条符合条件的文档
   db.col.update({'title':'MongoDB 教程'},{$set:{'title':'MongoDB'}})
   
   ; 更新全部符合条件的文档
   db.col.update({'title':'MongoDB 教程'},{$set:{'title':'MongoDB'}},{multi:true})
   
   
   ; 通过传入的文档来替换已有文档，_id 主键存在就更新，不存在就插入
   db.col.save({
       "_id" : ObjectId("56064f89ade2f21f36b03136"),
       "title" : "MongoDB",
       "description" : "MongoDB 是一个 Nosql 数据库",
       "by" : "Runoob",
       "url" : "http://www.runoob.com",
       "tags" : [
               "mongodb",
               "NoSQL"
       ],
       "likes" : 110
   })
   ```

3. 删除文档

   ```ini
   ; 删除全部
   db.col.remove({})
   db.col.find()
   
   ; 删除满足指定条件的全部文档
   db.col.remove({'title':'MongoDB 教程'})
   
   ; 删除满足指定条件的第一条文档, 未测试
   db.col.remove({'title':'MongoDB 教程'}, {justOne:true})
   ```

4. 查询文档

   ```ini
   ; 查询全部
   db.collection.find()
   
   ; and 条件
   db.collection.find({k1:v1, k2:v2})
   
   ; or 条件
   db.col.find(
      {
         $or: [
            {key1: value1}, {key2:value2}
         ]
      }
   ).pretty()
   ```

5. 分页

   ```ini
   ; 查询前两条
   db.col.find({},{"title":1,_id:0}).limit(2)
   
   ; 跳过指定数量的记录
   db.col.find({},{"title":1,_id:0}).limit(1).skip(1)
   ```

6. 排序

   ```ini
   ; 1是升序 -1是降序
   db.COLLECTION_NAME.find().sort({KEY:1})
   ```

7. 索引

   ```ini
   ; 创建索引
   db.collection.createIndex(keys, options)
   
   ; title是索引,1指定为升序
   db.col.createIndex({"title":1})
   
   ; 创建联合索引
   db.col.createIndex({"title":1,"description":-1})
   
   ; 后台创建索引
   db.values.createIndex({open: 1, close: 1}, {background: true})
   
   db.collection.createIndex({"title":1}, { unique: true } )
   ```

8. 连接数查看

   ```ini
   db.serverStatus().connections
   ```

   
