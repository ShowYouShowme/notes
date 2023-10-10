# 第一章 简介



## 1.0 安装

1. 下载安装包安装

   ```shell
   wget https://go.dev/dl/go1.19.linux-amd64.tar.gz
   tar -zxvf go1.19.linux-amd64.tar.gz
   mv go $HOME/local
   ```

   

2. 设置环境变量

   ```shell
   mkdir doc local app tmp
   ```

   ```shell
   export GOROOT=$HOME/local/go              		#go安装目录。
   export GOPATH=$HOME/doc/go     				    #保持第三方依赖包,goland里面需要配置
   export GOBIN=$GOPATH/bin           				#可执行文件存放
   export PATH=$GOPATH:$GOBIN:$GOROOT/bin:$PATH    #添加PATH路径ls
   
   
   # windows 安装,使用goland或者vscode开发,需要配置环境变量GOROOT和GOPATH
   ```

3. 开启go mod并配置代理

   ```shell
   go env -w GO111MODULE=on
   go env -w GOPROXY="https://goproxy.io,direct"
   ```

4. 创建项目

   ```ini
   mkdir socks5-server
   cd socks5-server/
   go mod init s5-server
   ; 编写代码
   vim main.go
   
   ; 安装依赖
   go mod tidy
   
   ;构建项目, 使用当前目录构建
   ; 或者  go build .
   go build
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
   
3. 静态编译

   ```shell
   CGO_ENABLED=0 go build -a -ldflags '-extldflags "-static"' .
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


//一次赋值给多个,左边的a,b,c至少有一个是新变量
a,b,c := 1,2,3
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



