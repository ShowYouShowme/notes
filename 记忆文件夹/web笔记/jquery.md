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

2. 小部件

   1. button：让所有按钮保持一致的样式
   2. 日历
   3. 对话框

## 第三方插件



## 自定义插件

1. jQuery validation

2. 文件上传

   + 普通上传
   + ajax上传
   + 插件上传

3. 富文本编辑器：wysiwyg

   必须的文件：jquery.wysiwyg.css

   ​						jquery.wysiwyg.bg.png

   ​						jquery.wysiwyg.gif

   ​						必须和css同目录

   

   ​						js ： jquery.wysiwyg.js

   ​								wysiwyg.image.js

   ​								wysiwyg.link.js

   ​								wysiwyg.table.js

   问题：只支持旧版的jquery 比如1.6.1

4. masonry 彩砖墙

5. ajax封装

   ```javascript
   $.ajax({
      url: "xxx.php",
      type:"get|post|delete...",
       data:"变量=值&变量=值$..." 或 {变量:值,变量:值} 或 ${form}.serialize()
   
   	dataType: "服务器响应回消息的类型" text|json|xml|script|jsonp  jsonp必须写,其它的可以不写,服务器指定
   
   	// 旧版的写法,成功返回响应后,新版用then
   	// 成功收到响应且状态码为200
   	success(data){
           
       },
       error(){
           
       },
       // 请求完成后触发,无论成功失败
       complete(){
           
       }
   // 发送前处理
   	beforeSend(){
           
       }
   })
   // ajax 的流程
   xhr.onreadystatechange=function(){
       if(xhr.readState == 4){
           if(xhr.status == 200){
               success()
           }else{
               //404 500 ...
               error()
           }
       }
   }
   
   xhr.open()
   beforeSend()
   xhr.send()
   ```

   简写

   ```javascript
   $.get("url",[data],fn)
   或者 $.get("url",[data]).then()
   
   分支：了解
   $.getJSON("url",[data],fn)
   $.getScript("url",[data],fn)
   
   $.post("url",[data],fn)
   
   总结：只要响应头定义了content-type jquery可以自己识别
   
   // 加载html代码,并加载到父元素中
   $("parent").load("header.html", function(){
       
   })
   ```

