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
   // go test -v .
   // 或者 go test -v
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

***

1. 工厂模式

   ```go
   func TestMapWithFunValue(t *testing.T)  {
   	m := map[int]func(op int)int{}
   	m[1] = func (op int)int  {
   		return op
   	}
   
   	m[2] = func (op int)int  {
   		return op * op
   	}
   
   	m[3] = func (op int)int  {
   		return op * op *op
   	}
   
   	t.Log(m[1](2), m[2](2),m[3](2))
   }
   ```

   

2. 实现set

   ```go
   // 实现set
   func TestMapForSet(t *testing.T)  {
   	mySet := map[int]bool{}
   	mySet[1] = true
   
   	var n = 1
   	// 判断元素是否存在
   	if mySet[n]{
   		t.Logf("%d is existing", n)
   	}else{
   		t.Logf("%d is not existing", n)
   	}
   
   	mySet[3] = true
   	t.Log(len(mySet))
   
   	//删除元素
   	delete(mySet, 1) // 指定key
   
   	if mySet[n]{
   		t.Logf("%d is existing", n)
   	}else{
   		t.Logf("%d is not existing", n)
   	}
   }
   ```

   





# 第四章 字符串



## 4.1 差异

1. string 是数据类型，不是引用或者指针
2. string 是只读的byte slice，len函数可以得到它所包含的byte数
3. string的 byte 数组可以存放任何数据



## 4.2 案例

1. 字符串切割和拼接

   ```go
   func TestStringFn(t *testing.T)  {
   	s := "A,B,C"
   	parts := strings.Split(s,",")
   	for _, part := range parts{
   		t.Log(part)
   	}
   	t.Log(strings.Join(parts, "-"))
   }
   ```

2. 字符串转换

   ```go
   func TestConv(t *testing.T)  {
   	s := strconv.Itoa(10)
   	t.Log("str " + s)
   	if i, err := strconv.Atoi("20"); err ==nil{
   		t.Log(10 + i)
   	}
   }
   ```

3. 字符串编码

   ```go
   // string 可以存放任意数据
   func TestString(t *testing.T)  {
   	var s string
   	t.Log(s)
   
   	s = "hello"
   	t.Log(len(s))
   
   	s = "\xE4\xB8\xA5" // 存放二进制数据
   	t.Log(s)
   	//s[1] = '3' // 错误,string 不可更改
   
   	t.Log("==========")
   	s = "中"
   	t.Log(len(s))
   
   
   	c := []rune(s) // 转为unicode
   	t.Log(len(c))
   
   	t.Logf("中 unicode %x", c[0])
   	t.Logf("中 UTF8 %x",s)
   }
   
   func TestStringToRune(t *testing.T)  {
   	s := "中华人民共和国"
   	for _, c := range s{
   		// c 是rune
   		t.Logf("%c %x", c, c)
   	}
   }
   ```

   

# 第五章 函数



## 5.1 函数



### 5.1.1 差异

***

1. 可以有多个返回值
2. 全部参数都是值传递
3. 函数可以作为变量的值
4. 函数可以作为参数和返回值



### 5.1.2 案例

***

1. 多返回值的函数

   ```go
   func returnMultiValues()(int,int)  {
   	return rand.Intn(10), rand.Intn(20)
   }
   ```

2. 函数装饰器

   ```go
   // 计算函数调用的时间
   func timeSpend(inner func(op int) int)func(op int)int  {
   	return func(n int) int {
   		start := time.Now()
   		ret := inner(n)
   		fmt.Println("time spend: ", time.Since(start).Seconds())
   		return ret
   	}
   }
   
   func slowFun(op int) int {
   	time.Sleep(time.Second * 2)
   	return op
   }
   
   func TestFn(t *testing.T)  {
   	tsSF := timeSpend(slowFun)
   	t.Log(tsSF(10))
   }
   ```

   

## 5.2 可变参数和defer



### 5.2.1 可变参数

***

```go
// 可变长参数
func sum(ops ...int) int {
	s := 0
	for _, op := range ops{
		s += op
	}
	return s
}

func TestVarParam(t *testing.T)  {
	t.Log(sum(1,2,3,4))
	t.Log(sum(1,2,3,4,5,6,7,8,9,10))
}
```





### 5.2.2 defer

***

1. 作用：函数延迟执行，在调用函数退出前执行，主要用于释放资源

2. 案例

   ```go
   // 延迟执行
   func TestDefer(t *testing.T)  {
   	// 函数退出先执行,用于清理资源,释放锁
   	defer func() {
   		t.Log("Clear resources")
   	}()
   
   	t.Log("Started")
   	panic("err") // 即使panic,defer依旧执行
   }
   ```

   

# 第六章 面向对象编程



## 6.1 行为的定义和实现



## 6.2 go语言的相关接口



## 6.3 扩展和复用



## 6.4 多态





# 第七章 编写好的错误处理



## 7.1 编写错误处理



### 7.1.1 错误机制

***

1. 没有异常机制
2. error类型实现了error接口
3. 用error.New快速创建错误实例



### 7.1.2 案例

***

1. 抛出指定错误

   ```go
   var LessThanTwoError  = errors.New("n should be not less than 2")
   var LargeThanHundredError = errors.New("n should be not large than 100")
   func GetFibonacci(n int)  ([]int, error){
   	if n < 2 {
   		return nil, LessThanTwoError
   	}
   
   	if n > 100{
   		return nil, LargeThanHundredError
   	}
   	fibList := []int{1,1}
   	for i := 2; i< n; i++{
   		fibList = append(fibList, fibList[i -2] + fibList[i -1])
   	}
   	return fibList, nil
   }
   func TestGetFibonacci(t *testing.T)  {
   	if v,err := GetFibonacci(-10); err != nil{
   		if err == LessThanTwoError{
   			t.Log("It is less.")
   		}
   		t.Error(err)
   	}else{
   		t.Log(v)
   	}
   }
   ```

   

