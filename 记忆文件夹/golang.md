# 第一章 简介



## 1.0 安装

1. 下载安装包安装

2. 设置环境变量

   ```shell
   # GOLANG 的安装目录
   export GOROOT=/usr/local/go
   
   # go.exe的目录
   export PATH=$PATH:$GOROOT/bin
   ```

   

## 1.1 第一个程序

```go
// 文件路径 src/main/hello_world.go
package main // 包，表明代码所在模块

import "fmt"  // 引入依赖
func main()  {
	fmt.Println("Hello World!")
}
```



## 1.2 运行

1. 直接运行

   ```shell
   go run ${file_name}
   ```

2. 编译

   ```shell
   go build ${file_name}
   ```



## 1.3 程序入口

1. 必须是main包：<b style="color:red">package main</b>
2. 必须是main方法：<b style="color:red">func main()</b>
3. 文件名不一定是：<b style="color:red">main.go</b>



## 1.4 退出返回值

1. go中main函数不支持任何返回值
2. 通过<b style="color:red">os.Exit()</b>来返回状态



## 1.5 获取命令行参数

```go
package main

import "fmt"
import "os"
func main()  {
	fmt.Println("Hello World!")

	fmt.Println(os.Args)

	os.Exit(12)
}
```



# 第二章 程序基本结构



## 2.1 变量和常量



### 2.1.1 编写测试程序

***

1. 源码文件以<b style="color:red">_test</b>结尾：xxx_test.go

2. 方法名以Test开头：func Testxxx()

3. 代码示例

   ```GO
   // go test -v first_test.go
   package try_test
   
   import (
   	"testing"
   )
   
   func TestFirstTry(t *testing.T)  {
   	var a int = 1
   	var b int = 2
   	t.Log("a = ", a, " b = " , b)
   }
   ```



### 2.1.2 变量赋值

***

```GO
var a int = 1
var b int = 2

c := 3 // 自动类型推导
```



### 2.1.3 常量

***

```go
	const (
		Mon = 1
		Tue = 2
		Wed = 3
	)

	const (
		Readable = 1 << iota
		Writeable
		Executable
	)
// Readable  : 1
// Writeable : 2
// Executable : 4
	fmt.Print(Readable, " Writeable : ", Writeable , " Executable : ", Executable)
```



## 2.2 数据类型



### 2.2.1 类型

***

1. 布尔值

   ```
   bool
   ```

2. 字符串

   ```
   string
   ```

3. 整形

   ```
   int int8 int16 int32 int64
   ```

4. 无符号整形

   ```
   uint uint8 uint16 uint32 uint64
   ```

5. 字节

   ```
   byte
   ```

6. Unicode编码值

   ```
   rune
   ```

7. 浮点

   ```
   float32 float64
   ```

8. 复数

   ```
   complex64 complex128
   ```



### 2.2.2 类型转换

***

1. go语言不允许隐式类型转换

2. 别名和原有类型也不能进行隐式类型转换

3. 示例

   ```go
   // go test -v type_test.go
   package type_test
   
   import "testing"
   
   type MyInt int64
   func TestImplicit(t *testing.T)  {
   	var a int = 1
   	var b int64
   	b = int64(a) + 1
   
   	var c MyInt
   	c = MyInt(b) + 1
   	t.Log("a = ",a, " c = ", b," c = ",c)
   }
   ```





### 2.2.3 类型预定值

***

```go
math.MaxInt64

math.MaxFloat64

math.MaxUint32
```



### 2.2.4 指针类型

***

1. 不支持指针运算

2. string是值类型，默认为空字符串不是nil

3. 示例

   ```GO
   func TestPoint(t *testing.T) {
   	var a int = 1
   	var aPtr *int = &a
   	t.Log(a, aPtr)
   	t.Logf("%T %T", a, aPtr)//打印数据类型
   }
   
   func TestString(t *testing.T) {
   	var s string
   	t.Log("*" + s + "*") // string 默认为空字符串
   	t.Log(len(s))
   }
   ```



## 2.3 运算符



### 2.3.1 算术运算符

***

| 运算符 | 描述 |
| :----: | :--: |
|   +    |  加  |
|   -    |  减  |
|   *    |  乘  |
|   /    |  除  |
|   %    | 求余 |
|   ++   | 自增 |
|   --   | 自减 |

go没有前置++(++a)，只有后置++(a++)



数组比较

```GO
func TestCompareArray(t *testing.T){
	a := [...]int{1,2,3,4}
	b := [...]int{1,3,4,5}
	//c := [...]int{1,2,3,4,5} 长度不同不能比较,会导致编译错误
	d := [...]int{1,2,3,4}

	t.Log(a == b) // 两个数组长度相同且每个值相等,则数组相等
	t.Log(a == d)
}
```





### 2.3.2 位运算符

***

&^ 按位置零

```go
// 右边为1,则结果为0
// 右边为0,则结果为左边数据
1 &^ 0 --1
1 &^ 1 --0
0 &^ 1 --0
0 &^ 0 --0
```

```go
const(
	Readable = 1
	Writeable = 2
	Executable = 4
)

func TestBitClear(t *testing.T) {
	var a int = 7
	a = a &^ Readable
	a = a &^ Writeable
	t.Log(a&Readable == Readable,a&Writeable == Writeable, a&Executable == Executable)
}
```





## 2.4 条件和循环



### 2.4.1 循环

***

只支持for循环

```go
func TestWhileLoop(t *testing.T) {
	var n int = 0
	for n < 5{
		t.Log(n)
		n++
	}
}

// 无限循环
func TestLoopInfinite(t *testing.T){
	var n int = 0
	for {
		t.Log(n)
		n++
	}
}
```



### 2.4.2 条件

***

```GO
// condition 结果必须为布尔值
// 第一种条件语句
if condition{
    
}else{
    
}

// 第二种条件语句
if condition-1{
    
}else if condition-2{
    
}else{
    
}

// 第三种
if var declaration; condition{
    
}
```



# 第三章  常用集合





# 第四章 字符串



# 第五章 函数



# 第六章 面向对象编程



# 第七章 编写好的错误处理



# 第八章 包和依赖管理



# 第九章 并发编程



# 第十章 典型并发任务



# 第十一章 测试



# 第十二章 反射和Unsafe



# 第十三章 常见架构模式的实现



# 第十四章 常见任务



# 第十五章 性能调优



# 第十六章 高可用性服务设计

