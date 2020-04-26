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

+ 前提 => 默认情况下路由响应GET方法

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

  