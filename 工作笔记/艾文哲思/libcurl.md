# libcurl的使用

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
>
> 4. 示例代码
>
>    + 将接收到的数据保存到本地
>
>   ```cpp
>   #include "curl/curl.h"
>   #include <stdio.h>
>   #include <iostream>
>   using namespace std;
>   /**
>       *	@brief libcurl接收到数据时的回调函数
>    *
>       *	将接收到的数据保存到本地文件中，同时显示在控制台上。
>    *
>       *	@param [in] buffer 接收到的数据所在缓冲区
>       *	@param [in] size 数据长度
>       *	@param [in] nmemb 数据片数量
>       *	@param [in/out] 用户自定义指针
>       *	@return 获取的数据长度
>    */
>   
>   size_t process_data(void *buffer, size_t size, size_t nmemb, void *user_p)
>   {
>   	FILE *fp = (FILE *)user_p;
>   	size_t return_size = fwrite(buffer, size, nmemb, fp);
>   	cout << (char *)buffer << endl;
>   	return return_size;
>   }
>   
>   int main(int argc, char **argv)
>   {
>   	// 初始化libcurl
>   	CURLcode return_code;
>   	return_code = curl_global_init(CURL_GLOBAL_WIN32);
>   	if (CURLE_OK != return_code)
>   	{
>   		cerr << "init libcurl failed." << endl;
>   		return -1;
>   	}
>   
>   	// 获取easy handle
>   	CURL *easy_handle = curl_easy_init();
>   	if (NULL == easy_handle)
>   	{
>   		cerr << "get a easy handle failed." << endl;
>   		curl_global_cleanup();
>   		return -1;
>   	}
>   
>   	FILE *fp = fopen("data.html", "ab+");	// 
>   	// 设置easy handle属性
>   	curl_easy_setopt(easy_handle, CURLOPT_URL, "https://www.baidu.com");
>   	curl_easy_setopt(easy_handle, CURLOPT_WRITEFUNCTION, &process_data);
>   	curl_easy_setopt(easy_handle, CURLOPT_WRITEDATA, fp);
>   
>   	// 执行数据请求
>   	curl_easy_perform(easy_handle);
>   	// 释放资源
>   
>   	cout << "============" << endl;
>   	fclose(fp);
>   	curl_easy_cleanup(easy_handle);
>   	curl_global_cleanup();
>   
>   	return 0;
>   }
>   ```
>
>   
>
>    + 基本使用
>
>   ```cpp
>   #include <stdio.h>
>   #include <curl/curl.h>
>   
>   int main(void)
>   {
>   	CURL *curl;
>   	CURLcode res;
>   
>   	curl_global_init(CURL_GLOBAL_DEFAULT);
>   
>   	curl = curl_easy_init();
>   	if (curl) {
>   		curl_easy_setopt(curl, CURLOPT_URL, "http://127.0.0.1:8000/a.html");
>   
>   #ifdef SKIP_PEER_VERIFICATION
>   		/*
>         		 * If you want to connect to a site who isn't using a certificate that is
>         		 * signed by one of the certs in the CA bundle you have, you can skip the
>         		 * verification of the server's certificate. This makes the connection
>         		 * A LOT LESS SECURE.
>   		 *
>         		 * If you have a CA cert for the server stored someplace else than in the
>         		 * default bundle, then the CURLOPT_CAPATH option might come handy for
>         		 * you.
>   		 */
>   		curl_easy_setopt(curl, CURLOPT_SSL_VERIFYPEER, 0L);
>   #endif
>   
>   #ifdef SKIP_HOSTNAME_VERIFICATION
>   		/*
>         		 * If the site you're connecting to uses a different host name that what
>         		 * they have mentioned in their server certificate's commonName (or
>         		 * subjectAltName) fields, libcurl will refuse to connect. You can skip
>         		 * this check, but this will make the connection less secure.
>   		 */
>   		curl_easy_setopt(curl, CURLOPT_SSL_VERIFYHOST, 0L);
>   #endif
>   
>   		/* Perform the request, res will get the return code */
>   		res = curl_easy_perform(curl);
>   		/* Check for errors */
>   		if (res != CURLE_OK)
>   			fprintf(stderr, "curl_easy_perform() failed: %s\n",
>   				curl_easy_strerror(res));
>   
>   		/* always cleanup */
>   		curl_easy_cleanup(curl);
>   	}
>   
>   	curl_global_cleanup();
>   
>   	return 0;
>   }
>   ```
>

