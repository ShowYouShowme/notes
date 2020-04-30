## 01 第一个应用

***

```python
import flask

app = flask.Flask(__name__)
@app.route('/')
def hello_world():
    return 'hello_world!'

if __name__ == '__main__':
    # 启动debug模式时，代码修改了会自动重新加载无需重启服务
    app.run(host = '127.0.0.1', port = '1234', debug=True)
```



## 02 路由

***

+ 用`route装饰器`

  ```python
  @app.route('/hello')
  def say_hello():
      return 'say hello to you!'
  ```

+ 用`add_url_rule函数绑定`

  ```python
  def good_morning():
      return "good morning to you!"
  
  app.add_url_rule('/morning',  view_func=good_morning)
  ```



## 03 动态url

***

+ 字符串变量路由

  ```python
  @app.route('/hello/<name>')
  def hello_to_someone(name):
      return 'hello {0} !'.format(name)
  ```

+ 转换器路由

  1. int转换器     => 接受整数

  2. float转换器 => 接受浮点数

  3. path转化器 => 接受用作木楼分隔符的斜杠

  4. 示例代码

     ```python
     @app.route('/blog/<int:postID>')
     def show_blog(postID):
         return 'blog num {0}'.format(postID)
     
     
     @app.route('/rev/<float:revNo>')
     def revision(revNo):
         return 'revision number is {0}'.format(revNo)
       
     # 请求/hello/ 时，直接返回结果
     # 请求/hello 时，重定向到/hello/
     @app.route('/hello/')
     def say_hello():
         return 'say hello to you!'  
     ```

+ 利用函数构建动态url

  ```python
  import flask
  
  app = flask.Flask(__name__)
  @app.route('/admin')
  def hello_admin():
      return 'Hello Admin'
  
  @app.route('/guest/<guest>')
  def hello_guest(guest):
      return 'hello {0} as Guest !'.format(guest)
  
  @app.route('/user/<name>')
  def hello_user(name):
      if name == 'admin':
          # 函数名是参数
          return flask.redirect(flask.url_for('hello_admin'))
      else:
          # 用关键字参数来给函数传入参数
          return flask.redirect(flask.url_for('hello_guest', guest = name))
  ```



## 04 http

***

+ 前提 ==> 默认情况下路由响应GET方法

+ 注册POST方法的路由

  ```python
  from flask import  Flask, url_for, redirect, request, render_template
  app = Flask(__name__)
  
  @app.route('/')
  def index():
      return render_template('login.html')
  
  @app.route('/success/<name>')
  def success(name):
      return 'welcome {0}'.format(name)
  
  @app.route('/login', methods = ['POST', 'GET'])
  def login():
      # python 变量作用范围不像C++只作用于'{}'
      user : str = None
      if request.method == 'POST':
          user = request.form['nm']
          return redirect(url_for('success', name = user))
      else:
          user = request.args.get('nm')
          return redirect(url_for('success', name = user))
  if __name__ == '__main__':
      # 启动debug模式时，代码修改了会自动重新加载无需重启服务
      app.run(host = '127.0.0.1', port = '1234', debug=True)
  ```

  login.html

  ```html
  <!DOCTYPE html>
  <html>
     <body>
  
        <form action = "http://localhost:1234/login" method = "get">
           <p>Enter Name:</p>
           <p><input type = "text" name = "nm" /></p>
           <p><input type = "submit" value = "submit" /></p>
        </form>
  
     </body>
  </html>
  ```

  



## 05 模板

***

+ 前提 ==> 在python里生成html内容很麻烦，比如放置变量数据和python语言元素(条件或循环)

+ 解决方案 ==> 利用jinja2模板

+ 模板相关知识

  1. 模板文件位于`templates`目录里

  2. 模板分隔符

     ```python
     1.{% ... %} 用于语句
     
     2.{{ ... }} 用于变量
     
     3.{# ... #} 注释
     
     4.# ... ## 用于行语句
     ```