// 利用break跳出循环
val := 100
for {
    fmt.Printf("val = %v \n", val)
    if val > 105 {
        break
    }
    val += 1
}
fmt.Printf("...")
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
   
   
   	// 如果是C语言, 128、126、125 都执行一个语句
       // Go语言, 128和126 则什么也不做
   	var age int32
   	age = 128
   	switch age {
   	case 128:
   	case 126:
   	case 125:
   		fmt.Println("name = ", age)
   	case 127:
   		fmt.Println("age = 127")
   	}
   	fmt.Println("finished...")
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
   
   func main() {
   	array := []int64{11, 22, 33, 44, 55}
   	for index, value := range array {
   		fmt.Printf("index = %v, value = %v \n", index, value)
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
       
       t.Log(arr3[1:3])
   }
   ```



### 3.1.2 切片

***

1. 切片其实就是C++的Vector

2. 示例代码

   ```GO
   // 切片定义时 中括号里为空 数组定义时中括号有... 或者数字
   func TestSliceInit(t *testing.T)  {
   	var s0 []int // 定义方式一
   	t.Log(len(s0), cap(s0)) // 和C++的vector类似
   
   	s0 = append(s0,1)
   	t.Log(len(s0), cap(s0))
   
   	s1 := []int{1,2,3,4} // 定义方式二
   	t.Log(len(s1), cap(s1))
   
   	s2 := make([]int, 3, 5) // size == 3 capacity == 5 定义方式三 
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

3. 切片截取

   ```go
   a := []int64{11, 22, 33, 44, 55}
   b := a[1:2] // [22]     前闭后开的区间  [start, end)
   c := a[3:]  // [44,55]
   d := a[:2]  // [11,22]
   ```

4. 末尾插入元素

   ```go
   // 指定多个元素
   a1 := []int64{1, 2, 3, 4}
   a1 = append(a1, 11, 22, 33)
   
   // 解构slice
   a1 := []int64{1, 2, 3, 4}
   a2 := []int64{5, 6, 7}
   a1 = append(a1, a2...)
   ```

5. copy 数组

   + 方式一

     ```go
     arr := []int64{0x11, 0x21, 0x31}
     
     arr2 := make([]int64, 0)
     arr2 = append(arr2, arr...)
     ```

   + 方式二

     ```go
     arr := []int64{0x11, 0x21, 0x31}
     
     arr2 := make([]int64, len(arr))
     copy(arr2, arr)
     ```

6. 切片作为参数传入函数，并且插入元素

   ```go
   func arrayPushBack(param *[]int64, val int64) {
   	*param = append(*param, val)
   }
   
   func main() {
       a1 := []int64{1, 2, 3}
       arrayPushBack(&a1, 12)
       fmt.Printf("%v \n", a1)
   }
   ```

   

7. 切片作为参数传入函数，并且删除元素

   ```go
   func erase(array *[]int64, position int) {
   	*array = append((*array)[:position], (*array)[position+1:]...)
   	fmt.Printf("........")
   }
   
   	arr := []int64{0x11, 0x21, 0x31}
   	erase(&arr, 1)
   ```

8. 切片作为参数传入函数，并且修改元素

   ```go
   func changeElem(arr []int64) {
   	arr[1] = 990
   }
   
   arr := []int64{1, 2, 3, 4}
   changeElem(arr)
   ```

9. Map 对应几个操作的笔记

   + 插入元素

     ```go
     func InsertElem(arr map[int64]int64) {
     	arr[5] = 55
     	fmt.Printf("........")
     }
     
     	arr := map[int64]int64{1: 11, 2: 22, 3: 33, 4: 44}
     	InsertElem(arr)
     ```

     

   + 删除元素

     ```go
     func DeleteElem(arr map[int64]int64) {
     	delete(arr, 2)
     	fmt.Printf("........")
     }
     
     	arr := map[int64]int64{1: 11, 2: 22, 3: 33, 4: 44}
     	DeleteElem(arr)
     ```

     

   + 修改元素

     ```go
     func changeElem(arr map[int64]int64) {
     	arr[1] = 990
     	fmt.Printf("........")
     }
     	arr := map[int64]int64{1: 11, 2: 22, 3: 33, 4: 44}
     	changeElem(arr)
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

4. 遍历：遍历的时候并不是有序的，每次遍历的次序都可能不同，因为会有一个随机位置

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
2. <b style="color:red">全部参数都是值传递</b>
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

2. 执行次序：一个函数里存在多个defer时，后面的defer先执行

3. 案例

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



### 6.1.1  数据封装

***

```go
// 大写开头的成员,包外可见; 小写开头的成员,包内可见
type Employee struct{
	Id string
	Name string
	Age int
}

func main()  {
	e := Employee{"0", "Bob", 20}
	e1 := Employee{Name: "Mike", Age: 30}
	e2 := new(Employee) // 等价于 e2 := &Employee{}
	e2.Id = "2"
	e2.Name = "Rose"

	fmt.Println(e)
	fmt.Println(e1)
	fmt.Println(e1.Id)
	fmt.Println(e2)
	fmt.Printf("e is %T \n", e) // 输出类型
	fmt.Printf("e2 is %T \n", e2)
}
```







### 6.1.2 行为定义

***

1. 方式一

   ```go
   // 会有对象copy,不建议使用
   func (e Employee)String() string {
   	return fmt.Sprintf("ID:%s-Name:%s-Age:%d", e.Id, e.Name, e.Age)
   }
   ```

   

2. 方式二

   ```go
   // 不存在对象COPY
   func (e *Employee)String() string {
   	fmt.Printf("Address is %x \n", unsafe.Pointer(&e.Name))
   	return fmt.Sprintf("...ID:%s-Name:%s-Age:%d", e.Id, e.Name, e.Age)
   }
   ```

   

## 6.2 go语言的相关接口



### 接口实现

***

1. 接口为非入侵性，<b style="color:red">实现不依赖于接口定义</b>

2. 接口定义可以包含在接口使用者包内

3. 示例代码

   ```go
   type Programmer interface {
   	WriteHelloWorld() string
   }
   
   type GoProgrammer struct{
   
   }
   
   func (self *GoProgrammer) WriteHelloWorld() string {
   	return "fmt.Println(\"Hello World!\")"
   }
   
   func TestClient(t *testing.T) {
   	var p Programmer = new(GoProgrammer)
   	t.Log(p.WriteHelloWorld())
   }
   ```



### 自定义类型

***

```go
type IntConv func(op int) int

func timeSpent(inner IntConv)IntConv  {
	return func(op int) int {
		start := time.Now()
		ret := inner(op)
		fmt.Println("time spent:", time.Since(start).Seconds())
		return ret
	}
}

func f1(param int)int{
	for i := 0; i < param; i++{
		time.Sleep(time.Second)
		fmt.Println(".")
	}
	return param
}

func TestFunWrap(t *testing.T) {
	timeSpent(f1)(3)
}
```



## 6.3 扩展和复用

1. 组合

   ```go
   type Pet struct{
   
   }
   
   func (this *Pet)Speak()  {
   	fmt.Println("...")
   }
   
   func (this *Pet)SpeakTo(host string)  {
   	this.Speak()
   	fmt.Println(" ", host)
   }
   
   // 组合
   type Dog struct {
   	p *Pet
   }
   
   func (this *Dog)Speak()  {
   	this.p.Speak()
   }
   
   func (this *Dog)SpeakTo(host string)  {
   	this.p.SpeakTo(host)
   }
   
   func TestDog(t *testing.T) {
   	dog := new(Dog)
   	dog.SpeakTo("Chao")
   }
   ```

2. 不支持override

3. 匿名嵌套

   ```go
   type Pet struct{
   
   }
   
   func (this *Pet)Speak()  {
   	fmt.Println("...")
   }
   
   func (this *Pet)SpeakTo(host string)  {
   	this.Speak()
   	fmt.Println(" ", host)
   }
   
   // 1-- 匿名嵌套
   // 2-- 组合
   type Dog struct {
   	Pet
   }
   
   // 尝试override Pet 的函数,失败
   func (this *Dog)Speak()  {
   	fmt.Println("Wang!")
   }
   
   func TestDog(t *testing.T) {
   	dog := new(Dog)
   	dog.SpeakTo("Chao")
   }
   ```

   

4. 不支持里氏替换

   ```go
   // Dog 和 Pet 都是struct,不能进行类型转换
   // 下面的代码是错误的
   var dog Pet := new(Dog)
   ```

   



## 6.4 多态



### 多态

***

```go
type Code string

type Programmer interface {
	WriteHelloWorld() Code
}

type GoProgrammer struct {
}

func (this *GoProgrammer) WriteHelloWorld() Code {
	return "fmt.Println(\"Hello World!\")"
}

type JavaProgrammer struct {

}

func (this *JavaProgrammer) WriteHelloWorld() Code {
	return "System.out.Println(\"Hello World!\")"
}

func writeFirstProgram(p Programmer)  {
	// %v 使用默认类型输出 , 不同的数据类型不一样
	fmt.Printf("%T %v\n", p, p.WriteHelloWorld())
}

func TestPolymorphism(t *testing.T)  {
	goProg := new(GoProgrammer)
	javaProg := new(JavaProgrammer)
	writeFirstProgram(goProg)
	writeFirstProgram(javaProg)
}
```





### 空接口与类型断言

***

1. 空接口可以表示任何类型

2. 通过断言将空接口转换为制定类型

3. 示例代码

   ```go
   func DoSomething(p interface{})  {
   	if i, ok := p.(int); ok{
   		fmt.Println("Integer", i)
   		return
   	}
   
   	if s, ok :=p.(string);ok{
   		fmt.Println("string", s)
   		return
   	}
   
   	fmt.Println("unknown Type")
   }
   
   func TestEmptyInterfaceAssertion(t *testing.T) {
   	DoSomething(10)
   	DoSomething("123")
   	DoSomething(false)
   }
   ```

   示例二

   ```go
   func DoSomething(p interface{})  {
   	switch v:=p.(type) {
   	case int:
   		fmt.Println("Integer",v)
   	case string:
   		fmt.Println("string",v)
   	default:
   		fmt.Println("unknown type")
   	}
   }
   
   func TestEmptyInterfaceAssertion(t *testing.T) {
   	DoSomething(10)
   	DoSomething("123")
   	DoSomething(false)
   }
   ```

   

### 接口实践

***

1. 倾向于使用小的接口定义，很多接口只包含一个方法

   ```go
   type Reader interface{
       Read(p []byte)(n int, err error)
   }
   
   type Writer interface{
       Write(p []byte)(n int, err error)
   }
   ```

   

2. 较大的接口，由多个小接口组合而成

   ```go
   type ReadWriter interface{
       Reader
       Writer
   }
   ```

   

3. 只依赖于必要功能的最小接口

   ```go
   func StoreData(reader Reader)error{
       //...
   }
   ```

   





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

3. 全局panic

   ```go
   package main
   
   import "fmt"
   
   func getName() {
   	panic("error from getName")
   }
   
   func testWrong(input int32) {
   	if input == 5 {
   		panic("wrong info from testWrong")
   	} else {
   		getName()
   	}
   }
   
   func main() {
   	defer func() {
   		if err := recover(); err != nil {
   			fmt.Println("recovered from ", err)
   		}
   	}()
   
   	testWrong(6)
   }
   
   ```




## 7.3 错误处理通用流程

```go
package main

import "log"

// panic 类似Java异常,可以让调用方自己来处理
// 错误处理的第一种方式,直接panic,让调用方自己处理
func add(a int32, b int32) int32 {
	if a < 0 || b < 0 {
		panic("invalid param")
	}
	return a + b
}

// 错误处理的第二种方式,增加一个变量表示error
// 建议用第一种方式,代码更加简洁
func sub(a int32, b int32) (result int32, reason any) {
	defer func() {
		if err := recover(); err != nil {
			log.Printf("error : %v", err)
			result = -1
			reason = err
		}
	}()
	if a < b {
		panic("a must greater than b")
	}
	return a - b, nil
}

func main() {
	defer func() {
		if err := recover(); err != nil {
			log.Printf("err : %v", err)
		}
	}()
	var a int32 = 50
	var b int32 = 10
	//var c int32 = add(a, b)
	c, err := sub(a, b)
	if err != nil {
		panic(err)
	}
	log.Printf("a = %v, b = %v, c = %v", a, b, c)
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

   ```shell
   go get github.com/armon/go-socks5
   ```

   

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


### 8.1.4 使用

***

1. 使用gopath创建项目时，所有代码放在目录$GOPATH/src下
2. 用goland创建项目时，项目类型选择go



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
   #记得用go env 查看其值
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

6. 删除下载的模块缓存

   ```shell
   go clean --modcache
   ```

7. 使用goland创建项目时，项目类型选择Go modules

### 8.2.5 使用项目内的包

***

1. 开启GO111MODULE

   ```shell
   go env -w GO111MODULE=on
   
   #查看是否开启
   go env
   
   ##以下是结果
   GO111MODULE="on"#注意这里为on
   GOARCH="amd64"
   GOBIN="/home/nash/go/bin"
   GOCACHE="/home/nash/.cache/go-build"
   GOENV="/home/nash/.config/go/env"
   GOEXE=""
   GOFLAGS=""
   GOHOSTARCH="amd64"
   GOHOSTOS="linux"
   GOINSECURE=""
   GOMODCACHE="/home/nash/go/pkg/mod"
   GONOPROXY=""
   GONOSUMDB=""
   #未开启go mod
   GO111MODULE="" # 注意这里为空
   GOARCH="amd64"
   GOBIN="/home/nash/go/bin"
   GOCACHE="/home/nash/.cache/go-build"
   GOENV="/home/nash/.config/go/env"
   GOEXE=""
   GOFLAGS=""
   GOHOSTARCH="amd64"
   GOHOSTOS="linux"
   GOINSECURE=""
   
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
   ## 必须有文件package 为main,并且存在main函数
   
   # STEP-1 进入源码目录
   cd ../src
   
   # STEP-2 编译
   go build
   或者
   go build .
   
   # 不要这样编译,如果有多个文件都是package main,会报错
   go build main.go 
   ```



## 8.3 GOPATH与go mod对比

***

1. 使用GOPATH 时，所有代码必须放在$GOPATH/src目录下
2. 使用go mod则无此要求，记得使用go env 查看GO111MODULE是否为on




## 8.4 安装第三方生态应用

go install

```shell
# 安装 protoc
go install google.golang.org/protobuf/cmd/protoc-gen-go@latest
```



## 8.5 vscode搭建开发环境

1. 安装golang插件

   ```shell
   Go Team at Google go.dev
   ```

2. 安装go的工具

   + dlv：调试用的插件

     ```shell
     go install github.com/go-delve/delve/cmd/dlv@latest
     ```

   + gopls：代码提示插件

     ```shell
     go install golang.org/x/tools/gopls@latest
     ```

   + protoc-gen-go：生成protobuf的工具

     ```shell
     go install google.golang.org/protobuf/cmd/protoc-gen-go@latest
     ```

     

3. 创建项目

   ```shell
   mkdir helloWorld
   cd helloWorld
   go mod init helloWorld
   
   
   # 安装模块,类似npm install
   go mod tidy
   
   
   # 编译
   go build
   
   # 调式
   按下F5,需要配置launch.json
   ```

4. 配置调试：launch.json

   ```json
   {
       // Use IntelliSense to learn about possible attributes.
       // Hover to view descriptions of existing attributes.
       // For more information, visit: https://go.microsoft.com/fwlink/?linkid=830387
       "version": "0.2.0",
       "configurations": [
           {
               "name": "Launch Package",
               "type": "go",
               "request": "launch",
               "mode": "auto",
               "program": "${fileDirname}"
           }
       ]
   }
   ```

   

   配置文件参数介绍

   | 属性    | 说明                                                         |
   | ------- | ------------------------------------------------------------ |
   | name    | 定义配置名字                                                 |
   | type    | 指定语言，这里填写go即可                                     |
   | request | 对于已经运行的程序用attach，其它情况用launch                 |
   | mode    | 对于 `launch` 有 `auto`, `debug`, `remote`, `test`, `exec`, 对于 `attach`只有`local`,`remote` |
   | program | 指定包, 文件或者是二进制的绝对路径                           |
   | env     | 调试程序时需要注入的环境变量, 例如:`{ "ENVNAME": "ENVVALUE" }` |
   | envFile | 绝对路径,`env`的值会覆盖`envFile`的值                        |
   | args    | 需要传给调试程序的命令行参数                                 |
   | showLog | 布尔值，是否在调试控制台打印日志, 一般为`true`               |
   |         |                                                              |

   调试时使用vsCode内置变量

   + `${workspaceFolder}` 在工作区的的根目录调试程序
   + `${file}` 调试当前文件
   + `${fileDirname}` 调试当前文件所属的程序包





## 8.6 多文件编程

### 8.6.1 同一目录下多文件编程

1. 同一目录下的所有的Go文件必须是同一个package
2. 同一个目录下调用其他文件的函数不需要加package名称



### 8.6.2 不同目录下多文件编程

1. 不同目录指的是不同的go源文件位于不同的路径下

2. 目录结构

   ```shell
   src
   |
   |
   |--------test
   |          |
   |          |
   |          |----test.go
   |
   |---main.go
   ```

3. 项目模块名：journey

4. 文件代码

   main.go

   ```go
   // main.go
   package main
   
   import "journey/Test"
   
   func main() {
   	Test.Myprint()
   }
   ```

   test.go

   ```go
   // test.go
   package Test
   
   import "fmt"
   
   func Myprint() {
   	fmt.Println("hello")
   }
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

select 语法

1. 如果多个case都可以运行，随机选中一个执行
2. 如果没有case可以执行
   + 存在default，执行default
   + 不存在default，阻塞
3. for select配合时，break并不能跳出循环，需要使用标签

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

```go
package main

import (
	"encoding/json"
	"log"
)

type BasicInfo struct {
	Name string `json:"name"`
	Age  int    `json:"age"`
}

type JobInfo struct {
	Skills []string `json:skills`
}

type Employee struct {
	BasicInfo BasicInfo `json:"basic_info"`
	JobInfo   JobInfo   `json:"job_info"`
}

func main() {
	//反序列化
	var jsonStr = "{\"basic_info\":{\"name\":\"Mike\",\"age\":30},\"job_info\":{\"skills\":[\"Java\",\"Go\",\"C++\"]}}"
	e := new(Employee)
	err := json.Unmarshal([]byte(jsonStr), e)
	if err != nil {
		log.Fatal(err)
	}
	log.Println(e)
	log.Println("....")

	//序列化
	var e1 = BasicInfo{
		Name: "powell",
		Age:  29,
	}
	if v, err := json.Marshal(e1); err != nil {
		log.Fatal(v)
	} else {
		log.Println(string(v))
	}
	log.Println("....")
}

```



## 14.2 easyjson

1. 安装

   ```shell
   # WIN 上可通过everything 查找 easyjson的路径
   go get -u github.com/mailru/easyjson/...
   ```

2. 生成代码文件

   ```shell
   # 类似Protobuf
   
   # 项目路径
   tests/（在gopath目录下）
   └── src
       ├── json_test.go
       └── models
           ├── models_easyjson.go	（easyjson命令生成的文件)
           └── models.go	（模型文件）
   ```

   ```go
   // models.go
   package models
   
   type Request struct {
   	TransactionID string `json:"transaction_id"`
   	PayLoad       []int  `json:"payload"`
   }
   
   type Response struct {
   	TransactionID string `json:"transaction_id"`
   	Expression    string `json:"exp"`
   }
   ```

   执行命令

   ```shell
   easyjson -all models.go
   ```

   

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

      3. 代码

         ```go
         package main
         // import 里增加 _ "net/http/pprof" 即可
            import (
            	"fmt"
            	"net/http"
            	_ "net/http/pprof"
            )
         
            func GetFibonacciSerie(n int) []int {
            	ret := make([]int, 2, n)
            	ret[0] = 1
            	ret[1] = 1
            	for i := 2; i < n; i++ {
            		ret = append(ret, ret[i-2]+ret[i-1])
            	}
            	return ret
            }
         
            func createFBS(w http.ResponseWriter, r *http.Request) {
            	var fbs []int
            	for i := 0; i < 1000000; i++ {
            		fbs = GetFibonacciSerie(50)
            	}
            	w.Write([]byte(fmt.Sprintf("%v", fbs)))
         
            }
         
            func main() {
            	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
            		w.Write([]byte("Welcome!"))
            	})
            	http.HandleFunc("/Fibonacci", createFBS)
             http.ListenAndServe(":8080", nil)
            }
         ```

## 15.2 性能调优示例



### 通过bench产生profile

***

1. cpu profile

   ```shell
   # 产生cpu profile
   go test -bench=. -cpuprofile=cpu.prof
   
   go tool pprof cpu.prof
   ```

2. mem profile

   ```shell
   go test -bench=. -memprofile=mem.prof
   
   go tool pprof mem.prof
   ```

3. 调优代码

   + 代码目录

     ```shell
     ---models
     |    |
     |    |------structs.go
     |
     |-----optimization_test.go
     |
     |-----optmization.go
     ```

   + structs.go

     ```go
     package models
     
     type Request struct {
     	TransactionID string `json:"transaction_id"`
     	PayLoad       []int  `json:"payload"`
     }
     
     type Response struct {
     	TransactionID string `json:"transaction_id"`
     	Expression    string `json:"exp"`
     }
     
     ```

   + optimization_test.go

     ```go
     package profiling
     
     import "testing"
     
     func TestCreateRequest(t *testing.T) {
     	str := createRequest()
     	t.Log(str)
     }
     
     func TestProcessRequest(t *testing.T) {
     	reqs := []string{}
     	reqs = append(reqs, createRequest())
     	reps := processRequest(reqs)
     	t.Log(reps[0])
     }
     
     func BenchmarkProcessRequest(b *testing.B) {
     
     	reqs := []string{}
     	reqs = append(reqs, createRequest())
     	b.ResetTimer()
     	for i := 0; i < b.N; i++ {
     		_ = processRequest(reqs)
     	}
     	b.StopTimer()
     
     }
     ```

   + optmization.go

     ```go
     package profiling
     
     import (
     	"demo_01/src/models"
     	"encoding/json"
     	"strconv"
     )
     
     func createRequest() string {
     	payload := make([]int, 100, 100)
     	for i := 0; i < 100; i++ {
     		payload[i] = i
     	}
     	req := models.Request{"demo_transaction", payload}
     	v, err := json.Marshal(&req)
     	if err != nil {
     		panic(err)
     	}
     	return string(v)
     }
     
     func processRequest(reqs []string) []string {
     	reps := []string{}
     	for _, req := range reqs {
     		reqObj := &models.Request{}
     		json.Unmarshal([]byte(req), reqObj)
     		ret := ""
     		for _, e := range reqObj.PayLoad {
     			ret += strconv.Itoa(e) + ","
     		}
     		repObj := &models.Response{reqObj.TransactionID, ret}
     		repJson, err := json.Marshal(&repObj)
     		if err != nil {
     			panic(err)
     		}
     		reps = append(reps, string(repJson))
     	}
     	return reps
     }
     
     ```

     





## 15.3 别让性能锁住



#### 读锁对性能影响

***

```go
package main