> + 代码
>
>   ```c++
>   // GET 请求获取响应
>   #include <stdio.h>
>   #include <curl/curl.h>
>   #include <string>
>   #include <iostream>
>   using namespace std;
>   
>   using uint = unsigned int;
>   
>   /* curl write callback, to fill tidy's input buffer...  */
>   // 注意:返回值必须是body长度
>   uint write_cb(char *in, uint size, uint nmemb, void *out)
>   {
>   	uint r;
>   	r = size * nmemb;
>   	string buf(in, in + size * nmemb);
>   	cout << "response : " << buf << endl;
>   	return r;
>   }
>   
>   
>   int main(int argc, char **argv)
>   {
>   	CURL *curl;
>   	char curl_errbuf[CURL_ERROR_SIZE];
>   	int err;
>   
>   	curl = curl_easy_init();
>   	curl_easy_setopt(curl, CURLOPT_URL, "http://10.10.10.188:8080/reference/HelloWorld.html");
>   	curl_easy_setopt(curl, CURLOPT_ERRORBUFFER, curl_errbuf);
>   	curl_easy_setopt(curl, CURLOPT_NOPROGRESS, 0L);
>   	curl_easy_setopt(curl, CURLOPT_VERBOSE, 1L);
>   	curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, write_cb);
>   	curl_easy_setopt(curl, CURLOPT_WRITEDATA, nullptr);
>   	err = curl_easy_perform(curl);
>   	if (!err) {
>   		cout << "GET req success!" << endl;
>   	}
>   	else
>   		fprintf(stderr, "%s\n", curl_errbuf);
>   
>   	/* clean-up */
>   	curl_easy_cleanup(curl);
>   	return err;
>   
>   	return 0;
>   }
>   ```
>
>   ```c++
>   // 常见选项的设置
>   static bool init(CURL *&conn, char *url)
>   {
>   	CURLcode code;
>   
>   	conn = curl_easy_init();
>   
>   	if (conn == NULL) {
>   		fprintf(stderr, "Failed to create CURL connection\n");
>   		exit(EXIT_FAILURE);
>   	}
>   
>   	code = curl_easy_setopt(conn, CURLOPT_ERRORBUFFER, errorBuffer);
>   	if (code != CURLE_OK) {
>   		fprintf(stderr, "Failed to set error buffer [%d]\n", code);
>   		return false;
>   	}
>   
>   	code = curl_easy_setopt(conn, CURLOPT_URL, url);
>   	if (code != CURLE_OK) {
>   		fprintf(stderr, "Failed to set URL [%s]\n", errorBuffer);
>   		return false;
>   	}
>   
>   	code = curl_easy_setopt(conn, CURLOPT_FOLLOWLOCATION, 1L); // 跟踪爬取重定向的页面
>   	if (code != CURLE_OK) {
>   		fprintf(stderr, "Failed to set redirect option [%s]\n", errorBuffer);
>   		return false;
>   	}
>   
>   	code = curl_easy_setopt(conn, CURLOPT_WRITEFUNCTION, writer);
>   	if (code != CURLE_OK) {
>   		fprintf(stderr, "Failed to set writer [%s]\n", errorBuffer);
>   		return false;
>   	}
>   
>   	code = curl_easy_setopt(conn, CURLOPT_WRITEDATA, &buffer);
>   	if (code != CURLE_OK) {
>   		fprintf(stderr, "Failed to set write data [%s]\n", errorBuffer);
>   		return false;
>   	}
>   
>   	return true;
>   }
>   ```
>
>   ```cpp
>   // POST 请求;编码方式 urlencode
>   #include <stdio.h>
>   #include <curl/curl.h>
>   
>   int main(void)
>   {
>   	CURL *curl;
>   	CURLcode res;
>   
>   	/* In windows, this will init the winsock stuff */
>   	curl_global_init(CURL_GLOBAL_ALL);
>   
>   	/* get a curl handle */
>   	curl = curl_easy_init();
>   	if (curl) {
>   		/* First set the URL that is about to receive our POST. This URL can
>   		just as well be a https:// URL if that is what should receive the
>   		data. */
>   		curl_easy_setopt(curl, CURLOPT_URL, "http://10.10.10.188:8090/cplusplus.com/reference/");
>   		/* Now specify the POST data */
>   		curl_easy_setopt(curl, CURLOPT_POSTFIELDS, "name=daniel&project=curl");
>   
>   		/* Perform the request, res will get the return code */
>   		res = curl_easy_perform(curl);
>   		/* Check for errors */
>   		if (res != CURLE_OK)
>   			fprintf(stderr, "curl_easy_perform() failed: %s\n",
>   				curl_easy_strerror(res));
>   
>   		/* always cleanup */
>   		curl_easy_cleanup(curl);
>   	}
>   	curl_global_cleanup();
>   	return 0;
>   }
>   ```

