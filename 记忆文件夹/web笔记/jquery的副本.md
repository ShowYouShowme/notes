# 第0章 网页引入jquery

```html
<head>
    <meta charset="UTF-8">
    <title>登录页面</title>
    <script src="https://cdn.staticfile.org/jquery/1.10.2/jquery.min.js"></script>
</head>
```





```shell
var importJs=document.createElement('script')  //在页面新建一个script标签
importJs.setAttribute("type","text/javascript")  //给script标签增加type属性
importJs.setAttribute("src", "https://cdn.staticfile.org/jquery/1.10.2/jquery.min.js") //给script标签增加src属性， url地址为cdn公共库里的
document.getElementsByTagName("head")[0].appendChild(importJs) //把importJs标签添加在页面
```

```javascript
// 打开多个页面
 $(".list_box>a").each(function (idx, elem) {
               
                var url = $(elem).attr("href")
                console.log(url)
                url = 'https://en.xxx-av.com' + url
                 var frame=window.open("about:blank","_blank");
        	frame.location= url;
                
            })
```




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



## 4.1 官方插件 jQuery UI



### 4.1.1 简介

***

1. 简介：jQuery 官方出的，现成的UI效果和功能的库
2. UI：user interface
3. UI库：用html/css/js实现的现成的页面效果的集合
4. 网址：https://jqueryui.com/
5. 下载：下载前选择主题风格，然后将image文件夹，css和js文件复制到项目目录
7. 学习建议
   + 看官网demo
   + 开发时不懂查手册
7. <b style="color:red">相关文件说明</b>

   + 把整个文件夹放到项目根目录

   + 引入`jquery-ui.js`前先引入`jquery.js`

   + 代码

     ```html
         <link rel="stylesheet" href="jquery-ui/jquery-ui.theme.css">
         <link rel="stylesheet" href="jquery-ui/jquery-ui.css">
         <script src="js/jquery.js"></script>
         <script src="jquery-ui/jquery-ui.js"></script>
     ```

### 4.1.2 组件

***

1. Interactions 交互效果

   + Draggable：让选中的元素可拖拽
   + Selectable：可以多选，该api具有侵入性，会为元素自动添加需要的class。问题：部分侵入的class未定义，需要用户自己定义
   + Sortable：让多个li可拖拽，重新排列
   + Resizable：可以用鼠标改变元素大小
   + Droppable：可将一个元素拖入另外一个元素内

2. <b style="color:green">Widgets 小部件</b>

   + accordion：手风琴

   + autocomplete：自动补全

   + Button：让所有的按钮统一样式

   + Checkboxradio：单选框和复选框

   + Controlgroup：将多个按钮和其它小部件分组为可视集

   + Datepick：日历插件

   + Dialog：对话框

      模态对话框：对话框不关闭，无法操作网页内容

   + Menu：菜单

   + Progressbar：进度条

   + Selectmenu：可选菜单

   + Slider：滑杆

   + Spinner：微调器，用于输入数字，可以用上下方向键设置

   + Tabs：标签页

   + Tooltip：工具提示，鼠标放上去会提示信息

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

     



## 4.2 第三方插件

### 4.2.1 layui

官网：https://www.layui.com/



### 4.2.2 ydui

官网：http://www.ydui.org/



### 4.2.3 bootstrap

***



### 4.2.4 laydate


1. 简介：日期与时间组件，不依赖于jQuery
2. 官网：https://www.layui.com/laydate/



### 4.2.5 jQuery.validator

1. 简介：表单验证的插件，基于jQuery
2. 只需要引入`jquery.validate.js`
3. 官网：https://jqueryvalidation.org/



### 4.2.6 masonry 彩砖墙

***

1. 官网：https://masonry.desandro.com/





# 第八章 ajax





## 8.1 原生Ajax

1. 原生的ajax请求

   ```javascript
   let xhr = new XMLHttpRequest();
   xhr.onreadystatechange = function () {
       if(xhr.readyState == 4 &&
          xhr.status == 200){
           $("[name=desc]").text(xhr.responseText)
       }
   }
   
   xhr.open('get', 'http://127.0.0.1:9090/v1.0/search?term=1');
   xhr.send();
   ```



## 8.2 jQuery封装的Ajax

1. API

   ```javascript
   $.ajax({
      url: "xxx.php",
      type:"get|post|delete...",
      data:"变量=值&变量=值$..." 或 {变量:值,变量:值} 或 ${form}.serialize()
      dataType: "服务器响应回消息的类型" text|json|xml|script|jsonp  jsonp必须写,其它的可以不写,服务器指定
   
   	// 旧版的写法,成功返回响应后,新版用then
   	// 成功收到响应且状态码为200
   	success:function(data){
       },
       error:function(){
       },
       // 请求完成后触发,无论成功失败
       complete:function(){
       }
   // 发送前处理
   	beforeSend:function(){    
       }
   })
   ```

   ```javascript
   $.ajax({
       url:"http://127.0.0.1:9080/v1.0/search",
       type:"get",
       data:"term=1",
       dataType:"json",// 响应的数据类型
       success:function (data) {
           $(".layui-textarea").text(JSON.stringify(data[0]))
       },
       error:function () {
           console.log("请求失败")
       }
   })
   ```