import (
	"fmt"
	"sync"
	"testing"
)

var cache map[string]string

const NUM_OF_READER int = 40
const READ_TIMES = 100000

func init()  {
	cache = make(map[string]string) // map构造方法

	cache["a"] = "aa"
	cache["b"] = "bb"
}

func lockFreeAccess()  {
	var wg sync.WaitGroup
	wg.Add(NUM_OF_READER)
	for i := 0; i < NUM_OF_READER; i++ {
		go func() {
			for j := 0; j < READ_TIMES; j++{
				_, err := cache["a"]
				if !err{
					fmt.Println("Nothing")
				}
			}
			wg.Done()
		}()
	}
	wg.Wait()
}

func lockAccess()  {
	var wg sync.WaitGroup
	wg.Add(NUM_OF_READER)
	m := new(sync.RWMutex) // 读写锁
	for i := 0; i< NUM_OF_READER; i++{
		go func() {
			for j := 0; j < READ_TIMES; j++{
				m.RLock()
				_, err := cache["a"]
				if err == false{
					fmt.Println("Nothing")
				}
				m.RUnlock()
			}
			wg.Done()
		}()
	}
	wg.Wait()
}

func BenchmarkLockFree(b *testing.B) {
	b.ResetTimer() // TODO 为什么不用加stopTimer
	for i := 0; i < b.N; i++ {
		lockFreeAccess()
	}

}