+ 例子

  1. 变量替换

     ```python
     @app.route('/hello/<user>')
     def hello_name(user):
         return render_template('hello.html', name = user)
     ```

     hello.html

     ```html
     <!doctype html>
     <h1>Hello {{ name }}!</h1>
     ```

  2. 使用条件语句

     ```python
     @app.route('/hello/<float:score>')
     def hello_name(score):
         return render_template('hello.html', marks = score)
     ```

     hello.html

     ```html
     <!doctype html>
     
     {% if marks > 50 %}
     <h1>Your result is pass!</h1>
     {% else %}
     <h1>Your result is fail!</h1>
     {% endif %}
     ```

  3. 使用循环语句

     ```python
     @app.route('/result')
     def result():
         dict = {
             'phy' : 50,
             'che' : 60,
             'maths' : 70
         }
         return render_template('result.html', result = dict)
     ```

     result.html

     ```html
     <!DOCTYPE html>
     <html>
     <body>
      <table border="1">
         {% for key in result %}
         <tr>
            <th> {{ key }} </th>>
            <td> {{ result[key] }} </td>
         </tr>
        {% endfor %}
       </table>
     </body>
     </html>
     ```



## 06 静态文件

***

+ 前提 => 静态文件放在路径`/static`

+ 示例

  1. 例子一

     ```python
     @app.route('/')
     def index():
         return render_template('index.html')
     ```

     index.html

     ```html
     <html>
     
         <head>
             <script type="text/javascript" src = "{{ url_for('static', filename = 'hello.js') }}">
     
             </script>
         </head>
     
         <body>
             <input type = "button" onclick="sayHello()" value="Say Hello" />
         </body>
     
     </html>
     ```

     hello.js

     ```javascript
     function sayHello(){
         alert("Hello world!")
     }
     ```

  2. 例子二

     + python和javascript的代码不变

     + index.html

       ```html
       <html>
       
           <head>
               <script type="text/javascript" src = "/static/hello.js">
       
               </script>
           </head>
       
           <body>
               <input type = "button" onclick="sayHello()" value="Say Hello" />
           </body>
       
       </html>
       ```

  3. 例子三

     ```python
     @app.route('/')
     def index():
         url = url_for('static', filename = 'hello.js')
         return render_template('index.html', path_to_hello = url)
     ```

     index.html

     ```html
     <html>
     
         <head>
             <script type="text/javascript" src = "{{ path_to_hello }}">
     
             </script>
         </head>
     
         <body>
             <input type = "button" onclick="sayHello()" value="Say Hello" />
         </body>
     
     </html>
     ```

     javascript的代码不变

  

  ## 07 Flask Request对象

  ***

  + form => 字典对象，保持urlencode的表单参数
  + args => GET请求查询字符串的内容
  + cookies => cookies相关信息
  + files => 上传文件相关的数据
  + method => 当前请求方法

  

  

  ## 08 表单数据发送到模板

  ***

  + 示例代码

    ```python
    @app.route('/')
    def student():
        return render_template('student.html')
    
    @app.route('/result', methods = ['POST'])
    def result():
        result = request.form
        return render_template('result.html', result = result)
    ```

    student.html

    ```html
      <form action = "http://localhost:1234/result" method = "POST">
         <p>Name <input type = "text" name = "Name" /></p>
         <p>Physics <input type = "text" name = "Physics" /></p>
         <p>Chemistry <input type = "text" name = "chemistry" /></p>
         <p>Maths <input type ="text" name = "Mathematics" /></p>
         <p><input type = "submit" value = "submit" /></p>
      </form>
    ```

    result.html

    ```html
    <!DOCTYPE html>
    <html>
    <body>
     <table border="1">
        {% for key in result %}
        <tr>
           <th> {{ key }} </th>>
           <td> {{ result[key] }} </td>
        </tr>
       {% endfor %}
      </table>
    </body>
    </html>
    ```

  

  ## 09 cookies

  ***

  + 设置cookies

    ```python
    1. 使用make_response()函数从视图函数的返回值获取响应对象
    2. 使用响应对象的set_cookie()函数来存储cookie
    ```

  + 读取cookies

    ```python
    request.cookies属性的get()方法用于读取cookie
    ```

  + 示例代码

    ```python
    @app.route('/')
    def student():
        return render_template('index.html')
      
    @app.route('/setcookie', methods = ["POST"])
    def set_cookie():
        user : str = request.form["nm"]
        resp = make_response(render_template('read_cookie.html'))
        resp.set_cookie("userID", user)
        return resp
    
    @app.route('/getcookie')
    def get_cookie():
        name = request.cookies.get("userID")
        return 'welcome {0}'.format(name)
    ```

    index.html

    ```html
    <html>
    
    <body>
    
        <form action = "/setcookie" method="post">
            <p>
                <h3>Enter userID</h3>
            </p>
            <p>
                <input type="text" name="nm" />
            </p>
            <p>
                <input type="submit" value="Login" />
            </p>
        </form>
    </body>
    
    </html>
    ```

    read_cookie.html

    ```html
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>read cookies</title>
    </head>
    <body>
        <a href="/getcookie" target="_blank">
            click here to get cookies!
        </a>
    </body>
    </html>
    ```

  

  ## 10 session

  ***

  + 知识点

    ```python
    1.session 可以认为是socket连接的一个封装，每个client对应一个session，可以往session里面存储数据
    2.服务器会对session数据签名，因此要指定SECRET_KEY
    ```

  + 示例代码

    ```python
    from flask import  Flask, url_for, redirect, request, render_template, make_response, session
    app = Flask(__name__)
    app.secret_key = " this is random string"
    @app.route('/')
    def index():
        if 'username' in session:
            username = session['username']
            return 'Login as {0} <br> <a href = "/logout"> click here to log out</a>'.format(username)
        else:
            return '''
            you are not logged in <br>
            <a href = "/login"> click here to login</a>
            '''
    
    @app.route('/login', methods = ['POST', 'GET'])
    def login():
        if request.method == "POST":
            session["username"] = request.form["username"]
            return redirect(url_for("index"))
        else:
            return '''
            <form action = '/login' method = 'post'>
                <p>
                    <input type = 'text' name = 'username' />
                </p>
                <p>
                    <input type = 'submit' value = 'Login' />
                </p>
            </form>
            '''
    
    @app.route("/logout")
    def logout():
        session.pop("username", None)
        return redirect(url_for("index"))
    if __name__ == '__main__':
        # 启动debug模式时，代码修改了会自动重新加载无需重启服务
        app.run(host = '0.0.0.0', port = '1234', debug=True)
    ```

    测试

    ```shell
    1. 在本机用浏览器测试
    2. 在虚拟机里面用curl测试
    ```

  

  ## 11 重定向

  ***

  + 知识点

    1. 函数原型

       ```python
       redirect(location, code=302, Response=None)
       ```

    2. 状态吗

       ```shell
       300:MULTIPLE_CHOICES
       301:MOVED_PERMANENTLY
       302:FOUND
       303:SEE_OTHER
       304:NOT_MODIFIED
       305:USE_PROXY
       306:RESERVED
       307:TEMPORARY_REDIRECT
       ```

  + 示例代码

    1. 例子一

       ```python
       @app.route('/')
       def index():
           return render_template('login.html')
       
       @app.route('/login', methods = ['POST', 'GET'])
       def login():
           if request.method == 'POST' and request.form['username'] == 'admin':
               return redirect(url_for('success'))
           else:
               return redirect(url_for('index'))
       
       @app.route('/success')
       def success():
           return 'logged in successfully!' 
       ```

       login.html

       ```html
       <!DOCTYPE html>
       <html>
          <body>
       
             <form action = "http://localhost:1234/login" method = "post">
                <p>Enter Name:</p>
                <p><input type = "text" name = "username" /></p>
                <p><input type = "submit" value = "submit" /></p>
             </form>
       
          </body>
       </html>
       ```

    2. 例子二 => abort返回错误信息

       函数原型

       ```python
       flask.abort(code)
       ```

       错误码

       ```she l
       400:错误请求
       401:身份未交验
       403:Forbidden
       404:Not Found
       406:Not Acceptable
       415:不支持的媒体类型
       429:请求过多
       ```

       

       ```python
       # login.html 和上面一样
       
       @app.route('/')
       def index():
           return render_template('login.html')
       
       @app.route('/login', methods = ['POST', 'GET'])
       def login():
           if request.method == 'POST':
               if request.form['username'] == 'admin':
                   return redirect(url_for('success'))
               else:
                   abort(401) # 返回错误信息给客户端
           else:
               return redirect(url_for('index'))
       
       @app.route('/success')
       def success():
           return 'logged in successfully!'
       ```