2. 减少嵌套

   ```go
   func GetFibonacci1(str string)  {
   	var i int
   	var err error
   	var list []int
   
   	// 双层嵌套
   	if i, err = strconv.Atoi(str); err == nil{
   		if list, err = GetFibonacci(i); err == nil{
   			fmt.Println(list)
   		}else{
   			fmt.Println("Error", err)
   		}
   	}else{
   		fmt.Println("Error", err)
   	}
   }
   
   func GetFibonacci2(str string)  {
   	var i int
   	var err error
   	var list []int
   
   	if i, err = strconv.Atoi(str); err != nil{
   		fmt.Println("Error", err)
   		return
   	}
   
   	if list, err = GetFibonacci(i); err != nil{
   		fmt.Println("Error", err)
   		return
   	}
   	fmt.Println(list)
   }
   ```

   



## 7.2 panic和recover



### 7.2.1 panic

***

1. 用于不可恢复的错误
2. panic退出前会指定defer指定的内容



os.Exit 与 panic

1. os.Exit 退出时不会调用defer指定的函数
2. os.Exit 退出时不输出当前调用栈的信息



代码

1. 示例一

   ```go
   // defer 不会被调用
   func main()  {
   	defer func() {
   		fmt.Println("final")
   	}()
   	fmt.Println("start")
   	os.Exit(128)
   }
   ```

   

2. 示例二

   ```go
   // defer 被调用,并且显示调用栈信息
   func main()  {
   	defer func() {
   		fmt.Println("final")
   	}()
   	fmt.Println("start")
   	panic("wrong info")
   }
   ```

   



### 7.2.2 recover

***

1. 和C++对比

   ```c++
   // recover 类似C++的此功能
   try{
       ...
   }catch(...){
       // 捕获全部异常
   }
   ```

2. 从panic中恢复

   ```go
   func main()  {
   	defer func() {
           // 处理错误
   		if err := recover(); err != nil{
   			fmt.Println("recovered from ", err)
   		}
   	}()
   	fmt.Println("start")
   	panic("wrong info") // 抛出错误
   }
   ```

   



# 第八章 包和依赖管理



## 8.1 构建可复用的模块



### 8.1.1 package

***

1. 以<b style="color:red">首字母大写</b>来表明可被包外代码访问
2. 代码package可以和所在目录不一致
3. 同一目录里的go代码的package要保持一致



获取package

1. 通过go get 获取远程依赖

   + go get -u 强制从网络更新远程依赖

2. 注意代码在GitHub上的组织形式，以适应go get

   直接以代码路径开始，不要有src



本地包

1. 在$GOPATH/目录下，创建如下结构的文件夹和文件：

   ```shell
   |----bin
   |----pkg
   |----src
   |    |
   	 |------hello
   	 |      |-------hello2.go
   	 |      |-------hello.go
   	 |------main
   	        |
   	        |------main.go
   ```

2. 代码

   hello.go

   ```go
   package hello
    
   import (
     "fmt"
   )
    
   func SayHello() {
     fmt.Println("SayHello()-->Hello")
   }
   ```

   hello2.go

   ```go
   package hello
    
   import (
     "fmt"
   )
    
   func SayWorld() {
     fmt.Println("SayWorld()-->World")
   }
   ```

   main.go

   ```go
   package main
    
   import (
     "hello"
   )
    
   func main() {
     hello.SayHello()
     hello.SayWorld()
   }
   ```

3. 总结：GitHub上面的代码，直接copy到src目录下就可以使用了



### 8.1.2 init 方法

***

1. main函数执行前，全部依赖的package的init方法都会被执行
2. 不同包的init函数按照包导入的依赖关系决定执行顺序
3. 每个包可以有多个init函数
4. 包的每个源文件也可以有多个init函数



代码

```go
// import 该包的时候会调用两个init函数
package series

import "fmt"

func init()  {
	fmt.Println("init1")
}

func init()  {
	fmt.Println("init2")
}

func GetFibonacciSerie(n int) []int {
	ret := []int{1,1}
	for i := 2; i < n; i++{
		ret = append(ret, ret[i - 2] + ret[i - 1])
	}
	return ret
}

func Square(input int)int  {
	return input * input
}

```





### 8.1.3 使用远程package

***

1. 命令行

   ```shell
   # 每次都从网络更新
   go get -u ${URL}
   
   # URL 
   https://github.com/easierway/concurrent_map.git
   
   # 去掉前缀 https:// 和 后缀 .git
   
   go get -u github.com/easierway/concurrent_map
   ```

2. 代码示例

   ```go
   package remote_package
   
   import "testing"
   import cm "github.com/easierway/concurrent_map"  // 重命名包
   func TestConcurrentMap(t *testing.T)  {
   	m := cm.CreateConcurrentMap(99)
   	m.Set(cm.StrKey("key"), 10)
   	t.Log(m.Get(cm.StrKey("key")))
   }
   ```

   



## 8.2 依赖管理



### 8.2.1 依赖问题

***

1. 同一环境下，不同项目无法使用同一包的不同版本
2. 无法管理对包的特定版本的依赖



### 8.2.2 vendor 路径

***

1. Go 1.5 release 支持vendor目录

2. 依赖查找次序如下

   > 1. 当前包的vendor目录
   > 2. 向上级目录查找，直到找到src下的vendor目录
   > 3. 在GOPATH下面查找依赖包
   > 4. 在GOROOT目录下查找



### 8.2.3 依赖管理工具

***

1. godep
2. glide
3. dep
4. <b style="color:red">go mod：官方的包管理器，推荐使用</b>





### 8.2.4 go mod 使用

***

1. 设置代理

   ```shell
   # 必须要设置,否则包下载容易出错
   go env -w GOPROXY="https://goproxy.io,direct"
   ```

2. 开启

   ```shell
   go env -w GO111MODULE=on
   ```

3. 编辑

   ```shell
   go mod edit
   ```

4. 拉取缺少的模块，移除不用的模块

   ```shell
   go mod tidy
   ```

5. 初始化

   ```shell
   go mod init ${name}
   ```

   

### 8.2.5 使用项目内的包

***

1. 开启GO111MODULE

   ```shell
   go env -w GO111MODULE=on
   ```

