## JQuery 特性

1. 一个函数两用
   + 不传参数是读取
   + 传入参数是写入
   
2. 自带遍历

3. 几乎每个jqueryAPI都返回jQuery对象本身，支持链式的操作

4. 修改

   ```shell
   .html() => .innerHTML
   .text() => .textContent
   .val()  => .value
   
   标准属性: .attr("属性名",值)
   状态属性: .prop("状态属性", 值)
   自定义属性: .data("属性名", 值)
   ```

5. 节点关系

   ```shell
   父元素:	.parent() =>.parentNode
   直接子元素:	.children() => .children
   	查找父元素下符合条件的子元素
   		.children("selector") 只能在直接子元素中找
   		.find("selector") 在所有后代中找
   第一个子元素:	.children().first()
   最后一个子元素:	.children().last()
   前一个兄弟:	.prev()
   			.prevAll()
   后一个兄弟:	.next()
   			.nextAll()
   除我之外的全部兄弟:	.siblings()
   ```

6. 内容过滤

   ```shell
   1. 按包含的文本内容过滤 :contains(text)
   
   2. 按子元素特征过滤 :has(selector) 查找内容中包含符合selector要求的子元素的父元素
   
   3. 按是否包含内容过滤
   	:empty 空元素
   	:parent 非空的元素
   ```

7. 可见性过滤

   ```shell
   :hidden 只能选择 display:none input type=hidden 的元素
   
   :visible 可见元素
   
   ```

8. 状态过滤

   ```shell
   :disabled
   :checked
   :selected
   ```

9. 表单元素过滤

   ```shell
   :input 选择所有四类表单元素
   	input button textarea selected
   ```

10. 介绍

    + 简化的DOM操作库,会用jQuery就不用学Dom的操作了
    + 屏蔽浏览器兼容问题
    + 生产版本建议用cdn网络引入jQuery\

11. 创建jQuery对象

    + 用$("selector")直接查找
    + 如果已经获得Dom对象，用$(dom对象)封装为jQuery对象
    
    
    
    
    
12. 强调
    
    + 尽量减少jQuery对象的创建
    
    + 尽量减少查找次数
    
    + 建议
    
      ```shell
      1. 使用链式操作,但是不方便调试
      2. 将jQuery对象保存到临时变量中
      ```
    
13. 批量修改样式

    + 追加样式

      ```
      $(...).addClass("className")
      ```

    + 移除样式

      ```
      $(...).removeClass("className")
      ```

    + 判断是否有样式

      ```
      $(...).hasClass("className")
      ```

    + 切换class

      ```shell
      $(...).toggleClass("className")
      ```

14. 添加,删除，替换，克隆

    1. 添加
    
       ```shell
       # step--1
       用$()创建元素 var ${新元素}=${"html片段"}
       
       # step--2
       $("parent").append($新元素)
       		   .prepend($新元素)
       $("child").before($新元素)
       		  .after($新元素)
       ```
    
    2. 删除
    
       ```shell
       $(...).remove()
       ```
    
       
    
    3. 替换
    
       ```shell
       $(...).replaceWith()
       ```
    
       
    
    4. 克隆
    
       ```shell
       # 浅克隆,克隆出来的没有事件
       $(...).clone()
    
       # 深克隆,连事件也会注册
       $(...).clone(true)
       ```
       
       
    
15. index

    ```shell
    # 查找child的index
    var i=$("child").index()
    ```

16. 判断是否为指定标签

    ```shell
    $target.is("img")
    ```
    
    
    
    
    
## 事件绑定


1. Dom

   ```shell
   addEventListener("事件名", handler)
   removeEventListener(...)
   ```

2. jQuery

   ```shell
   bind("事件名", handler)
   unbind("事件名", handler) # 函数指针要保存下来
   unbind("事件名") # 移除当前元素上指定事件的全部handler
   unbind() # 移除全部事件
   
   one("事件名", handler) # 只触发一次
   
   ```

3. delegate

   ```shell
   $("parent").delegate("selector","事件名", handler)
   
   1. 获得目标元素  this 或者 e.target
   2. 筛选目标，满足条件selector 的元素才能触发
   ```

   

4. bind和delegate的区别

   ```shell
   # 1
   bind 直接绑定到目标元素
   delegate 绑定到父元素上
   
   # 2
   bind 监听个数多--每个目标元素都添加
   delegate 只给父元素添加一个
   
   # 3
   bind 只能对现有元素添加事件监听，新增元素无法自动获取监听
   delegate 无论现有还是新增，都能自动获取父元素事件监听
   ```

5. on/off(以后所有绑定全部用on)

   ```shell
   # 1
   代替 bind: on("事件名", handler)
   
   # 2
   代替delegate: on("事件名", "selector", handler)
   
   # 3
   off 替代 unbind 
   ```

6. 终极简化

   ```shell
   # 注册事件
   .${事件名}=
   
   .click(function(){
   
   })
   ```



## 页面加载后执行

1. DOMContentLoaded: 仅DOM内容加载完，就可提前执行。DOM内容包括：html和js。比windown.onload 提前触发，不依赖于css和图片的全部操作都可以在DOM内容加载后，提前触发，比如事件绑定

   ```shell
   # <script>标签放在 <body>标签结尾也是DOM加载完成后执行
   
   # jQuery 解决了浏览器兼容性问题
   $(document).ready(function(){
   
   })
   
   ## 简化
   $().ready(function(){
   
   })
   
   ## 终极简化
   $(function(){
   
   })
   
   或者
   $(()=>{
   
   })
   ```

   

2. windown.onload() 在所有页面内容加载完成触发，包括html，css，js，图片等。如果js必须依赖css或者图片才能执行，用这个



## 鼠标事件

1. mouseover 和 mouseout :进出子元素，会频繁触发父元素的处理函数

