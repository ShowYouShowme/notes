# 连接超时

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

   



# 读取超时

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
   
     
   
# 超时重试

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