2. 初始化项目

   ```shell
   go mod init ${name}
   ```

3. 文件架构

   ```shell
   -----SRC
   |     |
   |     |-------src
   |			   |
   |			   |-----hello.go
   |		       |-----main.go
   |			   |-----signal
   |			           |
   |					   |
   |					   |-------http.go
   |					   |-------rand.go
   |					   |-------signal.go
   |-----go.mod
   ```

4. 注释

   ```shell
   # package signal
   http.go
   rand.go
   signal.go
   
   # package main
   hello.go
   main.go
   ```

5. main.go 引用signal包

   ```go
   // save-to-disk 是go.mod 内 module的名称
   import "save-to-disk/src/signal"
   ```

6. 编译

   ```shell
   # STEP-1 进入源码目录
   cd ../src
   
   # STEP-2 编译
   go build
   或者
   go build .
   
   # 不要这样编译,如果有多个文件都是package main,会报错
   go build main.go 
   ```

   







# 第九章 并发编程



## 9.1 协程机制

```go
func TestGroutine(t *testing.T)  {
	for i := 0; i< 10; i++{
		go func(i int) {
			fmt.Println(i)
		}(i) // 传值进函数,不会有问题

		// 下面这种写法会存在竞争,导致结果出错
		//go func() {
		//	fmt.Println(i)
		//}()
	}

	time.Sleep(time.Microsecond * 50)
}
```



## 9.2 共享内存并发机制

1. 非线程安全程序

   ```go
   func TestCounter(t *testing.T) {
   	counter := 0
   	for i := 0; i < 5000; i++ {
   		go func() {
   			counter++
   		}()
   	}
   	time.Sleep(1 * time.Second)
   	t.Logf("counter = %d \n", counter)
   }
   ```

2. 线程安全

   ```go
   func TestCounterThreadSafe(t *testing.T) {
   	counter := 0
   	var mut sync.Mutex
   	for i := 0; i < 5000; i++ {
   		go func() {
   			defer func() {
   				mut.Unlock()
   			}()
   			mut.Lock()
   			counter++
   		}()
   	}
   	time.Sleep(1 * time.Second)
   	t.Logf("counter = %d \n", counter)
   }
   ```

3. 线程同步，等待其它线程完成WaitGroup

   ```go
   func TestCounterWaitGroup(t *testing.T) {
   	counter := 0
   	var mut sync.Mutex
   	var wg sync.WaitGroup
   	for i := 0; i < 5000; i++ {
   		wg.Add(1)
   		go func() {
   			defer func() {
   				mut.Unlock()
   			}()
   			mut.Lock()
   			counter++
   			wg.Done()
   		}()
   	}
   	wg.Wait() // 等待其它线程完成
   	t.Logf("counter = %d \n", counter)
   }
   ```

   

## 9.3 CSP并发机制

1. 顺序执行

   ```go
   func service() string {
   	time.Sleep(time.Microsecond * 50)
   	return "Done"
   }
   
   func otherTask() {
   	fmt.Println("working on something else")
   	time.Sleep(time.Microsecond * 100)
   	fmt.Println("Task is done")
   }
   
   func TestServie(t *testing.T) {
   	fmt.Println(service())
   	otherTask()
   }
   ```

2. 异步执行[用channel进行数据交互]

   ```go
   func service() string {
   	time.Sleep(time.Microsecond * 50)
   	return "Done"
   }
   
   func AsyncService() chan string {
   	retCh := make(chan string)
   	
   	go func() {
   		ret := service()
   		fmt.Println("return result.")
   		retCh <- ret // 阻塞,直到对方读取
   		fmt.Println("service exited.")
   	}()
   	return retCh
   }
   
   func otherTask() {
   	fmt.Println("working on something else")
   	time.Sleep(time.Microsecond * 1000)
   	fmt.Println("Task is done.")
   }
   
   func TestAsyncService(t *testing.T)  {
   	retCh := AsyncService()
   	otherTask()
   	fmt.Println(<-retCh) // 阻塞,直到有数据可读
   	time.Sleep(time.Second * 1)
   }
   ```

   



### 9.3.1 channel

***

1. 普通channel

   > + 写入会阻塞，直到另一方读取
   > + 读取会阻塞，直到另一方写入

2. buffer channel

   > + 容量未满，可以直接写入，不阻塞；如果容量满了，必须等到接受消息的一方读取一个数据
   > + 读取数据时，如果channel有数据直接返回；否则阻塞到对方写入数据



## 9.4 多路选中和超时

```go
func service() string {
	time.Sleep(time.Millisecond * 50)
	return "Done"
}

func AsyncService() chan string {
	retCh := make(chan string)
	
	go func() {
		ret := service()
		fmt.Println("return result.")
		retCh <- ret // 阻塞,直到对方读取
		fmt.Println("service exited.")
	}()
	return retCh
}

// 设置超时
func TestSelect(t *testing.T) {
	select {
	case ret := <-AsyncService():
		t.Log(ret)
	case <-time.After(time.Millisecond * 10):
		t.Error("time out")
	}
}
```



## 9.5 channel的关闭和广播



### 9.5.1 channel的关闭

***

1. <b style="color:red">向关闭的channel发数据，会导致panic</b>

2. <b style="color:green">从已关闭的channel读取数据，返回数据的0值</b>

3. 安全读取

   ```go
   // ok 为bool值,true表示正常接受,false表示通道关闭
   v,ok <-ch
   ```

