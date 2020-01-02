# libcurl示例代码

> 1. 将接收到的数据保存到本地
>
>    ```cpp
>    #include "curl/curl.h"
>      #include <stdio.h>
>      #include <iostream>
>      using namespace std;
>      /**
>               *	@brief libcurl接收到数据时的回调函数
>      *
>             *	将接收到的数据保存到本地文件中，同时显示在控制台上。
>       *
>             *	@param [in] buffer 接收到的数据所在缓冲区
>                *	@param [in] size 数据长度
>             *	@param [in] nmemb 数据片数量
>             *	@param [in/out] 用户自定义指针
>             *	@return 获取的数据长度
>    */
>    
>       size_t process_data(void *buffer, size_t size, size_t nmemb, void *user_p)
>      {
>      	FILE *fp = (FILE *)user_p;
>      	size_t return_size = fwrite(buffer, size, nmemb, fp);
>      	cout << (char *)buffer << endl;
>      	return return_size;
>      }
>      
>      int main(int argc, char **argv)
>      {
>      	// 初始化libcurl
>      	CURLcode return_code;
>      	return_code = curl_global_init(CURL_GLOBAL_WIN32);
>      	if (CURLE_OK != return_code)
>      	{
>      		cerr << "init libcurl failed." << endl;
>      		return -1;
>      	}
>      
>      	// 获取easy handle
>      	CURL *easy_handle = curl_easy_init();
>      	if (NULL == easy_handle)
>      	{
>      		cerr << "get a easy handle failed." << endl;
>      		curl_global_cleanup();
>      		return -1;
>      	}
>      
>      	FILE *fp = fopen("data.html", "ab+");	// 
>      	// 设置easy handle属性
>      	curl_easy_setopt(easy_handle, CURLOPT_URL, "https://www.baidu.com");
>      	curl_easy_setopt(easy_handle, CURLOPT_WRITEFUNCTION, &process_data);
>      	curl_easy_setopt(easy_handle, CURLOPT_WRITEDATA, fp);
>      
>      	// 执行数据请求
>      	curl_easy_perform(easy_handle);
>      	// 释放资源
>      
>      	cout << "============" << endl;
>      	fclose(fp);
>      	curl_easy_cleanup(easy_handle);
>      	curl_global_cleanup();
>      
>      	return 0;
>      }
>    ```
>
> 2. 基本使用
>
>    ```cpp
>    #include <stdio.h>
>    #include <curl/curl.h>
>    
>    int main(void)
>    {
>    	CURL *curl;
>    	CURLcode res;
>    
>    	curl_global_init(CURL_GLOBAL_DEFAULT);
>    
>    	curl = curl_easy_init();
>    	if (curl) {
>    		curl_easy_setopt(curl, CURLOPT_URL, "http://127.0.0.1:8000/a.html");
>    
>    #ifdef SKIP_PEER_VERIFICATION
>    		/*
>              		 * If you want to connect to a site who isn't using a certificate that is
>              		 * signed by one of the certs in the CA bundle you have, you can skip the
>              		 * verification of the server's certificate. This makes the connection
>              		 * A LOT LESS SECURE.
>    		 *
>            		 * If you have a CA cert for the server stored someplace else than in the
>            		 * default bundle, then the CURLOPT_CAPATH option might come handy for
>            		 * you.
>    		 */
>    		curl_easy_setopt(curl, CURLOPT_SSL_VERIFYPEER, 0L);
>    #endif
>    
>    #ifdef SKIP_HOSTNAME_VERIFICATION
>    		/*
>              		 * If the site you're connecting to uses a different host name that what
>              		 * they have mentioned in their server certificate's commonName (or
>              		 * subjectAltName) fields, libcurl will refuse to connect. You can skip
>              		 * this check, but this will make the connection less secure.
>    		 */
>    		curl_easy_setopt(curl, CURLOPT_SSL_VERIFYHOST, 0L);
>    #endif
>    
>    		/* Perform the request, res will get the return code */
>    		res = curl_easy_perform(curl);
>    		/* Check for errors */
>    		if (res != CURLE_OK)
>    			fprintf(stderr, "curl_easy_perform() failed: %s\n",
>    				curl_easy_strerror(res));
>    
>    		/* always cleanup */
>    		curl_easy_cleanup(curl);
>    	}
>    
>    	curl_global_cleanup();
>    
>    	return 0;
>    }
>    ```
>
> 3. 获取响应
>
>    ```cpp
>    // GET 请求获取响应
>    #include <stdio.h>
>    #include <curl/curl.h>
>    #include <string>
>    #include <iostream>
>    using namespace std;
>    
>    using uint = unsigned int;
>    
>    /* curl write callback, to fill tidy's input buffer...  */
>    // 注意:返回值必须是body长度
>    uint write_cb(char *in, uint size, uint nmemb, void *out)
>    {
>    	uint r;
>    	r = size * nmemb;
>    	string buf(in, in + size * nmemb);
>    	cout << "response : " << buf << endl;
>    	return r;
>    }
>    
>    
>    int main(int argc, char **argv)
>    {
>    	CURL *curl;
>    	char curl_errbuf[CURL_ERROR_SIZE];
>    	int err;
>    
>    	curl = curl_easy_init();
>    	curl_easy_setopt(curl, CURLOPT_URL, "http://10.10.10.188:8080/reference/HelloWorld.html");
>    	curl_easy_setopt(curl, CURLOPT_ERRORBUFFER, curl_errbuf);
>    	curl_easy_setopt(curl, CURLOPT_NOPROGRESS, 0L);
>    	curl_easy_setopt(curl, CURLOPT_VERBOSE, 1L);
>    	curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, write_cb);
>    	curl_easy_setopt(curl, CURLOPT_WRITEDATA, nullptr);
>    	err = curl_easy_perform(curl);
>    	if (!err) {
>    		cout << "GET req success!" << endl;
>    	}
>    	else
>    		fprintf(stderr, "%s\n", curl_errbuf);
>    
>    	/* clean-up */
>    	curl_easy_cleanup(curl);
>    	return err;
>    
>    	return 0;
>    }
>    ```
>
> 4. 常见选项设置
>
>    ```cpp
>    // 常见选项的设置
>    static bool init(CURL *&conn, char *url)
>    {
>    	CURLcode code;
>    
>    	conn = curl_easy_init();
>    
>    	if (conn == NULL) {
>    		fprintf(stderr, "Failed to create CURL connection\n");
>    		exit(EXIT_FAILURE);
>    	}
>    
>    	code = curl_easy_setopt(conn, CURLOPT_ERRORBUFFER, errorBuffer);
>    	if (code != CURLE_OK) {
>    		fprintf(stderr, "Failed to set error buffer [%d]\n", code);
>    		return false;
>    	}
>    
>    	code = curl_easy_setopt(conn, CURLOPT_URL, url);
>    	if (code != CURLE_OK) {
>    		fprintf(stderr, "Failed to set URL [%s]\n", errorBuffer);
>    		return false;
>    	}
>    
>    	code = curl_easy_setopt(conn, CURLOPT_FOLLOWLOCATION, 1L); // 跟踪爬取重定向的页面
>    	if (code != CURLE_OK) {
>    		fprintf(stderr, "Failed to set redirect option [%s]\n", errorBuffer);
>    		return false;
>    	}
>    
>    	code = curl_easy_setopt(conn, CURLOPT_WRITEFUNCTION, writer);
>    	if (code != CURLE_OK) {
>    		fprintf(stderr, "Failed to set writer [%s]\n", errorBuffer);
>    		return false;
>    	}
>    
>    	code = curl_easy_setopt(conn, CURLOPT_WRITEDATA, &buffer);
>    	if (code != CURLE_OK) {
>    		fprintf(stderr, "Failed to set write data [%s]\n", errorBuffer);
>    		return false;
>    	}
>    
>    	return true;
>    }
>    ```
>
> 5. Post请求
>
>    ```cpp
>    // POST 请求;编码方式 urlencode
>    #include <stdio.h>
>    #include <curl/curl.h>
>    
>    int main(void)
>    {
>    	CURL *curl;
>    	CURLcode res;
>    
>    	/* In windows, this will init the winsock stuff */
>    	curl_global_init(CURL_GLOBAL_ALL);
>    
>    	/* get a curl handle */
>    	curl = curl_easy_init();
>    	if (curl) {
>    		/* First set the URL that is about to receive our POST. This URL can
>    		just as well be a https:// URL if that is what should receive the
>    		data. */
>    		curl_easy_setopt(curl, CURLOPT_URL, "http://10.10.10.188:8090/cplusplus.com/reference/");
>    		/* Now specify the POST data */
>    		curl_easy_setopt(curl, CURLOPT_POSTFIELDS, "name=daniel&project=curl");
>    
>    		/* Perform the request, res will get the return code */
>    		res = curl_easy_perform(curl);
>    		/* Check for errors */
>    		if (res != CURLE_OK)
>    			fprintf(stderr, "curl_easy_perform() failed: %s\n",
>    				curl_easy_strerror(res));
>    
>    		/* always cleanup */
>    		curl_easy_cleanup(curl);
>    	}
>    	curl_global_cleanup();
>    	return 0;
>    }
>    ```
>
>    
>



