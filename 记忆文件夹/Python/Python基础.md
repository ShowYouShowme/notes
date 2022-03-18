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

## 1.3 第一个程序

***

```python
def main():
	print("Hello World!")

    
if __name__ == "__main__":
    main()
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

```python
#重新抛出异常
#使用raise后面不加参数
def exec_sql(sql : str, data):
    try:
        raise NameError("this is error")
        return results
    except Exception as e:
        #重新抛出异常
        raise

if __name__ == "__main__":
    try:
        result = exec_sql("select * from userinfo ", None)
    except Exception as e:
        logging.exception(e)
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



# 第十章 语法规范

## 10.1 优雅的定义

1. 终端里import this
2. [PEP 8](https://www.python.org/dev/peps/pep-0008/)



## 10.2 代码格式化工具

1. autopep8

   + 安装 pip3 install autopep8 --proxy http://127.0.0.1:8090
   + 配置
   ![](C:\Users\nash\Desktop\Python\img\pep8_configure.png)

   + 使用
   ![](C:\Users\nash\Desktop\Python\img\pep8_use.png)

2. Pycharm自带格式化工具



# 第十一章 面向对象编程

## 类与实例

```python
class Player:
    def __init__(self, name, hp):#构造函数
        self.__name = name #私有成员变量
        self.__hp = hp

    def print_role(self):
        print("%s %s" %(self.__name, self.__hp))

user1 = Player("tom", 100)#不需要写new
user1.print_role()
```



## 类的继承

```python
# 子类构造函数不会自动调用父类构造函数
class Shape:
    def __init__(self):
        print("construct Shape")
        return

    def cal_area(self):
        return
class Rectangle(Shape):#继承
    def __init__(self,width,height):
        print("construct Rectangle")
        self.__width = width
        self.__height = height

    def cal_area(self):
        return self.__height * self.__width

class Circle(Shape):
    def __init__(self,radius):
        super().__init__()
        print("construct Circle")
        self.__radius = radius

    def cal_area(self):
        return 3.14 * self.__radius * self.__radius

r1 = Rectangle(3,5)
print(r1.cal_area())
print("+" * 15)
c1 = Circle(5)
print(c1.cal_area())

#类型判断
print(type(r1))
print(isinstance(r1, Rectangle))
```



## 自定义with语句

```python
class TestWith:
    def __enter__(self):
        print("run")

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("exit")

with TestWith():
    print("Test is running!")
```

```python
class TestWith:
    def __enter__(self):
        print("run")

    #@param:exc_type 异常类型
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_tb is None:# None 相当于NULL
            print("正常结束")
        else:
            print("has error:%s" %exc_tb)
        return True #返回True表示异常不往外抛出
with TestWith():
    print("Test is running!")
    raise NameError("TestNameError")
```



# 第十二章 多线程编程

## 12.1 多线程编程的定义

```python
import threading
import time
from threading import current_thread
def myThread(arg1, arg2):
    print(current_thread().getName(),'start')
    print("%s %s" %(arg1, arg2))
    time.sleep(1)
    print(current_thread().getName(),'end')
for i in range(1,6):
    t1 = threading.Thread(target=myThread, args=(i,i+1)) #创建线程
    t1.start()#启动线程

print(current_thread().getName(),'end')
```

```python
import threading
from threading import current_thread

class MyThread(threading.Thread):
    def run(self):#start内部调用该函数
        print(current_thread().getName(),'start')
        self._target()
        print(current_thread().getName(),'end')

def handler():
    print('call Handler')

t1 = MyThread(target=handler)
t1.start()
t1.join()#等待t1结束
print(current_thread().getName(),'end')
```



## 12.2 经典的生产者和消费者问题

```python
from threading import Thread,current_thread
import time
import random
from queue import Queue

queue = Queue(5)#队列满会阻塞,加锁操作已经在Queue里面封装

class ProducerThread(Thread):
    def run(self):
        name = current_thread().getName()
        nums = range(100)
        global queue
        while True:
            num = random.choice(nums)
            queue.put(num)
            print("生产者 %s 生成了数据 %s" %(name, num))
            t = random.randint(1,3)
            time.sleep(t)
            print("生产者 %s 睡眠了 %s 秒" %(name,t))


class ConsumerThread(Thread):
    def run(self):
        name = current_thread().getName()
        global queue
        while True:
            num = queue.get()
            queue.task_done()
            print("消费者 %s 消耗了数据 %s" %(name,num))
            t = random.randint(1,5)
            time.sleep(t)
            print("消费者 %s 睡眠了 %s 秒" %(name, t))


p1 = ProducerThread(name="p1")
p1.start()
p2 = ProducerThread(name="p2")
p2.start()
p3 = ProducerThread(name="p3")
p3.start()

c1 = ConsumerThread(name="c1")
c1.start()
c2 = ConsumerThread(name="c2")
c2.start()
```



# 第十三章 标准库

## 13.1 标准库的定义
+ [标准库参考文档](https://docs.python.org/3/library/index.html)
+ 常用库
  1. Text Processing Services
  2. Data Types
  3. Generic Operating System Services
  4. 网络部分处理
  5. 开发工具与调试工具
## 13.2 正则表达式

+ 正则表达式库re

  ```python
  import re
  
  pattern = re.compile("ca*t")
  print(pattern.match("caaaat"))
  ```

+ 元字符

  1. **.** 匹配任意单个字符(不包括换行符'\n')
  2. **^** 以指定内容开头
  3. **$ **以指定内容结尾
  4. ***** 匹配0到多次
  5. **?** 匹配0或1次
  6. **+ **匹配1次或多次
  7. **{m[,n]}**
     + **{m}** 匹配m次
     + **{m,n}** 匹配m到n次
  8. **[]** 匹配括号里的某个字符
  9. **|** 字符选择左边或右边,常与()一起使用
  10. **\d** 匹配数字 [0-9]
  11. **\D** 匹配非数字
  12. **\s** 匹配空白
  13. **()** 分组,提取变量
  14. **^$** 匹配空行
  15. **.\*?** 不使用贪婪模式 匹配html的成对标签

+ 分组功能

  ```python
  import re
  
  pattern = re.compile("c.t")
  print(pattern.match("c\nt"))#.不能匹配'\n'
  ```

  ```python
  import re
  
  pattern = re.compile(r"(\d+)-(\d+)-(\d+)")
  print(pattern.match("2018-05-10").groups())
  
  print(r"x\nx") #反斜杠不转义,正常"\\"表示"\"
  ```

  ```python
  import re
  
  p = re.compile(r'(\d+)-(\d+)-(\d+)')
  print(p.match('2018-05-10').group(2))
  print(p.match('2018-05-10').groups())
  
  year,month,day= p.match("2018-05-10").groups()
  print("year:%s month:%s day:%s" %(year,month,day))
  ```

  

+ match与search对比

  1. match是完全匹配整个字符串

  2. search只要匹配字符串的一部分

  3. 代码演示

     ```python
     import re
     
     pattern = re.compile(r"(\d+)-(\d+)-(\d+)")
     # print(pattern.match("aa2018-05-10bb").groups()) #此处抛出异常
     
     print(pattern.search("aa2018-05-10bb").groups())
     ```

+ sub函数 字符串替换substitute

  ```python
  import re
  
  phone = "123-456-789 #这是电话号码"
  p2 = re.sub(r'#.*$','',phone)
  print(p2)
  print("-" * 15)
  p3 = re.sub(r'\D','',p2)
  print(p3)
  ```

+ findall 查找全部匹配结果

## 13.3 日期和时间

+ 相关模块

  1. time
  2. datetime

+ 示例代码

  ```python
  import time
  
  print(time.time())#获取秒数
  print(time.localtime())#获取年月日信息
  print(time.strftime('%Y-%m-%d %H:%M:%S'))
  ```

  ```python
  import datetime
  
  # 获取10分钟后的时间
  print(datetime.datetime.now())
  new_time_delta = datetime.timedelta(minutes=10)
  print(datetime.datetime.now() + new_time_delta)
  
  #获取间隔指定日期指定时长的新日期
  one_day = datetime.datetime(2008,5,27)
  day_delta =datetime.timedelta(days=10)
  print(one_day+day_delta)
  ```

## 13.4 数学

+ 相关模块

  1. math
  2. random

+ 示例代码

  ```python
  import random
  
  print(random.randint(1,3))
  
  print(random.choice(['aa','bb','dd']))
  ```

## 13.5 文件和目录

+ 使用命令行对文件和文件夹操作

  1. ls
  2. pwd
  3. cd 绝对路径|相对路径
  4. mkdir
     + mkdir -p /tmp/a/b/c/d (自动创建不存在的目录)

+ 文件和目录操作库

  1. 相关库

     + os.path
     + pathlib

  2. 示例代码

     ```python
     import os
     
     print(os.path.abspath("."))
     print(os.path.exists('test.py'))#判断文件是否存在
     print(os.path.isfile('sanguo.txt'))
     print(os.path.isdir('weapon.txt'))
     #路径拼接
     print(os.path.join('/tmp/dir','name.txt'))
     ```

     ```python
     import pathlib
     #获取路径
     p = pathlib.Path('.')
     print(p.resolve())
     
     q = pathlib.Path("./img/a/b/c")
     pathlib.Path.mkdir(q,parents=True)#上层目录不存在自动创建
     ```




# 第十四章  机器学习

## 14.1 处理步骤

1. 数据采集
2. 数据预处理
3. 数据清洗
4. 建模和测试

## 14.2 NumPy

+ 作用：数据预处理
+ 安装：pip3 install numpy



## 14.3 NumPy的数组与数据类型

```python
import numpy
arr1 = numpy.array([2,3,4])
print(arr1)
print(arr1.dtype)#打印数据类型

arr2 = numpy.array([1.2,3.4,5.6])
print(arr2)
print(arr2.dtype)

print(arr1 + arr2)
```



## 14.4 NumPy数组和标量的计算

```python
import numpy
arr1 = numpy.array([2,3,4])
print(arr1 * 15)#矩阵与标量计算

#二维矩阵
data = [[1,2,3],[4,5,6]]
arr3 = numpy.array(data)
print(arr3)
print(arr3.dtype)

#其它方法
print(numpy.zeros(5))#一维矩阵
print(numpy.zeros((3,5)))#二维矩阵
print(numpy.ones((4,6)))
print(numpy.empty(3))#置空
```



## 14.5 NumPy数组的索引和切片

```python
import numpy

arr = numpy.arange(10)
print(arr[5])
print(arr[0:3])#获取切片
arr[0:3] = 99 #赋值
print(arr)

arr_slice = arr[3:].copy()#获取副本
print(arr_slice)
arr_slice[:] = 998
print(arr_slice)
```



## 14.6 pandas安装与Series结构





# 第十五章 爬虫

## 15.1 网页数据的采集与urlib库

### 15.1.1 网络库介绍

+ urlib库      http协议常用库，系统标准库

+ request库 http协议常用库，第三方库

+ BeautifulSoup库 xml格式处理库

  ```python
  from urllib import request
  
  url = "http://www.baidu.com"
  response = request.urlopen(url,timeout=1)
  print(response.read().decode("utf-8"))
  ```



### 15.1.2 urlib库的使用

#### 15.1.2.1 Get与Post

+ 简单介绍Get与Post方法

+ 代码演示

  ```python
  from urllib import parse
  from urllib import request
  #先设置操作系统http、https、ftp代理服务器
  data = bytes(parse.urlencode({"word":"hello"}), encoding="utf8")
  response = request.urlopen("http://httpbin.org/post", data=data, timeout=10)
  print(response.read().decode("utf8"))
  ```
  
  ```python
  import urllib
  from urllib import request
  import socket
  #先设置操作系统http、https、ftp代理服务器
  try:
      req = request.urlopen("http://httpbin.org/get?a=888&b=999", timeout=5)
      print(req.read().decode("utf8"))
  except urllib.error.URLError as e:
      if isinstance(e.reason, socket.timeout):
          print("TIME OUT")
  ```
  
  ```python
  # 用json格式发请求
  from urllib import request
  import json
  
  # 请求体数据
  request_data = {
      "serial": True,
      "items": [{"server_id": 41, "command": "restart"}]
  }
  
  headers = {
      "content-type": "application/json"
  }
  
  req = request.Request(url="http://10.10.10.168:3000/pages/server/api/add_task",
                        headers=headers,
                        data=json.dumps(request_data).encode("utf-8"))
  
  reps = request.urlopen(req).read().decode("utf-8")
  ```
  
  

#### 15.1.2.2 HTTP头部信息模拟

```python
from urllib import request
from urllib import parse

#构造http头部信息
url = "http://httpbin.org/post"
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, sdch",
    "Accept-Language": "zh-CN,zh;q=0.8",
    "Connection": "close",
    "Cookie": "_gauges_unique_hour=1; _gauges_unique_day=1; _gauges_unique_month=1; _gauges_unique_year=1; _gauges_unique=1",
    "Referer": "http://httpbin.org/",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36 LBBROWSER"
}

data = bytes(parse.urlencode({"word":"helloHttp8457"}),encoding="utf8")
req = request.Request(url=url,data=data,headers=headers,method="POST")
response = request.urlopen(req,timeout=10)
print(response.read().decode("utf8"))
```



## 15.2 requests库的基本使用

+ 安装 *pip3 install requests --proxy http://127.0.0.1:8090*

+ 使用第三方包
	+ 直接用项目中的pip安装
	+ 用系统的pip安装，在pycharm中进行设置
		1. 文件-->默认设置-->项目解释器，添加系统解释器
		2. 文件-->设置-->项目解释器  设置python解释器为系统解释器

+ 代码示例
	```python
	import requests
	
	url = "http://httpbin.org/get"
	data = {"key":"value","abc":"xyz"}
	
	response = requests.get(url,data)
	print(response.text)
	print("*" * 20)
	#post 请求
	url = "http://httpbin.org/post"
	data = {"key":"value","abc":"xyz"}
	response = requests.post(url,data)
	print(response.json())
	```
	
+ 结合正则表达式爬取图片链接

```python
import requests
import re

url = 'http://www.cnu.cc/discoveryPage/hot-人像'
content = requests.get(url).text

pattern = re.compile(r'<img src="(.*?)".*?alt="(.*?)">',re.S)
result = re.findall(pattern, content)
for elem in result:
    uri,name = elem
    pos = str(uri).find("?")
    uri = uri[0:pos]
    pattern = re.compile(r".*\.(.*)")
    postfix = re.findall(pattern, uri)[0]
    content = requests.get(uri).content
    name = re.sub("[\"”“ ]","",name)
    try:
        f = open("img/" + name + "." + postfix,"wb")
        f.write(content)
        f.close()
    except Exception as e:
        print(e)
        print("%s.%s 下载失败" %(name,postfix))
print("图片下载完成")
```



## 15.3 BeautifulSoup

### 15.3.1 安装和基本用法

+ 安装
	1. pip3 install bs4 
	2. pip3 install lxml 
+ 使用
	1. 基本功能
		+  格式化 *soup.prettify()*
		+  获取标签
		   +  根据标签名获取
		   +  根据id获取
		+  获取标签里面的内容
		+  获取标签属性
		+  获取全部满足指定条件的标签
	2. 示例代码
	```python
	from bs4 import BeautifulSoup
	
	html_doc = """
	<html><head><title>The Dormouse's story</title></head>
	<body>
	<p class="title"><b>The Dormouse's story</b></p>
	
	<p class="story">Once upon a time there were three little sisters; and their names were
	<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
	<a href="http://example.com/lacie" class="
	sister" id="link2">Lacie</a> and
	<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
	and they lived at the bottom of a well.</p>
	
	<p class="story">...</p>
	"""
	
	soup = BeautifulSoup(html_doc, "lxml")
	print(soup.prettify())#格式化
	
	print(soup.title)#获取title标签
	print(soup.title.string)#获取title标签里面的内容
	#找到所有的a标签
	print(soup.find_all("a"))
	print(soup.a["href"])#获取标签的属性
	print(soup.find(id="link3"))#通过id获取标签
	```

### 15.3.2 使用爬虫爬取新闻网站

+ 下载网页源码至html文件里，也可以用***requests.get***获取网页源码
+ 源码
```python
from bs4 import BeautifulSoup

url = "https://www.infoq.cn/"
f = open("src.html","r",encoding="utf-8")
root_path = "https://www.infoq.cn/"
html = f.read()
soup = BeautifulSoup(html,"lxml")
title_hrefs = soup.find_all("div", class_="list-item image-position-right")
for title_href in title_hrefs:
    title = title_href.find("a",class_="com-article-title")
    print("标题：%s 链接:%s" %(title.string, root_path + title.get("href")))
```
### 15.3.3 获取图片链接并下载图片
```python
from bs4 import  BeautifulSoup
import requests
import os
import shutil

#1: 下载图片
#2: 实现翻页
#3: 利用多线程
headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.8",
    "Connection": "close",
    "Cookie": "_gauges_unique_hour=1; _gauges_unique_day=1; _gauges_unique_month=1; _gauges_unique_year=1; _gauges_unique=1",
    "Referer": "http://www.infoq.com",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36 LBBROWSER"
}

def download_img(url,path):
    response = requests.get(url,stream=True)
    if response.status_code == 200:
        with open(path,"wb") as f:
            response.raw.decode_content = True
            shutil.copyfileobj(response.raw, f)
def download_all_img(url):
    response = requests.get(url,headers=headers)
    soup = BeautifulSoup(response.text,"lxml")
    for pic_href in soup.find_all("div", class_="container pc"):
        for pic in pic_href.find_all("img"):
            img_url = pic.get("src")
            pos = str(img_url).find('?')
            img_url = img_url[0:pos]
            # print(img_url)
            dir = os.path.abspath("./img")
            file_name = os.path.basename(img_url)
            img_path = os.path.join(dir,file_name)
            print("开始下载 %s" %img_url)
            download_img(img_url,img_path)


url = "http://www.cnu.cc/discoveryPage/hot-人像?page="
for i in range(1,6):
    print("第 %d 页" %i)
    download_all_img(url + str(i))
```







## 15.4 文件上传

1. http头部

   ```shell
   Content-Type: multipart/form-data; boundary=${bound}
   ```

2. 示例代码

   ```python
   import os, random, sys, requests
   from requests_toolbelt.multipart.encoder import MultipartEncoder
   
   url = 'http://10.10.10.23:8081/file_upload'
   headers = {
       'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:50.0) Gecko/20100101 Firefox/50.0',
       'Referer': url
       }
   
   file = './cros.html'
   # image 是表单的字段名
   multipart_encoder = MultipartEncoder(
       fields={
           'image': (os.path.basename(file) , open(file, 'rb'), 'application/octet-stream')
           #file为路径
           },
           boundary='-----------------------------' + str(random.randint(1e28, 1e29 - 1))
       )
   
   headers['Content-Type'] = multipart_encoder.content_type
   #请求头必须包含一个特殊的头信息，类似于Content-Type: multipart/form-data; boundary=${bound}
   
   r = requests.post(url, data=multipart_encoder, headers=headers)
   print(r.text)
   ```

   ```html
   <!DOCTYPE html>
   <html lang="en">
   <head>
       <meta charset="UTF-8">
       <title>文件上传演示</title>
   </head>
   <body>
   <h3>文件上传:</h3>
   选择一个文件上传:<br/>
   <form action="file_upload" method="post" enctype="multipart/form-data">
       <input type="file" name="image" size="50">
       <br/>
       <input type="submit" value="文件上传">
   </form>
   </body>
   </html>
   ```

   ```javascript
   import express = require("express");
   import fs = require("fs");
   import bodyParser = require("body-parser");
   import multer = require("multer");
   
   
   
   let app : express.Application = express();
   app.use(express.static('public'));
   app.use(bodyParser.urlencoded({extended : false}));
   app.use(multer({dest:'/tmp'}).array('image'));
   
   app.get("/", (req: express.Request, res : express.Response):void=>{
       let path : string = __dirname + "/" +"form.html"
       res.sendFile(path);
   });
   
   app.post('/file_upload', (req : express.Request, res : express.Response):void=>{
       let files   : Express.Multer.File[] = req.files as Express.Multer.File[];
       let file    : Express.Multer.File   = files[0];
       console.log(file);
   
       let des_file : string = __dirname + "/" + file.originalname;
       fs.readFile(file.path, (err, data):void=>{
           fs.writeFile(des_file, data, (err):void=>{
               let response : any = null;
               if (err){
                   console.error(err);
               } else{
                   response = {
                       message:'File uploaded successfully',
                       filename:file.originalname
                   }
               }
               console.log(response);
               res.end(JSON.stringify(response));
           })
       })
   
   });
   
   let server = app.listen(8081);
   ```

   

# 第十六章 类型注解

## 16.1 变量注解

```python
a: int = 2
```



## 16.2 函数注解

```python
def add(a : int, b : int) -> int:
    return a + b
```



## 16.3 集合类型注解

```python
from typing import List, Tuple, Dict

names: List[str] = ['Germey', 'Guido']
version: Tuple[int, bool, str] = (3, True, 'Nash')
operations: Dict[str, bool] = {'show': False, 'sort': True}
```



## 16.4 无返回值

```python
from typing import NoReturn

def help_info() -> NoReturn:
    print("Hello")
```



## 16.5 返回任意类型

```python
from typing import List, Tuple, Dict,NoReturn,Any

# Any 是任意类型
def get_info(param : int) -> Any:
    if param == 3 :
        return "GET method"
    else:
        return 128

def main():
    a : str = get_info(3)
    print(a)
    b : int = get_info(12)
    print(b)
    print("=============")
```



## 16.6 兼容多种类型

```python
from typing import TypeVar

height = 1.75
Height = TypeVar('Height', int, float, None) # int|float|None
def get_height() -> Height:
 return height
```



## 16.7 Union

```python
# Union[X, Y] 代表要么是 X 类型，要么是 Y 类型 类似Typescript的"|"
def process(fn: Union[str, Callable]):
 if isinstance(fn, str):
  # str2fn and process
  pass
 elif isinstance(fn, Callable):
  fn()
```



## 16.8 定义新类型

```python
# 类型C++的Typedef
from typing import NewType
Person = NewType('Person', Tuple[str, int, float])
person = Person(('Mike', 22, 1.75))
```



## 16.9 函数类型

```python
from typing import Callable
def date(year: int, month: int, day: int) -> str:
 return f'{year}-{month}-{day}'
 
 # 调用此函数返回一个函数,函数的参数是int,int,int 函数返回值是str
def get_date_fn() -> Callable[[int, int, int], str]:
 return date
```



## 16.10 Optional

```python
# Optional[int]表明参数可以是int或者None
def judge(result: bool) -> Optional[str]:
 if result: return 'Error Occurred'
```



## 16.11 Generator

```python
# 生成器类型 === 暂时用不到
```





# 第十七章 操作系统

## 17.1 执行shell命令

```python
import subprocess
import os

def log_info(cmd : str):
    msg : str = "\033[32m======>{0}".format(cmd)
    print(msg)
    print("\033[0m")

def log_error(cmd : str):
    msg : str = "\033[31m{0}=======> failed!".format(cmd)
    print(msg)
    print("\033[0m")

def exec_shell_cmd(cmd : str):
    child = subprocess.Popen(cmd, shell=True)
    child.wait()
    if child.returncode != 0:
        log_error(cmd)
        raise NameError("occur error!")
```

```python
#监控指定进程使用的内存
# 监控指定进程使用的内存 把这部分代码加入到笔记当中
import logging
import subprocess
import time

process_name = "lotus-bench"


def get_cmd_output(cmd):
    logging.info(">>>>>get_cmd_output")
    pi = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    raw_data = bytes(pi.stdout.read())
    cmd_output = raw_data.decode()  # bytes 转换为string
    logging.debug("cmd {0} output {1}".format(cmd, cmd_output))
    logging.info("<<<<<get_cmd_output")
    return cmd_output


def main():
    mem_file = open("mem.txt", "w", encoding="utf8")
    mem_file.write("[")
    index_file = open("index.txt", "w", encoding="utf8")
    index_file.write("[")
    index = 1
    while True:
        output = get_cmd_output("ps -C {} -f".format(process_name))
        entry = output.split('\n')[: -1]
        if len(entry) != 2:
            logging.error("can not find process {}".format(process_name))
            exit(-1)
        items = entry[-1].split()
        pid = int(items[1])

        output = get_cmd_output("cat /proc/{}/status | grep RSS".format(pid))
        entry = output.split()
        VmRSS = int(entry[1])
        print("[{},{}]".format(index, VmRSS))
        mem_file.write("{},".format(VmRSS))
        mem_file.flush()
        index_file.write("{},".format(index))
        index_file.flush()
        time.sleep(1)
        index += 1


if __name__ == "__main__":
    main()
```



# 第十八章 日期和时间

# 18.1 日期时间

## 18.1.1  相关类

1. date

   > 日期对象，常用属性有year，month和day

2. time

   > 时间对象

3. datetime

   > 日期时间对象，常用属性对象有hour，minute，second和microsecond

4. timedelta

   > 两个时间点间的时间间隔

5. tzinfo

   > 时区信息对象



## 18.1.2 date类

1. 构造

   ```python
   d = datetime.date(year=2020, month=10, day=25)
   ```

2. 常用方法

   > + 比较大小
   >
   >   ```shell
   >   # 等于
   >   a.__eq__(b)
   >
   >   # 大于等于
   >   a.__ge__(b)
   >
   >   # 大于
   >   a.__gt__(b)
   >
   >   # 小于等于
   >   a.__le__(b)
   >
   >   # 小于
   >   a.__lt__(b)
   >
   >   # 不等于
   >   a.__ne__(b)
   >   ```
   >
   > + <font color="deep pink">获取两个日期相差多少天</font>
   >
   >   ```python
   >   d1 - d2
   >   ```
   >
   > + 标准化日期
   >
   > + <font color="deep pink">其它方法</font>
   >
   >   > 1. **timetuple**
   >   >
   >   >    ```shell
   >   >    # 返回一个类型为time.struct_time的数组
   >   >    ```
   >   >
   >   > 2. **fromtimestamp**
   >   >
   >   >    ```shell
   >   >     # 根据给定的时间戮，返回一个date对象
   >   >    ```
   >   >
   >   > 3. **today**
   >   >
   >   >    ```shell
   >   >    # 返回当前日期
   >   >    ```
   >
   > + 日期字符串输出



## 18.1.3 time类







## 18.1.4 datetime类

1. 示例

   ```python
   # 字符串转为datetime param:202003161155
   def to_datetime(param):
       d = datetime.datetime.strptime(param, '%Y%m%d%H%M')
       return d
   
   # datetime转为时间戳
   def to_timestamp(param):
       return int(time.mktime(param.timetuple()))
   ```

   ```python
   # 将iso格式的字符串转换为datetime
   d1 = datetime.datetime.fromisoformat('2020-04-28T04:03:10')
   d2 = datetime.datetime.fromisoformat('2020-04-28T04:03:25')
   # 计算两个日期间隔的秒数
   t = (d2 - d1).seconds
   ```
   
   



# 18.2 常见问题

## 18.2.1 获取昨天的日期

```python
def get_yesterday():
    timestamp   : int           = time.time()
    today       : datetime.date = datetime.date.fromtimestamp(timestamp)
    yesterday   : datetime.date = datetime.date.fromtimestamp(timestamp - 24 * 60 * 60)
    return yesterday.isoformat()
```





# 第十九章 调试



## 19.1 pdb 命令列表

| 命令                    | 简写                | 作用                   |
| ----------------------- | ------------------- | ---------------------- |
| break                   | b                   | 设置断点               |
| continue                | c                   | 继续执行               |
| list                    | l                   | 查看当前行代码段       |
| **step**                | **s**               | **进入函数**           |
| return                  | r                   | 从当前函数返回         |
| quit                    | q                   | 终止并退出             |
| **next**                | **n**               | **执行下一行**         |
| **print**               | **p**               | **打印变量值**         |
| help                    | h                   | 帮助信息               |
| args                    | a                   | 查看传入参数           |
| break                   | b                   | 显示所有断点           |
| break ${lineno}         | b ${lineno}         | 在指定行设置断点       |
| break ${file}:${lineno} | b ${file}:${lineno} | 在指定文件的行设置断点 |
| clear ${num}            |                     | 删除指定断点           |
| bt                      |                     | 查看函数调用堆栈       |



## 19.2 调试命令

```shell
python3 -m pdb some.py
```





# 第二十章 包和依赖管理



## 20.1 包管理器

***



### 20.1.1 安装

```shell
# step1
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py

# step2
python3 ./get-pip.py

# Ubuntu 18.04 安装方案
sudo apt-get install python3-pip

sudo -H pip3 install -U pip # 升级pip 到最新版本
```



### 20.1.2 使用阿里云镜像

1. 临时使用

   ```shell
   pip install -i https://mirrors.aliyun.com/pypi/simple/ ${package}
   ```

2. 默认使用

   ```shell
   pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/
   ```

3. 查看设置结果

   ```shell
   pip config list
   ```

4. 取消设置

   ```shell
   pip config unset global.index-url
   ```



# 第二十一章 日志系统



## 21.1 基本用法

```python
import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(filename)s:%(funcName)s:%(lineno)d  - %(message)s')


def test():
    logging.info("Start print log")
    logging.debug("Do something")
    logging.warning("Something maybe fail.")
    logging.info("Finish")


if __name__ == "__main__":
    test()
```







# 第二十二章 MySQL



## 22.1 基本操作

***

```python
import  pymysql
def _exec_sql(sql : str, data):
    conn = pymysql.connect(host="192.168.0.79", port=8001, user="root", password="vsvIxMVS5c4VBFoh", database="test")
    cursor = conn.cursor()
    try:
        cursor.execute(sql, data) #防止sql注入
        conn.commit()
        results = cursor.fetchall()
        conn.close()
        return results
    except Exception as e:
        conn.rollback()
        print(e)
        conn.close()
```



## 22.2 超时设置

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

   



## 22.3 事务处理

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




## 22.4 SQL 注入

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





# 第二十三章 Redis



## 23.1 基本用法

```python
#删除指定key
import redis
from typing import List, Tuple, Dict

conn = redis.Redis(host='10.10.10.168', port=7111)


keys : List[str] = conn.keys("1:100:*")

for key in keys:
    conn.delete(key)
print(keys)
```



# 第二十四章 Requests

## 24.1 连接超时

****

1. 对应tcp的connect函数调用

2. 例子

   ```python
   import time
   import requests
   
   url = 'http://www.google.com.hk'
   
   print(time.strftime('%Y-%m-%d %H:%M:%S'))
   try:
       html = requests.get(url, timeout=5).text # 设置连接超时为5s,默认是21s
       print('success')
   except requests.exceptions.RequestException as e:
       print(e)
   
   print(time.strftime('%Y-%m-%d %H:%M:%S'))
   ```

   



## 24.2 读取超时

***

1. **读取超时如果不设置，程序将一直处于等待状态，无法响应**

2. 设置方式

   + connect 和 read 共用一个timeout

     ```python
     r = requests.get('https://github.com', timeout=5)
     ```

   + connect 和 read 分别用自己的timeout

     ```python
     r = requests.get('https://github.com', timeout=(3.05, 27))
     ```

3. 代码示例

   + 不设置超时，一直等待
   
     ```python
     import time
     import requests
     
     
     # FLASK 搭建的http服务,该接口sleep 123456 秒
     url = 'http://127.0.0.1:8101/api/gather/tx'
     print(time.strftime('%Y-%m-%d %H:%M:%S'))
     
     try:
         html = requests.get(url).text  # 会一直阻塞等待
         print('success')
     except requests.exceptions.RequestException as e:
         print(e)
     
     print(time.strftime('%Y-%m-%d %H:%M:%S'))
     ```
   
   + 设置超时
   
     ```python
     import time
     import requests
     
     
     # FLASK 搭建的http服务,该接口sleep 123456 秒
     url = 'http://127.0.0.1:8101/api/gather/tx'
     print(time.strftime('%Y-%m-%d %H:%M:%S'))
     
     try:
         html = requests.get(url,timeout=(5, 15)).text
         print('success')
     except requests.exceptions.RequestException as e:
         print(e)
     
     print(time.strftime('%Y-%m-%d %H:%M:%S'))
     ```
   
     
## 24.3 超时重试

***

   1. 例子
   
      ```python
      import time
      import requests
      from requests.adapters import HTTPAdapter
      
      s = requests.Session()
      s.mount('http://', HTTPAdapter(max_retries=3))
      s.mount('https://', HTTPAdapter(max_retries=3))
      
      print(time.strftime('%Y-%m-%d %H:%M:%S'))
      try:
          r = s.get('http://www.google.com.hk', timeout=5)
          return r.text
      except requests.exceptions.RequestException as e:
          print(e)
      print(time.strftime('%Y-%m-%d %H:%M:%S'))
      ```
   
      
   
   2. 分析
   
      > `max_retries` 为最大重试次数，重试3次，加上最初的一次请求，一共是4次，所以上述代码运行耗时是20秒而不是15秒



# 第二十五章 json



## 25.1 相关API

```shell
json.loads()  	#将json转换为dict
json.dumps()	#将dict转换为json

# 文件与JSON
json.load() 	#将json文件转换为dict
json.dump() 	#将dict转换为json文件 person.jon
```



## 25.2  dict转换为json

```python
import json
person = {
  'name': 'jack',
  'age': 15,
  'email': 'jack@litets.com'
}
print('dict：', person)
person_json = json.dumps(person) # 转换为json
print('json：', person_json)
```



## 25.3 json转换为dict

```python
import json
person_dict = json.loads('{"name": "jack", "age": 15, "email": "jack@litets.com"}')
print('person dict:', person_dict)
```



## 25.4 对象转换为json

```python
import json
class Person:
  def __init__(self, name, age, email):
    self.name = name
    self.age = age
    self.email = email
person = Person('tom', 38, 'tom@litets.com')
person_json = json.dumps(person.__dict__)
print('person json:', person_json)
```



## 25.5 json转换为对象

```python
import json
class Person:
  def __init__(self, name, age, email):
    self.name = name
    self.age = age
    self.email = email
def convert2json(dict_json):
  return Person(dict_json['name'], dict_json['age'], dict_json['email'])
person = json.loads('{"name": "tom", "age": 38, "email": "tom@litets.com"}', object_hook=convert2json)
print('person:', person)
```



## 25.6 dict转换为json文件

```python
import
person = {"name": "tom", "age": 38, "email": "tom@litets.com"}
with open('person.json', 'w') as f:
  json.dump(person, f)
```



## 25.7 json文件转换为dict

```python
import json
with open('person.json', 'r') as f:
  print(json.load(f))
```

# 

# 第二十六章 其它问题



## 26.1 循环引用

***

1. 将导入语句放到函数或者类的内部

2. 组织代码

   ```shell
   # 可以将代码合并到一起
   
   # 可以把一部分import提取到第三个文件中
   ```




## 26.2 排序

***

+ 简单list排序

  ```python
      # l.sort() 直接排序数组
      l = [1, 6, -1,0]
      l.sort()
      print(l)
  ```

  ```python
      # sorted : 返回排序后的数组,原来的数组不变
      l = [1, 6, -1,0]
      l1 = sorted(l)
      print(l)
  ```

  

+ list内嵌dict的排序

  ```python
      l = [
          {
              "age" : 20,
              "salary" : 57,
          },
          {
              "age" : 40,
              "salary" : 15,
          },
          {
              "age" : 12,
              "salary" : 0,
          },
          {
              "age" : 2,
              "salary" : -1
          }
      ]
  
      l.sort( key=lambda k : k["age"],reverse=True)
      print(l)
  ```

  

# 第二十七章 网络编程



## 27.1 TCP客户端

```shell
import socket

host = '127.0.0.1'
port = 8080
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))
msg = 'hello'
client.send(msg.encode('utf-8'))
data = client.recv(1024)
print("服务的发来的消息：%s" %data)
client.close()
```





## 27.2 TCP 服务端

```python
import socket

host = '127.0.0.1'
port = 8080
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)       # 创建一个基于网络通信的TCP协议的socket对象
server.bind((host, port))
server.listen(5)    # 5表示最大的同时连接数

conn,addr = server.accept()  # conn表示链接；addr表示地址；返回的结果是一个元组
msg = conn.recv(1024)   # 接受信息，1024表示接收1024个字节的信息
print("客户端发来的消息是:%s" %msg.decode('utf-8'))
conn.send(msg.upper())  # 发送的消息

# 断开链接
conn.close()
server.close()
```