6. 跨域

   + 定义：一个域名下的网页，想访问另一个域名下的资源；ajax请求会遇到跨域问题。xhr禁止发送跨域的ajax请求

   + 哪些情况算跨域

     1. 协议不一样：https443端口，http80端口
     2. 端口不一样
     3. 域名/IP不同
     4. 二级域名不同

   + 解决方案

     1. 使用特殊标签跨域

        ```shell
        <link href>  	# 样式
        <script src> 	# jsonp --> jQuery 封装了该方式
        <img src> 		# 图片
        <iframe> 		# 基本不用
        ```

     2. 服务器的响应头增加字段

        ```python
        response.headers["Access-Control-Allow-Origin"] = "*"
        ```

     3. nginx反向代理：把跨域请求代理到本服务器其它路由

     4. websocket

   + jsonp跨域

     1. 在客户端定义js函数

        ```javascript
        function callback(data){
            // 使用data
        }
        
        ```
     

    请求头里携带callback名
        ```

     2. 服务器：返回js代码，包含数据
     
        ```javascript
         1--从header里获取callback名
        2--设置content-type :application/javascript
        2-返回callback(msg)
        ```
     
     3. 动态创建script元素，设置src为restful路径
     
     4. 删除创建的script元素

   + jquery中跨域

     ```shell
     # 底层不是用ajax实现的,只是为了api统一
     $.ajax({
     type:"GET",
     url:"remote.php",
     data:xxx,
     success:fn,
     dataType:"jsonp"
     })
     ```

     

7. 添加jQuery全局函数

   + jQuery全局函数：直接定义在jQuery构造函数上，所有对象都可以使用
   + jQuery实例函数：定义在jQuery.fn原型对象上，只有jQuery的查询结果对象才能使用





# 第一章 选择器

api手册：https://jquery.cuishifeng.cn/



## 1.1 基本选择器

1. 根据id选择

   ```html
   <body>
       <button id="btn1">click me!</button>
       <script>
           $("#btn1").click(function () {
               console.log("jQuery 选择器")
           })
       </script>
   </body>
   ```

2. 根据标签选择

   ```html
   <body>
       <button id="btn1">0</button>
       <button id="btn2">0</button>
       <button id="btn3">0</button>
       <script>
           let btns = $("button");
           btns.click(function () {
               let $tar = $(arguments[0].target);
               let count = parseInt($tar.html()) + 1;
               $tar.html(count);
           })
       </script>
   </body>
   ```

   

3. 根据class选择

   ```html
   <body>
       <div class="notMe">div class="notMe"</div>
       <div class="myClass">div class="myClass"</div>
       <span class="myClass">span class="myClass"</span>
       <script>
           $(".notMe").css("background", "red");
       </script>
   </body>
   ```



## 1.2 层级

1. 种类

   ```
   ancestor descendant
   parent > child
   prev + next
   prev ~ siblings
   ```




## 1.3 属性

1. 种类

   ```
   [attribute]
   [attribute=value]
   [attribute!=value]
   [attribute^=value]
   [attribute$=value]
   [attribute*=value]
   [attrSel1][attrSel2][attrSelN]
   ```

   

## 1.4 内容选择器

1. 包含指定内容

   ```html
   <button>鱼香肉丝</button>
   <button>酸菜鱼</button>
   <button>水煮鱼</button>
   <button>麻辣烫</button>
   <script>
       $("button:contains(鱼)").css("color", "red");
   </script>
   ```

   

2. 内容为空

3. 包含匹配选择器的元素



## 1.5 表单选择器

1. 种类

   ```
   :input
   :text
   :password
   :radio
   :checkbox
   :submit
   :image
   :reset
   :button
   :file
   ```

2. 代码

   ```html
   用户名:<input disabled>
   <br/>
   密码:<input type="password" disabled>
   <br/>
   <input type="checkbox"> 我同意本站的使用条款
   <br/>
   <input type="submit" value="提交注册信息" disabled />
   <script>
       var $cnb=$(":checkbox");
       var $others=$(":input:not(:checkbox)");
       $cnb.click(function(){
           $others.prop("disabled", !$(arguments[0].target).prop("checked"));
       })
   </script>
   ```

   



## 1.3 同时匹配多个条件

```html
<div >
    <div class="alert" id="alert1">
        第一个警告框
    </div>

    <div class="alert" id="alert2">
        <span class="close">x</span>
        第二个警告框
    </div>
</div>
<script src="js/jquery-3.5.1.js"></script>
<script>
    // div标签 && 有alert Class && 子元素有close 类
    $("div.alert:has(.close)").css("color", "blue");

    // div标签 && 有alert Class && 子元素没有close 类
    $("div.alert:not(:has(.close))").css("color", "blue");
