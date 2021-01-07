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

1. index.html

   ```html
   <h1>Hello World!</h1>
   ```

2. user.html

   ```html
   <h1>Hello, {{name}}!</h1>
   ```

   



### 3.1.1 渲染模板

***

```python
from flask import Flask,render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)
```





### 3.1.2 变量

***





### 3.1.3 控制结构

***

1. 条件判断

   ```html
   {% if user %}
       Hello, {{user}}
   {% else %}
       Hello,stranger!
   {% endif %}
   ```

2. 循环

   ```shell
   <ul>
       {% for comment in comments %}
           <li>{{ comment }}</li>
       {% endfor %}
   </ul>
   ```

   ```python
   from flask import Flask,render_template
   
   app = Flask(__name__)
   
   @app.route('/')
   def index():
       return render_template('index.html')
   
   @app.route('/user')
   def user():
       comments = ['11','22','33','44']
       return render_template('user.html', comments=comments)
   ```

3. 宏（类似Python的函数）：可以把宏保存在单独的文件中，需要时导入

   ```html
   {% macro render_comment(comment) %}
       <li>{{ comment }}</li>
   {% endmacro %}
   <ul>
       {% for comment in comments %}
           {{ render_comment(comment) }}
       {% endfor %}
   </ul>
   ```

4. <font color=blue>模板继承</font>

   base.html

   ```html
   <html>
       <head>
           {% block head %}
               <title>{% block title %} {% endblock %} - My Application</title>
           {% endblock %}
       </head>
   
       <body>
           {% block body %}
           {% endblock %}
       </body>
   </html>
   ```

   ext.html：super()引用基模板同名区块中的内容

   ```html
   {% extends "base.html" %}
   {% block title %}Index {% endblock %}
   
   {% block head %}
           {{ super() }}
   <style>
   </style>
   {% endblock %}
   
   {% block body %}
   <h1>Hello,World!</h1>
   {% endblock %}
   ```

   





## 3.2 使用Flask-Bootstrap集成Bootstrap

1.  集成Bootstrap

   ```shell
   # 安装依赖
   pip install flask-bootstrap
   
   # 初始化
   from flask import Flask,render_template
   from flask_bootstrap import Bootstrap
   
   app = Flask(__name__)
   bootstrap = Bootstrap(app) # 初始化扩展
   
   ```

   继承模板

   ```html
   {% extends "bootstrap/base.html" %}
   
   {% block title %}
   Flask
   {% endblock %}
   
   {% block content %}
       <div class="container">
           <div class="page-header">
               <h1>Hello, {{name}}!</h1>
           </div>
       </div>
   {% endblock %}
   ```

   ```python
   from flask import Flask,render_template
   from flask_bootstrap import Bootstrap
   
   app = Flask(__name__)
   bootstrap = Bootstrap(app) # 初始化扩展
   
   @app.route('/')
   def index():
       return render_template('ext.html')
   
   @app.route('/user')
   def user():
       return render_template('user.html', name='nash') 
   ```

   

## 3.3 自定义错误页面

1. 常见错误类型

   + 404：请求未知页面
   + 500：应用有未处理的异常

   

2.示例代码：代码必须用非debug模式运行，否则无法看到500的页面

+ hello.py

  ```python
  from flask import Flask,render_template
  from flask_bootstrap import Bootstrap
  
  app = Flask(__name__)
  bootstrap = Bootstrap(app) # 初始化扩展
  
  @app.route('/')
  def index():
      a = '1' + 2
      return render_template('ext.html')
  
  @app.route('/user')
  def user():
      return render_template('user.html', name='nash')
  
  @app.errorhandler(404)
  def page_not_found(e):
      return render_template('404.html'),404
  
  @app.errorhandler(500)
  def internal_server_error(e):
      return render_template('500.html'),500
  ```

+ base.html

  ```html
  {% extends "bootstrap/base.html" %}
  
  {% block title %}Flasky{% endblock %}
  
  {% block navbar %}
  <div class="navbar navbar-inverse" role="navigation">
      <div class="container">
          <div class="navbar-header">
              <button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-collapse">
                  <span class="sr-only">Toggle navigation</span>
                  <span class="icon-bar"></span>
                  <span class="icon-bar"></span>
                  <span class="icon-bar"></span>
              </button>
              <a class="navbar-brand" href="/">Flasky</a>
          </div>
          <div class="navbar-collapse collapse">
              <ul class="nav navbar-nav">
                  <li><a href="/">Home</a></li>
              </ul>
          </div>
      </div>
  </div>
  {% endblock %}
  
  {% block content %}
  <div class="container">
      {% block page_content %}{% endblock %}
  </div>
  {% endblock %}
  
  ```

+ 404.html

  ```html
  {% extends "base.html" %}
  
  {% block title %} Flask - Page Not Found{% endblock %}
  
  {% block page_content %}
  <div class="page-header">
      <h1>Not Found</h1>
  </div>
  {% endblock %}
  ```

+ 500.html

  ```html
  {% extends "base.html" %}
  
  {% block title %}Flasky{% endblock %}
  
  {% block page_content %}
  <div class="page-header">
      <h1>Hllo, {{name}}!</h1>
  </div>
  {% endblock %}
  ```

  

## 3.4 链接

1. 生成动态链接：url_for

   ```shell
   url_for('index') # 返回'/'
   
   url_for('index', _external=True) # 返回 http://localhost:5000/
   
   url_for('user', name='jonh', page=2, version=1) # 传入参数
   ```

   

## 3.5 静态文件

1. 文件放在static的子目录下

2. 示例代码

   ```python
   from flask import Flask,render_template,redirect,url_for
   from flask_bootstrap import Bootstrap
   
   app = Flask(__name__)
   bootstrap = Bootstrap(app) # 初始化扩展
   
   @app.route('/')
   def index():
       return redirect(url_for('static',filename='html/index.html'))
   ```

   index.html

   ```html
   <!DOCTYPE html>
   <html lang="en">
   <head>
       <meta charset="UTF-8">
       <title>Hi</title>
   </head>
   <body>
       <h1>Say hi to you!</h1>
   </body>
   </html>
   ```

   

## 3.6 使用Flask-Moment本地化日期和时间









# 第四章 Web表单



## 4.1 配置





## 4.2 表单类





## 4.3 把表单渲染成HTML





## 4.4 在视图函数中处理表单





## 4.5 重定向和用户会话





## 4.6 闪现消息