2. mouseenter 和 mouseleave 进出子元素，不再频繁触发父元素的处理函数

3. 同时绑定鼠标进入和移出事件，简写为hover

   ```shell
   # mouseenter  和 mouseleave 事件
   $().hover(f1(){}, f2(){})
   ```

4. 模拟触发：虽然没有触发，但是依然可以用程序模拟执行元素的事件处理函数

   ```shell
   $(...).trigger("事件名")
   
   # 简化
   $(...).事件名()
   ```

   

## 总结

jQuery简化了DOM五大操作：

​	查找，修改，添加，删除和事件绑定







## 通过class批量修改样式

1. 判断是否含有class

   ```javascript
   $("...").hasClass("类名")
   ```

2. 添加class

   ```javascript
   $("...").addClass("类名")
   ```

3. 移除class

   ```javascript
   $("...").removeClass("类名")
   ```

4. 切换class

   ```javascript
   $("...").toggleClass("类名")
   ```



## 添加

1. 创建新元素

   ```javascript
   var $newElem=$("html代码片段")
   ```

2. 将新元素添加到DOM树

   + 结尾/开头插入

     ```javascript
     $(parent).append($newElem)
     
     $(parent).prepend($newElem)
     ```

   + 在某个child前后插入

     ```javascript
     $(child).before($newElem)
     
     $(child).after($newElem)
     ```



## 删除

```javascript
$(...).remove()
```





## 替换

```javascript
$("现有元素").replaceWith("新元素html代码")

$("新元素html代码").replaceAll("现有元素")
```



## 克隆

+ 浅克隆

  ```javascript
  // 鼠标点击事件无法复制
  $("...").clone()
  ```

+ 深克隆

  ```javascript
  $("...").clone(true)
  ```



## 事件

1. bind/unbind

   ```javascript
   .unbind("事件名",fn)	// 删除一个事件下的指定handler
   .unbind("事件名")  // 删除一个事件下注册的全部handler
   .unbind()		  // 删除所有handler
   ```

2. one

   ```javascript
   .one("事件名",fn) // 只触发一次
   ```

3. delegate/undelegate

   + delegate和bind对比

     ```shell
     # 1
     bind 直接绑定到目标元素
     delegate 绑定到父元素上
     
     # 2
     bind 监听个数多--每个目标元素都添加
     delegate 只给父元素添加一个
     
     # 3
     bind 只能对现有元素添加事件监听，新增元素无法自动获取监听
     delegate 无论现有还是新增，都能自动获取父元素事件监听
     ```

4. on/off

5. 终极简化





# 动画



### 简单动画

***

1. 显示隐藏：$(...).show|hide|toggle() --> 要掌握
2. 上滑下滑：slideUp|slideDown|slideToggle(ms,cb)
3. 淡入淡出fadeIn|fadeOut|fadeToggle
4. 特点：所有函数可以选择加2个参数（动画持续时间ms和结束后的回调）
5. 缺点
   + 效果写死，不便于维护和定制
   + 用js定时器实现的动画，效率低
6. 建议：使用transition来实现





### 万能动画

***

1. $(...).animate({},ms,cb)  只支持单个数值的css属性，不支持颜色动画

2. 没有transition好用

3. 必须要掌握，比上面的3组API好用

4. 对比transition

   ```shell
   效率: transition高
   
   支持属性种类: transition高支持颜色过渡,animate不支持
   
   灵活性: animate可随意停止  transition 不可中断
   ```

5. 停止动画：$(...).stop()

   ```javascript
   $tar.is(":animated") // 判断动画是否执行中
   
   $(...).stop()
   
   $(...).stop(true) //清空后序队列
   ```

6. 排队

   ```javascript
   // 两个动画先后执行,也可以用cb来实现
   $tar.animate({opacity:0},1000)
   .animate({opacity:1},1000,function () {
   $(this).hide();
   })
   ```

7. 延迟执行 setTimeout()



# 类数组对象操作

1. get(index) 等效于[index]，返回dom元；get()：返回标准的数组对象
2. length 长度
3. each(callback)等效于数组中的forEach
4. index() 等效于数组中的indexOf
   + var i = $("selector").index(jq对象|DOM对象) ：查找右边的元素在左边的结果集合中的下标位置
   + var i = $(...).index()：查找当前元素在其父元素下的下标位置
5. $.each(obj, cb)：可以用来遍历数组和对象

# 插件

1. 定义：拥有独立功能的函数或程序
2. 作用：重用



## 官方插件

1. jQuery官方插件：jQuery UI

   + 交互行为：了解

   + 效果：重写jQuery中的函数，了解

     ```shell
     # 1
     让 addClass可添加动画持续事件和回调函数，但是依旧使用定时器模拟过渡效果
     
     # 2
     让animate 支持颜色动画
     
     # 3
     为show/hide/toggle添加了更多的动画效果
     ```

   + **[重点]小部件，拥有完整样式和功能的小功能，包含**

     1. 部件的样式：.CSS文件

     2. 部件的行为：.js文件

     3. 部件的内容和格式：自定义

     4. 使用

        + 下载并引入css和js文件，必须先引入jqeury.js，再引入jquery-ui.js.  jquery-ui.css和jquery-ui的images的文件夹放在同一个目录下

        + 按照部件的要求定义HTML内容和格式

        + 在自定义脚本中：找到要应用部件的HTML元素，调用部件的函数

        + 示例

          ```html
          jquery-ui.js 放到js文件夹
          images 文件夹和jquery-ui.css 放到images文件夹
          
          <link rel="stylesheet" href="css/jquery-ui.css">
          <script src="js/jquery-3.5.1.js"></script>
          <script src="js/jquery-ui.js"></script>
          ```

          

## 第三方插件



## 自定义插件



