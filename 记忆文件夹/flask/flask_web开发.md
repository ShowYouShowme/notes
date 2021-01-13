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

1. 安装flask-monent

   ```shell
   pip install flask-moment
   ```

2. 引入Moment.js

   ```shell
   # templates/base.html
   
   {% block scripts %}
   {{ super() }}
   {{ moment.include_moment() }}
   {% endblock %}
   ```

3. 修改模板index.html

   ```html
   {% extends "base.html" %}
   
   {% block title %} Flask - Page Not Found{% endblock %}
   
   
   {% block page_content %}
   <div class="page-header">
   
   </div>
       <p>local time is {{ moment(current_time).format('LLL') }}</p>
       <p>That is {{ moment(current_time).fromNow(refresh=True) }}</p>
   {% endblock %}
   ```

   

4. 在hello.py中初始化Flask-Moment

   ```python
   from flask_moment import  Moment
   
   app = Flask(__name__)
   moment = Moment(app)
   ```

5. 在hello.py中添加datetime变量

   ```python
   from datetime import datetime
   
   @app.route('/')
   def index():
       return render_template('index.html', current_time=datetime.utcnow())
   ```

   







# 第四章 Web表单



## 4.1 配置

1. 安装WTF包

   ```shell
   pip install flask-wtf
   ```

2. 配置密钥

   ```shell
   app.config['SECRET_KEY'] = 'hard to guess string'
   ```

   



## 4.2 表单类

1. 继承自FlaskForm类

2. 示例

   ```python
   class NameFrom(FlaskForm):
       name = StringField('What is your name', validators=[DataRequired()])
       submit = SubmitField('Submit')
   ```

   



## 4.3 把表单渲染成HTML

+ 调用表单字段渲染

  ```python
  from flask import Flask,render_template
  from flask_bootstrap import Bootstrap
  from flask_wtf import FlaskForm
  from wtforms import StringField, SubmitField
  from wtforms.validators import DataRequired
  app = Flask(__name__)
  bootstrap = Bootstrap(app) # 初始化扩展
  app.config['SECRET_KEY'] = 'hard to guess string'
  
  
  class NameFrom(FlaskForm):
      name = StringField('What is your name', validators=[DataRequired()])
      submit = SubmitField('Submit')
  
  
  @app.route('/')
  def index():
      return render_template('index.html', form=NameFrom())
  ```

  ```html
  {% extends "base.html" %}
  
  {% block title %} Flask - Page Not Found{% endblock %}
  
  
  {% block page_content %}
  <div class="page-header">
  
  </div>
  
  <form method="post">
      {{ form.hidden_tag() }}
      {{ form.name.label }} {{ form.name(id = 'my-text-field') }} <!--指定属性-->
      {{ form.submit() }}
  </form>
  {% endblock %}
  ```

+ 用Bootstrap表单样式渲染

  ```html
  {% extends "base.html" %}
  {% import "bootstrap/wtf.html" as wtf %}   <!--导入依赖-->
  {% block title %} Flask - Page Not Found{% endblock %}
  
  
  {% block page_content %}
  <div class="page-header">
      <h1>Hello, {% if name %} {{ name }}  {% else %} Stranger {% endif %}!</h1>
  </div>
  
  {{ wtf.quick_form(form) }} <!--用辅助函数渲染-->
  {% endblock %}
  ```

  



## 4.4 在视图函数中处理表单

1. 问题：在一个视图函数里面同时处理GET和POST请求
2. 



## 4.5 重定向和用户会话

1. 问题：提交表单后刷新，浏览器会弹出确认警告

2. 利用重定向和会话解决问题

   ```python
   from flask import Flask,render_template,session,redirect,url_for
   from flask_bootstrap import Bootstrap
   from flask_wtf import FlaskForm
   from wtforms import StringField, SubmitField
   from wtforms.validators import DataRequired
   app = Flask(__name__)
   bootstrap = Bootstrap(app) # 初始化扩展
   app.config['SECRET_KEY'] = 'hard to guess string'
   
   
   class NameFrom(FlaskForm):
       name = StringField('What is your name', validators=[DataRequired()])
       submit = SubmitField('Submit')
   
   
   @app.route('/', methods=['GET','POST'])
   def index():
       form = NameFrom()
       if form.validate_on_submit():
           session['name'] = form.name.data  # 用户信息存储到session中
           return redirect(url_for('index')) # 重定向url
       return render_template('index.html', form=NameFrom(), name=session.get('name'))
   ```

   



