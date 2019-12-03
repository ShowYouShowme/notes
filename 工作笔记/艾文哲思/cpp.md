# 可变模板参数

```c++
template<typename T>
std::string toString(T t){
	ostringstream os;
	os << t;
	return os.str();
}
template<typename T, typename... Args>
std::string toString(T head, Args... args){
	ostringstream os;
	os << head;
	return os.str() + toString(args...);
}
int main(){
	std::string s1 = toString(12, "ABC", 12.5, true);
	std::cout << s1 << std::endl;
	return 0;
}
```



## 获取日期

```cpp
static std::string DatetimeToString(time_t time)
{
	tm *tm_ = localtime(&time);                // 将time_t格式转换为tm结构体
	int year, month, day;// 定义时间的各个int临时变量。
	year = tm_->tm_year + 1900;                // 临时变量，年，由于tm结构体存储的是从1900年开始的时间，所以临时变量int为tm_year加上1900。
	month = tm_->tm_mon + 1;                   // 临时变量，月，由于tm结构体的月份存储范围为0-11，所以临时变量int为tm_mon加上1。
	day = tm_->tm_mday;                        // 临时变量，日。

	int hour = tm_->tm_hour;
	int minute = tm_->tm_min;
	int second = tm_->tm_sec;

	std::ostringstream os;
	os << year << "-"  
	   << std::setw(2) << std::setfill('0') << month << "-"  
	   << std::setw(2) << std::setfill('0') << day << " "
	   << std::setw(2) << std::setfill('0') << hour << ":"  
	   << std::setw(2) << std::setfill('0') << minute << ":"  
	   << std::setw(2) << std::setfill('0') << second;
	std::string date = os.str();
	return date;                                // 返回转换日期时间后的string变量。
}
```