func BenchmarkLock(b *testing.B) {
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		lockAccess()
	}
}
```

运行测试

```shell
go test -bench=.
```

分析影响性能的代码

```shell
go test -bench=. -cpuprofile=cpu.prof
go tool pprof cpu.prof
top -cum
list lockAccess
exit
```





#### 使用锁的注意点

***

1. 减少锁的影响范围
2. 减少发生锁冲突的概率
   + sync.Map
   + ConcurrentMap
3. 避免锁的使用



#### 线程安全的锁

***

```go
// 定义接口
type Map interface {
	Set(key interface{}, value interface{})
	Get(key interface{})(interface{}, bool)
	Del(key interface{})
}
```

```go
// RWLock 实现的Map
type RWLockMap struct {
	m map[interface{}]interface{}
	lock sync.RWMutex
}

func (this *RWLockMap)Get(key interface{})  (interface{}, bool){
	this.lock.RLock()
	v, ok := this.m["key"]
	this.lock.RUnlock()
	return v,ok
}

func (this *RWLockMap)Set(key interface{},value interface{})  {
	this.lock.Lock()
	this.m[key] = value
	this.lock.Unlock()
}

func (this *RWLockMap) Del(key interface{}) {
	this.lock.Lock()
	delete(this.m, key)
	this.lock.Unlock()
}

func CreateRWLockMap() *RWLockMap {
	m := make(map[interface{}]interface{}, 0)
	return &RWLockMap{m : m}
}
```

```go
// sync.map 实现的Map
// 比RWLock 实现的Map性能高很多
type SyncMap struct {
	m sync.Map
}

func (this *SyncMap)Get(key interface{})  (interface{}, bool){
	return this.m.Load(key)
}

func (this *SyncMap)Set(key interface{},value interface{})  {
	this.m.Store(key, value)
}

func (this *SyncMap) Del(key interface{}) {
	this.m.Delete(key)
}

func CreateSyncMap() *SyncMap {
	return &SyncMap{}
}
```

```go
// 测试代码
import (
	"strconv"
	"sync"
	"testing"
)

const (
	NumOfReader = 100
	NumOfWriter = 200
)
func benchmarkMap(b *testing.B, mp Map) {
	for i := 0; i < b.N; i++ {
		var wg sync.WaitGroup
		for i := 0; i < NumOfWriter; i++{
			wg.Add(1)
			go func() {
				for j := 0; j < 100; j++{
					mp.Set(strconv.Itoa(i), i * i)
					mp.Set(strconv.Itoa(i), i * i)
					mp.Del(strconv.Itoa(i))
				}
				wg.Done()
			}()
		}

		for i := 0; i < NumOfReader; i++{
			wg.Add(1)
			go func() {
				for j:=0; j < 100; j++{
					mp.Get(strconv.Itoa(i))
				}
				wg.Done()
			}()
		}
		wg.Wait()
	}
}

func BenchmarkName(b *testing.B) {

	b.Run("RWLock", func(b *testing.B) {
		hm := CreateRWLockMap()
		benchmarkMap(b, hm)
	})

	b.Run("sync.map", func(b *testing.B) {
		hm := CreateSyncMap()
		benchmarkMap(b, hm)
	})
}
```





## 15.4 GC友好代码



#### 避免内存分配和复制

***

1. 复杂对象传入引用
   + 数组的传递
   
     ```go
     // go test -bench=.
     import "testing"
     
     const NumOfElems = 1000
     
     type Content struct {
     	Detail [10000]int
     }
     
     func withValue(arr [NumOfElems]Content)int  {
     	return 0
     }
     
     func withRef(arr *[NumOfElems]Content)int  {
     	return 0
     }
     
     func BenchmarkWithValue(b *testing.B){
     	var arr [NumOfElems]Content
     
     	b.ResetTimer()
     	for i := 0; i < b.N; i++{
     		withValue(arr)
     	}
     	b.StopTimer()
     }
     
     func BenchmarkWithRef(b *testing.B){
     	var arr [NumOfElems]Content
     
     	b.ResetTimer()
     	for i := 0; i < b.N; i++{
     		withRef(&arr)
     	}
     	b.StopTimer()
     }
     ```
   
   + 结构体传递
   
2. 初始化至合适大小：比如数组

   ```go
   import "testing"
   
   const numOfElems = 100000
   const times = 1000
   
   func BenchmarkAutoGrow(t *testing.B)  {
   	for i := 0; i < times; i++{
   		var s []int
   		for j := 0; j < numOfElems; j++{
   			s = append(s,j)
   		}
   	}
   }
   
   func BenchmarkProperInit(t *testing.B)  {
   	for i := 0; i < times; i++{
   		s := make([]int,0,numOfElems)
   		for j := 0; j < numOfElems; j++{
   			s = append(s,j)
   		}
   	}
   }
   
   func BenchmarkOverSizeInit(t *testing.B)  {
   	for i := 0; i< times; i++{
   		s := make([]int, 0, numOfElems * 8)
   		for j := 0; j < numOfElems; j++{
   			s = append(s,j)
   		}
   	}
   }
   ```

   

3. 复用内存

4. 打印GC日志

   ```shell
   # win
   set GOGCTRACE=1
   set GODEBUG=gctrace=1
   go test -bench=BenchmarkWithRef
   ```

5. 使用trace查看GC

   ```shell
   # 产生文件
   go test -bench=BenchmarkWithRef -trace=trace_value.out
   
   # 利用web打开查看
   go tool trace trace_value.out
   ```

   



# 第十六章 高可用性服务设计



## 16.1 高效字符串连接



#### 字符串拼接方法

***

1. fmt.Sprintf
2. <b style="color:red">strings.Builder</b>
3. bytes.Buffer
4. 字符串相加



#### 示例代码

***

```go
import (
	"bytes"
	"fmt"
	"strconv"
	"strings"
	"testing"
)

const numbers = 100

func BenchmarkSprintf(b *testing.B) {
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		var s string
		for i := 0; i < numbers; i++{
			s = fmt.Sprintf("%v%v", s, i)
		}
	}
	b.StopTimer()
}

func BenchmarkStringBuilder(b *testing.B) {
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		var builder strings.Builder
		for i := 0; i < numbers; i++{
			builder.WriteString(strconv.Itoa(i))
		}
		_ = builder.String()
	}
	b.StopTimer()
}

func BenchmarkBytesBuf(b *testing.B) {
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		var buf bytes.Buffer
		for i := 0; i < numbers; i++{
			buf.WriteString(strconv.Itoa(i))
		}
		_ = buf.String()
	}
	b.StopTimer()
}

func BenchmarkStringAdd(b *testing.B) {
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		var s string
		for i := 0; i < numbers; i++{
			s += strconv.Itoa(i)
		}
	}
	b.StopTimer()
}
```





## 16.2 面向错误的设计

1. 隔离错误

   > + 微内核模式：某个plugin出错不影响其它plugin
   > + 微服务设计：某个服务挂掉，依赖于它的服务可以降级，仍然能工作（比如缓存一部分信息）
   > + 重用和隔离：日志服务可打印普通日志和关键数据日志；部署两套，一套只用来打印普通日志，一套用来打印关键数据

2. 冗余

   > + router服务可以部署多个，不仅可以用来做负载均衡，还可以在某个router失效时，其它route依然正常工作
   > + 单点失效：一台MySQL服务最大支持1000QPS，客户端QPS为1500，因此部署两台MySQL服务，但是一台失效后，全部Query会请求到一台机器，导致其挂掉-->对其流量限制或者部署更多机器

3. 流量限制：token bucket

4. 慢响应：在所有的阻塞操作上加上超时

5. 错误传递：断路器

   > 好友服务依赖数据库的数据，如果多次访问数据库超时，那以后访问好友服务时，会直接返回缓存里面的数据；过一段时间后，好友服务再次尝试访问数据库，看其是否恢复正常。



## 16.3 面向恢复的设计



#### 健康检查

***

1. 注意僵尸进程

   > + 池化资源耗尽
   >
   > + 死锁
   >
   > + 检查方式
   >
   >   ```shell
   >   # 1-- http的ping  --> 必须要检查到关键路径
   >                                                                 
   >   # 2-- 检查进程是否存在
   >   ```
   >
   >   

   

#### Let it crash

***

> 对待未知错误的最好方式



#### 构建可恢复的系统

***

+ 拒绝单体系统：一部分功能出错时，不能单独重启该功能

+ 面向错误和恢复的设计

  > 1. 依赖服务不可用时，可以继续存活
  > 2. 快速启动
  > 3. 无状态



#### 与客户端协商

***

> 服务器：我太忙了，请慢点发送数据。
>
> 客户端：好，我一分钟后再发送。









## 16.4 Chaos Engineering

> 原理：在整个系统中在随机位置引发故障，以快速了解他们正在构建的服务是否健壮，是否可以弹性扩容，是否可以处理计划外的故障。
>
> 做法：在生产环境中注入错误
>
> 1. 任意关掉主机
> 2. 模拟慢响应
>
> 重要性：了解即可。



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



### 18.2.1 客户端

***

```go
package main