# libcurl 使用场景

### 1-url编解码

***

+ urlEncode

  ```c++
  string urlEncode(const string& input)
  {
  	char * escape_control = curl_escape(input.c_str(), input.size());
  	if (escape_control == nullptr){
  		throw logic_error("urlEncode failed!");
  	}
  	return string(escape_control);
  }
  ```

+ urlDecode

  ```c++
  string urlDecode(const string& input)
  {
  	char * unescape_control = curl_unescape(input.c_str(), input.size());
  	if (unescape_control == nullptr) {
  		throw logic_error("urlEncode failed!");
  	}
  	return string(unescape_control);
  }
  ```



### 2-设置请求url

***

```cpp
CURL * conn = curl_easy_init();
curl_easy_setopt(conn, CURLOPT_URL, url.c_str());
```



### 3-自定义请求头

***

```cpp
struct curl_slist* headers = NULL;
CURL * conn = curl_easy_init();
headers = curl_slist_append(headers, "Content-Type:application/json;charset=UTF-8");
headers = curl_slist_append(headers, "X-silly-header;"); // 请求头设置空
curl_easy_setopt(conn, CURLOPT_HTTPHEADER, headers);
```



### 4-设置请求方式为POST

***

```cpp
curl_easy_setopt(conn, CURLOPT_POST, 1);//本次操作为POST
```

