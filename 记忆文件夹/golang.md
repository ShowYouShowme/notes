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
   go env -w GOPROXY="https://goproxy.io,direct"
   ```

2. 开启

   ```shell
   go env -w GO111MODULE=on
   ```

3. 





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



## 9.3 CSP并发机制



## 9.4 多路选中和超时



## 9.5 channel的关闭和广播



## 9.6 任务的取消



## 9.7 Context与任务取消



# 第十章 典型并发任务



## 10.1 只运行一次



## 10.2 仅需任意任务完成



## 10.3 所有任务完成



## 10.4 对象池



## 10.5 sync.pool对象缓存





# 第十一章 测试



# 第十二章 反射和Unsafe



# 第十三章 常见架构模式的实现



# 第十四章 常见任务



# 第十五章 性能调优



# 第十六章 高可用性服务设计