## 4.6 闪现消息

1. 用于在web上显示提示信息

2. 代码

   ```python
   from flask import Flask,render_template,session,redirect,url_for,flash
   from flask_bootstrap import Bootstrap
   from flask_wtf import FlaskForm
   from wtforms import StringField, SubmitField
   from wtforms.validators import DataRequired
   app = Flask(__name__)
   bootstrap = Bootstrap(app) # 初始化扩展
   app.config['SECRET_KEY'] = 'hard to guess string'
   
   
   class NameFrom(FlaskForm):
       name = StringField('What is your name', validators=[DataRequired()])
       submit = SubmitField('Submit')
   
   
   @app.route('/', methods=['GET','POST'])
   def index():
       form = NameFrom()
       if form.validate_on_submit():
           old_name = session.get('name')
           if old_name is not None and old_name != form.name.data:
               flash('Looks like you have changed your name!')  # FLASH
           session['name'] = form.name.data
           return redirect(url_for('index'))
       return render_template('index.html', form=NameFrom(), name=session.get('name'))
   
   
   
   ```

   ```html
   {% extends "base.html" %}
   {% import "bootstrap/wtf.html" as wtf %}
   {% block title %} Flask - Page Not Found{% endblock %}
   
   
   {% block page_content %}
   <div class="page-header">
       {% for message in get_flashed_messages() %}
       {{ message }}
       {% endfor %}
       <h1>Hello, {% if name %} {{ name }}  {% else %} Stranger {% endif %}!</h1>
   </div>
   
   {{ wtf.quick_form(form) }}
   {% endblock %}
   
   ```



# 第五章 数据库



## 5.1 SQL数据库

介绍型内容，跳过



## 5.2 NoSQL数据库

介绍型内容，跳过



## 5.3 使用SQL还是NoSQL

介绍型内容，跳过

## 5.4 Python数据库框架

1. 常见数据库

   ```shell
   MySQL
   Postgres
   SQLite
   Redis
   MongoDB
   CouchDB
   DynamoDB
   ```

   

2. 选用数据库框架考虑因素

   + 易用性
   + 性能
   + 可移植性
   + Flask集成度

3. 推荐的框架：Flask-SQLALchemy

## 5.5 使用Flask-SQLALchemy管理数据库

1. 安装

   ```shell
   pip install flask-sqlalchemy
   ```

2. 指定URL

   ```shell
   # MySQL
   mysql://${username}:${password}@${hostname}/${database}
   
   # Postgres
   postgresql://${username}:${password}@${hostname}/${database}
   
   # SQLite(Linux,macOS)
   sqlite:////absolute/path/to/database
   
   # SQLite(Windows)
   sqlite:///c:/absolute/path/to/database
   ```

3. 配置URL

   + 配置app.config['SQLALCHEMY_DATABASE_URI'] 
   + 配置app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] 

   ```python
   from flask import Flask
   import os
   from flask_sqlalchemy import SQLAlchemy
   app = Flask(__name__)
   
   basedir = os.path.abspath(os.path.dirname(__file__))
   app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
   app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
   db = SQLAlchemy(app) # 初始化插件
   ```

   

## 5.6 定义模型

```python
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), unique = True)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), unique = True, index = True)
```

<font color=blue>SQLAlchemy的列类型和字段限制条件可以参考page49</font>

## 5.7 关系



## 5.8 数据库操作

1. 可以参考网站https://docs.sqlalchemy.org或者https://www.osgeo.cn/sqlalchemy/

2. 创建表

   ```shell
   # 创建db定义的全部模型对应的表
   db.create_all()
   
   # 删除
   db.drop_all()
   ```

   

3. 插入行

   ```python
   admin_role = Role(name = 'Admin')
   mod_role = Role(name = 'Moderator')
   db.session.add(admin_role)
   db.session.add(mod_role)
   db.session.commit()
   ```

   ```python
   admin_role = Role(name = '11')
   mod_role = Role(name = '22')
   db.session.add_all([admin_role, mod_role]) # 可用add_all一次性添加多个
   db.session.commit()
   ```

   

