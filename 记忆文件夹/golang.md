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



```go
func TestIfMultiSet(t *testing.T){
	if v,err := SomeFunc(); err=nil{
		t.Log("1==1")
	}else{
		t.Log("2==2")
	}
}
```



### 2.4.3 switch

***

1. 条件表达式不限制为常量或者整数

2. 单个case中，可以出现多个结果选项，使用逗号分隔

3. 与C语言等相反，不需要用break明确退出case

4. 可不设定switch后的条件表达式，此时整个switch与多个if...else逻辑相同

5. 示例

   ```go
   func TestSwitchMultiCase(t *testing.T){
   	for  i := 0; i < 5; i++{
   		switch i{
   		case 0, 2:
   			t.Log("Even")
   		case 1,3:
   			t.Log("Odd")
   		default:
   			t.Log("it is not 0-3")
   		}
   	}
   }
   
   // 类似多个if...else
   func TestSwitchCaseCondition(t *testing.T){
   	for i :=0; i< 5; i++{
   		switch{
   		case i%2 == 0:
   			t.Log("Even")
   		case i%2 == 1:
   			t.Log("Odd")
   		default:
   			t.Log("unknow")
   		}
   	}
   }
   ```

   

# 第三章  常用集合



## 3.1 数组和切片



### 3.1.1 数组

1. 数组定义

   ```go
   func TestArrayInit(t *testing.T)  {
   	var arr [3]int //未赋值
   	arr1 := [4]int{1,2,3,4} // 定义同时赋值
   	arr3 := [...]int{1,2,4,5} // 元素个数有赋的值决定
   	t.Log(arr[1], arr[2])
   	t.Log(arr1, arr3)
   }
   ```

2. 数组遍历

   ```go
   // 遍历
   func TestArrayTravel(t *testing.T){
   	arr3 := [...]int{1,3,4,5}
   	for i := 0; i < len(arr3);i++{
   		t.Log(arr3[i])
   	}
   
   	for idx, e:= range arr3{
   		t.Log(idx, e)
   	}
   
   	for _, e:= range arr3{
   		t.Log(e)
   	}
   }
   ```

3. 多维数组

   ```go
   // 多维数组
   c := [2][2]int{{1,2},{3,4}}
   ```

4. 截取数组一部分

   ```go
   func TestArraySection(t *testing.T)  {
   	arr3 := [...]int{1,2,3,4,5}
   	arr3_sec := arr3[3:]
   	t.Log(arr3_sec)
   }
   ```



### 3.1.2 切片

***

1. 切片其实就是C++的Vector

2. 示例代码

   ```GO
   // 切片定义时 中括号里为空 数组定义时中括号有... 或者数字
   func TestSliceInit(t *testing.T)  {
   	var s0 []int
   	t.Log(len(s0), cap(s0)) // 和C++的vector类似
   
   	s0 = append(s0,1)
   	t.Log(len(s0), cap(s0))
   
   	s1 := []int{1,2,3,4}
   	t.Log(len(s1), cap(s1))
   
   	s2 := make([]int, 3, 5) // size == 3 capacity == 5
   	t.Log(len(s2), cap(s2))
   	// t.Log(s2[0], s2[1], s2[3], s2[4])
   }
   
   // 增长模式类似C++的vector
   func TestSliceGrowing(t *testing.T)  {
   	s :=[]int{}
   	for i:= 0; i < 10; i++{
   		s = append(s,i)
   		t.Log(len(s), cap(s))
   	}
   }
   
   func TestSliceShareMemory(t *testing.T)  {
   	year := []string{"11","22","33","44","55","66",
   		"77","88", "99", "1010","1213", "1212"}
   	Q2 := year[3:6]
   	t.Log(Q2, len(Q2), cap(Q2))
   
   	summer := year[5:8]
   	t.Log(summer, len(summer), cap(summer))
   	summer[0] = "Unknow" // Q2也受到影响
   	t.Log(Q2)
   	t.Log(year)
   }
   ```

   





### 3.1.3 数组和切片对比

***

1. 数组容量不可伸缩，切片可以
2. 数组可以比较，切片不行



## 3.2 Map声明和访问



### 3.2.1 声明

***

1. 示例代码

   ```go
   m := map[string]int{"one":1, "two":2, "three":3}
   
   m1 := map[string]int{}
   
   m1["one" ] = 1
   
   m2 := make(map[string]int, 10) // 初始化时指定capacity
   ```

2. 初始化

   ```go
   func TestInitMap(t *testing.T)  {
   	m1 := map[int]int{1:1,2:4,3:9}
   	t.Log(m1[2])
   
   	t.Logf("Len m1=%d", len(m1))
   
   	m2 := map[int]int{}
   	m2[4] = 16
   	t.Logf("len m2=%d", len(m2))
   
   	m3 := make(map[int]int,10)
   	t.Logf("len m3=%d", len(m3))
   }
   ```

3. 访问不存在的元素

   ```go
   func TestAccessNotExistingKey(t *testing.T)  {
   	m1 := map[int]int{}
   	t.Log(m1[1]) // 类似C++,元素不存在返回默认值0
   
   	m1[2] = 0
   	t.Log(m1[2])
   	// m1[3] = 0 // 根据OK来判断元素是否存在
   
   	if v,ok := m1[3]; ok{
   		t.Logf("key 3's val is %d",v)
   	}else{
   		t.Log("key 3 is no existing")
   	}
   }
   ```

4. 遍历

   ```go
   func TestTravelMap(t *testing.T)  {
   	m1 := map[int]int{1:1,2:4,3:9}
   	for k,v := range m1{
   		t.Log(k,v)
   	}
   }
   ```

   



## 3.3 Map与工厂模式



### 3.3.1 知识点

1. Map的value可以是方法
2. 与Dock Type接口方式一起，可以实现单一方法对象的工厂模式



### 3.3.2 示例





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

