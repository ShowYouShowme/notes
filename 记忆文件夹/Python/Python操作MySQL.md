# 操作MySQL

***

+ 示例代码

  ```python
  import  pymysql
  
  def _exec_sql(sql : str):
      conn = pymysql.connect(host="192.168.0.79", port=8001, user="root", password="vsvIxMVS5c4VBFoh", database="test")
      cursor = conn.cursor()
      try:
          cursor.execute(sql)
          conn.commit()
          results = cursor.fetchall()
          conn.close()
          return results
      except Exception as e:
          conn.rollback()
          print(e)
          conn.close()
  ```

  