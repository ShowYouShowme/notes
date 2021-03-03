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



### 2.7.1 网页布局方法

***

1. Table布局
   + 好处：简单易控制
   + 不足：语义错误，页面渲染效率低
2. DIV+CSS布局
   + 好处：语义正确，页面渲染速度快
   + 不足：不易控制
3. Bootstrap栅格系统
   + 好处：简单易控，渲染速度快， <b style="color:red">支持响应式</b>
   + 不足：没有



### 2.7.2 使用方法

***

1. 最外层必须使用容器

   ```html
   <div class="container">
   <div>
   ```

2. 容器里可以放置任何内容，若想使用栅格系统，必须用<b style="color:red">div.row</b>

   ```
   <div class="row">
   <div>
   ```

3. 一个行中不能放置其它内容，只能放置列，列中可以放置任何内容

   ```html
   <div class="row">
       <div class="col-md-3 col-md-offset-9">
           <input type="text" class="form-control">
       </div>
   </div>
   ```

4. Bootstrap中行默认均分为<b style="color:red">12等分</b>，每个列必须指定行中占比

5. 栅格系统针对不同的屏幕提供不同列

   >.col-<b style="color:red">lg</b>-1/2/3/.../12
   >.col-<b style="color:red">md</b>-1/2/3/.../12
   >.col-<b style="color:red">sm</b>-1/2/3/.../12
   >.col-<b style="color:red">xs</b>-1/2/3/.../12



### 2.7.3 适用性

***

种类
+ .col-xs-*：适合于xs/sm/md/lg 屏幕
+ .col-sm-*：适合于sm/md/lg 屏幕
+ .col-md-*：适合于md/lg 屏幕
+ .col-lg-*：适合于lg 屏幕



常见错误

```html
<!--不同屏幕大小,指定列数量不能相同(重复了),否则报错-->
<div class="col-xs-12 col-sm-12">lg-6(lg)</div>
```



列隐藏

+ .hidden-xs：仅在xs屏幕下隐藏
+ .hidden-sm：仅在sm屏幕下隐藏
+ .hidden-md：仅在md屏幕下隐藏
+ .hidden-lg：仅在lg屏幕下隐藏

```html
<!-- xs-6 md-6 lg-6 sm隐藏 -->
<div class="row">
	<div class="col-xs-6 hidden-sm">lg-6(lg)</div>
</div>
```



嵌套：列中可以再嵌入行，行中再有列

```
.container>
	.row>
		.col-*-*>
			.row>
				.col-*-*>
```



## 2.8 表单

Bootstrap提供三种形式表单

1. 默认表单
2. 行内表单
3. 水平表单

<b style="color:green">官方demo更美观些</b>



### 2.8.1 默认表单

***

```html
<form>
  <div class="form-group">
    <label class="control-label">用户名</label>
    <input class="form-control">
    <label class="help-block">6~8位字母</label>
  </div>
</form>
```



### 2.8.2 行内表单

***

```html
<form class="form-inline">
  <div class="form-group">
    <!--读屏软件-->
    <label class="sr-only">用户名</label>
    <input class="form-control">
  </div>
</form>
```



### 2.8.3 水平表单

***

水平表单=表单+栅格系统（变形）

|          | 默认栅格系统  | 水平表单中栅格       |
| -------- | ------------- | -------------------- |
| 最外元素 | div.container | form.form-horizontal |
| 行       | div.row       | div.form-group       |
| 列       | div.col-\*-\* | div.col-\*-\*        |

```html
<!--写法类似栅格系统,比较麻烦-->
<form class="form-horizontal">
  <div class="form-group">
    <label for="inputEmail3" class="col-sm-2 control-label">Email</label>
    <div class="col-sm-10">
      <input type="email" class="form-control" id="inputEmail3" placeholder="Email">
    </div>
  </div>
</form>
```



# 第三章 组件



## 3.1 下拉菜单

下拉菜单必须有三级结构

```html
<div class="dropdown">
    <a data-toggle="dropdown">触发元素</a>
    <div data-toggle="dropdown-menu">隐藏元素</div>
</div>
```