4. channel的接受者会在channel关闭时，立刻返回，上述ok值为false。可利用此机制进行广播

   示例一

   ```go
   func dataProducer(ch chan int, wg *sync.WaitGroup) {
   	go func() {
   		for i := 0; i < 10; i++ {
   			ch <- i
   		}
   		wg.Done()
   	}()
   }
   
   func dataReceive(ch chan int, wg *sync.WaitGroup) {
   	go func() {
   		// 1-- 有时候不知道Producer放多少数据,如何知道对方已经放完了
   		// 1.1 -- 用特殊值表示已经放完,比如-1
   		// 1.2 -- 如果此时有多个Receive,Producer 必须知道Receive的个数
   		for i := 0; i < 10; i++ {
   			data := <-ch // 返回0值
   			fmt.Println(data)
   		}
   		wg.Done()
   	}()
   }
   
   func TestCloseChannel(t *testing.T) {
   	var wg sync.WaitGroup
   	ch := make(chan int)
   	wg.Add(1)
   	dataProducer(ch, &wg)
   	wg.Add(1)
   	dataReceive(ch, &wg)
   	wg.Wait()
   }
   ```

   示例二

   ```go
   func dataProducer(ch chan int, wg *sync.WaitGroup) {
   	go func() {
   		for i := 0; i < 10; i++ {
   			ch <- i
   		}
   		close(ch)
   		wg.Done()
   	}()
   }
   
   func dataReceive(ch chan int, wg *sync.WaitGroup) {
   	go func() {
   		for  {
               // 利用ok判断对方是否已经关闭
   			if data, ok := <-ch; ok{
   				fmt.Println(data)
   			} else{
   				break
   			}
   		}
   		wg.Done()
   	}()
   }
   
   func TestCloseChannel(t *testing.T) {
   	var wg sync.WaitGroup
   	ch := make(chan int)
   	wg.Add(1)
   	dataProducer(ch, &wg)
   	wg.Add(1)
   	dataReceive(ch, &wg)
   	wg.Add(1)
   	dataReceive(ch, &wg)
   	wg.Wait()
   }
   ```

   



## 9.6 任务的取消

示例代码

```go
func isCancelled(cancelChan chan struct{}) bool{
	select {
	case <- cancelChan:
		return true
	default:
		return false
	}
}

// 只能取消一个
func cancel_1(cancelChan chan struct{})  {
	cancelChan <- struct{}{}
}

// 取消全部
func cancel_2(cancelChan chan struct{})  {
	close(cancelChan)
}

func TestCancel(t *testing.T)  {
	cancelChan := make(chan struct{},0)
	for i := 0; i < 5; i++{
		go func(i int, cancelCh chan struct{}) {
			for{
				if isCancelled(cancelCh){
					break
				}
				time.Sleep(time.Millisecond * 5)
			}
			fmt.Println(i, "cancelled")
		}(i ,cancelChan)
	}
	cancel_2(cancelChan)
	time.Sleep(time.Second * 1)
}
```



## 9.7 Context与任务取消



### 9.7.1 Context

***

1. 根Context：通过context.Background()创建

2. 子Context：context.WithCancel(parentContext)创建

   ```go
   ctx, cancel := context.WithCancel(context.Background())
   ```

   

3. 当前Context被取消时，基于它的子context都会被取消

4. 接收取消通知<- ctx.Done()

5. 案例

   ```go
   func isCancelled(ctx context.Context) bool{
   	select {
   	case <- ctx.Done():
   		return true
   	default:
   		return false
   	}
   }
   
   func TestCancel(t *testing.T)  {
   	ctx, cancel := context.WithCancel(context.Background())
   	for i := 0; i < 5; i++{
   		go func(i int, ctx context.Context) {
   			for{
   				if isCancelled(ctx){
   					break
   				}
   				time.Sleep(time.Millisecond * 5)
   			}
   			fmt.Println(i, "cancelled")
   		}(i ,ctx)
   	}
   	cancel()
   	time.Sleep(time.Second * 1)
   }
   ```

   

# 第十章 典型并发任务



## 10.1 只运行一次

```go
type Singleton struct {

}

var singleInstance *Singleton
var once sync.Once
func GetSingletonObj() *Singleton {
	once.Do(func() {
		fmt.Println("Create Obj")
		singleInstance = new(Singleton)
	})
	return singleInstance
}

func TestGetSingletonObj(t *testing.T)  {
	var wg sync.WaitGroup
	for i := 0; i < 10; i++{
		wg.Add(1)
		go func() {
			obj := GetSingletonObj()
			fmt.Printf("%x \n", unsafe.Pointer(obj))
			wg.Done()
		}()
	}
	wg.Wait()
}
```



## 10.2 仅需任意任务完成

```go
func runTask(id int) string {
	time.Sleep(10 * time.Millisecond)
	return fmt.Sprintf("the result is from %d", id)
}

func FirstResponse() string {
	numOfRunner := 10
	ch := make(chan string, numOfRunner) // 确保其他协程可以完成
	for i := 0; i < numOfRunner; i++{
		go func(i int) {
			ret := runTask(i)
			ch <- ret
		}(i)
	}
	return <-ch
}

func TestFirstResponse(t *testing.T)  {
	t.Log("Before:", runtime.NumGoroutine())
	t.Log(FirstResponse())
	time.Sleep(time.Second * 1)
	t.Log("After:", runtime.NumGoroutine())
}
```



## 10.3 所有任务完成

```go
func runTask(id int) string {
	time.Sleep(10 * time.Millisecond)
	return fmt.Sprintf("the result is from %d", id)
}

func AllResponse() string {
	numOfRunner := 10
	ch := make(chan string, numOfRunner)
	for i := 0; i < numOfRunner; i++{
		go func(i int) {
			ret := runTask(i)
			ch <- ret
		}(i)
	}

	finalRet := ""
	for j := 0; j < numOfRunner; j++{
		finalRet += <-ch + "\n"
	}
	return finalRet
}

func TestAllResponse(t *testing.T)  {
	t.Log("Before:", runtime.NumGoroutine())
	t.Log(AllResponse())
	time.Sleep(time.Second * 1)
	t.Log("After:", runtime.NumGoroutine())
}

```



## 10.4 对象池