## 12 消息闪现

***

+ 作用 => 向用户提供有关交互的反馈，类似javascript的警报

+ 代码

  ```python
  from flask import  Flask, url_for, redirect, request, render_template, flash
  app = Flask(__name__)
  app.secret_key = " this is random string"
  
  @app.route('/')
  def index():
      return render_template('index.html')
  
  @app.route('/login', methods = ['GET', 'POST'])
  def login():
      error : str = None
      if request.method == 'POST':
          if request.form['username'] != 'admin' or \
              request.form['password'] != 'admin':
              error = 'Invalid username or password. Please try again!'
              return render_template('login.html', error=error)
          else:
              flash('You were successfully logged in')
              return redirect(url_for('index'))
      else:
          return render_template('login.html', error = error)
  
  if __name__ == '__main__':
      # 启动debug模式时，代码修改了会自动重新加载无需重启服务
      app.run(host = '0.0.0.0', port = '1234', debug=True)
  ```

  index.html

  ```html
  <html>
  
  <body>
  
      {% with messages = get_flashed_messages() %}
          {% if messages %}
          <ul>
              {% for message in messages %}
              <li>{{ message }}</li>
              {% endfor %}
          </ul>>
          {% endif %}
      {% endwith %}
      <h1>Flask Message Flashing Example</h1>
      Do you want to <a href="/login">log in ?</a>
  </body>
  
  </html>
  ```

  login.html

  ```html
  <!DOCTYPE html>
  <html>
     <body>
  
        {% if error %}
        <p><strong>Error:</strong>{{ error }}</p>
        {% endif %}
        <form action = "http://localhost:1234/login" method = "post">
           <p>Login</p>
           <p>Username:<input type = "text" name = "username" /></p>
           <p>Password:<input type = "password" name = "password" /></p>
           <p><input type = "submit" value = "submit" /></p>
        </form>
  
     </body>
  </html>
  ```

  