import (
	"log"
	"net"
	"strconv"
)

const (
	SERVER_IP       = "127.0.0.1"
	SERVER_PORT     = 10006
	MTU = 1600
)

func main() {
	address := SERVER_IP + ":" + strconv.Itoa(SERVER_PORT)
	conn, err := net.Dial("tcp", address)
	if err != nil{
		panic(err)
	}

	for {
		msg := "what is up,dude"
		n, err := conn.Write([]byte(msg))
		if err != nil{
			panic(err)
		}
		log.Printf("send %d bytes", n)

		buffer := make([]byte, MTU)
		n, err = conn.Read(buffer)
		if err != nil{
			panic(err)
		}
		log.Printf("recv %d bytes, msg : %s", n, buffer)
	}
}
```



### 18.2.2 服务器

***

```go
package main

import (
	"log"
	"net"
	"strconv"
	"strings"
)

const (
	SERVER_IP       = "127.0.0.1"
	SERVER_PORT     = 10006
	MTU = 1600
)

func handler(conn net.Conn)  {
	var n int
	var err error
	buf := make([]byte, MTU)

	for{
		if n, err = conn.Read(buf); err != nil{
			// n = 0  且 err 为EOF 时对方关闭描述符
			panic(err)
		}

		data := buf[:n]
		log.Printf("recv : %s", data)

		upper := strings.ToUpper(string(data))
		if _, err = conn.Write([]byte(upper)); err != nil{
			panic(err)
		}
		log.Printf("send : %s", upper)

		// TODO 这里可以close
	}

}
func main()  {
	address := SERVER_IP + ":" + strconv.Itoa(SERVER_PORT)
	sock, err := net.Listen("tcp", address)
	if err != nil{
		panic(err)
	}

	for {
		conn, err := sock.Accept()
		if err != nil{
			panic(err)
		}
		go handler(conn)
	}
}
```







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





# 第二十章 文件



## 20.1 二进制文件



### 读取

***

1. ioutil

   ```go
   	content, err := ioutil.ReadFile("output.bin")
   	if err != nil{
   		log.Fatal(err)
   		return
   	}
   ```

2. file.Read

   ```go
   	file, err := os.Open("output.bin")
   	if err != nil {
   		fmt.Println("打开文件失败: ", err.Error())
   		return
   	}
   	defer file.Close()
   
   	st, err := file.Stat()
   	if err != nil{
   		fmt.Println("获取文件状态失败")
   		return
   	}
   	fileSize := st.Size()
   
   	data := make([]byte, fileSize,fileSize)
   	_, err = file.Read(data)
   	if err != nil{
   		log.Fatal(err)
   		return
   	}
   	if err := file.Close(); err != nil{
   		fmt.Println("关闭文件失败...")
   	}
   	fmt.Println("编码成功")
   ```

   

### 写入

***

1. ioutil

   ```go
   	var buf []byte = []byte{0x11,0x22,0x33,0x44,0x88,0x99}
   	if err := ioutil.WriteFile("out.bin",buf,0666); err != nil{
   		log.Fatal(err)
   	}
   ```

2. file.write

   ```go
   func writeBufferToFile(buf *[]byte)  {
   	file, err := os.Create("output.bin")
   	if err != nil {
   		fmt.Println("文件创建失败 ", err.Error())
   		return
   	}
   	defer file.Close()
   
   	file.Write(*buf)
   	if err := file.Close(); err != nil{
   		fmt.Println("关闭文件失败...")
   	}
   	fmt.Println("编码成功")
   }
   ```

   

## 20.2 文本文件





# 第二十一章 格式化输出



## 21.1 参数介绍

***

| %v   | 按值的本来值输出                         |
| ---- | ---------------------------------------- |
| %+v  | 在 %v 基础上，对结构体字段名和值进行展开 |
| %#v  | 输出 Go 语言语法格式的值                 |
| %T   | 输出 Go 语言语法格式的类型和值           |
| %%   | 输出 % 本体                              |
| %b   | 整型以二进制方式显示                     |
| %o   | 整型以八进制方式显示                     |
| %d   | 整型以十进制方式显示                     |
| %x   | 整型以十六进制方式显示                   |
| %X   | 整型以十六进制、字母大写方式显示         |
| %U   | Unicode 字符                             |
| %f   | 浮点数                                   |
| %p   | 指针，十六进制方式显示                   |



## 21.2 例子

***

```go
package mainimport "fmt"import "os"type point struct {

x, y int}func main() {



// Go 为常规 Go 值的格式化设计提供了多种打印方式。例

// 如，这里打印了 `point` 结构体的一个实例。

p := point{1, 2}

fmt.Printf("%v\n", p)

// 输出：{1 2}



// 如果值是一个结构体，`%+v` 的格式化输出内容将包括

// 结构体的字段名。

fmt.Printf("%+v\n", p)

// 输出：{x:1 y:2}



// `%#v` 形式则输出这个值的 Go 语法表示。例如，值的

// 运行源代码片段。

fmt.Printf("%#v\n", p)

// 输出：main.point{x:1, y:2}



// 需要打印值的类型，使用 `%T`。

fmt.Printf("%T\n", p)

// 输出：main.point



// 格式化布尔值是简单的。

fmt.Printf("%t\n", true)

// 输出：true



// 格式化整形数有多种方式，使用 `%d`进行标准的十进

// 制格式化。

fmt.Printf("%d\n", 123)

// 输出：123



// 这个输出二进制表示形式。

fmt.Printf("%b\n", 14)

// 输出：1110



// 这个输出给定整数的对应字符。

fmt.Printf("%c\n", 33)

// 输出：!



// `%x` 提供十六进制编码。

fmt.Printf("%x\n", 456)

// 输出：1c8



// 对于浮点型同样有很多的格式化选项。使用 `%f` 进

// 行最基本的十进制格式化。

fmt.Printf("%f\n", 78.9)

// 输出：78.900000



// `%e` 和 `%E` 将浮点型格式化为（稍微有一点不

// 同的）科学技科学记数法表示形式。

fmt.Printf("%e\n", 123400000.0)

// 输出：1.234000e+08

fmt.Printf("%E\n", 123400000.0)

// 输出：1.234000E+08



// 使用 `%s` 进行基本的字符串输出。

fmt.Printf("%s\n", "\"string\"")

// 输出："string"



// 像 Go 源代码中那样带有双引号的输出，使用 `%q`。

fmt.Printf("%q\n", "\"string\"")

// 输出："\"string\""



// 和上面的整形数一样，`%x` 输出使用 base-16 编码的字

// 符串，每个字节使用 2 个字符表示。

fmt.Printf("%x\n", "hex this")

// 输出：6865782074686973



// 要输出一个指针的值，使用 `%p`。

fmt.Printf("%p\n", &p)

// 输出：0x42135100



// 当输出数字的时候，你将经常想要控制输出结果的宽度和

// 精度，可以使用在 `%` 后面使用数字来控制输出宽度。

// 默认结果使用右对齐并且通过空格来填充空白部分。

fmt.Printf("|%6d|%6d|\n", 12, 345)

// 输出：| 12| 345|



// 你也可以指定浮点型的输出宽度，同时也可以通过 宽度.

// 精度 的语法来指定输出的精度。

fmt.Printf("|%6.2f|%6.2f|\n", 1.2, 3.45)

// 输出：| 1.20| 3.45|



// 要左对齐，使用 `-` 标志。

fmt.Printf("|%-6.2f|%-6.2f|\n", 1.2, 3.45)

// 输出：|1.20 |3.45 |



// 你也许也想控制字符串输出时的宽度，特别是要确保他们在

// 类表格输出时的对齐。这是基本的右对齐宽度表示。

fmt.Printf("|%6s|%6s|\n", "foo", "b")

// 输出：| foo| b|



// 要左对齐，和数字一样，使用 `-` 标志。

fmt.Printf("|%-6s|%-6s|\n", "foo", "b")

// 输出：|foo |b |



// 到目前为止，我们已经看过 `Printf`了，它通过 `os.Stdout`

// 输出格式化的字符串。`Sprintf` 则格式化并返回一个字

// 符串而不带任何输出。

s := fmt.Sprintf("a %s", "string")

fmt.Println(s)

// 输出：a string



// 你可以使用 `Fprintf` 来格式化并输出到 `io.Writers`

// 而不是 `os.Stdout`。

fmt.Fprintf(os.Stderr, "an %s\n", "error")

// 输出：an error}
```





# 第二十二章  protobuf



## 22.1 安装

1. windows

   ```ini
   [下载protoc]
   url = https://github.com/protocolbuffers/protobuf/releases/download/v21.5/protoc-21.5-win64.zip
   
   [下载protoc-gen-go]
   url = https://github.com/protocolbuffers/protobuf-go/releases/download/v1.28.1/protoc-gen-go.v1.28.1.windows.amd64.zip
   
   [安装]
   step1 = 解压protoc,将bin目录加入path
   step2 = 解压protoc-gen-go,将protoc-gen-go.exe 放到protoc-21.5-win64\bin 里面
   
   
   [产生pb文件]
   cmd = protoc --go_out=. person.proto
   ```

2. centos

   ```ini
   [下载protoc]
   url = https://github.com/protocolbuffers/protobuf/releases/download/v21.5/protoc-21.5-linux-x86_64.zip
   
   [下载protoc-gen-go]
   url = https://github.com/protocolbuffers/protobuf-go/releases/download/v1.28.1/protoc-gen-go.v1.28.1.linux.amd64.tar.gz
   
   [安装]
   step1 = unzip protoc-21.5-linux-x86_64.zip
   step2 = tar -zxvf protoc-gen-go.v1.28.1.linux.amd64.tar.gz --warning=no-timestamp
   step3 = mv protoc-gen-go bin/
   step4 = 把bin目录加入系统path
   ```



## 22.2 编译

1. person.proto

   ```protobuf
   syntax = "proto3";
   package Business;
   option go_package="/netMessage"; // go语言必须加这行,分号前是生成文件路径;后面是package名称
   
   message person {    //  aa 会生成 Aa 命名的结构体
     int32 id = 1;
     string name = 2;
   }
   
   message all_person {    //  aa_bb 会生成 AaBb 的驼峰命名的结构体
     repeated person Per = 1;
   }
   ```

2. 编译，项目根目录执行

   ```shell
   protoc --go_out=. .\message.proto
   ```




# 第二十三章 http客户端



## 23.1 Get请求

```go
// 基本的GET请求
package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"net/http"
)