```go
type ReuseableObj struct {

}

type ObjPool struct {
	bufChan chan *ReuseableObj
}

func NewObjPool(numOfObj int) *ObjPool {
	objPool := ObjPool{}
	objPool.bufChan = make(chan *ReuseableObj, numOfObj)
	for i := 0; i < numOfObj; i++{
		objPool.bufChan <- &ReuseableObj{}
	}
	return &objPool
}

func (p *ObjPool) GetObj(timeout time.Duration)(*ReuseableObj,error) {
	select {
	case ret := <- p.bufChan:
		return ret, nil
	case <- time.After(timeout): // 超时控制
		return nil, errors.New("time out")
	}
}

func (p *ObjPool)ReleaseObj(obj *ReuseableObj) error{
	select {
	case p.bufChan <- obj:
		return nil
	default:
		return errors.New("overflow")
	}
}

func TestObjPool(t *testing.T) {
	pool := NewObjPool(10)

    // 往满的池子放对象
	//if err := pool.ReleaseObj(&ReuseableObj{}); err != nil{
	//	t.Error(err)
	//}
    
    // 多拿一个对象,会导致出错
	for i := 0; i < 11; i++{
		if v, err := pool.GetObj(time.Second * 1); err != nil{
			t.Error(err)
		}else{
			fmt.Printf("%T \n", v)
			//if err := pool.ReleaseObj(v); err != nil{
			//	t.Error(err)
			//}
		}
	}
	fmt.Println("Done")
}
```



## 10.5 sync.pool对象缓存

1. 生命周期受到GC影响，不时候做连接池等，需自己管理生命周期的资源的池化

2. 协程安全，会有锁的开销

3. 适合于通过复用，降低复杂对象的创建和GC代价

4. 示例代码

   示例一

   ```go
   func TestSyncPool(t *testing.T)  {
   	pool := &sync.Pool{
   		New: func() interface{}{
   			fmt.Println("Create a new object.")
   			return 100
   		},
   	}
   
   	v := pool.Get().(int)
   	fmt.Println(v)
   	pool.Put(3)
   
   	runtime.GC() // 强制GC,会清空Pool
   	v1, _ := pool.Get().(int)
   	fmt.Println(v1)
   	//v2, _ := pool.Get().(int)
   	//fmt.Println(v2)
   	//v3, _ := pool.Get().(int)
   	//fmt.Println(v3)
   }
   ```

   示例二

   ```go
   func TestSyncPoolInMultiGroutine(t *testing.T){
   	pool := &sync.Pool{
   		New : func() interface{}{
   			fmt.Println("Create a new object")
   			return 10
   		},
   	}
   
   	pool.Put(100)
   	pool.Put(100)
   	pool.Put(100)
   
   	var wg sync.WaitGroup
   	for i := 0; i < 10; i++{
   		wg.Add(1)
   		go func(id int) {
   			fmt.Println(pool.Get())
   			wg.Done()
   		}(i)
   	}
   	wg.Wait()
   }
   ```

   

   



# 第十一章 测试



## 11.1 单元测试





内置单元测试框架

1. Fail，Error：该测试失败，该测试继续执行，其它测试继续执行

   ```go
   func TestErrorInCode(t *testing.T) {
   	fmt.Println("Start")
   	t.Error("Error")
   	fmt.Println("End")
   }
   ```

   

2. FailNow，Fatal：该测试失败，该测试终止，其它测试继续执行

   ```go
   func TestFailInCode(t *testing.T) {
   	fmt.Println("Start")
   	t.Fatal("Error")
   	fmt.Println("End")
   }
   ```

   

3. 代码覆盖率

   ```shell
   # 不需要指定文件
   go test -v -cover
   ```

4. 断言

   ```shell
   https://github.com/stretchr/testify/
   ```

   示例代码

   ```go
   // 不使用断言
   func TestSquare(t *testing.T) {
   	inputs := [...]int{1,2,3}
   	expected := [...]int{1,4,19}
   	for i:=0; i < len(inputs); i++{
   		ret := square(inputs[i])
   		if ret != expected[i]{
   			t.Errorf("inputs is %d, the expected is %d, the actual %d",inputs[i], expected[i], ret)
   		}
   	}
   }
   ```

   ```go
   // 使用断言
   import (
   	"fmt"
   	"github.com/stretchr/testify/assert"
   	"testing"
   )
   func TestSquareWithAssert(t *testing.T) {
   	inputs := [...]int{1,2,3}
   	expected := [...]int{1,4,19}
   	for i:=0; i < len(inputs); i++{
   		ret := square(inputs[i])
   		assert.Equal(t, expected[i], ret)
   	}
   }
   ```

   



## 11.2 Benchmark

1. 示例代码

   ```go
   func BenchmarkConcatStringByAdd(b *testing.B) {
   
   	elems := []string{"1","2","3","4","5"}
   	b.ResetTimer()
   	for i := 0; i < b.N; i++ {
   		ret := ""
   		for _, elem := range elems{
   			ret += elem
   		}
   	}
   	b.StopTimer()
   }
   
   func BenchmarkConcatStringByBytesBuffer(b *testing.B) {
   	elems := []string{"1","2","3","4","5"}
   	b.ResetTimer()
   	for i := 0; i < b.N; i++ {
   		var buf bytes.Buffer
   		for _, elem := range elems{
   			buf.WriteString(elem)
   		}
   	}
   	b.StopTimer()
   }
   ```

2. 运行性能测试

   ```shell
   go test -bench=.
   
   # 显示内存分配情况
   go test -bench=. -benchmem
   ```

3. 结果说明

   ```shell
   BenchmarkConcatStringByAdd-6             9460536               127.3 ns/op
   BenchmarkConcatStringByBytesBuffer-6    20035194                59.75 ns/op
   
   # -6 CPU核心数
   # 9460536               127.3 ns/op
   # 执行9460536次,每次花费127.3 ns
   ```

   



## 11.3 BDD

1. 框架地址

   ```shell
   # BDD 是一个测试框架
   https://github.com/smartystreets/goconvey.git
   ```

2. 安装

   ```shell
   go get -u github.com/smartystreets/goconvey
   ```

3. 启动WEB UI

   ```shell
   $GOPATH/bin/goconvey
   ```

4. 测试代码

   ```go
   package test
   
   import (
   	. "github.com/smartystreets/goconvey/convey"
   	"testing"
   )
   func TestSpec(t *testing.T) {
   	Convey("Given 2 even numbers", t, func(){
   		a := 2
   		b := 4
   
   		Convey("When add the two numbers", func(){
   			c := a + b
   
   			Convey("Then the result is still even", func() {
   				So(c % 2, ShouldEqual, 0)
   			})
   		})
   	})
   }
   ```