2. <b style="color:green">简写，推荐</b>

   ```
   $.get("url",[data],fn)
   或者 $.get("url",[data]).then()
   
   $.post("url",[data],fn)
   或者
   $.post("url",[data]).then()
   ```

   ```javascript
   $.get("http://127.0.0.1:9090/v1.0/search?term=1").then(function (data) {
       console.log(data)
   })
   ```

   ```javascript
   // 数据是百分号编码,类似get请求 param1=v1&param2=v2,只是放在body里
   let data = $(".layui-form").serialize();
   $.post("http://127.0.0.1:9090/v1.0/login_test", data).then(function (data) {
       console.log(data)
   })
   ```

   ```javascript
   // POST 请求，数据为json
   // 原理：如果跨域,先发起一次options请求，当options请求成功返回后，真正的ajax请求才会再次发起
   $(".layui-btn").click(function () {
       let data = {"name":"yd","pwd":"123456"}
       $.ajax({
           url     :"http://127.0.0.1:9090/v1.0/login_json",
           type    :"post",
           contentType: "application/json;charset=utf-8",
           data: JSON.stringify(data),
       }).then(function (data) {
           console.log(data)
       })
   })
   
   // Flask 服务器设置
   // 先安装依赖 pip install -U flask-cors
   from flask_cors import CORS
   
   app = Flask(__name__)
   CORS(app)
   ```



## 8.3 跨域

  

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
     
     # 如果请求数据是json格式,会先发起options请求,服务器要另外配置
     ```

  3. nginx反向代理：把跨域请求代理到本服务器其它路由

  4. websocket

+ jsonp跨域

  1. 在客户端定义回调函数，在回调函数最后删除创建的\<script>

     ```javascript
     function handler(data) {
         console.log(data['name'], data['age'], data['salary']);
         $("body>script:last-child").remove();
     }
     
     $("#b1").click(function () {
         let $elem = $("<script>");
         // 可以在url里面传入其它参数
         $elem.attr("src", "http://127.0.0.1:9090/v1.0/jsonp?callback=handler");
         $("body").append($elem);
     })
     ```

  2. 动态创建script元素，设置src为restful路径

  3. 服务器：返回js代码，包含数据

     ```
     1--从header里获取callback名
     2--设置content-type :application/javascript
     3--返回callback(msg)
     ```

+ jquery中跨域

  ```shell
  # 底层不是用ajax实现的,只是为了api统一
  $.ajax({
  url:"http://127.0.0.1:9090/v1.0/jsonp",
  type:"get",
  dataType:"jsonp"
  }).then(function (data) {
  console.log(data)
  })
  ```

  ```python
  # python 代码
  def jsonp():
      data = {
          'name'      : 'nash',
          'salary'    : 123,
          'age'       : 80
      }
      callback = request.args['callback']
      return '{}({})'.format(callback,json.dumps(data))
  ```

  



# 第九章 添加jQuery全局函数



## 6.1 jQuery全局函数

1. 定义：直接定义在jQuery构造函数上，所有对象都可以使用。可以认为是jQuery类的静态成员函数

2. 示例

   ```html
   <ul id="nav">
       <li>1</li>
       <li>2</li>
       <li>3</li>
       <li>4</li>
       <li>5</li>
   </ul>
   <script>
           // 静态成员函数
           $.sum = function (elem_array) {
               let sum = null;
               let len = null;
               let i   = null;
               if(Array.isArray(elem_array)){
                   len = elem_array.length;
                   for(i = 0; i < len; ++i){
                       sum += elem_array[i];
                   }
                   return sum;
               }else{
                   sum = 0;
                   elem_array.each(function (idx, elem) {
                       sum += parseInt($(elem).text());
                   })
                   return sum;
               }
           }
           console.log("sum : " + $.sum($("#nav>li")));
           console.log("sum : " + $.sum([7,8,9,10]))
   </script>
   ```

   



## 6.2 jQuery实例函数

1. 定义：定义在jQuery.fn原型对象上，只有jQuery的查询结果对象才能使用。可以认为是jQuery类的成员函数

2. 示例

   ```html
   <ul id="nav">
       <li>1</li>
       <li>2</li>
       <li>3</li>
       <li>4</li>
       <li>5</li>
   </ul>
       <script>
           // 成员函数
           jQuery.fn.sum = function(){
               // this --> jQuery 对象
               let sum = 0;
               $(this).each(function (idx, elem) {
                   sum += parseInt($(elem).text())
               })
               return sum;
           }
           console.log("sum = " + $("#nav>li").sum());
       </script>
   ```

   