Bootstrap 示例

```html
<div class="dropdown">
  <button class="btn btn-default dropdown-toggle" type="button" id="dropdownMenu1" data-toggle="dropdown" aria-haspopup="true" aria-expanded="true">
    Dropdown
    <span class="caret"></span>
  </button>
  <ul class="dropdown-menu" aria-labelledby="dropdownMenu1">
    <li><a href="#">Action</a></li>
    <li><a href="#">Another action</a></li>
    <li><a href="#">Something else here</a></li>
    <li role="separator" class="divider"></li>
    <li><a href="#">Separated link</a></li>
  </ul>
</div>
```



## 3.2 导航



### 3.2.1 标签页式导航--页签组件

***

```html
<ul class="nav nav-tabs">
    <li><a data-toggle="tab" href=#>十元套餐</a></li>
    <li class="active"><a data-toggle="tab" href=#>二十元套餐</a></li>
    <li><a data-toggle="tab" href=#>三十元套餐</a></li>
</ul>
```





## 3.3  图标字体

Web项目中常用的图标字体

1. FontAwesome：675免费的图标
2. Glyphicons：800多个收费的图标



常用小图标

```
主页、用户、配置、汉堡包、刷新、打分、我喜欢、发邮件、拍照、定位、购物车、放大镜、删除、加号、减号、叉号、前进、后退、前一张、后一张、播放、暂停、快进、快退
```



服务器端字体使用

1. web服务器项目目录必须有字体文件

2. 使用

   ```html
   <span class="glyphicon glyphicon-cloud"></span>
   ```



## 3.4 <b style="color:red">导航栏</b>

![](img\navbar.png)

### 3.4.1 导航条颜色

***

+ 浅色底深色字：.navbar-default
+ 深色底浅色字：.navbar-inverse



### 3.4.2 导航条定位方式

***

+ 相对定位：默认
+ 绝对定位：.nav-fixed-*



### 3.4.3 导航条位置

***

+ 顶部：.navbar-fixed-top
+ 底部：.navbar-fixed-bottom



## 3.5 按钮组

+ 水平按钮组

  ```html
  <div class="btn-group">
      <a href="#" class="btn btn-success">
          <span class="glyphicon glyphicon-backward"></span>
      </a>
      <a href="#" class="btn btn-success">
          <span class="glyphicon glyphicon-play"></span>
      </a>
      <a href="#" class="btn btn-success">
          <span class="glyphicon glyphicon-pause"></span>
      </a>
      <a href="#" class="btn btn-success">
          <span class="glyphicon glyphicon-stop"></span>
      </a>
      <a href="#" class="btn btn-success">
          <span class="glyphicon glyphicon-forward"></span>
      </a>
  </div>
  ```

+ 垂直按钮组

  ```html
  <div class="btn-group-vertical">
      <a href="#" class="btn btn-success">
      	<span class="glyphicon glyphicon-backward"></span>
      </a>
      <a href="#" class="btn btn-success">
      	<span class="glyphicon glyphicon-play"></span>
      </a>
      <a href="#" class="btn btn-success">
      	<span class="glyphicon glyphicon-pause"></span>
      </a>
      <a href="#" class="btn btn-success">
      	<span class="glyphicon glyphicon-stop"></span>
      </a>
      <a href="#" class="btn btn-success">
      	<span class="glyphicon glyphicon-forward"></span>
      </a>
  </div>
  ```



## 3.6 警告框

1. 危险警告框

   ```html
   <div class="alert alert-danger">
       <h4>
           <span class="glyphicon glyphicon-alert"></span>
           警告
       </h4>
       <p>
           您的浏览器版本太低，请更新!
           您的浏览器版本太低，请更新!
           您的浏览器版本太低，请更新!
           您的浏览器版本太低，请更新!
           您的浏览器版本太低，请更新!
           您的浏览器版本太低，请更新!
       </p>
   </div>
   ```