</script>
```



## 1.2 操作Dom元素

1. 将dom元素封装为jQuery对象

   ```html
   <body>
       <button id="btn1">0</button>
       <script>
           $("#btn1").click(function () {
               let event = arguments[0];
               let elem = event.target; // 触发点击事件的Dom元素
               let count = parseInt($(elem).html()); // $(dom元素) --> 返回jQuery对象
               count += 1;
               $(elem).html(count);
           })
       </script>
   </body>
   ```

   

# 第二章 属性



## 2.1 属性

1. 标准属性

   ```shell
   # 获取属性
   $("img").attr("src");
   
   # 设置属性
   $("img").attr({ src: "test.jpg", alt: "Test Image" });
   ```

   代码

   ```html
   <img src="img/1.jpg" alt="1">
   <script>
       $("img").click(function () {
           let $tar= $(arguments[0].target);
           let alt = parseInt($tar.attr("alt"));
           alt += 1;
           if(alt >4) alt = 1;
           $tar.attr({
               src: "img/" + alt + ".jpg",
               alt : alt
           });
       })
   </script>
   ```

   

2. 状态属性

   ```shell
   # 获取属性
   $("input[type='checkbox']").prop("checked");
   
   # 设置属性
   $("input[type='checkbox']").prop({
     disabled: true
   });
   ```

   

3. 自定义属性

   ```shell
   .data("属性名", 值)
   ```

   代码

   ```html
   <div>
       <img src="img/1.jpg" data-target="img/1.jpg"
            class="my-small">
       <img src="img/2.jpg" data-target="img/2.jpg"
            class="my-small">
       <img src="img/3.jpg" data-target="img/3.jpg"
            class="my-small">
       <img src="img/4.jpg" data-target="img/4.jpg"
            class="my-small">
       <hr/>
       <img src="img/1.jpg" class="my-big">
   </div>
   <script>
       $("div>img:not(:last-child)").click(function (e) {
           let $tar=$(e.target);
           let img_path = $tar.data("target");
           $("div>img:last-child").attr({
               src:img_path
           })
       })
   </script>
   ```

   

## 2.2 CSS类

1. api

   ```shell
   # 添加class
   addClass
   
   # 移除class
   removeClass
   
   # 开关class
   toggleClass
   
   #存在class
   hasClass
   ```

   

2. 代码

   ```html
   <button>双态按钮</button>
   <script>
       $("button").click(function () {
           let $tar = $(this);
           if($tar.hasClass("down"))
               $tar.removeClass("down");
           else
               $tar.addClass("down");
       })
   </script>
   ```

   ```html
   <button>双态按钮</button>
   <script>
       $("button").click(function () {
           let $tar = $(this);
           $tar.toggleClass("down");
       })
   </script>
   ```

   ```html
   <h1>标签页切换</h1>
   <ul class="tabs">
           <li class="active">
               <a data-toggle="tab" href="#">十元套餐</a>
           </li>
           <li>
               <a data-toggle="tab" href="#">二元套餐</a>
           </li>
           <li>
               <a data-toggle="tab" href="#">三元套餐</a>
           </li>
       </ul>
       <script>
           $("[data-toggle=tab]").click(function () {
               var $this=$(this);
               var $parent=$this.parent();
               if($parent.hasClass("active") == false){
                   $parent.addClass("active");
                   $parent.siblings(".active").removeClass("active");
               }
           })
       </script>
   ```

   

## 2.3 HTML代码/文本/值

1. html

   ```shell
   # 获取html内容
   $('p').html();
   
   # 设置html内容
   $("p").html("Hello <b>world</b>!");
   ```

2. text

   ```shell
   # 获取元素内容
   $('p').text();
   
   # 设置元素内容
   $("p").text("Hello world!");
   ```

3. val

   ```shell
   # 获取元素值
   $("input").val();
   
   # 设置元素值
   $("input").val("hello world!");
   ```

   

# 第三章 文档处理



## 3.1 插入



### 3.1.1 内部插入

***

```
append(content|fn)
appendTo(content)
prepend(content|fn)
prependTo(content)
```

### 3.1.2 外部插入

***

```
after(content|fn)
before(content|fn)
insertAfter(content)
insertBefore(content)
```



## 3.2 替换

```
replaceWith(content|fn)
```

代码

```html
<div id="chosen" >
    <img src="img/1.jpg">
</div>
<hr/>
<div id="list" >
    <img src="img/2.jpg">
    <img src="img/3.jpg">
    <img src="img/4.jpg">
</div>
<script>
    $("#list").click(function (e) {
        var $target=$(e.target);
        if($target.is("img")){
            $("#chosen>img").replaceWith($target.clone());
        }
    })
</script>
```



## 3.3 删除

```
remove([expr])
```



## 3.4 复制

```shell
clone()

