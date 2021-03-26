# 第一章 CSS概述



## 1.1 什么是CSS

```
层叠样式表，简称样式表
```



## 1.2 CSS 与 HTML 之间的关系

HTML：构建网页结构

CSS：构建HTML元素样式



## 1.3 HTML属性与CSS样式使用原则

原则：尽量使用CSS样式取代HTML属性

```
html ： <body text="red">
css : color:red
```

HTML 只需要记住四大属性：id，class，title，style



# 第二章 CSS 语法



## 2.1 使用CSS样式表



### 2.1.1 使用方式

***

1. 内联：将样式声明在元素的style属性中

   ```html
   <ANY style="样式声明1;样式声明2;样式声明3"></ANY>
   
   每个样式声明由两部分组成
   样式属性:属性值
   
   ex:
   样式属性    属性值
   color:	  red
   font-size: 100px
   background-color:blue
   ```

2. 内部样式表：将样式声明定义在页面的style元素当中

   1. 在\<head>中添加\<style>\</style>元素

   2. 在style中添加任意多样式规则

      ```
      选择器{
      	样式声明;  /*属性:值*/
      	样式声明;
      }
      ```

      选择器：规范页面中哪些元素能使用定义好的样式

      ```shell
      # 定义页面中所有p元素的样式
      p{
       color:red;
       font-size:48px;
       background-color:green
      }
      ```

      

3. 外部样式表

   步骤：

   1. 创建一个单独的样式表文件保存规则  *.css

   2. 在需要的页面上引入样式表文件

      ```html
      <!-- type属性可以不写 -->
      <head>
      	<link rel="stylesheet" type="text/css" href="css/custom.css">
      </head>
      ```



### 2.1.2 样式表特征

1. 继承性：子级元素可以直接使用父级元素声明好的样式。大部分的css样式属性是可以被继承的

2. 层叠性：可以为一个元素声明多个样式规则，如果样式不冲突的话，多个样式规则中的样式可以层叠为一个

3. 优先级：样式定义冲突时，按照不同样式使用的方式的优先级来应用样式

   1. 浏览器缺省设置（User Agent Stylesheet），**优先级最低**

   2. 外部样式表或内部样式表：就近原则，谁离元素近，就用谁，**中优先级**

   3. 内联样式，**高优先级**

   4. !important  规则：显式调整样式的优先级，优先级最高

      ```
      属性名称:值 !important
      ```

      尽可能少用：

      1. ie6以及以下的浏览器不支持
      2. 打破默认优先级规则



## 2.2 CSS基础选择器

1. 作用：规范页面中哪些元素能使用定义好的样式。目的：匹配页面元素

2. 详解

   1. 通用选择器：匹配页面中的所有元素；**尽量不用，效率低**

      ```
      *{样式声明;}
      ```

   2. 元素选择器：定义页面上某一标签的默认样式

      ```
      元素{
      样式声明;
      }
      
      div{
       font-size:12px
      }
      ```

   3. 类选择器：由css定义好，可以被任意标记的class属性值进行引用的选择器

      ```
      .类名{
      样式声明
      }
      
      1. 类名不能以数字开始
      2. 除了_，-以外不能有其他特殊符号
      
      <ANY class="类名"></ANY>
      ```

      多类选择器的引用：可以将多个类，同时应用在一个元素中

      ```
      <ANY class= "c1 c2 c3 c4"></ANY>
      ```

      分类选择器

      ```
      元素选择器.类选择器{
      	样式声明;
      }
      
      // 定义class 为 important 的div 的元素的样式
      div.important{
      
      }
      ```

   4. ID选择器：针对指定ID值的元素定义

      ```
      #ID值{
      样式声明;
      }
      ```

   5. 群组选择器：选择器声明用**逗号**隔开的选择器列表

      ```
      选择器1,选择器2,选择器3
      
      span,.important,#main{
      
      }
      ```

   6. 后代选择器

      后代：只要具备层级关系的元素，被嵌套的都可以称之为 后代元素

      ```
      // 用空格间隔
      选择器1 选择器2{
      样式声明;
      }
      
      #d1 span{} // id为d1中的span元素
      ```

   7. 子代选择器

      子代：只具备一级层级关系的元素，被嵌套的称之为子代元素

      ```
      选择器1>选择器2{
      样式声明;
      }
      
      #d1>span{} // id为d1中的下一级span元素
      ```

   8. 伪类选择器：匹配页面元素的不同状态的选择器

      分类：

      1. 链接伪类

         ```
         :link   	匹配尚未被访问的超链接的状态
         
         :visited 	匹配访问过后的超链接的状态
         
         // 匹配页面中id为anchor的未被访问过的状态
         #anchor:link{
         
         }
         
         #myAn:visited{
         
         }
         ```

         

      2. 动态伪类

         ```
         :hover 匹配鼠标悬停在元素的状态 [重点]
         
         :active 匹配元素被激活时的状态
         
         :focus 匹配元素获取焦点时的状态，针对text，password，textarea
         ```

3. 选择器优先级：选择器的权值加到一起，大的优先；如果权值相同，后定义的优先

   | 选择器类型 | 权值 |
   | ---------- | ---- |
   | 元素选择器 | 1    |
   | 类选择器   | 10   |
   | 伪类选择器 | 10   |
   | ID选择器   | 100  |
   | 内联样式   | 1000 |



# 第三章 尺寸与边框



## 3.1 单位



### 3.1.1 尺寸单位

***

+ <span style="color:red;font-weight:bold">% 百分比：相对于父元素的百分比</span>
+ in 英寸：用的不多
+ cm 厘米：用的不多
+ mm 毫米：用的不多
+ <span style="color:red;font-weight:bold">pt 磅</span>
+ <span style="color:red;font-weight:bold">px 像素</span>
+ <span style="color:red;font-weight:bold">em 1em等于当前的字体尺寸</span>



### 3.1.2 颜色单位

<hr/>

+ rgb(r,g,b)，RGB值，如rgb(255,0,0)
+ rgb(x%,y%,z%)：RGB百分比，如rgb(100%,0%,0%)
+ <span style="color:red;font-weight:bold">#rrggbb：十六进制数，如#ff0000</span>
+ #rgb：简写的十六进制数，#aabbcc 可简写为#abc
+ 表示颜色的英文单词，比如red