5. 运行测试

   ```shell
   go test -v
   ```

   





# 第十二章 反射和Unsafe



## 12.1 反射编程

1. 基本代码

   ```go
   func CheckType(v interface{})  {
   	t := reflect.TypeOf(v)
   	switch t.Kind() {
   	case reflect.Float32, reflect.Float64:
   		fmt.Println("Float")
   	case reflect.Int,reflect.Int32,reflect.Int64:
   		fmt.Println("integer")
   	default:
   		fmt.Println("Unknown",t)
   	}
   }
   
   func TestBasicType()  {
   	var f float64 = 12
   	CheckType(f)
   }
   
   func TestTypeAndValue()  {
   	var f int64 = 10
   	fmt.Println(reflect.TypeOf(f), reflect.ValueOf(f))
   	fmt.Println(reflect.ValueOf(f).Type())
   }
   ```

2. 利用反射访问对象成员和方法

   ```go
   type Employee struct{
   	EmployeeID string
   	Name string `format:"normal"`
   	Age  int
   }
   
   func (e *Employee)UpdateAge(newVal int)  {
   	e.Age = newVal
   }
   func main()  {
   	e := &Employee{"1","Mike",30}
   	v := reflect.ValueOf(*e).FieldByName("Name") // 通过名称访问成员
   	fmt.Printf("%v, %T", v,v)
   
   	if nameField, ok := reflect.TypeOf(*e).FieldByName("Name"); !ok{
   		fmt.Println("failed to get Name's field.")
   	}else{
   		fmt.Println("Tag:format", nameField.Tag.Get("format"))
   	}
   
   // 通过名称调用成员函数
   reflect.ValueOf(e).MethodByName("UpdateAge").Call([]reflect.Value{reflect.ValueOf(3)})
   	fmt.Println("Update Age : ", e)
   }
   ```

   

## 12.2 万能程序



### 12.2.1 比较切片和map

***

```go
func TestDeepEqual(t *testing.T)  {
	a := map[int]string{1:"one", 2:"two", 3:"three"}
	b := map[int]string{1:"one", 2:"two", 4:"three"}

	//t.Log(a == b)
	t.Log(reflect.DeepEqual(a,b))

	s1 := []int{1,2,3}
	s2 := []int{1,2,3}
	s3 := []int{2,3,1}
	t.Log("s1 == s2 : ", reflect.DeepEqual(s1, s2))
	t.Log("s1 == s3 : ", reflect.DeepEqual(s1, s3))
}
```





### 12.2.1 反射的特点

***

1. 提高程序灵活性
2. 降低程序可读性
3. 降低程序的性能



通过反射设置不同类的对象的相同属性

```go
type Employee struct {
	EmployeeID string
	Name string `format:"normal"`
	Age  int
}

type Customer struct {
	CookieID string
	Name     string
	Age      int
}

func fillBySettings(st interface{}, settings map[string]interface{}) error  {
	if reflect.TypeOf(st).Kind() != reflect.Ptr{
		return errors.New("not ptr")
	}
	
	if reflect.TypeOf(st).Elem().Kind() != reflect.Struct{
		return errors.New("not struct")
	}

	var (
		field reflect.StructField
		exist bool
	)
	for k,v := range settings{
		if field, exist = reflect.TypeOf(st).Elem().FieldByName(k); exist == false{
			continue
		}

		if reflect.TypeOf(v) != field.Type{
			continue
		}

		// 设置值
		reflect.ValueOf(st).Elem().FieldByName(k).Set(reflect.ValueOf(v))
	}
	fmt.Println("success")
	return nil
}

func TestFillNameAndAge(t *testing.T)  {
	m := map[string]interface{}{"Name":"nash", "Age":28}
	e := new(Employee)
	fillBySettings(e, m)

	fmt.Println(e)

	c := &Customer{}
	fillBySettings(c, m)
	fmt.Println(c)
}
```



## 12.3 不安全编程



1. 类型转换

   ```go
   func TestUnsafe(t *testing.T)  {
   	i := 10
   	f := *(*float64)(unsafe.Pointer(&i))
   	t.Log(unsafe.Pointer(&i))
   	t.Log(f)
   }
   ```

2. 别名之间类型转换

   ```go
   type MyInt int
   
   func TestConvert(t *testing.T)  {
   	a := []int{1,2,3,4}
   	b := *(*[]MyInt)(unsafe.Pointer(&a))
   	t.Log(b)
   }
   ```

3. 共享buffer实现线程安全

   ```go
   func TestAtomic(t *testing.T)  {
   	var shareBufPtr unsafe.Pointer
   
   	writeDataFun := func() {
   		data := []int{}
   		for i := 0; i < 100; i++ {
   			data = append(data, i)
   		}
   		atomic.StorePointer(&shareBufPtr, unsafe.Pointer(&data))
   	}
   
   	readDataFun := func() {
   		data := atomic.LoadPointer(&shareBufPtr)
   		fmt.Println(data, (*[]int)(data))
   	}
   
   	var wg sync.WaitGroup
   
   	writeDataFun()
   	for i := 0; i < 10; i++{
   		wg.Add(1)
   		go func() {
   			for i := 0; i < 10; i++{
   				writeDataFun()
   				time.Sleep(time.Millisecond * 100)
   			}
   			wg.Done()
   		}()
   
   		wg.Add(1)
   		go func() {
   			for i := 0; i< 10; i++{
   				readDataFun()
   				time.Sleep(time.Millisecond * 100)
   			}
   			wg.Done()
   		}()
   	}
       wg.Wait()
   }
   ```

   

# 第十三章 常见架构模式的实现



# 第十四章 常见任务



## 14.1 内置JSON解析



## 14.2 easyjson



## 14.3 HTTP服务



路由规则

1. URL分为两种

   > 以/结尾，表示子树，可以匹配它的子路径
   >
   > 末尾不是/，表示叶子

