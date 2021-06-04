# 第一章 解析



## 1.1 简单的例子

```c++
#include <rapidjson/document.h>
#include <rapidjson/writer.h>
#include <rapidjson/stringbuffer.h>
#include <iostream>
using namespace std;
using namespace rapidjson;

int main() {
	// 1. Parse a JSON string into DOM.
	const char* json = "{ \"name\":\"nash\",\"detail\":{\"height\":182,\"weight\":100}}";
	Document d;
	d.Parse(json);
    // 判断解析是否成功
	if (d.HasParseError()) {
		return -1;
	}

	// 2. 获取value
	if (d.HasMember("name") && d["name"].IsString()) {
		string name = d["name"].GetString();
			cout << "name : " << name << endl;
	}

	// 3. 获取嵌套的value
	if (d.HasMember("detail") && d["detail"].HasMember("height") && d["detail"]["height"].IsInt()) {
		int height = d["detail"]["height"].GetInt();
			cout << "height : " << height << endl;
	}

	// 4. document 转换为JSON 字符串
	StringBuffer buffer;
	Writer<StringBuffer> writer(buffer);
	d.Accept(writer);
	std::cout << "detail : " << buffer.GetString() << std::endl;

	// 5. Value 转换为字符串
	{
		StringBuffer buffer;
		Writer<StringBuffer> writer(buffer);
		d["detail"].Accept(writer);
		std::cout << "detail : " << buffer.GetString() << std::endl;
	}

	// 6. 构造JSON字符串,通常用于http server 的响应
	{
		StringBuffer s;
		Writer<StringBuffer> writer(s);
		writer.StartObject();
		writer.Key("cmd");
		writer.String("vm_canceled_save");
		writer.Key("args");
		writer.StartObject();
		writer.Key("private_ip");
		writer.String("127.0.0.1");
		writer.Key("name");
		writer.String("peter");
		writer.EndObject();

		writer.Key("arr");
		writer.StartArray();                // Between StartArray()/EndArray(),
		for (unsigned i = 0; i < 4; i++)
			writer.Uint(i);                 // all values are elements of the array.
		writer.EndArray();

		writer.EndObject();
		std::string message = s.GetString();
		cout << "message : " << message << endl;
	}
	return 0;
}
```