type Result struct {
	Name string `json:"name"`
	Age  int    `json:age`
}

func main() {
	resp, err := http.Get("http://192.168.2.110:8100")
	if err != nil {
		fmt.Println(err)
		return
	}
	defer resp.Body.Close()
	body, err := ioutil.ReadAll(resp.Body)
	fmt.Println(string(body))
	fmt.Println(resp.StatusCode)
	if resp.StatusCode == 200 {
		fmt.Println("ok")
	}

	//解析json
	var res = new(Result)
	_ = json.Unmarshal(body, res)
	fmt.Println(res)
}
```

添加请求头

```go
package main

import (
	"fmt"
	"io/ioutil"
	"net/http"
)

func main() {
	client := &http.Client{}
	req, _ := http.NewRequest("GET", "http://192.168.2.110:8100", nil)
	req.Header.Add("name", "zhaofan")
	req.Header.Add("age", "3")
	resp, _ := client.Do(req)
	body, _ := ioutil.ReadAll(resp.Body)
	fmt.Printf(string(body))
}
```



## 23.2 Post请求



### 23.2.1 表单

1. 做法一

   ```go
   package main
   
   import (
       "fmt"
       "io/ioutil"
       "net/http"
       "net/url"
   )
   
   func main() {
       urlValues := url.Values{}
       urlValues.Add("name","zhaofan")
       urlValues.Add("age","22")
       resp, _ := http.PostForm("http://httpbin.org/post",urlValues)
       body, _ := ioutil.ReadAll(resp.Body)
       fmt.Println(string(body))
   }
   ```

2. 做法二

   ```go
   //或者
   package main
   
   import (
   	"fmt"
   	"io/ioutil"
   	"net/http"
   	"net/url"
   	"strings"
   )
   
   func main() {
   	urlValues := url.Values{
   		"name": {"nash"},
   		"age":  {"9902"},
   	}
   	reqBody := urlValues.Encode()
   	resp, _ := http.Post("http://127.0.0.1:5234/login", "application/x-www-form-urlencoded", strings.NewReader(reqBody))
   	body, _ := ioutil.ReadAll(resp.Body)
   	fmt.Println(string(body))
   }
   ```

   



### 23.2.2 json

1. 推荐的写法

   ```go
   package main
   
   import (
       "bytes"
       "encoding/json"
       "fmt"
       "io/ioutil"
       "net/http"
   )
   
   func main() {
       data := make(map[string]interface{})
       data["name"] = "zhaofan"
       data["age"] = "23"
       bytesData, _ := json.Marshal(data)
       resp, _ := http.Post("http://httpbin.org/post","application/json", bytes.NewReader(bytesData))
       body, _ := ioutil.ReadAll(resp.Body)
       fmt.Println(string(body))
   }
   ```

2. 另一个做法

   ```go
   package main
   
   import (
       "bytes"
       "encoding/json"
       "fmt"
       "io/ioutil"
       "net/http"
   )
   
   func main() {
       client := &http.Client{}
       data := make(map[string]interface{})
       data["name"] = "zhaofan"
       data["age"] = "23"
       bytesData, _ := json.Marshal(data)
       req, _ := http.NewRequest("POST","http://httpbin.org/post",bytes.NewReader(bytesData))
       req.Header.Set("Content-Type", "application/json")
       resp, _ := client.Do(req)
       body, _ := ioutil.ReadAll(resp.Body)
       fmt.Println(string(body))
   
   }
   ```

   





# 第二十四章 sqlite3



## 24.1 安装依赖

```shell
#官网:https://github.com/mattn/go-sqlite3
go get github.com/mattn/go-sqlite3
```



## 24.2 安装gcc

```shell
#windows,设置环境变量;linux下直接用yum安装即可
wget https://github.com/niXman/mingw-builds-binaries/releases/download/12.2.0-rt_v10-rev0/x86_64-12.2.0-release-win32-seh-rt_v10-rev0.7z
```



## 24.3 示例代码

```go
package main

import (
	"database/sql"
	"fmt"
	_ "github.com/mattn/go-sqlite3"
	"log"
	"os"
)

