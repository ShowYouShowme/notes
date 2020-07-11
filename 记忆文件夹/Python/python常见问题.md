## 循环引用

***

1. 将导入语句放到函数或者类的内部

2. 组织代码

   ```shell
   # 可以将代码合并到一起
   
   # 可以把一部分import提取到第三个文件中
   ```




## 排序

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

  