2. 提示警告框

   ```html
   <div class="alert alert-info" data-dismiss="alert">
       <span class="close">&times;</span>
       <h4 class="glyphicon glyphicon-alert">通知</h4>
       <p>
           您的浏览器版本太低，请更新!
           您的浏览器版本太低，请更新!
           您的浏览器版本太低，请更新!
       </p>
   </div>
   ```

3. 其它警告框：查看Bootstrap官方Demo



## 3.7 进度条

1. 普通进度条

   ```html
   <div class="progress">
       <div class="progress-bar progress-bar-danger" style="width: 10%">10%</div>
   </div>
   ```

2. 带条纹进度条

   ```html
   <div class="progress">
       <div class="progress-bar progress-bar-warning progress-bar-striped" style="width: 45%">45%</div>
   </div>
   ```

3. 动态效果进度条

   ```html
   <div class="progress">
       <div class="progress-bar progress-bar-warning progress-bar-striped active" style="width: 45%">45%</div>
   </div>
   ```

## 3.8 缩略图

```html
<div class="thumbnail">
    <img src="img/1.png">
    <div class="caption">
        <h4>世界名画--01</h4>
        <p>$9999.99</p>
        <a href="#">添加到购物车</a>
    </div>
</div>
```



## 3.9 面板

```html
<div class="panel panel-颜色">
    <div class="panel-heading"></div>
    <div class="panel-body"></div>
    <div class="panel-footer"></div>
</div>
```



重要用途：实现手风琴

## 3.10 自学组件

1. 面包屑
2. 分页条
3. 分页器
4. 徽章
5. 巨幕
6. 页头
7. 水井



# 第四章 插件



# 第五章 定制



## 5.1 静态样式语言

css可以直接被浏览器解析；但是缺少编程语言很多概念：数据类型，函数，变量，运算等，导致<b style="color:green">可维护性很差</b>



## 5.2 动态样式语言

 

三种动态样式语言

1. Sass
2. SCSS
3. <b style="color:green">less</b>

上面三个动态样式语言，添加了编程语言必须的很多特性，提高样式的可维护性。浏览器只能识别CSS，因此动态样式语言必须先编译为CSS。





## 5.3 Less样式语言



### 5.3.1 简介

***

中文网站：http://lesscss.cn/



### 5.3.2 使用方法

***

1. 在客户端使用less.js,一般用于学习

   ```
   在html中引入x.less文件，然后再引入less.js即可
   ```

2. 服务器中使用less

   ```
   程序员编写x.less，然后编译成x.css，再编写html，html里面引用编译好的x.css
   ```



### 5.3.3 语法

***

1. 支持全部css语法

2. 支持多行/单行注释，但是只有多行注释编译到css文件，推荐使用单行注释。

   ```less
   //单行注释
   
   /*多行注释*/
   ```

3. 支持变量

   ```
   定义：@变量名
   使用：color:@变量名
   变量可以取值为任意合法样式值
   ```

4. 支持变量和常量的算术运算

5. 支持 选择器混入

   ```
   选择器1{}
   选择器2{
   	选择器1
   }
   ```

6. 样式混入时指定参数

   ```
   选择器(@param1, @param2){
   
   }
   ```

7. 内置十几个函数

   ```shell
   ceil() 				#向上取整
   floor()				#向下取整
   percentage(num)		#把小数转化为百分比的形式
   darken(color,per)	#把指定颜色变暗
   lighten(color,per)	#把指定颜色变亮
   ```

8. 使用@import来实现文件包含

   ```less
   @import "01.less"
   @import "02"  		//可以省略后缀
   ```



## 5.4 定制Bootstrap



### 5.4.1 定制方法

***

修改Bootstrap的less文件



### 5.4.2 定制目标

***

1. 瘦身：删除不需要的样式。只需要注释bootstrap.less中不需要的@import
2. 粗粒度定制：只需要修改variables.less
3. 细粒度修改：修改对应组件的less文件，比如dropdown.less



### 5.4.3 生成css文件

***

1. 安装lessc

   ```shell
   npm install -g less
   ```

2. 修改Bootstrap源码的less文件

3. 生成新css文件

   ```shell
   lessc bootstrap.less bootstrap.css
   ```