## 13 文件上传

***

+ 代码

  ```python
  from flask import  Flask,request, render_template
  from werkzeug.utils import secure_filename
  app = Flask(__name__)
  app.secret_key = " this is random string"
  
  @app.route('/')
  def index():
      return render_template('upload.html')
  
  @app.route('/uploader', methods = ['POST'])
  def upload_file():
      f1 = request.files['f']
      f1.save(secure_filename(f1.filename))
      return 'file upload successfully!'
  
  
  if __name__ == '__main__':
      # 启动debug模式时，代码修改了会自动重新加载无需重启服务
      app.run(host = '0.0.0.0', port = '1234', debug=True)
  ```

  upload.html

  ```html
  <!DOCTYPE html>
  <html lang="en">
  <head>
      <meta charset="UTF-8">
      <title>upload</title>
  </head>
  <body>
  
      <form action="/uploader" method="post" enctype="multipart/form-data">
          <input type="file" name="f"/>
          <input type="submit" />
      </form>
  </body>
  </html>
  ```

  



## 14 拓展

***



### 14-1 邮件

***

+ 知识点 => 发送邮件的流程

+ 流程

  1. 安装扩展

     ```shell
     pip install Flask-Mail
     ```

  2. 配置应用程序参数

     ```shell
     MAIL_SERVER:电子邮件服务器的域名/IP地址
     MAIL_PORT:  服务器端口号
     MAIL_USE_TLS: 是否启用TLS
     MAIL_USE_SSL: 是否启用SSL
     MAIL_USERNAME:发件人用户名
     MAIL_PASSWORD:发件人授权码
     ```

     

  3. 构造对象`Mail`和`Message`发送邮件

+ 示例代码

  ```python
  # 发送邮件的demo
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
  
  @app.route("/")
  def index():
     msg = Message('new day', sender = 'wzc_0618@126.com', recipients = ['861949775@qq.com'])
     msg.body = "Hello Flask message sent from Flask-Mail"
     mail.send(msg)
     return "Sent"
  
  if __name__ == '__main__':
     app.run(debug = True, port=7890)
  ```

  

### 14-2 WTF

***



### 14-3 SQLite

***