func main() {
	os.Remove("./foo.db")

	db, err := sql.Open("sqlite3", "./foo.db")
	if err != nil {
		log.Fatal(err)
	}
	defer db.Close()

	sqlStmt := `
	create table foo (id integer not null primary key, name text);
	delete from foo;
	create table IF NOT EXISTS photo (id integer not null primary key, data blob);
	delete from photo;
	`
	_, err = db.Exec(sqlStmt)
	if err != nil {
		log.Printf("%q: %s\n", err, sqlStmt)
		return
	}

    // 事务操作
	tx, err := db.Begin()
	if err != nil {
		log.Fatal(err)
	}
	stmt, err := tx.Prepare("insert into foo(id, name) values(?, ?)")
	if err != nil {
		log.Fatal(err)
	}
	defer stmt.Close()
	for i := 0; i < 100; i++ {
		_, err = stmt.Exec(i, fmt.Sprintf("こんにちは世界%03d", i))
		if err != nil {
			log.Fatal(err)
		}
	}
	err = tx.Commit()
	if err != nil {
		log.Fatal(err)
	}

    //查询
	rows, err := db.Query("select id, name from foo")
	if err != nil {
		log.Fatal(err)
	}
	defer rows.Close()
	for rows.Next() {
		var id int
		var name string
		err = rows.Scan(&id, &name)
		if err != nil {
			log.Fatal(err)
		}
		fmt.Println(id, name)
	}
	err = rows.Err()
	if err != nil {
		log.Fatal(err)
	}

	stmt, err = db.Prepare("select name from foo where id = ?")
	if err != nil {
		log.Fatal(err)
	}
	defer stmt.Close()
	var name string
	err = stmt.QueryRow("3").Scan(&name)
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println(name)

    // 删除
	_, err = db.Exec("delete from foo")
	if err != nil {
		log.Fatal(err)
	}

    // 插入
	_, err = db.Exec("insert into foo(id, name) values(1, 'foo'), (2, 'bar'), (3, 'baz')")
	if err != nil {
		log.Fatal(err)
	}
    
    // 更新
	_, err = db.Exec("update foo set name='nash' where id = 2")
	if err != nil {
		log.Fatal(err)
	}

	rows, err = db.Query("select id, name from foo")
	if err != nil {
		log.Fatal(err)
	}
	defer rows.Close()
	for rows.Next() {
		var id int
		var name string
		err = rows.Scan(&id, &name)
		if err != nil {
			log.Fatal(err)
		}
		fmt.Println(id, name)
	}
	err = rows.Err()
	if err != nil {
		log.Fatal(err)
	}
    
    // 二进制数据操作
	stmt, err = db.Prepare("insert into photo(id, data) values(?, ?)")
	if err != nil {
		log.Fatal(err)
	}
	defer stmt.Close()
	var content = []byte{19, 22, 33, 47, 58, 60}
	_, err = stmt.Exec(2, content)
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println(name)

	{
		rows, err = db.Query("select id, data from photo where id = 2")
		if err != nil {
			log.Fatal(err)
		}
		defer rows.Close()
		for rows.Next() {
			var id int
			var name []byte
			err = rows.Scan(&id, &name)
			if err != nil {
				log.Fatal(err)
			}
			fmt.Println(id, name)
		}
		err = rows.Err()
		if err != nil {
			log.Fatal(err)
		}
	}
}
```



## 24.4 sqlite3和protobuf组合

1. 只有用一个表Role，里面有两个字段uid和data(blob类型)
2. 数据用protobuf序列化再存进去
3. protobuf的proto文件里面的Role[序列化存入data里]类型的字段，可以增加，不能删除，也不能修改字段的索引，即可兼容。
4. 如果增加新字段后，希望默认值不是protobuf的默认值，可以自己定义version字段和upgrade函数，类似居家修仙那样。





# 第二十五章 LevelDB

Google 开源的高性能的key-value 数据库，数据存在硬盘上，redis是存在硬盘里面。



## 25.1 安装

```shell
go get github.com/syndtr/goleveldb/leveldb
```



## 25.2 基本使用



### 25.2.1 打开数据库

```go
db, err := leveldb.OpenFile("path/to/db", nil)
...
defer db.Close()
...
```





### 25.2.2 读写数据库

```go
// 注意：返回数据结果不能修改
data, err := db.Get([]byte("key"), nil)
...
err = db.Put([]byte("key"), []byte("value"), nil)
...
err = db.Delete([]byte("key"), nil)
...
```



### 25.2.3 数据库遍历

```go
iter := db.NewIterator(nil, nil)
for iter.Next() {
    key := iter.Key()
    value := iter.Value()
    ...
}
iter.Release()
err = iter.Error()
...
```



### 25.2.4 迭代查询

```go
iter := db.NewIterator(nil, nil)
for ok := iter.Seek(key); ok; ok = iter.Next() {
    // Use key/value.
    ...
}
iter.Release()
err = iter.Error()
...
```





### 25.2.5 按区间查询

```go
iter := db.NewIterator(&util.Range{Start: []byte("foo"), Limit: []byte("xoo")}, nil)
for iter.Next() {
    // Use key/value.
    ...
}
iter.Release()
err = iter.Error()
...
```





### 25.2.6 按前缀查询

```go
iter := db.NewIterator(util.BytesPrefix([]byte("foo-")), nil)
for iter.Next() {
    // Use key/value.
    ...
}
iter.Release()
err = iter.Error()
...
```



### 25.2.7 批量写

```go
batch := new(leveldb.Batch)
batch.Put([]byte("foo"), []byte("value"))
batch.Put([]byte("bar"), []byte("another value"))
batch.Delete([]byte("baz"))
err = db.Write(batch, nil)
...
```





### 25.2.8 不使用内存，直接读写硬盘

```go
o := &opt.Options{
    Filter: filter.NewBloomFilter(10),
}
db, err := leveldb.OpenFile("path/to/db", o)
...
defer db.Close()
...
```





## 25.3 示例代码

```go
package main

import (
	"fmt"
	"github.com/syndtr/goleveldb/leveldb"
)

func main() {
	db, err := leveldb.OpenFile("level/game", nil)
	if err != nil {
		panic(err)
	}
	defer db.Close()
	err = db.Put([]byte("name"), []byte("trump"), nil)

	myName, err := db.Get([]byte("name"), nil)
	if err != nil {
		panic(err)
	}
	fmt.Println("myName = ", string(myName))
}

```





# 第二十六章  Redis



网站：https://github.com/go-redis/redis





# 第二十七章 socks5代理

xshell 、chrome、火狐浏览器可以配置socks5代理来加速。



服务实现

1. 安装包

   ```shell
   go get github.com/armon/go-socks5
   ```

2. 源码

   ```go
   package main
   
   import "github.com/armon/go-socks5"
   
   func main() {
   	// Create a SOCKS5 server
   	conf := &socks5.Config{}
   	server, err := socks5.New(conf)
   	if err != nil {
   		panic(err)
   	}
   
   	// Create SOCKS5 proxy on localhost port 8000
   	if err := server.ListenAndServe("tcp", "0.0.0.0:8000"); err != nil {
   		panic(err)
   	}
   }
   ```

   



# 第二十八章  Gin

1. 示例

   ```go
   package main
   
   import (
   	"net/http"
   
   	"github.com/gin-gonic/gin"
   )
   
   func main() {
   	r := gin.Default()
   	r.GET("/ping", func(c *gin.Context) {
   		c.JSON(http.StatusOK, gin.H{
   			"message": "pong",
   		})
   	})
   	r.Run() // listen and serve on 0.0.0.0:8080 (for windows "localhost:8080")
   }
   
   ```

2. 编译

   ```shell
   go mod tidy
   go build
   ```

3. 解决跨域问题

   ```go
   import (
   	"github.com/gin-contrib/cors"
   	"github.com/gin-gonic/gin"
   )
   
   func main() {
   	app := gin.New()
   	app.Use(cors.Default())
   
   }
   ```

   



# 第二十九章  日志

 常用的日志库logrus



用法

```go
log "github.com/sirupsen/logrus"

// 其它地方的API 接口就和系统自带的log完全一样
```





示例代码

```go
package main

import (
	log "github.com/sirupsen/logrus"
)

func main() {
	log.SetLevel(log.TraceLevel)
	log.Info("hello")
	log.Trace("this is trace msg")
	log.Debug("this is debug msg")
	log.Warn("this is warn msg")
	log.Error("this is error msg")
	log.Fatal("this is fatal msg")
}
```





# 第三十章  Mongodb



使用MongoDB的版本 4.2.24



驱动版本：go.mongodb.org/mongo-driver v1.11.7





## 30.1 连接

```go
func testMongoConnect() {

	// The Stable API feature requires MongoDB Server 5.0 or later.
	// Stable API 要求MongoDB 服务版本在5.0 之后
	// Use the SetServerAPIOptions() method to set the Stable API version to 1
	//serverAPI := options.ServerAPI(options.ServerAPIVersion1)
	//opts := options.Client().ApplyURI(uri).SetServerAPIOptions(serverAPI)
	opts := options.Client().ApplyURI(uri)

	// Create a new client and connect to the server
	// 发起链接
	client, err := mongo.Connect(context.TODO(), opts)
	if err != nil {
		panic(err)
	}
	defer func() {
		// 断开链接
		if err = client.Disconnect(context.TODO()); err != nil {
			panic(err)
		}
	}()
	// Send a ping to confirm a successful connection
	var result bson.M
	if err := client.Database("admin").RunCommand(context.TODO(), bson.D{{"ping", 1}}).Decode(&result); err != nil {
		panic(err)
	}
	fmt.Println("Pinged your deployment. You successfully connected to MongoDB!")
}
```





## 30.2 插入数据

```go
type Address struct {
       Street string
       City   string
       State  string
}

type Student struct {
       FirstName string  `bson:"first_name,omitempty"`
       LastName  string  `bson:"last_name,omitempty"`      // 没有赋值,就不插入
       Address   Address 
       Age       int
}