4. 修改行

   ```python
   # Role是定义的模型
   # 先查询到指定记录,然后再修改
   record = Role.query.filter_by(id = 2).first()
   record.name = 'justin bieber'
   db.session.add(record)
   db.session.commit()
   ```

   

5. 删除行

   ```python
   # 先查询到记录，然后删除
   @app.route('/delete')
   def delete():
       record = Role.query.filter_by(id = 3).first()
       db.session.delete(record)
       db.session.commit()
       return '222'
   ```

   

6. 查询行

   + 查询过滤器

     | 过滤器      | 返回结果                                         |
     | ----------- | ------------------------------------------------ |
     | filter()    | 把过滤器添加到原查询上，返回一个新查询           |
     | filter_by() | 把等值过滤器添加到原查询上，返回一个新查询       |
     | limit()     | 使用指定的值限定原查询返回的结果                 |
     | offset()    | 偏移原查询返回的结果，返回一个新查询             |
     | order_by()  | 根据指定条件对原查询结果进行排序，返回一个新查询 |
     | group_by()  | 根据指定条件对原查询结果进行分组，返回一个新查询 |

     

   + 查询执行方法

     | 执行函数       | 返回结果                                     |
     | -------------- | -------------------------------------------- |
     | all()          | 以列表形式返回查询的所有结果                 |
     | first()        | 返回查询的第一个结果，如果未查到，返回None   |
     | first_or_404() | 返回查询的第一个结果，如果未查到，返回404    |
     | get()          | 返回指定主键对应的行，如不存在，返回None     |
     | get_or_404()   | 返回指定主键对应的行，如不存在，返回404      |
     | count()        | 返回查询结果的数量                           |
     | paginate()     | 返回一个Paginate对象，它包含指定范围内的结果 |

     

## 5.9 在视图函数中操作数据库

```python
from flask import Flask,render_template,session,redirect,url_for,flash
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import os
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
bootstrap = Bootstrap(app) # 初始化扩展
app.config['SECRET_KEY'] = 'hard to guess string'

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class NameFrom(FlaskForm):
    name = StringField('What is your name', validators=[DataRequired()])
    submit = SubmitField('Submit')


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    name = db.Column(db.String(64), unique = True)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), unique = True, index = True)


@app.route('/', methods=['GET','POST'])
def index():
    form = NameFrom()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username = form.name.data)
            db.session.add(user)
            db.session.commit()
            session['known'] = False
        else:
            session['known'] = True
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('index'))
    name = session.get('name')
    known = session.get('known', False)
    return render_template('index.html', form=NameFrom(), name= name, known = known)

if __name__ == '__main__':
    app.run(debug=True)
```

HTML
```html
{% extends "base.html" %}
{% import "bootstrap/wtf.html" as wtf %}
{% block title %} Flask - Page Not Found{% endblock %}


{% block page_content %}
<div class="page-header">
    {% for message in get_flashed_messages() %}
    {{ message }}
    {% endfor %}
    <h1>Hello, {% if name %} {{ name }}  {% else %} Stranger {% endif %}!</h1>
    <h1> {% if not known %} please to meet you! {% else %} happy to see you again! {% endif %} </h1>
</div>

{{ wtf.quick_form(form) }}
{% endblock %}

```



## 5.10 集成Python shell

+ 跳过，这节内容没用

## 5.11 使用Flask-Migrate实现数据库迁移

1. 创建迁移仓库

   + 安装依赖

     ```shell
     pip install flask-migrate
     ```

   + python代码

     ```python
     from flask_migrate import Migrate
     
     # ...
     db = SQLAlchemy(app)
     migrate = Migrate(app, db)
     ```

   + 创建仓库

     ```shell
     flask db init
     ```

     