## 3.2 尺寸属性

1. 作用：用于设置元素的宽度和高度

   单位：百分比 或 像素

2. 宽度属性

   + width：设置元素宽度
   + min-width：设置元素的最小宽度
   + max-width：设置元素的最大宽度

3. 高度属性

   + height：设置元素高度
   + min-height：设置元素最小高度
   + max-height：设置元素最大高度

4. 允许修改宽和高的元素

   + 块级元素

   + 大部分的行内块元素

     ```
     大部分表单控件元素
     单选按钮，复选框，无法修改尺寸
     ```

   + 存在width和height属性的html元素允许被修改

     比如：img，table

5. 溢出：使用尺寸属性限制元素大小时，如果内容所需空间大于元素本身，会导致溢出

   溢出处理：

   1. overflow

      ```
      visible：溢出可见
      hidden：溢出隐藏
      scroll：滚动，元素会出现滚动条，当内容溢出时，滚动条可用
      auto：自动，内容溢出时，会显示滚动条并且可用；不溢出没有滚动条
      ```

   2. overflow-x：横向溢出处理

      ```
      visible：溢出可见
      hidden：溢出隐藏
      scroll：滚动，元素会出现滚动条，当内容溢出时，滚动条可用
      auto：自动，内容溢出时，会显示滚动条并且可用；不溢出没有滚动条
      ```

   3. overflow-y：纵向溢出处理

      ```
      visible：溢出可见
      hidden：溢出隐藏
      scroll：滚动，元素会出现滚动条，当内容溢出时，滚动条可用
      auto：自动，内容溢出时，会显示滚动条并且可用；不溢出没有滚动条
      ```




## 3.3 边框属性



### 3.3.1 边框

***



#### 边框[重点]

***

1. 简写方式：一个属性控制四个方向边框的效果

   ```shell
   border：width style color
   
   width：粗细
   style：样式
   	solid：实线
   	dotted：虚线
   	dashed：虚线
   color：颜色
   	rgb
   	transparent（透明）
   	
   # 取消边框
   border:none  或者 border:0
   ```

2. 单边定义

   ```
   border-方向:width style color
   
   方向:
   top right bottom left
   
   border-left:1px dotted red
   ```

3. 单属性定义

   ```
   border-属性:值
   
   值:width/style/color
   
   border-color:#00f
   border-style:dotted
   ```

4. 单边单属性定义

   ```
   border-方向-属性:值
   
   border-left-color:red
   border-bottom-style:dotted
   ```



#### 边框倒角[重点]

***

作用：将四个方向的角倒成圆角

```
border-radius
取值：绝对数值 或 百分比

border-radius:5px
border-radius:50%  如果当前宽和高相等，则将元素改为圆形
```





#### 边框阴影

***

```
box-shadow

取值：
h-shadow：必须 阴影的水平偏移距离，+ 右偏移 - 左偏移
v-shadow：必须 阴影的垂直偏移距离，+ 下偏移 - 上偏移
blur：模糊距离
spread：阴影尺寸
color：颜色
inset：默认的外阴影更改为内阴影，这是一个值

基本上只需要设置h-shadow和v-shadow
```



#### 轮廓

***

作用：绘制于元素周围的一条线，位于边框之外

```shell
# 很少使用
outline: width style color
outline-width
outline-color
outline-style

# 取消元素轮廓
outline:none  或者 outline:0
```



## 3.4 框模型



### 3.4.1 什么是框模型

***

框：页面一切元素都是框。

框模型：Box-Model，定义了元素框处理元素内容，内边距和外边距的方式



对象实际宽度：左右外边距 + 左右边框 + 左右内边距 + width



对象实际高度：上下外边距 + 上下边框 + 上下内边距 + height

### 3.4.2 外边距

***

1. 定义：围绕在元素边框周围的空白区域，正常情况下，不允许被其他元素所占据

2. 语法：

   ```shell
   # 四个方向外边距
   margin:value
   
   # 单边设置
   margin-top 上外边距
   
   margin-right 右外边距
   
   margin-bottom 下外边距
   
   margin-left 左外边距
   
   # 取值
   1. 单位  px
   	margin-top:20px
   	margin:15px
   2. 单位为%
   3. 取值为auto
   	左右外边距可以取值为auto，允许让块级元素水平居中显示。上下边距值auto无效,需要先指定块级元素的宽度
   4. 取值为负值
   	移动元素
   	左外边距为负数，元素向左移动
   	上外边距为负数，元素向上移动
   ```

3. 简洁写法

   ```shell
   margin:value # 四个方向外边距相同
   
   margin: v1 v2;# v1 上下边距 v2 左右边距
   
   margin: v1 v2 v3; # v1 上 v2 左右 v3 下
   
   margin: v1 v2 v3 v4; # 上 右 下 左
   ```

4. 默认具备外边距的元素

   ```
    body 元素也有外边距
   <body>
       <!--外边距-->
       <p>段落元素</p>
       <h1>1级标题</h1>
       <h2>2级标题</h2>
       <h3>3级标题</h3>
       <h4>4级标题</h4>
       <h5>5级标题</h5>
       <h6>6级标题</h6>
       <ul>
           <li>列表项1</li>
           <li>列表项2</li>
           <li>列表项3</li>
       </ul>
   
       <ol>
           <li>列表项1</li>
           <li>列表项2</li>
           <li>列表项3</li>
       </ol>
   
       <dl>
           <dt>外边距</dt>
           <dd>外边距是位于元素边框之外的空白距离</dd>
       </dl>
   
       <pre>预处理元素</pre>
   </body>
   ```

   编写网页时，一般会进行css重新，改变一些元素的默认样式。比如取消某些元素的默认外边距