clone(true) # 连事件也复制
```





# 第四章 事件



## 4.1 页面载入

1. : 仅DOM内容加载完，就可提前执行。DOM内容包括：html和js。比windown.onload 提前触发，不依赖于css和图片的全部操作都可以在DOM内容加载后，提前触发，比如事件绑定

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

   ```html
   <script>
       window.onload=function () {
           console.log("onload trigger!");
       }
   
       $(document).ready(function () {
           console.log("DOM 加载完毕!");
       })
   </script>
   ```

   

## 4.2 事件处理

1. api

   ```shell
   # on 具有 delegate 的功能
   on(eve,[sel],[data],fn)		# 绑定,推荐使用
   on("dblclick", "option", fun)
   on("dblclick", fun)
   
   off(eve,[sel],[fn])	   		# 解除绑定
   off("dblclick", "option", fun)
   off("dblclick", fun)
   
   bind(type,[data],fn)
   
   # 接触绑定
   unbind()  		# 解除全部
   unbind(type)	# 解除一个类型的
   unbind(type,fn) # 解除一个handler
   
   one(type,[data],fn)			# 仅仅触发一次
   trigger(type,[data]) # 触发事件
   
   ```



## 4.3 事件切换

```shell
hover([over,]out) # 同时注册 mouseenter 和 mouseleave事件
toggle([spe],[eas],[fn])1.9*
```



## 4.4 简化事件注册

1. api[推荐]

   ```
   blur([[data],fn])
   change([[data],fn])
   click([[data],fn])
   dblclick([[data],fn])
   error([[data],fn])1.8-
   focus([[data],fn])
   focusin([data],fn)
   focusout([data],fn)
   keydown([[data],fn])
   keypress([[data],fn])
   keyup([[data],fn])
   mousedown([[data],fn])
   mouseenter([[data],fn])
   mouseleave([[data],fn])
   mousemove([[data],fn])
   mouseout([[data],fn])
   mouseover([[data],fn])
   mouseup([[data],fn])
   resize([[data],fn])
   scroll([[data],fn])
   select([[data],fn])
   submit([[data],fn])
   ```




## 4.5 鼠标悬停事件



### 4.5.1 对比

***

1. mouseenter 和 mouseleave 进入/离开子元素时，父元素不触发事件
2. mouseover 和 mouseout 进入/离开子元素时，父元素也会触发事件



### 4.5.2 同时注册

***

```javascript
// 同时绑定两个事件 方法一
$("#d1").mouseenter(function(e){
console.log("进入" + e.target.id)
}).mouseleave(function(e){
console.log("离开" + e.target.id)
})

