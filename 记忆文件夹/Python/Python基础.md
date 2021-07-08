# 第一章  Python介绍和安装

## 1.1 课程目录介绍

+ Python介绍与安装
+ 变量、数字、序列、映射和集合
+ 条件与循环
+ 文件、输入输出、异常
+ 函数、模块
+ 面向对象编程
+ 多线程编程
+ 标准库
+ 第三方库
+ 综合项目
## 1.2 介绍和安装

+ 语言特点
	1. 语法简洁
	2. 跨平台
	3. 类库丰富
	4. 开放源码
	5. 可扩展，可以调用C/C++的库
+ 发展历史与版本
	+ 发展历史 
		1. 1990年诞生
		2. 2000年Python2.0发布
		3. 2008年Python3.0发布
		4. 2010年Python2.7发布(最后一个2.x版本)
	+ 版本
		1. Python2.x
		2. Python3.x
			1. 官方版本
			2. 发行版本[Anaconda](https://www.anaconda.com/)
	+ 开发工具
		1. [Python官方文档](https://docs.python.org)
		2. [iPython](https://ipython.org/)
		3. jupyter notebook，可以在网页编程
		4. sublime text 文本编辑器
		5. Pycharm 集成开发环境
		6. Pip 包管理器
+ 安装
	1. 安装python
	
	   1. Ubuntu18.04编译安装python3.7
	
	      ```shell
	      # 0 安装依赖
	      apt-get install zlib1g-dev libffi-dev gcc make
	      
	      # 1 下载安装包
	      wget https://www.python.org/ftp/python/3.7.1/Python-3.7.1.tgz
	      
	      # 2 解压
	      tar -zxvf Python-3.7.1.tgz
	      
	      # 3 编译安装
	      cd Python-3.7.1
	      ./configure
	      make
	      make install
	      
	      ```
	
	      
	
	2. 安装pycharm 
	
	3. 在终端里启动>python
	
	4. 在终端里退出>>>exit()
	
+ 源码编译安装

  1. 下载源码

     ```shell
     wget https://www.python.org/ftp/python/3.7.2/Python-3.7.2.tgz
     ```

  2. 安装依赖

     ```shell
     yum install -y gcc zlib* readline readline-devel libffi-devel openssl-devel
     ```

  3. 编译

     ```shell
     # 1 解压
     tar -zxvf Python-3.7.2.tgz
     
     # 2 进入目录
     cd ./Python-3.7.2
     
     # 3 配置 安装mod_wsgi会用到python的动态链接库
     ./configure --prefix=/usr/local/python3 --enable-shared
     
     # 4 编译
     make -j4
     
     # 5 安装
     make
     
     # 6 配置环境变量并注册动态链接库
     
     ## 6-1 配置环境变量
     vi /etc/profile
     export PATH=$PATH:/usr/local/python3/bin # 添加到文件末尾
     
     source /etc/profile
     
     ## 6-2 注册动态链接库
     vi /etc/ld.so.conf
     /usr/local/python3/lib # 添加到文件末尾
     ldconfig
     
     ```




# 第二章 Python基础语法

## 2.1 Python程序的书写规则

***

```python
# 这是我的第一个python程序

import time #模块导入

print(time.time())

if 10 - 9 > 0:
    print("10大于9")
```
## 2.2 基础数据类型

***

+ 数据类型
	1. 整数 8
	2. 浮点数 8.8
	3. 字符串 "Python" 'Python'
	4. 布尔值  True False
+ 获取变量数据类型 type(var)
+ 类型转换
	1. int('8')字符串转换为整数
	2. str(123)整数转换为字符串
	3. bool(123)数字转换为bool值

## 2.3 变量的定义和常用操作

***

+ 示例代码
	```python
	# 网络带宽计算
	
	bandwidth = 100
	ratio = 8
	print(bandwidth/8)
	```
+ 命名规范
	1. bandWidth
	2. BandWidth
	3. band_width 



## 2.4 数据类型归纳

***

1. 不可变数据类型（值类型）

   ```shell
   1. Number
   2. String
   3. Tuple
   ```

   

2. 可变数据类型（引用类型）

   ```shell
   1. List
   2. Dictionary
   3. Set
   4. 自定义的class
   ```



## 2.5 字符串相关

***

1. unicode编码字符串

   ```shell
   u'我含有中文字符'
   ```

2. 反斜杠不转义

   ```shell
   r'\n\t\r'
   ```

3. bytes对象

   ```shell
   b'yourBytes'
   ```




# 第三章 序列

## 3.1 序列的概念

***

+ 概念 成员有序排序，可以通过下标访问一个或多个元素
+ 类型
	+ 字符串 "abcd"
	+ 列表 [0,"abcd"]
	+ 元组("abc","def")
+ 示例代码
```python
# 记录生肖,根据年份来判断生肖

chinese_zodiac = "鼠牛虎兔龙蛇马羊猴鸡狗猪"
#元素的访问
print(chinese_zodiac[0])
print(chinese_zodiac[0:4])
print(chinese_zodiac[-1])
```
## 3.2 字符串的定义和使用

***

```python
# 记录生肖,根据年份来判断生肖

chinese_zodiac = "猴鸡狗猪鼠牛虎兔龙蛇马羊"

year = 2019
print(chinese_zodiac[year % 12])
```


## 3.3 字符串常用操作

***

+ 切片[:]
+ 重复*
+ 连接+
+ 查找
	1. in
	2. not in
+ 示例代码
```python
# 记录生肖,根据年份来判断生肖

chinese_zodiac = "猴鸡狗猪鼠牛虎兔龙蛇马羊"
print("狗" in chinese_zodiac) #查找
print(chinese_zodiac + "abcd")
print(chinese_zodiac * 3)
```


## 3.4 元组的定义和常用操作

***

+ 元祖与列表对比
  + 元祖元素不可变更
  + 列表元素可变
+ 代码演示
```python
#有bug
zodiac_name = (u'摩羯座', u'水瓶座', u'双鱼座', u'白羊座', u'金牛座', u'双子座',
               u'巨蟹座', u'狮子座', u'处女座', u'天秤座', u'天蝎座', u'射手座')
zodiac_days = ((1, 20), (2, 19), (3, 21), (4, 21), (5, 21), (6, 22),
               (7, 23), (8, 23), (9, 23), (10, 23), (11, 23), (12, 23))
(month, day) = (2, 15)
zodiac_day = filter(lambda x:x<=(month,day), zodiac_days)
zodic_len = len(list(zodiac_day))
print(zodiac_name[zodic_len])
```



## 3.5 列表的定义和常用操作

***

+ 操作
	1. 查找
		+ in
		+ not in
	2. 连接+
	3. 重复*
	4. 切片[:]
	5. 插入元素obj.append(elem)
	6. 删除元素obj.remove(elem)
+ 示例代码
```python
a_list = ['abc','xyz']
a_list.append('X')
print(a_list)
a_list.remove('xyz')
print(a_list)
```





# 第四章 条件与循环

## 4.1 条件语句

***

+ if

```python
if 表达式:
	代码块
```

```python
if 表达式:
	代码块
elif 表达式:
	代码块
else:
	代码块
```

+ 示例代码

```python
chinese_zodiac = "猴鸡狗猪鼠牛虎兔龙蛇马羊"
year = int(input("请用户输入出生年份:"))
if chinese_zodiac[year % 12] == "狗":
    print("狗年运势")
```



## 4.2 for循环

***

+ 语法
```python
for 迭代变量 in 可迭代对象:
    代码块
```
+ 示例代码
```python
chinese_zodiac = "猴鸡狗猪鼠牛虎兔龙蛇马羊"

for cz in chinese_zodiac:#for的用法
    print(cz)

#range的用法
for i in range(5):
    print(i)
for i in range(1,13):
    print(i)

for year in range(1989,2020):#格式化输出
    print("%s年的生肖是%s" %(year,chinese_zodiac[year%12]))
```



## 4.3 while循环

***

+ 语法

```python
while 表达式:
    代码块
```

+ 示例代码

```python
num = 5
while True:
    print("a")
    num += 1
    if num > 10:
        break
```

```python
import time
num = 5
while True:
    num += 1
    if num == 10:
        continue
    print(num)
    time.sleep(1)
```



## 4.4 for循环语句中嵌套if语句

***

```python
zodiac_name = (u'摩羯座', u'水瓶座', u'双鱼座', u'白羊座', u'金牛座', u'双子座',
           u'巨蟹座', u'狮子座', u'处女座', u'天秤座', u'天蝎座', u'射手座')
zodiac_days = ((1, 20), (2, 19), (3, 21), (4, 21), (5, 21), (6, 22),
              (7, 23), (8, 23), (9, 23), (10, 23), (11, 23), (12, 23))
#用户输入月份和日期
month = int(input("请输入月份:"))
day = int(input("请输入日期:"))

for index in range(len(zodiac_days)):
    if zodiac_days[index] >= (month,day):
        print(zodiac_name[index])
        break
    elif month == 12 and day > 23:
        print(zodiac_name[0])
        break
```

## 4.5 while循环中嵌套if语句

***

```python
zodiac_name = (u'摩羯座', u'水瓶座', u'双鱼座', u'白羊座', u'金牛座', u'双子座',
           u'巨蟹座', u'狮子座', u'处女座', u'天秤座', u'天蝎座', u'射手座')
zodiac_days = ((1, 20), (2, 19), (3, 21), (4, 21), (5, 21), (6, 22),
              (7, 23), (8, 23), (9, 23), (10, 23), (11, 23), (12, 23))
#用户输入月份和日期
month = int(input("请输入月份:"))
day = int(input("请输入日期:"))

n = 0
while zodiac_days[n] < (month,day):
    n += 1
    if n == len(zodiac_days):
        n = 0
        break
print(zodiac_name[n])
```





# 第五章 循环与字典

## 5.1 字典的定义和常用操作

***

+ 定义和赋值

```python
dict1 = {}
print(type(dict1))
dict2 = {"x":1,"y":2}
dict2["z"] = 3
print(dict2)
```

+ 遍历

```python
chinese_zodiac = "猴鸡狗猪鼠牛虎兔龙蛇马羊"
zodiac_name = (u'摩羯座', u'水瓶座', u'双鱼座', u'白羊座', u'金牛座', u'双子座',
           u'巨蟹座', u'狮子座', u'处女座', u'天秤座', u'天蝎座', u'射手座')
zodiac_days = ((1, 20), (2, 19), (3, 21), (4, 21), (5, 21), (6, 22),
              (7, 23), (8, 23), (9, 23), (10, 23), (11, 23), (12, 23))

cz_num = {}#生肖统计
for i in chinese_zodiac:
    cz_num[i] = 0

z_num = {}#星座统计
for i in zodiac_name:
    z_num[i] = 0
#用户输入月份和日期
while True:
    year = int(input("请输入年份:"))
    month = int(input("请输入月份:"))
    day = int(input("请输入日期:"))

    n = 0
    while zodiac_days[n] < (month,day):
        n += 1
        if n == len(zodiac_days):
            n = 0
            break
    print(zodiac_name[n])

    cz_num[chinese_zodiac[year % 12]] += 1
    z_num[zodiac_name[n]] += 1

    for key in cz_num.keys():
        print("生肖 %s 有 %s 个" %(key,cz_num[key]))

    for key in z_num.keys():
        print("星座 %s 有 %s 个" %(key, z_num[key]))
```



## 5.2 列表推导式与字典推导式

***

+ 列表推导式

```python
# 从 1 到 10 全部偶数的平方

#普通写法
alist = []
for i in range(1,11):
    if i % 2 == 0:
        alist.append(i * i)
print(alist)

#列表推导式
blist = [i*i for i in range(1,11) if i % 2 == 0]
print("blist:%s" %blist)
```



+ 字典推导式

```python
# 字典列表推导式
zodiac_name = (u'摩羯座', u'水瓶座', u'双鱼座', u'白羊座', u'金牛座', u'双子座',
           u'巨蟹座', u'狮子座', u'处女座', u'天秤座', u'天蝎座', u'射手座')

z_num = {key:0 for key in zodiac_name}
print(z_num)
```





# 第六章 文件与输入输出

## 6.1 文件的内建函数

***

+ 内建函数
    + open() 打开文件
    + read() 读取
    + readline() 读取一行
    + seek() 文件内移动
    + write() 写入
    + close() 关闭文件
+ 示例代码

```python
# 将小说的主要任务记录在文件中
file= open("name.txt", "w", encoding="utf8")
file.write("诸葛亮")
file.close()

file2 = open("name.txt","r", encoding="utf8")
print(file2.read())
file2.close()

file3 = open("name.txt","a", encoding="utf8")
file3.write("刘备")
file3.close()
```



## 6.2 文件的常用操作

***

+ 行操作

```python
file4 = open("name.txt", encoding="utf8")
print(file4.readline())#读取一行
file4.close()

file5 = open("name.txt", encoding="utf8")
lines = file5.readlines()#读取所有行
for line in lines:
    print(line)
    print("=" * 20)
file4.close()
```

+ 文件指针

```python
file = open("name.txt", encoding="utf8")
print("当前文件位置:%d" %(file.tell()))
file.read(1)
print("当前文件位置:%d" %(file.tell()))

#修改文件指针
#whence 0--表示从文件开头偏移 1--表示从当前位置偏移 2--表示从文件结尾偏移
#二进制模式打开才允许从当前位置和文件结尾开始偏移
file.seek(3,0)
print("当前文件位置:%d" %(file.tell()))
```



## 6.3 模块

***

### shutil

### 文档：File and Directory Access





# 第七章 错误和异常

## 7.1 异常

+ 处理流程

```python
try:
    <监控异常>
except Exception[,reason]:
    <异常处理代码>
finally:
    <无论异常是否发生都执行>
```

```python
try:
    year = int(input("请输入年份:"))
except ValueError:#异常类型可以查看pycharm报错信息
    print("年份要输入数字")
```

```python
#捕获多种异常
try:
    year = int(input("请输入年份:"))
except (ValueError,AttributeError,KeyError) as e:
    print("年份要输入数字")
```

```python
#打印错误信息
try:
    print(1/0)
except ZeroDivisionError as e:
    print("0不能做除数 %s" %e)
```

```python
#捕获所有异常
try:
    print(1/0)
except Exception as e:
    print("0不能做除数 %s" %e)
```

```python
#自定义错误提示信息
try:
    raise NameError("HelloError")
except Exception as e:
    print(e)
```

```python
try:
    file = open("name.txt","r", encoding="utf8")
    file.write("Hello")
except Exception as e:
    print(e)
finally:
    file.close()
    print("文件已经成功关闭")
```

```python
# 异常打印堆栈信息

import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(filename)s:%(funcName)s:%(lineno)d  - %(message)s')


def test():
    raise NameError("123")
    logging.info("Start print log")
    logging.debug("Do something")
    logging.warning("Something maybe fail.")
    logging.info("Finish")


if __name__ == "__main__":
    try:
        test()
    except Exception as e:
        logging.exception(e)
        print("---")
```



# 第八章 函数

## 8.1 函数的定义和常用操作

+ 函数定义

  ```python
  def 函数名称():
      代码
      return 需要返回的内容
  ```

+ 函数调用

  ```python
  函数名称(参数列表)
  ```

+ 代码演示

  ```python
  import re
  
  def find_item(hero):
      with open("sanguo.txt","r",encoding="utf8") as f:
          file_content = f.read().replace("\n","")
          name_num =len(re.findall(hero,file_content))
          print("主角 %s 出现 %s 次" %(hero,name_num))
      return name_num
  
  #读取人物信息
  name_dict = {}
  with open("name.txt","r",encoding="utf8") as f:
      for line in f:
          names = line.split("|")
          for name in names:
              name_dict[name] = find_item(name)
  
  items = name_dict.items()
  name_sorted = sorted(name_dict.items(),key=lambda item:item[1], reverse=True)
  print(name_sorted[0:10])
  ```

## 8.2 函数的可变长参数

+ 关键字参数

  ```python
  print("abc", end="\n")
  print("Abc")
  
  def func(a,b,c):
      print("a = %s" %a)
      print("c = %s" %b)
      print("c = %s" %c)
  
  func(1,c=3,b=2)
  ```

+ 可变长参数

  ```python
  def how_long(first,*other):
      return 1 + len(other)
  print(how_long(123,234,345,559))
  ```

  

## 8.3 函数的变量作用域

+ 问题

  1. 函数内部变量与外部变量同名出现什么问题
  2. 函数内如何引用外部变量

+ 示例代码

  ```python
  var1 = 123
  
  def func():
      var1 = 456
      print("func:%d" %var1)
  
  def func2():
      global  var1
      var1 = 779
      print("func2:%d" %var1)
  print("+" * 20)
  func()
  print(var1)
  print("-" * 20)
  func2()
  print(var1)
  ```

  

## 8.4 函数的迭代器与生成器

+ 迭代器

```python
list1 = [1,2,3,4]
it = iter(list1)

print(next(it))
print(next(it))
```

```python
for i in range(10,20,2):
    print(i)
```

+ 生成器

```python
#协程 和lua的一样
def frange(start, end, step):
    x =  start
    while x < end:
        yield x
        x += step

for i in frange(10, 20,0.5):
    print(i)
```



## 8.5 Lambda表达式

+ 普通函数与lambda的转换

```python
def add(x,y):
    return x + y
lambda x,y:x+y
```



## 8.6 Python内建函数

+ 内建函数
  + filter 获取满足指定条件的元素

    ```python
    a = [1,2,3,4,5,6,7]
    result = list(filter(lambda x : x >2,a))
    print(result)
    ```

  + map

    ```python
    a = [1, 2, 3]
    b = [4, 5, 6]
    result = list(map(lambda x,y : x + y,a,b))
    print(result)
    ```

    ```python
    a = [1, 2, 3]
    result = list(map(lambda x : x * x,a))
    print(result)
    ```

  + reduce

    ```python
    from functools import reduce
    
    #((1+2)+3)+4
    print(reduce(lambda x,y:x+y,[2,3,4],1))
    ```

  + zip

    ```python
    #类似矩阵转置
    for i in zip((1,2,3),(4,5,6)):
        print(i)
    ```

    ```python
    #将key 和 value对调
    dic = {'a': "aa", 'b':'bb'}
    dic = dict(zip(dic.values(),dic.keys()))
    print(dic)
    ```

    

+ 获取帮助文档

  1. 在终端输入help(函数名)
  2. [官方文档](https://www.python.org/doc/)

## 8.7 闭包的定义

+ 定义

```python
def sum(a):
    def add(b):#闭包可以捕获变量
        return a + b
    return add

fun = sum(5)
print(type(fun))
print(fun(10))
```

```python
def counter(first=0):
    cnt = [first] #这里不能用整型
    def impl():
        cnt[0] += 1
        return cnt[0]
    return impl


num1 = counter(5)
print(num1())
print(num1())

```

## 8.8 闭包的使用

```python
#表示直线
# a * x + b = y
def a_line(a,b):
    return lambda x : a * x + b
line1 = a_line(3, 5)
print(line1(20))
```

## 8.9 装饰器的定义

```python
import time
def timer(func):
    def wrapper():
        start_time = time.time()
        func()
        stop_time = time.time()
        print("运行时间是 %s 秒" %(stop_time - start_time))
    return wrapper

# 雏形
# def i_can_sleep():
#     time.sleep(3)
#
# f = timer(i_can_sleep)
# f()

@timer
def i_can_sleep():
    time.sleep(3)

i_can_sleep()
```



## 8.10 装饰器的使用

+ 装饰带参数的函数

```python
def tips(func):
    def impl(x,y):
        print("start")
        func(x,y)
        print("end")
    return impl

@tips
def add(x,y):#此时的add函数已经变成impl函数
    print(x + y)

add(4,5)
```

+ 带参数的装饰器

```python
def new_tips(param):
    def tips(func):
        def impl(x,y):
            print("start 参数:%s 函数名:%s" %(param, func.__name__))
            func(x,y)
            print("end")
        return impl
    return tips

@new_tips("add")
def add(x,y):
    print(x + y)

add(4,5)
```

## 8.11 自定义上下文管理器

```python
#文件处理

#普通方式
fp = open("name.txt", "r", encoding= "utf8")
try:
    for line in fp:
        print(line)
except Exception as e:
    print(e)
finally:
    fp.close()

#上下文管理器
with open("name.txt", "r", encoding="utf8") as f:
    for line in f:
        print(line)
```





# 第九章 模块

## 9.1 模块

+ 导入模块
  1. import 模块名称
  2. import 模块命名 as 自定义名称
  3. from 模块名称 import 方法名
+ 自定义模块

```python
#myModule.py
def print_me():
    print("me")
```

```python
import  myModule

myModule.print_me()
```