5. 外边距特殊处理

   1. 外边距合并：两个垂直外边距相遇时，他们将形成一个外边距，称为外边距合并。合并后的外边距的高度等于两个外边距中高度较大者。

   2. 外边距溢出：在某些特殊情况下，为子元素设置上下外边距时，有可能会作用到父元素上。

      特殊情况：

      1. 父元素没有上或下边框
      2. 必须为第一个子元素或最后一个子元素设置外边距时

      解决方案：

      1. 为父元素增加边框（上/下）
      2. 在父元素中增加子元素\<table>到第一个子元素位置处
      3. 通过设置父元素的上内边距来取代子元素的上外边距

   3. 为行内元素和行内块元素设置外边距

      1. 为行内元素设置上下外边距 无效
      2. 为行内块元素设置上下外边距整行内容都跟着变



### 3.4.3 内边距

***

1. 定义：内容区域与边框之间的距离。特点：会扩大元素边框所占用的区域

2. 语法

   ```
   padding：value
   
   单边设置
   padding-top/right/bottom/left:value
   
   取值：
   1. 单位可以为px
   2. 单位可以为%
   3. 不允许取负数
   ```

3. 简洁写法

   ```
   padding:value 四个方向的内边距
   
   padding:V1 V2;  V1 上下 V2 左右
   
   padding:V1 V2 V3;上 左右 下
   
   padding:V1 V2 V3 V4 上 右 下 左
   ```

4. 特殊处理

   对行内元素和行内块元素设置内边距时，只会影响自己，不会影响其他元素



## 3.4.4 box-sizing

作用：重新指定元素框模型的计算模式



元素边框内占地区域 = 左右边框 + 左右内边距 + width



取值

```
1. content-box 默认值，内边距 和 边框会累加到元素尺寸中
2. border-box 元素的真正尺寸会包含边框 和 内边距
```



## 3.5 背景属性



### 3.5.1 背景

***

1. 背景颜色

   ```
   background-color ： 取值 任意合法颜色 或者 transparent
   
   背景颜色会填充到元素 内容区域 内边距区域 以及 边框区域
   ```

2. 背景图片

   作用：以图像作为元素的背景

   属性：background-image

   取值：图片路径 url(背景图片路径)

3. 背景重复：控制重复数量

   属性：background-repeat

   取值：

   ```
   1. repeat 		默认值 水平垂直方向都平铺
   2. repeat-x		仅在水平方向平铺
   3. repeat-y		仅在垂直方向平铺
   4. no-repeat	不平铺
   ```

4. 背景图片尺寸

   属性：background-size

   取值：

   ```
   1. value1 value2  		指定宽度和高度,以px为单位
   2. value1% value2% 		指定宽度和高度，采用当前元素的宽和高的百分比
   3. cover  				覆盖，将背景图等比放大，直到背景图完全覆盖到元素的所有区域为止
   4. contain				将背景图等比放大，直到背景图像的下边或右边有一个边缘碰到元素为止
   ```

5. 背景图片固定

   属性：background-attachment

   取值：

   ```
   1. scroll 滚动，默认值，背景图会随着文档而滚动
   2. fixed 固定，背景图不会随着页面文档而发生滚动，一直保持在可视化区域中的固定位置
   ```

6. 背景图片的定位

   作用：改变背景图像在元素中的默认位置

   属性：background-position

   取值：

   ```
   1. x y  
   
   x： 背景图 水平偏移距离，取值为正，向右偏移，取值为负，向左偏移
   y： 背景图 垂直偏移距离，取值为正，向下偏移，取值为负，向上偏移
   
   
   2. x%  y%
   
   0% 0% 		： 背景图在元素左上角
   100% 100% 	： 背景图在元素右下角
   50% 50% 	： 背景图在元素的中间
   
   3. 关键字
   x：	left/center/right
   y:	top/center/bottom
   
   
   background-position:center; // 水平和垂直都在中间
   ```

7. CSS Sprites：精灵图

   作用：将一些小的背景图，合并到大的背景图当中去，以便实现 减少服务器端的请求次数 

   1. 根据 要看的图像大小，创建一个元素
   2. 将 精灵图 作为元素的背景图，再通过背景图像位置，实现位置偏移，将用户要看的图像，显示在元素中。

8. 背景属性

   属性：background

   取值：color url（） repeat attachment position

   注意：如果不设置其中的某个值，将采用默认值

   ```shell
   background: red  # 只设置颜色 其它用默认值
   background: url(a.jpg) -45px -112px
   ```

   



# 第四章 渐变



## 4.1 什么是渐变

1. 定义：两种或多种颜色间平滑过渡的效果
2. 分类
   + 线性渐变：按照直线方向渐变
   + 径向渐变：按照半径的方向渐变
   + 重复渐变



## 4.2 组成

1. 色标：决定了渐变的每种颜色及其出现的位置。每一种渐变效果都是由 多个 色标 组成的（2个以上）



## 4.3 渐变的语法

1. 语法

   ```
   属性：background-image
   值：	liner-gradien() 			   线性渐变
   	  radial-gradien() 				径向渐变
   	  repeating-liner-gradien() 	重复线性渐变  基本用不到
   	  repeating- radial-gradien() 	重复径向渐变  基本用不到
   ```

   

2. 线性渐变

   ```
   background-image:liner-gradien(angle, color-point, color-point,...)
   
   angle: 角度,渐变的填充方向
          值： to top: 从下向上填充
          	   to right: 从左向右填充
          	   to bottom: 从上向下填充
          	   to left:从右向左填充
          	   
          	   角度: 0deg-360deg
          	       0deg   --> to top
          	       90deg  --> to right
          	       180deg --> to bottom
          	       270deg --> to left
          	       
   color-point: 表示每个颜色值，及其出现的位置，多个色标之间用逗号分隔
   			ex:
   			  1. red  0%   开始的时候 是红色
   			  2. blue 50px 填充到50个像素时，变为 蓝色
   			  3. 色标的位置可以省略
   			     省略位置后，每个将平均分配元素区域
   ```

3. 径向渐变

   语法：

   background-image：radial-gradient([size-at-position],color-point, color-point)

   ```
   size-at-position：径向渐变的半径 以及 圆心的位置
   size: 圆的半径, px为单位
   position: 圆心位置
   	1. 0px 0px  圆心设置在元素的左上角
   	2. 50% 50% 	圆心设置在元素正中间
   	3. right bottom 关键字：top / right / bottom / left / center
   	   将圆心设置在元素的右下角
   ```

