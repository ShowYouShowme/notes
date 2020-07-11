任务

1. ~~最近7天的新增代币种类（get_tokens_statistics, websocket采集后保存数据库,）~~
2. ~~投票选举统计数据的采集和展示（get_elections，get_elections_supernode 保存数据库）~~
3. ~~账户用户余额降序（get_accounts定时采集区块链账户余额，或者看看elashsearch的功能是否满足）~~
4. 新的区块链起来后，查看写死的重要参数数据并从区块链取数据（比如stacknum）



新增加的任务

1 假数据

2 election接口采集和数据库存储

 https://www.showdoc.cc/baidang201?page_id=4239891060237794

https://www.showdoc.cc/baidang201?page_id=4170153253544588

3 tx详情显示的格式和页面同步，和李赫尧确定tx详情常见交易类型的显示 https://www.showdoc.cc/baidang201?page_id=4167634911838428

4 修改节点接口post node的签名验证功能  https://www.showdoc.cc/baidang201?page_id=4276835692704259



## 自己的任务

1. ~~复习w3c的flask文章~~

2. 跟着视频学完es

3. 跟着视频学完flask

4. 学习flask计时器的使用

5. 看完sqlite的书

6. 整理python的List的相关操作,如何对dict排序，如何像c++一样传入自定义的比较函数

7. 学习常用的消息队列

   ```shell
   1. kafka
   2. rabbitmq
   3. redis发布订阅
   4. zeromq
   ```

8. ~~Python值类型和引用类型的整理~~

9. 虚拟机里面部署python的服务，优化一下代码

10. 压力测试transfer的接口

11. 本地搭建dna的私有链

12. ~~用c++嵌入lua的方式，重写邮件之类的服务看看效果~~；再用nodejs实现对比一下

13. ~~用apache 和nginx 分别部署flask服务~~


14. 看区块链的业务知识 3-4章[这是重点]
15. 学习第4章，mysql数据库的管理
16. 学习使用solidity来进行区块链的开发，先熟悉整个开发的流程
17. 把网关 + 登录服务的思路记录下来
18. 熟悉dna-user-register-tapin的代码
19. redis和mysql的数据一致性如何保证
20. 配置centos的路由表，学习用traceroute 命令跟踪路由（-n 参数）；如何让局域网的数据包必须通过网关，而不是直接转发
21. ~~设置swap的大小，增加编译速度~~
22. 阅读一章的区块链的文章
23. 制作bitshare的docker镜像，学习多节点的部署方案
24. ~~装samba 实现文件夹共享~~
25. 配置服务器监控工具，在后台绘制曲线
26. 学习使用zeromq的方式来编写c++的多线程的代码，废弃共享状态的方式(锁，条件变量)
27. 购买<<许式伟的架构课>> ---> 用go语言开发替代c/c++(编译慢，出错难以排查)
28. 复习vue，做好详细的笔记。有时间可以看看视频学习一下，补充一下css相关的知识。




## 今日任务

***

3. 看es的视频5-10个

4. 看flask的视频5-10个

5. 看完zeromq的[guide](http://zguide.zeromq.org/page:all)，用python写一些简单的demo

6. python简单实用zookeeper

7. 测试

   ```shell
   1. 同一个进程内函数调用的时间
   2. 不同进程rpc调用的时间[本机和局域网其它机器]
   3. tcp建立连接消耗的时间
   ```

8. [高并发系统设计的40问](https://time.geekbang.org/column/intro/230)

9. ~~收集统计数据的借口要返回值，方便调试~~

10. python 定时器的使用

11. ~~python 用ws访问bitshare的api,自己去实现模块~~

12. 熟悉pycharm的各种操作命令，能大幅度提高开发效率





## python接口任务

***

+ 收集日志的接口要重新整理，有些可以将两个合并为一个

+ 自己利用python的计时器框架来定时采集任务，方便部署（不需要部署到crontab里面）

+ 处理完全部待确认的问题

+ 部署新的机器

+ 买蟑螂药到公司

+ 日志全部打印到log文件里面，而不是控制台

+ 利用dockerfile 制作docker镜像

+ 交易大小的计算

+ 使用swag自己搭建python的flask框架

+ 收集数据的几个表都增加字段，记录插入的时间；整理全部收集数据的表和代码逻辑

+ 实现收集选举数据的接口，增加crontab 的任务来收集数据，完善选举的功能

+ 指定用户的选举情况拆分为另外一个接口

+ 学习openresty开发tcp的网关，比如实现游戏的网关[哈哈哈]

+ 学习SQLAlchemy的使用方式

+ Election 表的round是唯一索引

+ 脚本一 ： 获取已经完成的全部选举的数据，写入数据库

+ 脚本二 ： 定时(每5分钟获取一次选举的数据，如果记录已经存在则更新)

+ 上线时要将选举的周期改为16天，在config.py里面的VOTING_CYCLE

+ 交易的分类是有问题的

+ 定时写入交易的脚本非常慢，需要修改

+ 整理几个影响性能的sql语句，要不然服务器实在是太慢了

+ ~~tokeninfos 的数据进行缓存~~

+ ~~tokeninfos 报错~~

  ```
  {
    "result": {},
    "status": {
      "error_msg": "unsupported operand type(s) for +=: 'int' and 'str'",
      "success": -1
    }
  }
  ```

+ 区块接口加hash，查看聊天记录

+ /api/v1/block/xxxx

  

  现在支持区块高度查询，需要增加支持区块hash查询区块。

  

  判断xxxx是数值就作为高度查询，不是数值就作为hash查询，查询不到就返回空。







+ 学习flask的缓存插件flask_caching 的使用方式
+ 查看日志文件又没有写入
+ 所有的异常信息更改为： 文明名 + 行数 + 错误详情；方便后端定位问题  ---> 这个是重点
+ Insert_time 每次修改记录后会自己更新吗
+ 根据账户名筛选election的接口没有实现
+ 函数_get_error_json 应该传入exception对象，然后在里面可以显示行数之类的具体信息
+ python 循环引用的处理，只导入指定符号，而不是导入整个模块？？
+ 学习sqlalchemy的使用，参考网页https://www.cnblogs.com/wangtaobiu/p/11007547.html
+ ~~脚本计算当前是第几轮，然后将当前轮的数据写入mysql里面~~
+ ~~插入选举记录，存在更新不是删除再插入~~
+ 选举的接口增加账户过滤的功能





# 2020-07-11

***

+ 处理sql注入的问题 --> 未发现问题
+ ~~实现收集选举信息的定时任务~~
+ ~~处理未解决的bug。  -----> 这个是重点~~
+ 整理python可能出异常的地方，以后写代码尽量不让其抛出异常
+ 收集交易的sql卡顿，优化提升其性能
+ sql用execute 来拼接，不要自己拼接sql语句，可能造成sql注入。----> 这个是重点
+ 注意部署是需要修改的配置参数
+ Swag 可选参数的使用
+ ~~写crontab计时任务收集选举情况~~
+ 学习dstat的使用
+ 自己测试区块浏览器的使用，看看是否有致命bug【区块浏览器的url 是多少了呢】
+ 学习域名的申请，ssl的部署，nginx部署网站。整套流程都需要理解
+ 部署正式环境时，隐藏测试接口
+ 处理代码中的todo --->重点
+ 将各种统计数据进行缓存





# 待确认问题

***

```python
[5, 10, 13, 14, 15,16]
```