### 5-设置请求体

***

```c++
// 默认不设置CURLOPT_POST 选择 和请求体,则为GET请求
std::string jsonData;
curl_easy_setopt(conn, CURLOPT_POSTFIELDS, jsonData.c_str());
curl_easy_setopt(conn, CURLOPT_POSTFIELDSIZE, jsonData.size());
```



### 6-获取响应状态码

***

```cpp
// 调用响应状态码保存的statusCode里面;必须先调用curl_easy_perform
long statusCode = -1;
CURLcode code = curl_easy_getinfo(easy_handle, CURLINFO_RESPONSE_CODE, &statusCode);

// 选项 CURLINFO_HEADER_SIZE 获取响应头大小

// 选项 CURLINFO_COOKIELIST 获取cookies列表
```



### 7-获取响应头

***

```cpp
#include <stdio.h>
#include <string.h>
#include <curl/curl.h>
#include <string>
#include <vector>
using namespace std;


static size_t read_head_fun(void *ptr, size_t size, size_t nmemb, void *stream) {
	vector<string>* pHeaders = (vector<string>*)stream;
	string header((const char*)ptr, (const char*)ptr + size*nmemb);
	pHeaders->push_back(header);
	return size*nmemb;
}

int main(int argc, char **argv)
{
	char* url = "http://127.0.0.1:3000";
	CURL* curl_handle;
	CURLcode res;

	vector<string> headers;
	curl_handle = curl_easy_init();
	if (curl_handle) {
		curl_easy_setopt(curl_handle, CURLOPT_URL, url);//set down load url
		curl_easy_setopt(curl_handle, CURLOPT_HEADERFUNCTION, read_head_fun);//set call back fun
		curl_easy_setopt(curl_handle, CURLOPT_HEADERDATA, &headers);//set call back fun

		//start down load
		res = curl_easy_perform(curl_handle);
		printf("curl fetch code %d\n", res);
	}
	if (curl_handle) {
		curl_easy_cleanup(curl_handle);
	}
	if (url) {
		free(url);
	}

	return 0;
}
```





### 8-获取响应body

***

