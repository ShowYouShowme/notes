# 第一章 安装



## 1.1 虚拟环境

+ 定义：python解释器的私有副本，在该环境中安装私有包，不会影响系统中安装的全局python解释器
+ 作用
  + 避免安装的包以及python版本和系统的冲突
  + 不需要管理员权限

## 1.2 创建虚拟环境

```shell
# step-1

sudo apt-get install python3-venv

# step-2
python3 -m venv ${virtual-environment-name}

## 例子
python3 -m venv venv
```



## 1.3 使用虚拟环境

+ Linux系统

  ```shell
  source venv/bin/activate
  ```

+ Win

  ```shell
  venv\Scripts\activate
  ```

  

## 1.4 安装flask

```shell
# 安装flask
pip install flask

# 查看虚拟环境中安装了哪些包
pip freeze


# 验证flask是否正确安装

(venv)$ python
>>> import flask  # 没有错误提醒即可
```





# 第二章 应用的基本结构



## 2.1 初始化

```shell
from flask import Flask
app = Flask(__name__)
```





## 2.2 路由和视图函数

+ 路由：处理URL和函数之间关系的程序称为路由

+ 定义路由

  ```shell
  @app.route('/')
  def index():
      return '<h1>Hello World!</h1>'
  ```

  ```shell
  def index():
      return '<h1>Hello World!</h1>'
      
  app.add_url_rule('/', 'index', index)
  ```

+ 可变路由

  ```shell
  @app.route('/user/<name>')
  def user(name):
      return '<h1>Hello {}!</h1>'.format(name)
  ```

  

## 2.3 完整应用

```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return '<h1>Hello World!</h1>'
```





## 2.4 启动服务

+ Linux

  ```shell
  # hello.py是脚本文件名
  (venv) $ export FLASK_APP=hello.py
  (venv) $ flask run
  ```

+ Win

  ```shell
  set FLASK_APP=hello.py
  flask run
  ```

+ 编程的方式启动（不推荐）

  ```shell
  if __name__= '__main__':
  	app.run()
  ```

  



## 2.5 调试模式

+ 优点

  ```shell
  1. 项目中的源文件变动时，自动重启服务
  
  2. 当应用抛出未处理的异常，堆栈信息会出现在浏览器中
  ```

+ 缺点

  ```shell
  客户端通过调试器能请求执行远程代码，攻击服务器
  ```
  
+ 启动方式
  
  ```shell
  (venv) $ export FLASK_APP=hello.py
  (venv) $ export FLASK_DEBUG=1
  (venv) $ flask run
  ```
  
  
## 2.6 命令行选项

```shell
flask --help

flask run --help
```



## 2.7 应用和请求上下文

+ 应用上下文

  + current_app：当前应用实例
  + g：处理请求时作临时对象，每次请求都会重置

+ 请求上下文

  + request：封装客户端http请求的内容
  + session：用户会话

  

## 2.8 请求分派

+ 分派：收到客户端请求时，找到对应url的处理函数并执行

+ 映射查看

  ```shell
  (venv) $ python
  >>> from hello import app
  >>> app.url_map
  ```



## 2.9 请求对象

+ 对象：request
+ 常见方法和属性





## 2.10 请求钩子

```python
# 处理第一个请求之前执行
before_first_request

# 每次请求之前运行
before_request

# 如果没有未处理的异常，每次请求之后运行
after_request

# 即使有未处理的异常抛出，也在每次请求后执行
teardown_request
```





## 2.11 响应

1. 响应方式

   + 元祖：第一个值html字符串，第二个值是响应码（默认200），第三个值是HTTP响应首部组成的字典

   + 响应对象

     ```python
     from flask import Flask
     from flask import make_response
     
     app = Flask(__name__)
     
     @app.route('/')
     def index():
         response = make_response('<h1>This document carries a cookie!</h1>')
         response.set_cookie('answer', '42')
         return response
     ```

     响应对象属性和方法

     ```shell
     status_code     # HTTP 数字状态码
     headers		    # 类似字典的对象，包含响应发送的全部头部
     set_cookie()    # COOKIE
     delete_cookie() # 删除cookie
     content_length  # 响应主体长度
     content_type    # 响应主体的媒体类型
     set_data()      # 使用字符串或字节值设定响应
     get_data()      # 获取响应主体
     ```

2. 重定向

   ```python
   from flask import Flask
   from flask import redirect
   
   app = Flask(__name__)
   
   @app.route('/')
   def index():
       return redirect('http://www.baidu.com')
   ```

   

3. 错误处理

   ```python
   from flask import Flask
   from flask import redirect,abort
   
   app = Flask(__name__)
   
   @app.route('/')
   def index():
       return redirect('http://www.baidu.com')
   
   @app.route('/user/<id>')
   def get_user(id):
       if id == '123':
           abort(404)
       return '<h1>Hello,{}</h1>'.format(id)
   ```





# 第三章 模板



## 3.1 Jinja2模板引擎



## 3.2 使用Flask-Bootstrap集成Bootstrap



## 3.3 自定义错误页面



## 3.4 链接



## 3.5 静态文件



## 3.6 使用Flask-Moment本地化日期和时间









# 第四章 Web表单



## 4.1 配置





## 4.2 表单类





## 4.3 把表单渲染成HTML





## 4.4 在视图函数中处理表单





## 4.5 重定向和用户会话





## 4.6 闪现消息

