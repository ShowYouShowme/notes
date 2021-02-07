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
   	左右外边距可以取值为auto，允许让块级元素水平居中显示。上下边距值auto无效
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



# 第七章 浮动