```cpp
// 注意回调函数的签名
static size_t  process_data(void *buffer, size_t size, size_t nmemb, void *param)
{
    std::string* pJson = (std::string *)param;
    pJson->assign((const char*)buffer, (const char*)buffer + size * nmemb);
    return size * nmemb;
}

// body 会被写入到json里面
std::string	json;
curl_easy_setopt(easy_handle, CURLOPT_URL, url.c_str());
curl_easy_setopt(easy_handle, CURLOPT_WRITEFUNCTION, &Request::process_data);
curl_easy_setopt(easy_handle, CURLOPT_WRITEDATA, &json);
```



### 9-连接超时

```cpp
curl_easy_setopt(conn, CURLOPT_CONNECTTIMEOUT, 3);	//连接超时
```



### 10-异步请求





### 11-读取数据超时

```cpp
// RPC 调用,10s超时时间
curl_easy_setopt(conn, CURLOPT_TIMEOUT, 10);		// 接收数据超时
```



### 12-设置代理

```cpp
curl_easy_setopt(conn, CURLOPT_PROXY, proxyAddr.c_str());//http://127.0.0.1:80
curl_easy_setopt(conn, CURLOPT_PROXYTYPE, CURLPROXY_HTTP);// 设置代理类型为http
curl_easy_setopt(conn, CURLOPT_HTTPPROXYTUNNEL, 1L);//隧道转发流量
```



### 13-使用Cookie

```cpp
curl_easy_setopt(curl, CURLOPT_COOKIEFILE, "/tmp/cookie.txt"); // 指定cookie文件
```



### 14-302重定向

```cpp
curl_easy_setopt(curl, CURLOPT_AUTOREFERER, 1); // 设置referrer 信息
curl_easy_setopt(curl, CURLOPT_FOLLOWLOCATION, 1);
curl_easy_setopt(curl, CURLOPT_MAXREDIRS, 1);// 设置最大重定向次数
```



### 15-注意事项

> 调用任意函数前，先调用`curl_global_init`,该函数只能调用一次且非线程安全。



### 16-API

***

```cpp
curl_global_init()		//初始化libcurl,只能调用一次
curl_easy_init()		// 创建easy interface型指针
curl_easy_setopt()		//设置传输选项
curl_easy_perform()		// 发起http请求
curl_easy_getinfo()
curl_easy_cleanup()		//释放内存
curl_global_cleanup()	//清理libcurl
```



### 17-打印函数调用的错误信息

***

```cpp
char errorBuffer[CURL_ERROR_SIZE];
CURLcode code = curl_easy_setopt(conn, CURLOPT_ERRORBUFFER, errorBuffer);
```

### 18-内存泄漏处理

```cpp
// 单线程可以用这种方式,多线程有问题

curl_global_init()
curl_easy_init()
// 设置选项 发起HTTP请求
curl_easy_cleanup()
curl_global_cleanup()
```

### 19-选项

***

```cpp
CURLOPT_VERBOSE // 打印调试信息
CURLOPT_RESUME_FROM_LARGE // 断点续传 -- 之前上/下载中断,可以从中断的地方继续上/下载

```

### 20-下载进度

```CPP
curl_easy_setopt(curl, CURLOPT_NOPROGRESS, 0L);// 开启下载进度功能
curl_easy_setopt(curl, CURLOPT_PROGRESSFUNCTION, my_progress_func); // 回调
curl_easy_setopt(curl, CURLOPT_PROGRESSDATA, Bar); // 传给回调的参数
```

### 21-异步http请求的代码