4. 浏览器的兼容问题

   各主流浏览器的主流版本 均支持渐变效果；对于不支持渐变的浏览器，可以尝试增加 浏览器前缀 去实现渐变显示。

   ```
   Firefox : -moz-
   Chrome和Safari: -webki-
   Opera: -o-
   ```

   前缀加载位置：

   1. 如果浏览器不支持属性，则将前缀加载到属性名称前

      ```
      ex：
      	animation: scroll 5s;
      	
      	加前缀
      	-moz-animation: scroll 5s;
      	-webki-animation: scroll 5s;
      	-o-animation: scroll 5s;
      ```

      

   2. 如果浏览器支持属性，但是不支持值的话，则将前缀加载到属性值的前面

      ```
      ex:
      	background-image: liner-gradient()
      	
      	background-image: -moz-liner-gradient()
      	background-image: -webki-liner-gradient()
      	background-image: -o-liner-gradient()
      ```

      



# 第五章 文本格式化



## 5.1 字体属性

1. 指定字体系列

   属性：font-family

   取值：value1,value2,...  [逐个匹配，看客户机器上有哪个字体]

   注意：字体取值包含 中文或者特殊符号，使用""引起来

   ```
   font-family:"宋体","微软雅黑",Arial
   ```

2. 字体大小

   属性：font-szie

   取值： px 或者 pt 或者 em

3. 字体加粗

   属性：font-weight

   取值：

   1. normal：正常体
   2. bold：加粗
   3. 400~900   400：normal  900：bold

4. 字体样式

   属性：font-style

   取值：

   1. normal：正常提
   2. italic：斜体

5. 小型大写字母[很少用]

   作用：针对英文字符，将小写字符变成大写字符，但是大小与小写一样

   属性：font-variant

   取值：

   1. normal
   2. small-caps

6. 字体属性

   属性：font

   取值：style variant weight size family

   注意：使用简写属性时，必须要设置 family的值，否则无效

   ```
   font: 12px; //无效
   
   font: 12px "微软雅黑"; //通过
   ```

   

## 5.2 文本属性

1. 文本颜色

   属性：color

   取值：任意合法颜色

2. 文本排列方式

   作用：指定当前元素中的文本，行内元素，行内块元素的 水平对齐方式

   属性 ：text-align

   取值：left / center / right

3. 文字修饰

   作用：指定文本的线条样式

   属性：text-decoration

   取值：

   1. none 没有线条显示
   2. underline 下划线 \<u>\</u>
   3. overline 上划线
   4. line-through 删除线  相当于\<s>\</s>

4. 行高

   作用：指定元素中一行数据的高度。如果行高的高度高于文字高度本身，那么该段文本将在行高的范围内呈现出 垂直居中的显示效果。

   场合：

   1. 控制一行文本垂直居中对齐
   2. 设置行间距

   属性：line-height

   取值：以px为单位的数值

5. 首行文本缩进

   属性：text-indent

   取值：缩进的距离，以px为单位的数值

6. 文本阴影

   属性：text-shadow

   取值：h-shadow v-shaow blur color;

# 第六章 表格



## 6.1 表格的常用属性

1. 边距属性：padding

2. 尺寸属性：width，height

3. 文本格式化属性

   +  font-*
   + text-align
   + color
   + text-indent
   + ....

4. 背景属性

   + 背景色
   + 背景图
   + 渐变

5. border属性

6. vertical-align

   作用：在单元格中，设置文本的垂直对齐方式

   取值：

   1. top
   2. middle
   3. bottom

## 6.2 表格的特有属性

1. 边框合并

   属性：border-collapse

   取值：

   1. separate：默认值，即分离边框模式
   2. collapse：边框合并效果

2. 边框边距

   作用：单元格之间的距离

   属性：border-spacing

   取值：

   1. 指定一个值，表示 水平 和 垂直间距是相同的
   2. 指定两个值。第一个值 表示单元格间的水平间距，第二个值 表示单元格间的垂直间距

   注意：仅仅限于边框分离状态时使用，即 border-collapse：separate

3. 标题位置

   属性：caption-side

   取值：

   1. top：默认值，标题显示在表格之上
   2. bottom：标题显示在表格之下

4. 显示规则

   作用：指定表格的布局方式

   默认布局方式为 自动表格布局，单元格的宽度实际上由内容来决定的，与设定的值无关。

   属性：table-layout

   取值：

   1. auto：默认值，自动表格布局
   2. fixed：固定表格布局，即单元格的宽度以设定的值为主，而不取决于内容

   自动表格 VS 固定表格布局

   1. 自动表格布局
      + 自动表格布局，单元格大小会适应内容大小
      + 缺点：表格复杂时加载速度慢
      + 适用于不确定每列大小的情况下使用
      + 虽然算法慢，但是能体现出传统表格的特点
   2. 固定表格布局
      + 单元格大小取决于td中设置的值
      + 有点：加载速度较快
      + 确定每列大小时，可以使用固定表格布局
      + 算法较快，缺点是不灵活



# 第七章 浮动

1. 定位概述：定义元素框相对于其正常位置，应该出现的位置在哪里。简单说，定位就是改变元素在页面上的默认位置。

2. 定位分类

   1. 普通流定位（元素默认定位方式）
   2. 浮动定位
   3. 相对定位
   4. 绝对定位
   5. 固定定位

3. 普通流定位

   页面中的块级元素按照从上到下的方式排列，而且每个元素独占一行

   页面中的行内元素，按照从左到有的方式排列，当前行显示不下多余行内元素时，会自动换行

   问题：如何让多个块级元素在一行内显示