2. 采用最长匹配原则

3. 如果没有找到任何匹配项，返回404错误



示例

```go
func main()  {
	http.HandleFunc("/", func(writer http.ResponseWriter, request *http.Request) {
		fmt.Fprintf(writer, "Hello World!")
	})

	http.HandleFunc("/time", func(writer http.ResponseWriter, request *http.Request) {
		t := time.Now()
		timeStr := fmt.Sprintf("\"time\": \"%s\"", t)
		writer.Write([]byte(timeStr))
	})

	http.ListenAndServe(":8080", nil)
}
```



处理GET请求

```go
	http.HandleFunc("/", func(writer http.ResponseWriter, request *http.Request) {
		request.ParseForm()
		if request.Method == "GET" {
			fmt.Println("method:", request.Method)
			username := request.Form.Get("username")
			password := request.Form.Get("password")
			fmt.Println("username : ", username, ", password :", password)
		}
		fmt.Fprintf(writer, "Hello World!")
	})
```



处理POST请求

```go
	http.HandleFunc("/update_user_info", func(writer http.ResponseWriter, request *http.Request) {
		if request.Method == "POST" {
			err := request.ParseForm()
			if err != nil{
				log.Fatal("ParseForm error")
				return
			}
			username := request.Form.Get("username")
			password := request.Form.Get("password")
			response := fmt.Sprintf("username : %s, password : %s \n", username, password)
			fmt.Fprintf(writer, response)
		}
	})

	type UserInfo struct {
	Name 	string 	`json:"name"`
	Age  	int    	`json:"age"`
	Salary 	int  	`json:"salary"`
}

	// POST 请求解析JSON
	http.HandleFunc("/statistics", func(writer http.ResponseWriter, request *http.Request) {

		// 在这里读取数据
		if request.Method == "POST" {
			body, err := ioutil.ReadAll(request.Body)
			u := new(UserInfo)
			// JSON的序列化
			err = json.Unmarshal([]byte(body), u)
			if err != nil{
				return
			}
			println(u.Name, u.Age, u.Salary)

			u.Name = "justin bieber"
			u.Age = 18
			// JSON的反序列化
			if jsonStr , err:= json.Marshal(u); err == nil{
				fmt.Println(jsonStr)
				fmt.Fprintf(writer, string(jsonStr))
			}
		}
	})
```



## 14.4 构建RESTful服务

1. 案例一

   ```go
   // 普通HTTP服务
   package main
   
   import (
   	"fmt"
   	"github.com/julienschmidt/httprouter"
   	"log"
   	"net/http"
   )
   
   func Index(w http.ResponseWriter, r *http.Request,_ httprouter.Params)  {
   	fmt.Fprint(w, "Welcome!\n")
   }
   
   func Hello(w http.ResponseWriter, r *http.Request,ps httprouter.Params)  {
   	fmt.Fprintf(w, "hello, %s!\n", ps.ByName("name"))
   }
   
   func main()  {
   	router := httprouter.New()
   	router.GET("/", Index)
   	router.GET("/hello/:name", Hello)
   	log.Fatal(http.ListenAndServe(":8080", router))
   }
   
   ```

2. 案例二

   ```go
   // RESTful 服务
   package main
   
   import (
   	"encoding/json"
   	"fmt"
   	"github.com/julienschmidt/httprouter"
   	"log"
   	"net/http"
   )
   
   type Employee struct {
   	ID 		string 	`json:"id"`
   	Name 	string 	`json:"name"`
   	Age 	int 	`json:"age"`
   }
   
   var employeeDB map[string]*Employee
   
   func init()  {
   	employeeDB = map[string]*Employee{}
   	employeeDB["Mike"] = &Employee{"e-1", "Mike", 35}
   	employeeDB["Rose"] = &Employee{"e-2", "Rose", 45}
   }
   func Index(w http.ResponseWriter, r *http.Request,_ httprouter.Params)  {
   	fmt.Fprint(w, "Welcome!\n")
   }
   
   func Hello(w http.ResponseWriter, r *http.Request,ps httprouter.Params)  {
   	qName := ps.ByName("name")
   	var ok bool
   	var info *Employee
   	var infoJson []byte
   	var err error
   
   	if info, ok = employeeDB[qName]; !ok{
   		w.Write([]byte("\"error\":\"Not Found\""))
   		return
   	}
   
   	if infoJson, err = json.Marshal(info); err != nil{
   		w.Write([]byte(fmt.Sprintf("{\"error\":\"%s\"}", err)))
   		return
   	}
   	w.Write(infoJson)
   }
   
   func main()  {
   	router := httprouter.New()
   	router.GET("/", Index)
   	router.GET("/hello/:name", Hello)
   	log.Fatal(http.ListenAndServe(":8080", router))
   }
   
   ```

   

# 第十五章 性能调优



## 15.1 性能分析工具



### 一、准备工作

***

+ 安装graphviz
+ 将$GOPATH/bin 加入$PATH
+ 安装go-torch





### 二、支持多种profile

***

+ go help testflag
+ url



### 三、案例

***

1. 代码

   ```go
   package main
   
   import (
   	"log"
   	"math/rand"
   	"os"
   	"runtime/pprof"
   	"time"
   )
   
   const (
   	col = 10000
   	row = 10000
   )
   
   func fillMatrix(m *[row][col]int) {
   	s := rand.New(rand.NewSource(time.Now().UnixNano()))
   
   	for i := 0; i < row; i++ {
   		for j := 0; j < col; j++ {
   			m[i][j] = s.Intn(100000)
   		}
   	}
   }
   
   func calculate(m *[row][col]int) {
   	for i := 0; i < row; i++ {
   		tmp := 0
   		for j := 0; j < col; j++ {
   			tmp += m[i][j]
   		}
   	}
   }
   
   func main()  {
   
   	// CPU profile
   	f, err := os.Create("cpu.prof")
   	if err != nil{
   		log.Fatal("could not create CPU profile:", err)
   	}
   
   	if err := pprof.StartCPUProfile(f); err != nil{
   		log.Fatal("could not start CPU profile:", err)
   	}
   
   	defer pprof.StopCPUProfile()
   
   	x := [row][col]int{}
   	fillMatrix(&x)
   	calculate(&x)
       
   	f1, err := os.Create("mem.prof")
   	if err != nil{
   		log.Fatal("Could not create memory profile:", err)
   	}
   	if err := pprof.WriteHeapProfile(f1); err != nil{
   		log.Fatal("could not write memory profile :", err)
   	}
   
   	f1.Close()
   
   	f2, err := os.Create("goroutine.prof")
   	if err != nil{
   		log.Fatal("could not create goroutine prof:", err)
   	}
   
   	if gProf := pprof.Lookup("goroutine"); gProf == nil{
   		log.Fatal("could not write goroutine profile:")
   	}else{
   		gProf.WriteTo(f2,0)
   	}
   	f2.Close()
   }
   ```

