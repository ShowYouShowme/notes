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

  

  ## 07 cookies

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

  

  ## 08 session

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

    

  