+ 示例代码

  ```python
  from flask import Flask, render_template, request
  import sqlite3
  app = Flask(__name__)
  
  # 创建表 第一次请求到来前触发
  @app.before_first_request
  def create_table():
      conn = sqlite3.connect('database.db')
      print("open database successfully")
      conn.execute('CREATE TABLE students (name TEXT, addr TEXT, city TEXT, pin TEXT)')
      print("Table created successfully!")
      conn.close()
  
  @app.route('/')
  def home():
      return render_template('home.html')
  
  @app.route('/enter_new')
  def new_student():
      return render_template('student.html')
  
  @app.route('/add_record', methods = ["POST"])
  def add_record():
      try:
          name = request.form['name']
          address = request.form['address']
          city = request.form['city']
          pin = request.form['pin_code']
  
          conn = sqlite3.connect("database.db")
          cursor = conn.cursor()
          cursor.execute("INSERT INTO students (name, addr, city, pin) VALUES (?, ?, ?, ?)", (name, address, city, pin))
          conn.commit()
          msg = "Record successfully added"
      except Exception as e:
          conn.rollback()
          msg = "error in insert operation"
          print(e)
      finally:
          return render_template('result.html', msg = msg)
          conn.close()
  
  @app.route('/list')
  def list():
      conn = sqlite3.connect("database.db")
      conn.row_factory = sqlite3.Row
      cursor = conn.cursor()
      cursor.execute("select * from students")
      rows = cursor.fetchall()
      return render_template("list.html", rows = rows)
  
  if __name__ == '__main__':
      app.run(debug=True, host="127.0.0.1", port=2345)
  ```

  home.html

  ```html
  <!DOCTYPE html>
  <html lang="en">
  <head>
      <meta charset="UTF-8">
      <title>Title</title>
  </head>
  <body>
      <h1>
          <a href="/enter_new">
              Add New Record
          </a>
      </h1>
  
      <h1>
          <a href="/list">
              Show List
          </a>
      </h1>
  </body>
  </html>
  ```

  student.html

  ```html
    <form action = "http://localhost:2345/add_record" method = "POST">
       <p>Name <input type = "text" name = "name" /></p>
       <p>Address <input type = "text" name = "address" /></p>
       <p>city <input type = "text" name = "city" /></p>
       <p>Pincode <input type ="text" name = "pin_code" /></p>
       <p><input type = "submit" value = "submit" /></p>
    </form>
  ```

  result.html

  ```html
  <!DOCTYPE html>
  <html>
  <body>
      result of addition : {{ msg }}
      <h2>
          <a href="/">
              go back to home page!
          </a>
      </h2>
  </body>
  </html>
  ```

  list.html

  ```html
  <!doctype html>
  <html>
     <body>
  
        <table border = 1>
           <thead>
              <td>Name</td>
              <td>Address>/td<
              <td>city</td>
              <td>Pincode</td>
           </thead>
  
           {% for row in rows %}
              <tr>
                 <td>{{row["name"]}}</td>
                 <td>{{row["addr"]}}</td>
                 <td> {{ row["city"]}}</td>
                 <td>{{row['pin']}}</td>
              </tr>
           {% endfor %}
        </table>
  
        <a href = "/">Go back to home page</a>
  
     </body>
  </html>
  ```

  

### 14-4 SQLAIchemy

***

+ 简介：**SQLAlchemy**是python的`Object Relation Mapping`包。

+ 安装

  ```shell
  pip3 install flask-sqlalchemy
  ```