2. 性能分析命令

   1. 查看cpu情况

      ```shell
      # STEP-1 载入prof文件
      
      go tool pprof ${app} ${prof}
      go tool pprof performance.exe cpu.prof
      
      # STEP-2 查看统计信息
      top
      
      # STEP-3 查看指定函数详情
      list fillMatrix
      
      # STEP-4  退出
      exit
      ```

   2. 查看内存

      ```shell
      # STEP-1 载入prof文件
      
      go tool pprof performance.exe mem.prof
      
      # STEP-2 查看统计信息
      top
      
      # STEP-3 查看指定函数详情
      list main
      
      # STEP-4  退出
      exit
      ```

   3. 查看协程

   4. 通过http输出profile

      1. 打开网页查看

         ```shell
         http://${host}:${port}/debug/pprof/
         ```

      2. 通过命令行查看

         ```shell
         # STEP-1
         go tool pprof http://127.0.0.1:8081/debug/pprof/profile
         
         # STEP-2 
         top
         
         # STEP-3 按累计时间排序
         top -cum 
         
         # STEP-4 查看某个函数详情
          list GetFibonacciSerie
          
         # STEP-5 退出
         exit
         ```

         

      

      

   

## 15.2 性能调优示例



## 15.3 别让性能锁住





## 15.4 GC友好代码





# 第十六章 高可用性服务设计



## 16.1 高效字符串连接





## 16.2 面向错误的设计





## 16.3 面向恢复的设计



## 16.4 Chaos Engineering





# 第十七章 计时器



## 17.1 定时执行

1. 示例一

   ```go
   	ticker := time.NewTicker(time.Second * 3)
   	for i := range ticker.C{
   		fmt.Println(i)
   	}
   ```

   

2. 示例二

   ```go
   	t := time.NewTimer(time.Second * 3)
   	for{
   		v := <- t.C
   		fmt.Println("timer running...",v)
   		t.Reset(time.Second * 3)
   	}
   ```



## 17.2 延迟执行

示例

```go
	fmt.Println("programme begin...", time.Now())
	t := time.After(time.Second * 5)
	fmt.Println("t = ", <-t)
```





## 17.3 睡眠

示例

```go
	fmt.Println("t1 : ", time.Now())
	time.Sleep(time.Second * 5)
	fmt.Println("t2 : ", time.Now())
```





# 第十八章 网络编程



## 18.1 UDP编程



### 18.1.1 客户端

***

```go
package main

import (
	"fmt"
	"net"
	"os"
	"strconv"
)

const (
	SERVER_IP       = "127.0.0.1"
	SERVER_PORT     = 10006
	SERVER_RECV_LEN = 10
)
func checkError(err error) {
	if err != nil {
		fmt.Println(err)
		os.Exit(1)
	}
}
func main() {
	serverAddr := SERVER_IP + ":" + strconv.Itoa(SERVER_PORT)
	conn, err := net.Dial("udp", serverAddr) // 连接
	checkError(err)

	defer conn.Close()
	for{
		fmt.Printf("请输入数据:")
		var input string
		fmt.Scanln(&input)
		if _, err = conn.Write([]byte(input)); err != nil{ // 发送数据
			panic(err)
		}
		fmt.Println("Write:", input)

		msg := make([]byte, SERVER_RECV_LEN)
		if _, err = conn.Read(msg); err != nil{   // 接收数据
			panic(err)
		}
		fmt.Println("Response:", string(msg))
	}

}
```





### 18.1.2 服务器

***

```go
package main

import (
	"fmt"
	"net"
	"strconv"
	"strings"
)

const (
	SERVER_IP       = "127.0.0.1"
	SERVER_PORT     = 10006
	SERVER_RECV_LEN = 10
)

func main() {
	address := SERVER_IP + ":" + strconv.Itoa(SERVER_PORT)
	var(
		addr *net.UDPAddr
		err error
		conn *net.UDPConn
		rAddr *net.UDPAddr
	)
	// STEP-1 创建地址
	if addr, err = net.ResolveUDPAddr("udp", address); err != nil{
		panic(err)
	}

	// STEP-2 监听端口
	if conn, err = net.ListenUDP("udp", addr); err != nil{
		panic(err)
	}

	defer conn.Close()
	for {
		// Here must use make and give the lenth of buffer
		data := make([]byte, SERVER_RECV_LEN)
		// STEP-3 接收数据
		if _, rAddr, err = conn.ReadFromUDP(data); err != nil{
			panic(err)
		}
		strData := string(data)
		fmt.Println("Received:", strData)
		upper := strings.ToUpper(strData)
		// STEP-4 发送数据
		if _, err = conn.WriteToUDP([]byte(upper), rAddr); err != nil{
			panic(err)
		}
		fmt.Println("Send:", upper)
	}
}

```





## 18.2 TCP编程







# 第十九章 语言特性



## 19.1 类型断言

```go
func assertType(param interface{}){
	str , ok:= param.(string) // 类型断言
	if ok == false{
		fmt.Println("param is not string")
		return
	}
	fmt.Println("param : ", str)
}

func TestTypeAssert(t *testing.T) {
	assertType(1)
	assertType([]int{1,2,6})
	assertType("justin")
}
```