4. <span style="color:red">浮动定位（重点）</span>

   1. 浮动定位概述：如果将元素的定位方式设置为浮动定位，那么将具备以下几个特点

      + 浮动元素会脱离文档流，元素不再占据页面空间，<b style="color:blue">其它未浮动元素要上前补位</b>
      + 浮动元素会停靠在父元素的左边或右边或停靠在其它已浮动元素的边缘上
      + 浮动元素只会在当前行内浮动
      + 浮动元素依然位于父元素之内
      + <b style="color:red">解决问题：让多个块级元素在一行内显示</b>

   2. 语法

      属性：float

      取值：

      1. none，默认值，无浮动定位
      2. left，左浮动，让元素停靠在父元素左边
      3. right，右浮动，让元素停靠在父元素右边

   3. 浮动引发的特殊效果

      1. 当父元素的宽度显示不下所有的已浮动子元素时，最后一个将换行（有可能被卡住）

      2. 元素一旦浮动起来后，宽度将变成自适应（未人为指定情况下）

      3. 元素浮动起来后，将变成块级元素，尤其对行内元素影响最大

         块级：运行修改尺寸

         行内：不允许修改尺寸

      4. 文本，行内元素，行内块元素时，采用环绕的方式排列的，是不会被浮动元素压在下面的，会巧妙的避开浮动元素

   4. 清除浮动

      元素浮动起来之后，除了影响自己的位置之外，还会影响后序元素。

      如果后序元素不想被前面浮动元素所影响，可以使用 清除浮动的效果来解决影响。

      属性：clear

      取值：

      1. none：默认值，不做任何清除操作
      2. left：清除当前元素的前面元素左浮动带来的影响。即当前元素不会上前占位，并且左边不允许有浮动元素。
      3. right：清除当前元素的前面元素右浮动带来的影响。即当前元素不会上前占位，并且右边不允许有浮动元素。
      4. both：清除前面元素左右浮动带来的影响。

   5. 浮动元素对父元素带来的影响

      由于浮动元素会脱离文档流，所以会导致元素不占据父元素的页面空间。所以会对元素高度带来影响。如果一个元素中所有的子元素全部都浮动了，那么该元素的高度就是0.

      解决方案：

      1. 直接设置父元素高度。弊端：必须要知道父元素的准确高度。
      2. 设置父元素也浮动。弊端：对后序元素有影响。
      3. 为父元素设置overflow，取值为hidden 或者 auto。弊端：如果有子级内容要溢出显示，也一同被隐藏了。
      4. <b style="color:green">在父元素中追加空子元素，并设置其clear属性为both</b>



# 第八章 显示效果



## 8.1 显示方式

1. 作用：决定了元素在页面中如何摆放定位

2. 语法

   >属性：display
   >
   >取值：
   >
   >1. none 
   >
   >   让生成的元素不显示 特点：脱离文档流即 不占据页面空间
   >
   >2. block 
   >
   >   让元素变得和块级元素一样，自己占一行，宽度默认100%，可以手动修改宽和高
   >
   >3. inline
   >
   >   让元素变得和行内元素一样，宽和高自适应
   >
   >4. inline-block
   >
   >   让元素变得和行内块元素一样。多个元素占一行，但是允许修改宽和高

## 8.2 显示效果

1. visibility 属性

   作用：控制元素的可见性（显示/隐藏）

   属性：visibility 

   取值：

   1. visible

      默认值，可见的

   2. hidden

      隐藏元素，但是依然占据页面空间

   3. collapse（了解）

      使用在表格元素上，删除一行活一列时，不影响表格整体布局

   注意：display：none 和 visibility：hidden区别

   1. display：none 脱离文档流，所以隐藏后不占据页面空间
   2. visibility：hidden 隐藏元素，但并不脱离文档流，导致空间依然占据

2. opacity 属性

   >作用：改变元素透明度
   >
   >属性：opacity
   >
   >取值：0.0（完全透明）~1.0（不透明）

3. vertical-align 属性

   > 属性：vertical-align
   >
   > 取值：
   >
   > top/middle/bottom/baseline(默认，基线对齐)
   >
   > 作用：
   >
   > 1. 设置单元格内容的垂直对齐方式
   >
   > 2. 对行内块元素设置vertical-align，相当于设置  该元素两端的文本相对于该元素的垂直对齐方式
   >
   > 3. 设置图片两端的文本相对于图片的对齐方式
   >
   >    baseline 类似于bottom，但是底下多3个像素空白

## 8.3 光标

属性：cursor

取值：

1. default：默认值
2. pointer：小手
3. crosshair：+
4. text：工
5. wait：等待，<b style="color:red">谨慎使用</b>
6. help：帮助，带一个问号





# 第九章 列表



## 9.1 列表项标识

+ 属性：list-style-type
+ 取值
  1. none：无标记
  2. disc：实心圆
  3. circle：空心圆
  4. square：实心方块



## 9.2 列表项图像

+ 作用：由自定义图像作为显示的标识

+ 属性：list-style-image

+ 取值

  url(图像路径)



## 9.3 列表项位置

列表项默认位置在 列表项内容区域之外，列表的内边距范围内 

+ 属性：list-style-position
+ 取值
  1. outside：默认值，列表项标识位置在列表项之外
  2. inside：将标识放在列表项区域之内



## 9.4 列表属性

+ 属性：list-style

+ 取值

  type url（） position

+ 常用方式

  list-style:none



## 9.5 列表使用场合

纵向排列 和 横向排列的元素中





# 第十章 定位方式



## 10.1 定位属性

1. position属性

   + 作用：指定元素的定位类型
   + 属性：position
   + 取值
     + static：默认值
     + relative：相对定位
     + absolute：绝对定位
     + fixed：固定定位

2. 偏移属性

   + 改变元素在页面中的位置（移动元素）
   + 属性
     1. top
     2. bottom
     3. left
     4. right
   + 取值：偏移距离，以px为单位的数值

3. 堆叠顺序

   作用：在元素出现堆叠效果时，改变他们的顺序

   属性：z-index

   取值：没有单位的数字，值越大，越靠上



## 10.2 定位方式



### 10.2.1 相对定位

***

1. 相对定位：元素会相对于它原来的位置偏移某个距离，相对定位元素原本所占的空间会被保留。

2. 语法

   语法：position：relative 配合着 偏移属性 top/bottom/left/right 实现元素的位置移动

3. 使用场合

   + 实现元素位置微调



### 10.2.2 绝对定位

***