```cpp

#include <stdio.h>
#include <string.h>
#include <thread>
#include <mutex>
#include <vector>
#include<string>
#include <iostream>
#include <functional>
#include <map>

/* somewhat unix-specific */

/* curl stuff */
#include <curl/curl.h>

/*
* Download a HTTP file and upload an FTP file simultaneously.
*/

using namespace std;
struct HttpParam
{
	CURL* handler;
	string response;
	vector<string> headers;
	int statusCode;
	function<void(const string& resBody, const vector<string>& resHeaders, int statusCode)> cb;
};

std::map<CURL*, HttpParam> g_handlers;
std::mutex mtx;




// 主线程调用此函数
void add_handler(const HttpParam& handler){
	mtx.lock();
	g_handlers.insert(make_pair(handler.handler, handler));
	mtx.unlock();
}

// 工作线程调用此函数
void add_handler(std::map<CURL*, HttpParam>& all_handlers, CURLM *multi_handle) {
	mtx.lock();
	for (auto& handler : g_handlers){
		curl_multi_add_handle(multi_handle, handler.first);
		all_handlers.insert(handler);
	}
	g_handlers.clear();
	mtx.unlock();
}


std::map<CURL*, HttpParam> all_handlers; // 仅仅在HttpLoop线程里面访问,不用加锁==可以用对象包起来
void httpLoop()
{
	/* we start some action by calling perform right away */
	int still_running = 0;
	CURLM* multi_handle = curl_multi_init();
	curl_multi_perform(multi_handle, &still_running);
	//while (still_running) {
	while (true) {
		struct timeval timeout;
		int rc; /* select() return code */
		CURLMcode mc; /* curl_multi_fdset() return code */

		fd_set fdread;
		fd_set fdwrite;
		fd_set fdexcep;
		int maxfd = -1;

		long curl_timeo = -1;

		FD_ZERO(&fdread);
		FD_ZERO(&fdwrite);
		FD_ZERO(&fdexcep);

		/* set a suitable timeout to play around with */
		timeout.tv_sec = 1;
		timeout.tv_usec = 0;

		curl_multi_timeout(multi_handle, &curl_timeo);
		if (curl_timeo >= 0) {
			timeout.tv_sec = curl_timeo / 1000;
			if (timeout.tv_sec > 1)
				timeout.tv_sec = 1;
			else
				timeout.tv_usec = (curl_timeo % 1000) * 1000;
		}

		/* get file descriptors from the transfers */
		mc = curl_multi_fdset(multi_handle, &fdread, &fdwrite, &fdexcep, &maxfd);

		if (mc != CURLM_OK) {
			fprintf(stderr, "curl_multi_fdset() failed, code %d.\n", mc);
			break;
		}

		/* On success the value of maxfd is guaranteed to be >= -1. We call
		select(maxfd + 1, ...); specially in case of (maxfd == -1) there are
		no fds ready yet so we call select(0, ...) --or Sleep() on Windows--
		to sleep 100ms, which is the minimum suggested value in the
		curl_multi_fdset() doc. */

		if (maxfd == -1) {
#ifdef _WIN32
			Sleep(100);
			rc = 0;
#else
			/* Portable sleep for platforms other than Windows. */
			struct timeval wait = { 0, 100 * 1000 }; /* 100ms */
			rc = select(0, NULL, NULL, NULL, &wait);
#endif
		}
		else {
			/* Note that on some platforms 'timeout' may be modified by select().
			If you need access to the original value save a copy beforehand. */
			rc = select(maxfd + 1, &fdread, &fdwrite, &fdexcep, &timeout);
		}

		switch (rc) {
		case -1:
			/* select error */
			break;
		case 0: /* timeout */
		default: /* action */
			add_handler(all_handlers, multi_handle); // 加入g_handlers里面的请求,并保存到all_handlers里面
			curl_multi_perform(multi_handle, &still_running);
			//cout << "still_running : " << still_running << endl;
			// 执行回调函数 == TODO 从这里开始写起
			int msgs_left = -1;
			CURLMsg* msg = nullptr;
			while ((msg = curl_multi_info_read(multi_handle, &msgs_left))) {
				if (msg->msg == CURLMSG_DONE) {
					CURL * finish_handler = msg->easy_handle;
					if (msg->data.result != CURLE_OK)
					{
						cout << "result Code :" << msg->data.result << endl;
						curl_easy_cleanup(finish_handler);
						continue;
					}
					long statusCode = -1;
					CURLcode code = curl_easy_getinfo(finish_handler, CURLINFO_RESPONSE_CODE, &statusCode);
					cout << "statusCode : " << statusCode << endl;
					if (statusCode == 200)
					{
						mtx.lock();
						auto it = all_handlers.find(finish_handler);
						if (it != all_handlers.end()) {
							HttpParam& httpParam = it->second;
							httpParam.statusCode = statusCode;
							httpParam.cb(httpParam.response, httpParam.headers, httpParam.statusCode);
							all_handlers.erase(it);
						}
						curl_multi_remove_handle(multi_handle, finish_handler);
						mtx.unlock();
						curl_easy_cleanup(finish_handler);
					}
				}
				break;
			}
		}
	}
}

static size_t  read_body(void *buffer, size_t size, size_t nmemb, void *param)
{
	CURL* handler = (CURL*)param;
	auto it = all_handlers.find(handler);
	if (it != all_handlers.end()){
		HttpParam& info = it->second;
		info.response.assign((const char*)buffer, (const char*)buffer + size * nmemb);
	}
	return size * nmemb;
}

static size_t  read_headers(void *buffer, size_t size, size_t nmemb, void *param)
{
	CURL* handler = (CURL*)param;
	auto it = all_handlers.find(handler);
	if (it != all_handlers.end()) {
		HttpParam& info = it->second;
		string header((const char*)buffer, (const char*)buffer + size * nmemb);
		info.headers.push_back(header);
	}
	return size * nmemb;
}


int succ_cnt = 0;
int main(void)
{
	
	std::thread t1(httpLoop);
	while (true)
	{
		// USAGE : 调用add_handler 添加请求即可
		for (auto i = 0; i < 1000; ++i){
			CURL* handler = curl_easy_init();
			curl_easy_setopt(handler, CURLOPT_URL, "http://10.10.10.23:8081");
			curl_easy_setopt(handler, CURLOPT_WRITEFUNCTION, read_body);
			curl_easy_setopt(handler, CURLOPT_WRITEDATA, handler);
			curl_easy_setopt(handler, CURLOPT_HEADERFUNCTION, read_headers);
			curl_easy_setopt(handler, CURLOPT_HEADERDATA, handler);
			curl_easy_setopt(handler, CURLOPT_CONNECTTIMEOUT, 3);
			curl_easy_setopt(handler, CURLOPT_TIMEOUT, 10);

			//curl_easy_setopt(handler, CURLOPT_PROXY, "127.0.0.1:8090");//http://127.0.0.1:80
			//curl_easy_setopt(handler, CURLOPT_PROXYTYPE, CURLPROXY_HTTP);// 设置代理类型为http
			//curl_easy_setopt(handler, CURLOPT_HTTPPROXYTUNNEL, 1L);//隧道转发流量
			//curl_easy_setopt(handler, CURLOPT_FOLLOWLOCATION, 1);

			HttpParam param;
			param.handler = handler;
			param.cb = [](const string& resBody, const vector<string>& resHeaders, int statusCode)->void{
				succ_cnt += 1;
				cout << "succ_cnt : " << succ_cnt << endl;
				cout << resBody << endl;
				cout << "======================" << endl << endl;
			};
			add_handler(param);
		}
		Sleep(10000);
	}
	return 0;
}

```