// 同时绑定两个事件 方法二 使用mouseenter 和mouseleave
$("#d1").hover(e=>{
console.log("进入" + e.target.id)
}, e=>{
console.log("离开" + e.target.id)
})
```



# 第五章 动画



## 3.1 基本

1. 显示

   ```shell
   .show()
   
   # 用法一
   $("#target").show()
   # 用法二  2000 是缓动时间
   $("#target").show(2000, callback)
   ```

2. 隐藏

   ```shell
   .hide()
   
   # 用法同上
   ```

3. 切换显示和隐藏

   ```shell
   .toggle()
   
   # 用法同上
   ```

   

## 3.2 滑动

1. 上滑

   ```shell
   .slideUp(ms,cb)
   ```

2. 下滑

   ```
   .slideDown(ms, cb)
   ```

3. 滑动切换

   ```
   .slideToggle(ms, cb)
   ```



## 3.3 淡入淡出

1. 淡入：元素由透明变为可见

   ```
   .fadeIn(ms,cb)
   ```

2. 淡出：元素逐渐变透明

   ```
   .fadeOut(ms,cb)
   ```

3. 切换

   ```
   .fadeToggle(ms,cb)
   ```



## 3.4 自定义

1. 缓动

   ```
   animate()
   ```

   ```javascript
   $("#btn1").click(function () {
       $("#d1").animate({
           borderRadius:50
       }, 2000, e=>alert("动画结束"))
   })
   ```

   ```javascript
   // 走直角 复合运动
   $("#s2").click(function (e) {
   	$(this).animate({
   		left:1000
   	}, 2000).animate({
   		top:1000
   	}, 2000)
   	})
   ```

2. 停止动画

   ```javascript
   stop() 		// 停止一个动画
   stop(true) // 停止全部动画,包括在排队中的
   ```

   ```javascript
   $("#s1").click(function (e) {
       if($(this).is(":animated")){
           $(this).stop()
       }else{
           $(this).animate({
               left:1000
           }, 2000,e=>alert("s1移动结束"))
       }
   })
   ```

   ```javascript
   $("#s2").click(function (e) {
       if($(this).is(":animated")){
           $(this).stop(true) // 注意此处
       }else{
           $(this).animate({
               left:1000
           }, 2000).animate({
               top:1000
           }, 2000)
       }
   })
   ```



# 第六章 类数组对象操作

1. get(index) 等效于[index]，返回dom元素；get()：返回标准的数组对象
2. length 长度
3. <b style="color:green">each(callback)</b>等效于数组中的forEach
4. index() 等效于数组中的indexOf
   + var i = $("selector").index(jq对象|DOM对象) ：查找右边的元素在左边的结果集合中的下标位置
   + var i = $(...).index()：查找当前元素在其父元素下的下标位置
5. <b style="color:green">$.each(obj, cb)</b>：可以用来遍历数组和对象



# 第七章 插件



## 4.1 jQuery ui



### 4.1.1 简介

***

1. 简介：jQuery 官方出的，现成的UI效果和功能的库
2. UI：user interface
3. UI库：用html/css/js实现的现成的页面效果的集合
4. 网址：https://jqueryui.com/
5. 下载：下载前选择主题风格，然后将image文件夹，css和js文件复制到项目目录
6. 引入`jquery-ui.js`前必须先引入`jquery.js`
7. 学习建议
   + 看官网demo
   + 开发时不懂查手册

### 4.1.2 组件

***

1. Interactions 交互效果

   + Draggable：让选中的元素可拖拽
   + Selectable：可以多选，该api具有侵入性，会为元素自动添加需要的class。问题：部分侵入的class未定义，需要用户自己定义
   + Sortable：让多个li可拖拽，重新排列
   + Resizable：可以用鼠标改变元素大小
   + Droppable：可将一个元素拖入另外一个元素内

2. Widgets 小部件

   + accordion：手风琴

   + autocomplete：自动补全

   + Datepick：日历插件

   + Button：让所有的按钮统一样式

   + Dialog：对话框

      模态对话框：对话框不关闭，无法操作网页内容

   + Tabs：标签页

   + Tooltip：工具提示，鼠标放上去会提示信息

   + Progressbar：进度条

3. Effects 效果

   + 为add/remove/toggleClass添加了动画("class", ms, callback)

   + show/hide/toggle添加了更多动画效果("效果名",ms,callback)

   + **让animate支持颜色动画**

     ```shell
     # 下面这三种颜色均可缓动
     ## 1--backgroundColor
     ## 2--borderColor
     ## 3--color
     
     $(...).animate({}, ms,callback)
     ```

     



## 4.2 layui



### 4.2.1 简介

***

1. 官网：https://www.layui.com/





## 4.3 ydui



### 4.3.1 简介

***

1. 官网：http://www.ydui.org/





## 4.4 bootstrap





## 4.5 第三方插件



### 4.5.1 laydate

***

1. 简介：日期与时间组件，不依赖于jQuery
2. 官网：https://www.layui.com/laydate/



### 4.5.2 jQuery.validator

***

1. 简介：表单验证的插件，基于jQuery
2. 只需要引入`jquery.validate.js`
3. 官网：https://jqueryvalidation.org/



### 4.5.3 masonry 彩砖墙

***

1. 官网：https://masonry.desandro.com/



# 第八章 ajax





# 第九章 添加jQuery全局函数



## 6.1 jQuery全局函数

1. 定义：直接定义在jQuery构造函数上，所有对象都可以使用。可以认为是jQuery类的静态成员函数



## 6.2 jQuery实例函数

1. 定义：定义在jQuery.fn原型对象上，只有jQuery的查询结果对象才能使用。可以认为是jQuery类的成员函数