coll := client.Database("school").Collection("students")
address1 := Address{ "1 Lakewood Way", "Elwood City", "PA" }
student1 := Student{ FirstName : "Arthur", Address : address1, Age : 8}
_, err = coll.InsertOne(context.TODO(), student1)
```





## 30.3 查询单条记录

```go
func testQuery() {
	opts := options.Client().ApplyURI(uri)
	// Create a new client and connect to the server
	// 发起链接
	client, err := mongo.Connect(context.TODO(), opts)
	if err != nil {
		panic(err)
	}
	defer func() {
		// 断开链接
		if err = client.Disconnect(context.TODO()); err != nil {
			panic(err)
		}
	}()
    
	// Send a ping to confirm a successful connection
	var result bson.M
	if err := client.Database("admin").RunCommand(context.TODO(), bson.D{{"ping", 1}}).Decode(&result); err != nil {
		panic(err)
	}

	// 查询一条记录, 并将其转换为json
	coll := client.Database("school").Collection("students")
	filter := bson.D{{"id", 1001}}
	type Student struct {
		Id       int
		NickName string
		Gold     int
	}
	// 指定数据类型后可以直接解析
	var student Student
	err = coll.FindOne(context.TODO(), filter).Decode(&student)
	if err != nil {
		panic(err)
	}

	//转换为JSON
	str, err := json.Marshal(student)
	log.Println(str)
}
```



## 30.4 查询多条记录

```go
func testQueryMany() {
	opts := options.Client().ApplyURI(uri)

	// Create a new client and connect to the server
	// 发起链接
	client, err := mongo.Connect(context.TODO(), opts)
	if err != nil {
		panic(err)
	}
	defer func() {
		// 断开链接
		if err = client.Disconnect(context.TODO()); err != nil {
			panic(err)
		}
	}()
	// Send a ping to confirm a successful connection
	var result bson.M
	if err := client.Database("admin").RunCommand(context.TODO(), bson.D{{"ping", 1}}).Decode(&result); err != nil {
		panic(err)
	}

	// 查询一条记录, 并将其转换为json
	coll := client.Database("school").Collection("students")
	filter := bson.D{{}}
	type Student struct {
		Id       int
		NickName string
		Gold     int
	}
	// 指定数据类型后可以直接解析
	var students []Student
	cursor, err := coll.Find(context.TODO(), filter)
	if err != nil {
		panic(err)
	}
	if err = cursor.All(context.TODO(), &students); err != nil {
		panic(err)
	}
	str, err := json.Marshal(students)
	log.Println(str)
}
```





## 30.5 更新记录

1. 直接使用bson更新

   ```go
   func testUpdate() {
   	opts := options.Client().ApplyURI(uri)
   
   	// Create a new client and connect to the server
   	// 发起链接
   	client, err := mongo.Connect(context.TODO(), opts)
   	if err != nil {
   		panic(err)
   	}
   	defer func() {
   		// 断开链接
   		if err = client.Disconnect(context.TODO()); err != nil {
   			panic(err)
   		}
   	}()
   	// Send a ping to confirm a successful connection
   	var result bson.M
   	if err := client.Database("admin").RunCommand(context.TODO(), bson.D{{"ping", 1}}).Decode(&result); err != nil {
   		panic(err)
   	}
   
   	// 查询一条记录, 并将其转换为json
   	coll := client.Database("school").Collection("students")
   	filter := bson.D{{"id", 1002}}
   	update := bson.D{{"$set", bson.D{{"gold", 90000}}}}
   	type Student struct {
   		Id       int
   		NickName string
   		Gold     int
   	}
   	// 指定数据类型后可以直接解析
   	//var student Student
   	r2, err := coll.UpdateOne(context.TODO(), filter, update)
   	if err != nil {
   		panic(err)
   	}
   
   	// TODO 如何转换为JSON
   
   	//str, err := json.Marshal(student)
   
   	log.Println(r2)
   }
   ```

2. 使用结构体更新

   ```shell
   func testUpdate() {
   	opts := options.Client().ApplyURI(uri)
   
   	// Create a new client and connect to the server
   	// 发起链接
   	client, err := mongo.Connect(context.TODO(), opts)
   	if err != nil {
   		panic(err)
   	}
   	defer func() {
   		// 断开链接
   		if err = client.Disconnect(context.TODO()); err != nil {
   			panic(err)
   		}
   	}()
   	// Send a ping to confirm a successful connection
   	var result bson.M
   	if err := client.Database("admin").RunCommand(context.TODO(), bson.D{{"ping", 1}}).Decode(&result); err != nil {
   		panic(err)
   	}
   
   	// 查询一条记录, 并将其转换为json
   	coll := client.Database("school").Collection("students")
   	filter := bson.D{{"id", 1002}}
   
   	type Student struct {
   		Id       int
   		NickName string
   		Gold     int
   	}
   
   	var student Student = Student{1002, "trump", 790000}
   
   	update := bson.D{{"$set", student}}
   
   	// 指定数据类型后可以直接解析
   	//var student Student
   	r2, err := coll.UpdateOne(context.TODO(), filter, update)
   	if err != nil {
   		panic(err)
   	}
   
   	// TODO 如何转换为JSON
   
   	//str, err := json.Marshal(student)
   
   	log.Println(r2)
   }
   ```

   



## 30.6 删除记录

```go
func testDelete() {
	opts := options.Client().ApplyURI(uri)

	// Create a new client and connect to the server
	// 发起链接
	client, err := mongo.Connect(context.TODO(), opts)
	if err != nil {
		panic(err)
	}
	defer func() {
		// 断开链接
		if err = client.Disconnect(context.TODO()); err != nil {
			panic(err)
		}
	}()
	// Send a ping to confirm a successful connection
	var result bson.M
	if err := client.Database("admin").RunCommand(context.TODO(), bson.D{{"ping", 1}}).Decode(&result); err != nil {
		panic(err)
	}

	// 查询一条记录, 并将其转换为json
	coll := client.Database("school").Collection("students")
	filter := bson.D{{"id", 1001}}
	type Student struct {
		Id       int
		NickName string
		Gold     int
	}
	// 指定数据类型后可以直接解析
	result2, err := coll.DeleteOne(context.TODO(), filter)
	if err != nil {
		panic(err)
	}

	// TODO 如何转换为JSON

	//str, err := json.Marshal(result2)

	log.Println(result2)
}
```





## 30.7 更新记录时，不存在则插入

```go
	opts := options.Update().SetUpsert(true)
	_, err = coll.UpdateOne(context.TODO(), filter, update, opts)
```





# 第三十一章 GRPC



## 31.1 安装protoc

参考上面的教程





## 31.2 安装protoc的Golang gRPC插件

```shell
go install google.golang.org/protobuf/cmd/protoc-gen-go@latest
go install google.golang.org/grpc/cmd/protoc-gen-go-grpc@latest
```





## 31.3 编写proto文件

```protobuf
syntax = "proto3";

option go_package="/proto";

package Business;

service Hello {
  rpc Say (SayRequest) returns (SayResponse);
}

message SayResponse {
  string Message = 1;
}

message SayRequest {
  string Name = 1;
}
```





## 31.4 生成代码

```shell
protoc --go_out=.  --go-grpc_out=. proto/hello.proto
```





## 31.5 服务端代码

服务端的项目名称为 grpcdemo

```go
package main

import (
    "context"
    "fmt"
    "grpcdemo/proto"
    "net"

    "google.golang.org/grpc"
)

type server struct {
    proto.UnimplementedHelloServer
}

func (s *server) Say(ctx context.Context, req *proto.SayRequest) (*proto.SayResponse, error) {
    fmt.Println("request:", req.Name)
    return &proto.SayResponse{Message: "Hello " + req.Name}, nil
}

func main() {
    listen, err := net.Listen("tcp", ":8001")
    if err != nil {
        fmt.Printf("failed to listen: %v", err)
        return
    }
    s := grpc.NewServer()
    proto.RegisterHelloServer(s, &server{})
    //reflection.Register(s)

    defer func() {
        s.Stop()
        listen.Close()
    }()

    fmt.Println("Serving 8001...")
    err = s.Serve(listen)
    if err != nil {
        fmt.Printf("failed to serve: %v", err)
        return
    }
}
```







## 31.6 客户端代码

客户端的项目名称为grpchello

```go
package main

import (
    "bufio"
    "context"
    "fmt"
    "grpchello/proto"
    "os"

    "google.golang.org/grpc"
    "google.golang.org/grpc/credentials/insecure"
)

func main() {

    var serviceHost = "127.0.0.1:8001"

    conn, err := grpc.Dial(serviceHost, grpc.WithTransportCredentials(insecure.NewCredentials()))
    if err != nil {
        fmt.Println(err)
    }
    defer conn.Close()

    client := proto.NewHelloClient(conn)
    rsp, err := client.Say(context.TODO(), &proto.SayRequest{
        Name: "BOSIMA",
    })

    if err != nil {
        fmt.Println(err)
    }

    fmt.Println(rsp)

    fmt.Println("按回车键退出程序...")
    in := bufio.NewReader(os.Stdin)
    _, _, _ = in.ReadLine()
}
```

