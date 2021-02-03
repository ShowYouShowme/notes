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

2. 内部样式表

3. 外部样式表