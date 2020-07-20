# APScheduler

***



## 1 介绍

***

APScheduler 是一个轻量级的任务调度器



## 2 特性

***

+ 基于日期和时间的调度
+ 基于时间间隔的调度
+ Cron方式的调度



## 3 安装

***

```shell
pip install apscheduler
```





## 4 使用

***



### 4-1 基于日期时间调度

***

```python
from datetime import date
from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()

def my_job(text):
    print(text)

# 在2009年11月6日执行
sched.add_job(my_job, 'date', run_date=date(2009, 11, 6), args=['text'])

# 在2009年11月6日 16:30:05 执行
# sched.add_job(my_job, 'date', run_date=datetime(2009, 11, 6, 16, 30, 5), args=['text'])

# 用文本设定时间
# sched.add_job(my_job, 'date', run_date='2009-11-06 16:30:05', args=['text'])

sched.start()
```





### 4-2 基于时间间隔调度

***

1. 用`add_job`注册任务

   ```python
   from datetime import datetime
   from apscheduler.schedulers.blocking import BlockingScheduler
   
   def job_function():
       print("Hello World")
   
   sched = BlockingScheduler()
   
   # 每2小时触发
   sched.add_job(job_function, 'interval', hours=2)
   
   sched.start()
   ```

2. 用`装饰器`注册任务

   ```python
   from apscheduler.scheduler import BlockingScheduler
   
   
   @sched.scheduled_job('interval', id='my_job_id', hours=2)
   def job_function():
       print("Hello World")
   ```

   



### 4-3 Cron方式调度

***

1. 用`add_job`函数注册任务

   ```python
   from apscheduler.schedulers.blocking import BlockingScheduler
   
   def job_function():
       print "Hello World"
   
   sched = BlockingScheduler()
   
   # 任务会在6月、7月、8月、11月和12月的第三个周五，00:00、01:00、02:00和03:00触发
   sched.add_job(job_function, 'cron', month='6-8,11-12', day='3rd fri', hour='0-3')
   
   sched.start()
   ```

   

2. 用**装饰器**注册任务

   ```python
   @sched.scheduled_job('cron', id='my_job_id', day='last sun')
   def some_decorated_task():
       print("I am printed at 00:00:00 on the last Sunday of every month!")
   ```

3. 表达式类型

   | 表达式 | 参数类型 | 描述                                     |
   | ------ | -------- | ---------------------------------------- |
   | *      | 所有     | 通配符。例：`minutes=*`即每分钟触发      |
   | */a    | 所有     | 可被a整除的通配符。                      |
   | a-b    | 所有     | 范围a-b触发                              |
   | a-b/c  | 所有     | 范围a-b，且可被c整除时触发               |
   | xth y  | 日       | 第几个星期几触发。x为第几个，y为星期几   |
   | last x | 日       | 一个月中，最后个星期几触发               |
   | last   | 日       | 一个月最后一天触发                       |
   | x,y,z  | 所有     | 组合表达式，可以组合确定值或上方的表达式 |
   |        |          |                                          |



### 4-4 相关错误

***

+ maximum number of running instances reached (1)

  ```python
  
  # max_instances默认值为1，id相同的任务实例数默认最多一个
  sched.add_job(child_job, max_instances=10, trigger=DateTrigger(), id="123")
  ```

  