1. 绝对定位的特点

   + 绝对定位的元素会脱离文档流----不占据页面空间
   + 绝对定位的元素会相对于它<b style="color:green">最近的已定位的祖先元素</b>实现位置的初始化,如果元素没有已定位的祖先元素，那么元素会相对于最初的包含块实现位置的初始化，如body，html
   + 已定位：absolute/relative/fixed 称为已定位元素
   + 祖先元素：无限父级元素

   

2. 语法

   语法：position：absolute
   
   配合着 偏移属性 实现位置的改变
   
   
   
3. 特殊效果
   
   + 绝对定位的元素会变成块级元素
   + 绝对定位的元素依然可以使用margin，但是正常情况下auto会失效
   
   
   
   
   
### 10.2.3 堆叠顺序

***

作用：改变元素的堆叠效果

属性：z-index

取值：没有单位的数字，值越大，越靠上；可以取负数，取负数时，该元素在页面所有元素内容之下

注意：

1. z-index 只能作用在 relative/absolute/fixed 定位的元素上
2. 如果不知道z-index，则后来者居上
3. 父子关系的元素，不能使用z-index修改堆叠顺序。永远都是子压在父上



### 10.2.4 固定定位

***

作用：将元素固定在页面的某个位置处，不会随着滚动条变化而发生变化。

语法

position：fixed

配合着 偏移属性 实现位置的定位



注意：

1. 固定定位元素脱离文档流
2. 固定定位元素会变成块级
3. 固定定位元素永远都相对于body实现位置摆放。





## 10.3 各种定位使用场合

1. 浮动：多个块级元素想在一行内显示
2. 相对定位：元素要实现自身位置微调时
3. 绝对定位：实现页面弹出内容，用绝对定位，配合着父元素做相对定位一起完成
4. 固定定位：顶部固定，边栏（广告），使用固定定位



# 第十一章 复杂选择器



## 11.1 兄弟选择器

+ 特点

  1. 通过位置关系匹配元素
  2. 只能向后找，不能向前找

+ 相邻兄弟选择器

  1. 相邻兄弟

     ```html
     <div id="d1"></div>
     <p id="p1"></p>
     <span id="span"></span>
     ```

  2. 语法

     选择器1+选择器2

     ```
     #d1+p{color:red}
     ```

+ 通用兄弟选择器

  1. 通用兄弟：后面所有兄弟

  2. 语法

     选择器1~选择器2

     ```
     #d1~p{color:green}
     
     #d1~.blueColor{color:blue}
     ```

## 11.2 属性选择器

+ 属性选择器：允许使用元素附带的属性及其值来匹配页面的元素

+ 语法

  [attr=值]

+ 详解

  1. [attr]：匹配 附带 attr属性的元素

     ```shell
     # 匹配附带id属性的元素
     ```

  2. elem[attr]

     elem：表示页面中某一具体元素

     ```
     div[id]：页面中所有附带id属性的div
     ```

  3. [attr1]\[attr2]\[attr3]...

     匹配同时具备attr1、attr2和attr3属性的元素

     ```
     p[id][class]:既有id属性又有class属性的p元素
     ```

  4. [attr=value]

     value：表示某一具体数值

     作用：匹配 attr 属性值为value的所有元素

     ```
     input[type=text]
     ```

  5. [class~=value]

     作用：

     1. 用在多类选择器中
     2. 匹配 class 属性值 是以 空格 隔开的值列表，并且value是value 是该值列表中一个独立的值

  6. [attr^=value]

     ^= : 以 ... 开始

     作用：匹配attr属性值以 value 作为开始的元素

     ```html
        <style>
                [class^=col]{
                 border: 1px solid black;
             }
        </style>
        <p class="col-red-1">col-red-1</p>
        <p class="col-blue-2">col-blue-2</p>
        <p class="col-green-3">col-green-3</p>
     ```

  7. [attr*=value]

     *= ：包含 ... 字符

     作用：匹配 attr 属性值 中 包含value字符的元素

  8. [attr$=value]

     $= ：以...作为结束

     作用：匹配 attr 属性值 以 value作为结束的元素

  9. 注意：属性选择器中，所有的值都可以用单引号或者双引号引起来

     ```
     [class="c1"]
     [class='c1']
     [class=c1]
     ```



## 11.3 伪类选择器

+ 目标伪类[了解]

  1. 作用：突出显示活动的HTML锚元素

  2. 语法

     :target 或者 elem:target

     ```html
     <head>
         <meta charset="UTF-8">
         <title>Title</title>
         <style>
             div:target{
                 font-weight: bold;
                 color: red;
                 background-color: yellow;
             }
         </style>
     </head>
     <body>
             <a href="#NO1">第一章节</a>
             <div style="height: 2000px"></div>
             <div id="NO1">第一章节：什么是CSS</div>
             <div style="height: 2000px"></div>
     </body>
     ```

+ 元素状态伪类[了解]

  1. 作用：匹配 元素已启用， 被禁用，被选中的状态。主要应用在表单控件上
  2. 语法
     1. :enabled--匹配 每个已启用的元素
     2. :disabled--匹配 每个被禁用的元素
     3. :checked--匹配 每个被选中的元素(radio，checkbox)

+ 结构伪类

  1. 作用：通过元素间的结构关系，来匹配元素

  2. 语法

     1. <b style="color:green">:first-child</b>--匹配属于其父元素中的首个子元素

        ```
        td:first-child{}
        ```

     2. <b style="color:green">:last-child</b>--匹配属于其父元素中的最后一个子元素

        ```
        td:last-child{color:red}
        ```

     3. <b style="color:green">:nth-child(n)</b>

        匹配属于其父元素中的第n个子元素

     4. :empty

        匹配没有子元素的元素

        注意：不能包含文本

     5. :only-child

        匹配属于其父元素中的唯一子元素

        ```html
        <div id="d1">
        	<p id="p1"></p>
        	<span></span>
        </div>
        ```

+ 否定伪类

  1. 作用：将 匹配的元素 排除出去

  2. 语法

     :not(选择器)

     ```
     #tb1 td:not(:first-child){color:red}
     ```



## 11.4 伪元素选择器

