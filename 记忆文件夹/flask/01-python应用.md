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
     ```

     