2. 创建迁移脚本

   + 命令

     ```shell
     flask db migrate -m "add table student"
     ```

   + 细节

     ```shell
     # 脚本中有两个函数 upgrade() 和 downgrade()
     
     def upgrade():
         # ### commands auto generated by Alembic - please adjust! ###
         op.create_table('student',
         sa.Column('id', sa.Integer(), nullable=False),
         sa.Column('level', sa.Integer(), nullable=True),
         sa.PrimaryKeyConstraint('id')
         )
         # ### end Alembic commands ###
     
     
     def downgrade():
         # ### commands auto generated by Alembic - please adjust! ###
         op.drop_table('student')
         # ### end Alembic commands ###
     ```

   + 过程：先在代码中修改表模型，然后执行命令`flask db migrate -m "add table student"`生成脚本，最后执行`flask db upgrade`将变化应用到数据库

3. 更新数据库

   ```shell
   flask db upgrade # 将变化应用到数据库
   
   flask db downgrade # 还原前一个脚本对数据库的改动
   ```

4. 总结

   1. 修改数据库模型
   2. 执行`flask db migrate`，生成迁移脚本
   3. 检查自动生成的脚本，改正不正确的地方
   4. 执行`flask db upgrade`，把改动应用到数据库中





# 第六章 电子邮件

 

## 6.1 提供电子邮件支持

1. 安装依赖

   ```shell
   pip install Flask-Mail
   ```

   

2. SMTP服务器配置

   | 配置          | 默认值    | 说明                        |
   | ------------- | --------- | --------------------------- |
   | MAIL_SERVER   | localhost | 电子邮件服务器的域名/IP地址 |
   | MAIL_PORT     | 25        | 服务器端口号                |
   | MAIL_USE_TLS  | False     | 是否启用TLS                 |
   | MAIL_USE_SSL  | False     | 是否启用SSL                 |
   | MAIL_USERNAME | None      | 发件人用户名                |
   | MAIL_PASSWORD | None      | 发件人授权码                |

3. 初始化

   ```python
   from flask import Flask
   from flask_mail import Mail, Message
   
   app =Flask(__name__)
   mail=Mail(app)
   
   # imap和pop3的选择 ==> 优先imap
   app.config['MAIL_SERVER']='smtp.126.com'
   app.config['MAIL_PORT'] = 465
   app.config['MAIL_USERNAME'] = 'wzc_0618@126.com'
   app.config['MAIL_PASSWORD'] = 'SAGJEOZIYUNKVLLH' # 授权码不是密码
   app.config['MAIL_USE_TLS'] = False
   app.config['MAIL_USE_SSL'] = True
   mail = Mail(app)
   ```

   

## 6.2 集成电子邮件发送功能

```python
from flask import Flask,render_template,session,redirect,url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import os
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Message, Mail
app = Flask(__name__)
bootstrap = Bootstrap(app) # 初始化扩展
app.config['SECRET_KEY'] = 'hard to guess string'

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.config['MAIL_SERVER']='smtp.126.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'wzc_0618@126.com'
app.config['MAIL_PASSWORD'] = 'SAGJEOZIYUNKVLLH' # 授权码不是密码
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)


class NameFrom(FlaskForm):
    name = StringField('What is your name', validators=[DataRequired()])
    submit = SubmitField('Submit')

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), unique = True, index = True)



def send_email(to, subject, template, **kwargs):
    msg = Message(subject, sender = 'wzc_0618@126.com', recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    mail.send(msg)

@app.route('/', methods=['GET','POST'])
def index():
    form = NameFrom()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            db.session.commit()
            session['known'] = False
            #
            send_email('861949775@qq.com', 'flask learn code', 'mail/new_user', user=user)
        else:
            session['known'] = True
        session['name'] = form.name.data
        return redirect(url_for('index'))
    return render_template('index.html', form=form,name=session.get('name'),
                           known = session.get('known', False))
if __name__ == '__main__':
    app.run(debug=True)
```



## 6.3 异步发送电子邮件

```python
# 创建线程来发送电子邮件
from threading import Thread
def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(to, subject, template, **kwargs):
    msg = Message(subject, sender = 'wzc_0618@126.com', recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=send_async_email, args=[app,msg])
    thr.start()
    return thr
```







# 第七章 大型应用结构



## 7.1 项目结构





## 7.2 配置选项



### 7.3.1 使用应用工厂函数

***



### 7.3.2 在蓝本中实现应用功能

***



## 7.3 应用包

 

## 7.4 应用脚本



## 7.5 需求文件



## 7.6 单元测试



## 7.7 创建数据库



## 7.8 运行应用