+ 示例代码

  ```python
  from flask import Flask,render_template,request,flash,redirect,url_for
  from flask_sqlalchemy import SQLAlchemy
  app = Flask(__name__)
  app.secret_key = "i am your doom!"
  
  app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
  db = SQLAlchemy(app)
  # 将表映射为class
  class Student(db.Model):
      global db
      id      = db.Column(db.Integer, primary_key = True)
      name    = db.Column(db.String(100))
      city    = db.Column(db.String(50))
      address = db.Column(db.String(200))
      pin     = db.Column(db.String(10))
      def __init__(self, name : str, city : str, address : str, pin : str):
          self.name       = name
          self.city       = city
          self.address    = address
          self.pin        = pin
  # 创建表
  @app.before_first_request
  def create_table():
      global db
      db.create_all()
  
  @app.route('/')
  def show_all():
      return render_template('show_all.html', students = Student.query.all())
  
  @app.route('/new', methods = ['GET', 'POST'])
  def new():
      if request.method == 'POST':
          if not request.form['name'] or \
              not request.form['city'] or \
              not request.form['address'] or \
              not request.form['pincode']:
              flash('please enter all the fields', 'error')
              return render_template('new.html')
          else:
              student = Student(request.form['name'], request.form['city'],
                                request.form['address'], request.form['pincode'])
              db.session.add(student) # 插入记录
              db.session.commit()
              flash('Record was successfully addedd')
              return redirect(url_for('show_all'))
      else:
          return render_template('new.html')
  
  if __name__ == '__main__':
      app.run(debug=True, host="127.0.0.1", port=2345)
  ```

  show_all.html

  ```html
  <!DOCTYPE html>
  <html lang="en">
  <head>
      <meta charset="UTF-8">
      <title>show_all</title>
  </head>
  <body>
  
  
      <h3>
          <a href="/new">Add student</a>
      </h3>
      <table border="1">
          <tr>
              <th>Name</th>
              <th>City</th>
              <th>Address</th>
              <th>Pin</th>
          </tr>
  
          {% for student in students %}
          <tr>
              <td>{{ student.name }}</td>
              <td>{{ student.city }}</td>
              <td>{{ student.address }}</td>
              <td>{{ student.pin }}</td>
          </tr>
          {% endfor %}
      </table>
  </body>
  </html>
  ```

  new.html

  ```html
  <!DOCTYPE html>
  <html lang="en">
  <head>
      <meta charset="UTF-8">
      <title>new</title>
  </head>
  <body>
  
          {% for category, message in get_flashed_messages(with_categories = true) %}
           <div class = "alert alert-danger">
              {{ message }}
           </div>
        {% endfor %}
      <form action="{{ request.path }}" method="post">
          <input type="text" name="name" placeholder="Name"/> Name<br/>
          <input type="text" name="city" placeholder="city"/> City<br/>
          <input type="text" name="address" placeholder="Address"> Address<br/>
          <input type="text" name="pincode" placeholder="PinCode"> PinCode<br/>
          <input type="submit" name="submit" />
      </form>
  </body>
  </html>
  ```

  

### 14-5 Sijax

***

+ 简介：python的**jquery**库，浏览器可以直接调用服务器的代码

+ 安装

  ```shell
  pip3 install flask-sijax
  ```

+ 示例代码

  ```python
  import os, sys
  path = os.path.join('.', os.path.dirname(__file__), '../')
  sys.path.append(path)
  
  from flask import Flask, g, render_template
  import flask_sijax
  
  app = Flask(__name__)
  app.config["SIJAX_STATIC_PATH"] = os.path.join('.', os.path.dirname(__file__), 'static/js/sijax/')
  app.config["SIJAX_JSON_URI"] = '/static/js/sijax/json2.js'
  flask_sijax.Sijax(app)
  
  @app.route("/")
  def hello():
      return "Hello World!<br /><a href='/sijax'>Go to Sijax test</a>"
  
  @app.route("/sijax", methods = ['GET', 'POST'])
  def hello_sijax():
    	# 函数有两个参数
      def hello_handler(obj_response, hello_from, hello_to):
          obj_response.alert('Hello from %s to %s' % (hello_from, hello_to))
          obj_response.css('a', 'color', 'green')
  
      # 函数没有参数
      def goodbye_handler(obj_response):
          obj_response.alert('Goodbye, whoever you are.')
          obj_response.css('a', 'color', 'red')
  
      if g.sijax.is_sijax_request:
          g.sijax.register_callback('say_hello', hello_handler)
          g.sijax.register_callback('say_goodbye', goodbye_handler)
          return g.sijax.process_request()
  
      return render_template('hello.html')
  
  if __name__ == '__main__':
      app.run(debug=True, port=2345)
  ```

  hello.html

  ```html
  <html>
  <head>
      <script type="text/javascript"
          src="http://ajax.googleapis.com/ajax/libs/jquery/1.5.1/jquery.min.js"></script>
      <script type="text/javascript" src="/static/js/sijax/sijax.js"></script>
      <script type="text/javascript">
          {{ g.sijax.get_js()|safe }}
      </script>
  </head>
  
  <body>
      <a href="javascript://" onclick="Sijax.request('say_hello', ['John', 'Greg']);">
          Say hello from John to Greg!
      </a>
      <br />
      <a href="javascript://" onclick="Sijax.request('say_goodbye');">
          Say goodbye!
      </a>
  </body>
  </html>
  ```

  

  

## 15 部署

***