# libcurl Linux编译

1. 创建目录

   ```shell
   mkdir /usr/local/curl
   ```

2. 安装openssl开发库

   ```shell
   yum -y install openssl-devel 
   ```

3. 编译
   
   ```shell
   # 配置安装目录
   ./configure --prefix=/usr/local/curl/
   
   make -j4
   make install
   ```
   
4. 注意
   
   > 系统里可能以及存在libcurl的动态链接库，如果存在需要先删除
   >
   > ```shell
   > # 查找libcurl的动态链接库
   > find / -name "libcurl*"
   > 
   > # 删除libcurl的动态链接库和对应的软连接
   > 
   > ```
   
5. 使用

   > 编译的时候加上选项 -I/usr/local/curl/include  -L/usr/local/curl/lib  -lcurl

   

# Windows编译

> 1. 下载源码
>
> ```shell
> wget https://curl.haxx.se/download/curl-7.67.0.tar.gz
> ```
>
> 2. 编译
>
> ```shell
> #用vs2017命令提示工具进入目录curl-7.67.0\winbuild
> E:
> cd E:\curl-7.67.0
> # 静态库 debug版本
> nmake /f Makefile.vc mode=static DEBUG=yes
> 
> # 动态库dll版本
> nmake /f Makefile.vc mode=dll DEBUG=yes
> 
> # 文件生成在目录curl-7.67.0\builds\libcurl-vc-x86-release-static-ipv6-sspi-winssl
> ```
>
> 3. 项目配置
>
>    + 设置附加包含目录
>
> ```shell
> ../../include
> ```
>
>    + 设置附加库目录
>
> ```shell
> ../../lib
> ```
>
>    + 设置附加依赖项
>
> ```shell
> Normaliz.lib;Crypt32.lib;winmm.lib;wldap32.lib;ws2_32.lib;libcurl_a_debug.lib;
> ```
>
>    + 添加预处理器定义
>
> ```shell
> #用静态库需要此宏定义,动态库不需要
> CURL_STATICLIB
> ```