+ 伪类：匹配元素的不同状态，匹配到的是元素

+ 伪元素：匹配的是某个元素中的某部分内容

+ 详解

  1. :first-letter 或者 ::first-letter

     匹配某元素的首字符

  2. :first-line 或者 ::first-line

     匹配某元素的首行字符

  3. ::selection

     匹配被用户选取的部分

+ <b style="color:green">单个冒号和双冒号的区别</b>

  1. ：既能表示 伪类选择器 也能表示 伪元素选择器(CSS2)
  2. :: 在CSS3 中 表示 伪元素选择器
  3. <b style="color:green">尽量使用单冒号</b>



# 第十二章  内容生成



## 12.1 伪元素选择器

1. :before 或者 ::before

   匹配 某元素的 内容区域之前

   ```
   <div>(:before)这是一个div</div>
   ```

2. :after 或者 ::after

   匹配 某元素的 内容区域之后

   ```
   <div>这是一个div(:after)</div>
   ```

3. 属性：content

   取值：

   1. <b style="color:red">字符串：用的最多</b>

      ```
      content:"台词"
      ```

   2. 图像：url()

      ```
      content:url(xxx.jpg)
      ```

   3. 计数器<b style="color:blue">[基本不用，难理解]</b>

      1. 定义：用CSS动态生成一组 有序的数字并且插入到元素中

      2. 语法

         > 属性：counter-reset
         >
         > 语法：counter-reset: 计数器名 初始值;
         >
         > counter-reset: 名1 值1 名2 值2;
         >
         > 注意：
         >
         > 	1. 初始值可以省略不写，默认为0
         >  	2. 不能放在使用的元素中声明，可以将计数器声明在使用元素的父元素中
         >
         > 属性：counter-increment
         >
         > 作用：指定计数器每次出现的增量,即每次出现的计数器值的变化范围
         >
         > 语法：counter-increment: 名 增量;
         >
         > counter-increment: 名1 增量1 名2 增量2;
         >
         > 注意：
         >
         > 1. 增量值可以为正，也可以为负数，也可以省略（默认为1）
         > 2. 哪个元素使用计数器，在哪个元素中设置计数器的增量
         >
         > 函数：counter()
         >
         > 作用：在指定元素中，使用计数器的值；必须配合content 属性一起使用
         >
         > 语法：
         >
         > ​	xx:before{
         >
         > ​	content:counter(名)
         >
         > }

4. 解决的问题

   1. 浮动元素的父元素高度
   2. 外边距溢出





# 第十三章 多列

1. <b style="color:red">用的不多，了解</b>

2. 语法

   1. 分隔列

      属性：column-count

      取值：数字

   2. 列间隔

      属性：column-gap

      取值：px为单位的数值

   3. 列规则

      作用：定义每两列之间的线条样式

      属性：column-rule

      取值： width style color

3. 兼容性

   Chrome:

   + -webkit-column-count
   + -webkit-column-gap
   + -webkit-column-rule

   Firefox

   + -moz-column-count
   + -moz-column-gap
   + -moz-column-rule

   



# 第十四章 CSS Hack

 

## 14.1 浏览器运行模式



模式

1. 混杂模式
2. 标准模式
3. 准标准模式



标准模式和混杂模式

1. 不同模式下，浏览器对CSS和js解析效果不同

2. 其它浏览器会根据DOCTYPE自动选择模式

3. 触发混杂模式：不声明DOCTYPE

4. 触发标准模式

   ```
   <!DOCTYPE html>
   ```



## 14.2 CSS Hack

+ 目的：针对不同浏览器编写不同的css样式

+ 原理：使用css属性优先级解决兼容性问题

+ 实现方式

  1. css类内部Hack

     在样式属性名或者值的前后增加前后缀以便识别不同的浏览器

  2. 选择器Hack

     在选择器前增加前缀来识别不同浏览器

     ```css
     /*IE6*/
     *div{
     	background-color:red
     }
     
     /*IE7*/
     *+div{
     	background-color:red
     }
     ```

  3. <b style="color:red">HTML头部引用Hack</b>

     使用HTML条件注释判断浏览器版本

     语法

     ```
     <!--[if 条件 IE 版本]>
     	要执行的操作
     <![endif]-->
     ```

     1. 版本

        取值：6~10直接的任意数值；省略版本，则判断是否为IE浏览器

        ```
        <!--[if 条件 IE 6]>
        	在 IE6 中执行的内容
        <![endif]-->
        ```

     2. 条件

        + gt：大于

          ```
              <!--[if gt IE 6]>
              <h1>只在IE6以上浏览器执行</h1>
              <![endif]-->
          ```

        + lt：小于

        + gte：大于等于

        + let：小于等于

        + ！：非

          ```
              <!--[if !IE 6]>
              <h1>只在非IE6浏览器执行</h1>
              <![endif]-->
          ```

        + 省略：判断是否为IE 或者 指定版本



# 第十五章 转换



## 15.1 简介

1. 转换：改变元素在页面中的大小、位置、形状、角度的一种方式。转换分为2D转换和3D转换

   2D转换：元素在x轴和y轴进行的转换操作

   3D转换：在2D的基础上，增加了Z轴

2. 转换属性

   1. 转换属性

      属性：transform

      取值：

      1. none
      2. transform-functions 一组转换函数，表示一个或者多个转换函数

   2. 转换的原点

      属性：transform-origin

      默认：原点在元素的中心处

      取值：

      两个值：值1(x) 值2(y)

      三个值：值1(x) 值2(y) 值3(z)



## 15.2 2D转换



### 15.2.1 位移

***

1. 2D位移：改变元素在x轴和y轴的位置

2. 语法

   属性：transform

   函数：

   1. translate(x)：改变元素在x轴上的位置；取值为正，右移
   2. translate(x,y)：改变元素在x轴和y轴上的位置
   3. translateX():改变元素在X轴的位置
   4. translateY()：改变元素在Y轴的位置



### 15.2.2 缩放

***

1. 定义：改变元素在x轴或y轴上的大小

