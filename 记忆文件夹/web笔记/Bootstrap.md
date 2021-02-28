# 第一章 起步



## 1.1 响应式网页

1. 手机发展历程

   + 1G：只能通话
   + 2G：通话，短信
   + 2.5G：GPRS、通话、短信、上网（WML）
   + 3G：ios、android，可以通话、短信、视频、上网（HTML）

2. 响应式网页：网页会根据用户<b style="color:red">浏览设备</b>不同，自动改变布局，可以在PC/PAD/PHONE正常浏览

3. 响应式网页必备条件

   1. 流式布局

      ```css
      float:left;
      display:inline-block;
      ```

   2. 可以改变尺寸

   3. 可以改变大小的文字

4. 响应式网页不足：代码复杂，不适合大型页面



## 1.2 编写响应式网页



### 1.2.1 Viewport

***

早期3G手机为浏览大尺寸网页，只能强行把页面缩小，导致图片、文字、超链接都很小。

IOS提出了视口，用于盛放网页内容，尺寸可以随意大小。用户可以上下左右滑动，看到超出视口的内容。



### 12.2 手机适配

***

1. 声明viewport元标签

   ```html
   <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=yes">
   
   width=device-width：视口宽度是设备屏幕宽度
   initial-scale=1.0：初始缩放比例
   user-scalable=yes：用户是否可以调整缩放比例
   ```

2. 使用流式布局

   ```css
   float:left;
   display:inline-block;
   ```

3. 所有容器使用相对尺寸，不用绝对尺寸

   ```css
   .container{
   	width:100%
   }
   ```

4. 文字使用相对尺寸，不用绝对尺寸

   ```css
   body{
       font-size:1.2em
   }
   ```

5. 图片使用相对尺寸

   ```css
   img{
   	width:50%;/*指定父元素中的宽度占比*/
   }
   ```

6. <b style="color:red">使用CSS3 Media Query 技术</b>

   Media：指浏览网页设备，比如pc、pad、phone、打印机

   Media Query：查询当前浏览网页的设备类型，以及特性（解析度、对比度、<b style="color:red">尺寸</b>和手持方向）不同，选择性执行CSS代码



### 1.2.3 媒体查询

***

1. 根据媒体查询结果执行不同外部CSS文件

   ```html
   <link media="screen and (min-width:768px) and (max-width:991px)" rel="stylesheet" href="pad.css">
   ```

2. 根据媒体查询结果执行不同<b style="color:red">CSS片段</b>

   ```css
   @media screen and (min-width:768px) and (max-width:991px){
       #d1{
           color:red;
       }
   }
   ```



## 1.3 Bootstrap

Bootstrap是一个HTML/<b style="color:red">CSS</b>/JS框架，用于开发响应式布局，移动设备优先的WEB项目。



内容

1. 起步

   ```
   1.	下载bootstrap https://www.bootcss.com/
   2.	下载jQuery（bootstrap依赖于jQuery）
   3.	从https://v3.bootcss.com/getting-started/ 复制模板，在模板的基础上开发
   ```

   模板

   ```html
   <!DOCTYPE html>
   <html lang="zh-CN">
   <!--为浏览器翻译功能确定基础语言,为读屏软件确定基础发音-->
   <head>
       <meta charset="utf-8">
       <!--X-UA-Compatible 指定IE浏览器的兼容性 仅IE浏览器读取,使用IE最新版本来渲染-->
       <meta http-equiv="X-UA-Compatible" content="IE=edge">
       <meta name="viewport" content="width=device-width, initial-scale=1">
       <!-- 上述3个meta标签*必须*放在最前面，任何其他内容都*必须*跟随其后！ -->
       <title>Bootstrap 101 Template</title>
   
       <!-- Bootstrap -->
       <link href="bootstrap/css/bootstrap.css" rel="stylesheet">
   
       <!-- HTML5 shim 和 Respond.js 是为了让 IE8 支持 HTML5 元素和媒体查询（media queries）功能 -->
       <!-- 警告：通过 file:// 协议（就是直接将 html 页面拖拽到浏览器中）访问页面时 Respond.js 不起作用 -->
       <!--[if lt IE 9]>
       <script src="https://cdn.jsdelivr.net/npm/html5shiv@3.7.3/dist/html5shiv.min.js"></script>
       <script src="https://cdn.jsdelivr.net/npm/respond.js@1.4.2/dest/respond.min.js"></script>
       <![endif]-->
   </head>
   <body>
       <div class="container">
   
       </div>
   
   <!-- jQuery (Bootstrap 的所有 JavaScript 插件都依赖 jQuery，所以必须放在前边) -->
   <script src="jQuery/jquery-3.5.1.js"></script>
   <!-- 加载 Bootstrap 的所有 JavaScript 插件。你也可以根据需要只加载单个插件。 -->
   <script src="bootstrap/js/bootstrap.js"></script>
   </body>
   </html>
   ```

   

2. <b style="color:red">全局CSS样式</b>

3. <b style="color:red">组件</b>

4. JS插件

5. 定制



# 第二章 全局CSS样式



## 2.1 按钮

+ .btn：按钮基础样式
+ .btn-default：白底黑色按钮
+ .btn-danger/warning/success/info/primary：五种颜色的按钮
+ .btn-lg/sm/xs：按钮大小
+ .btn-block：块级按钮



## 2.2 图片

+ .img-rounded：圆角图片
+ .img-circle：圆形图片
+ .img-thumbnail：缩略图（padding、边框）
+ .img-responsive：响应式图片



## 2.3 文本

+ .text-danger/success/warning/info/primary：文字颜色
+ .bg-danger/success/warning/info/primary：背景颜色
+ .text-left/center/right/justify：对齐方式
+ .text-uppercase/lowercase/capitailze：转换



## 2.4 列表

+ list-unstyled：去除提示符号
+ list-inline：行内列表



## 2.5 屏幕分类

1. 大型pc屏幕（Large-<b style="color:red">lg</b>）：width>=1200px
2. 中等pc屏幕（Medium-<b style="color:red">md</b>）：1200px>width>992px
3. 小型PAD屏幕（Small-<b style="color:red">sm</b>）：992px>width>768px
4. 超小PHONE屏幕（ExtraSmall-<b style="color:red">xs</b>）：769px>width



## 2.6 表格



### 2.6.1 表格样式

***

+ .table
+ .table-bordered：带边框的表格
+ <b style="color:red">.table-striped：隔行变色</b>
+ <b style="color:red">.table-hover：带悬停变色的表格</b>
+ .table-responsive：响应式表格（<b style="color:red">写在table的父元素中</b>）



### 2.6.2 Bootlint

***

Bootstrap官方检测HTML的工具。检测 bootstrap 样式结构

网址：https://github.com/twbs/bootlint

使用

```html
<!--在html里加上这个-->
<script>
+function(){
    var s=document.createElement("script");
    s.onload=function(){bootlint.showLintReportForCurrentDocument([]);};
    s.src="https://stackpath.bootstrapcdn.com/bootlint/latest/bootlint.min.js";
    document.body.appendChild(s)}()
</script>
```



## 2.7 <b style="color:red">栅格系统</b>



# 第三章 组件



# 第四章 插件



# 第五章 定制

