# 超时设置

***
1. 超时种类

   + 连接超时
   + 查询超时(类似requests的读取超时)

2. 导致超时的API

   + pymysql.connect：可能会连接超时，`connect_timeout`设置
   + 查询超时：`read_timeout`就是设置下面三个API的
     + cursor.execute()
     + conn.commit()
     + conn.rollback()

3. 例子

   ```python
   import pymysql
   
   
   
   def main():
       # 连接超时时间为connect_timeout
       conn = pymysql.connect(host='10.10.10.89', port=3306, user='root',
                              password='tars2015', database='test',
                              connect_timeout = 5,
                              read_timeout = 2) # 读取超时[cursor.execute(), conn.commit(),conn.rollback() ]
       cursor = conn.cursor() # 本地
       try:
           for i in range(666, 766):
               sql: str = 'INSERT INTO tb_money(`money`) VALUE({})'.format(i)
               cursor.execute(sql) # 需要网络,超时时间为read_timeout
               if i == 670:
                   raise NameError('error at index 670')
           conn.commit() # 提交事务, 需要网络,超时时间为read_timeout
           results = cursor.fetchall() # 本地
           conn.close() # 本地
           return results
       except Exception as e:
           conn.rollback() # 事务回滚,需要网络,超时事件为read_timeout
           print(e)
           conn.close()
           raise e
       print('finished')
   
   if __name__ == '__main__':
       main()
   ```

   



# 事务处理

***

1. 每次执行一条sql语句

   ```python
   # 每次插入一条记录 t2 - t1 : 10.614759922027588
   import pymysql
   import time
   
   
   def main():
       # 连接超时时间为connect_timeout
       conn = pymysql.connect(host='10.10.10.89', port=3306, user='root',
                              password='tars2015', database='test',
                              connect_timeout = 5,
                              read_timeout = 2)
       cursor = conn.cursor()
       try:
           t1 = time.time()
           for i in range(1, 10000):
               sql: str = 'INSERT INTO tb_money(`money`) VALUE({})'.format(i)
               cursor.execute(sql)
           	   conn.commit() # 注意这里,每条sql语句提交一次
           results = cursor.fetchall()
           conn.close()
           t2 = time.time()
           print('t2 - t1 : {}'.format(t2 - t1))
           return results
       except Exception as e:
           conn.rollback()
           print(e)
           conn.close()
           raise e
       print('finished')
   
   if __name__ == '__main__':
       main()
   ```

   

2. 多条sql语句放到一个事务来执行

   ```python
   # 使用事务插入1w条记录 t2 - t1 : 2.9334681034088135
   import pymysql
   import time
   
   
   def main():
       # 连接超时时间为connect_timeout
       conn = pymysql.connect(host='10.10.10.89', port=3306, user='root',
                              password='tars2015', database='test',
                              connect_timeout = 5,
                              read_timeout = 2)
       cursor = conn.cursor()
       try:
           t1 = time.time()
           for i in range(1, 10000):
               sql: str = 'INSERT INTO tb_money(`money`) VALUE({})'.format(i)
               cursor.execute(sql)
           conn.commit() # 一次性提交
           results = cursor.fetchall()
           conn.close()
           t2 = time.time()
           print('t2 - t1 : {}'.format(t2 - t1))
           return results
       except Exception as e:
           conn.rollback()
           print(e)
           conn.close()
           raise e
       print('finished')
   
   if __name__ == '__main__':
       main()
   ```




# SQL 注入

```python
import pymysql

user = "helln' -- skdjfskdf"
pwd = "234"

# 1.连接
conn = pymysql.connect(host='192.168.0.2', port=3306, user='root', password='tars2015', db='slzg', charset='utf8')
# 2.创建游标
cursor = conn.cursor()
sql = "select * from userinfo where username=%s and password=%s"
print('sql语句:', sql)

result = cursor.execute(sql, [user, pwd])  # 处理SQL 注入的问题,SQL 不要直接用字符串拼接
print('返回记录数:', result)                # 增加、删除、修改的时候必须commit,否则不生效

# 关闭连接，游标和连接都要关闭
cursor.close()
conn.close()
if result:
    print('登陆成功')
else:
    print('登录失败')
```