2. 语法

   属性：transform

   函数：

   scale（value）：只给一个值，x和y轴等比缩放。

   取值：

   ​	默认为1。

   ​	缩小：0到1之间的小数 

   ​	放大：大于1的数

   ​	负值：旋转180度效果显示

   scale(x,y)：分别改变元素在x轴 和y轴的大小

   scaleX(x)

   scaleY(y)



### 15.2.3 旋转

***

1. 语法

   属性：transform

   函数：rotate(ndeg)

   n是旋转角度；

   ​	取值为正，顺时针旋转；

   ​	取值为负，逆时针旋转

2. 注意

   1. 转换原点：旋转围绕着原点来做的，原点不同，转换效果也不同
   2. 旋转时，连同坐标轴也一同跟着转



### 15.2.4 倾斜

***

1. 定义：改变元素在页面中的形状。以原点为中心，围绕着x轴和y轴产生的倾斜角度

2. 语法

   1. 属性：transform

   2. 函数：

      skew(xdeg)

      ​	横向倾斜

      ​	值为正，y轴按逆时针角度倾斜

      ​	值为负，y轴按顺时针角度倾斜

      skew(xdeg，ydeg)

      ​	x：横向倾斜

      ​	y：纵向倾斜

      ​	值为正，x轴按顺时针角度倾斜

      ​	值为负，x轴按逆时针角度倾斜

      skewX(ndeg)

      skewY(ndeg)



## 15.3 3D转换

1. perspective 属性

   模拟	人眼	到	3D变换物体	之间的距离。

   浏览器兼容性：

   1. Chrome 和 Sarari：

      -webkit-perspective：数值

2. 3D转换--旋转

   属性：transform

   取值：

   1. rotateX（ndeg）
   
   2. rotateY（ndeg）
   
   3. rotateZ（ndeg）
   
   4. rotate3D(x，y，z，ndeg)
   
      x，y，z
   
      ：取值为0说明该轴不参加旋转
   
      ​    取值为1说明该轴参加旋转
   
      rotate3D(1，0，0，45deg)
   
      rotate3D(0，1，0，45deg)
   
3. 3D转换--位移

   1. 定义：改变元素在x，y，z上的位置

   2. 语法

      1. transform-style 属性

         如何处理子元素的摆放位置

         取值：

         1. flat：默认值，不保留子元素的3D位置
         2. preserve-3d：保留子元素的3D位置

      2. transform 属性

         取值：

         ​	1. translateZ(z)

         ​	2. translate3d(x,y,z)





# 第十六章 过渡

1. 什么是过渡

   使得CSS属性值，在一段时间内，平缓变化的一个效果

2. 过渡效果四要素

   1. <b style="color:red">指定过渡属性</b>

   2. <b style="color:red">指定过渡时间</b>

   3. 指定过渡时间的速率

      匀速

      先快后慢

      ......

   4. 指定过渡延迟时间

      当用户激发操作后，等待多长时间才激发效果

3. 过渡属性

   1. 指定过渡属性

      属性：transition-property

      取值：

      	1. none
       	2. all
       	3. property-name：使用过渡效果的属性名称

      ```
      transition-property:background
      ```

   2. 可以设置过渡效果的属性

      1. 颜色属性

         color、background-color、border-color

      2. 取值为数值的属性

         margin、padding、background-size

      3. 转换属性

         transform

      4. 渐变属性（用的不多）

      5. 阴影属性（用的不多）

      6. visibility（用的不多）

   3. 指定过渡时长

      属性：transition-duration

      取值：s|ms 	为单位数值

      注意：默认值为0s，即没有过渡效果

   4. 指定过渡时间速率

      属性：transition-timing-function

      取值：

      1. ease：默认值，先慢后快再慢
      2. linear：匀速
      3. ease-in：慢速开始，快速结束
      4. ease-out：快速开始，慢速结束
      5. ease-in-out：慢速开始结束，中间先快后慢

   5. 过渡延迟

      属性：transition-delay

      取值：s|ms	为单位的时间

   6. 简写方式

      transition：property duration timing-funtion delay

      ```
      transition： transform  linear 5s;background 3s
      ```



# 第十七章 动画



## 17.1 定义

使元素从一种样式逐渐变化为另外一种样式的过程。CSS中实现动画，会存在兼容性问题，与动画相关的操作尽量加上浏览器前缀



## 17.2 使用步骤

1. 声明动画：指定动画名称以及创建动画中的每个状态

2. 为元素调用动画

   指定	调用的动画名称，时长，播放次数

   



## 17.3 声明动画

指定动画名称及各个关键帧

关键帧：当前元素状态的	时间点	以及	样式

语法：

​	在样式表中声明

```
@keyframes	动画名称{

	%0|from{动画开始时的样式}
	......
	100%|to{动画结束时的样式}	

}
```



## 17.4 调用动画



动画属性

1. animation-name

   作用：指定调用动画名称

2. animation-duration

   作用：指定动画完成一个周期所用时间 s|ms

3. animation-timing-function

   作用：指定动画的速率

   取值：ease、linear、ease-in、ease-out、ease-in-out

4. animation-delay

   作用：指定动画的延迟	s|ms

5. animation-iteration-cout

   作用：指定动画播放次数

   取值：

   	1. 具体数值

    	2. infinite：无限次播放

6. animation-direction

   作用：指定动画播放方向

   默认：由0%播放到100%

   取值：

    1. normal：默认播放

    2. reverse：逆向播放

    3. alternate：轮流播放

       奇数次数：0%~100%

       偶数次数：·100%~0%

7. 简写

   属性：animation

   取值：name	duration	timing-function	delay	iteration-cout	direction

8. animation-fill-mode

   作用：规定动画播放前后的填充效果

   取值：

   	1. none：默认值，没有填充效果
    	2. forwards：动画播放完成后，会保持在最后一个帧的状态上
    	3. backwards：动画播放前，应用在第一个帧的状态上（只有在延迟（delay）时间内，才会显示在第一帧上）
    	4. both：播放前和播放后分别采用对应的填充状态

9. animation-play-state

   作用：规定动画是播放还是暂停

   取值：

   	1. paused：暂停
   
    	2. running：播放

# 第十八章 CSS优化

