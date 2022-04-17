# 第一章 网络编程



## 1.1 TCP



### 1.1.1 客户端

***

```c++
#include<stdio.h>
#include <stdlib.h>
#include <WinSock2.h>

#pragma comment(lib, "ws2_32.lib")
const char* IP = "172.18.80.183";
unsigned short PORT = 5670;
int main(int argc, char* argv[])
{
	int szClntAddr = 0;
	WSADATA wsaData;
	int ret = WSAStartup(MAKEWORD(2, 2), &wsaData);
	if (ret != 0) {
		printf("WSAStartup error! \n");
		return -1;
	}

	SOCKET client;
	client = socket(PF_INET, SOCK_STREAM, 0);
	if (client == INVALID_SOCKET){
		printf("socket error! \n");
		return -2;
	}

	SOCKADDR_IN serverAddr;
	memset(&serverAddr, 0, sizeof(serverAddr));
	serverAddr.sin_family = AF_INET;
	serverAddr.sin_addr.s_addr = inet_addr(IP);
	serverAddr.sin_port = htons(PORT);

	ret = connect(client, (SOCKADDR*)&serverAddr, sizeof(serverAddr));
	if (ret == SOCKET_ERROR){
		printf("connect error! \n");
		return -3;
	}

	{
		// 发送数据
		char buf[] = "Hello World!";
		// 返回值 >0		表示发送的字节数
		// 返回值 =-1	表示出错
		// 如果对端已经关闭,而本端未关闭,连续两次send 会触发信号SIGPIPE
		int strLen = send(client, buf, sizeof(buf) - 1, 0);
		if (strLen == -1) {
			printf("recv error! \n");
			return -3;
		}
	}
	char message[1024] = { 0 };
	// 返回值 >0		表示收到的字节数
	// 返回值 =0		表示对端关闭
	// 返回值 =-1	表示出错
	int strLen = recv(client, message, sizeof(message) - 1, 0);
	if (strLen == -1){
		printf("recv error! \n");
		return -3;
	}

	closesocket(client);
	WSACleanup();
	return 0;
}
```





### 1.1.2 服务器

***

```cpp
#include<stdio.h>
#include <stdlib.h>
#include <string.h>
#include<errno.h>
#include <unistd.h>
#ifdef WIN32
	#include <WinSock2.h>
	#pragma comment(lib, "ws2_32.lib")
#else
	#include<unistd.h>
	#include<arpa/inet.h>
	#include<sys/socket.h>
	#include <signal.h>
#endif // WIN32


#ifndef WIN32
typedef int SOCKET;
#define closesocket close
#define INVALID_SOCKET -1
#define SOCKET_ERROR -1
#define SOCKADDR sockaddr
#define SOCKADDR_IN sockaddr_in
#endif

unsigned short PORT = 5671;
int main(int argc, char* argv[])
{
	int szClntAddr = 0;
	int ret;
#ifdef WIN32
	WSADATA wsaData;
	ret = WSAStartup(MAKEWORD(2, 2), &wsaData);
	if (ret != 0) {
		printf("WSAStartup error! \n");
		return -1;
	}
#else
	// client 主动close时,server 第一次调用read,返回0,表示对端关闭
	// server 第一次对其调用write方法时, 如果发送缓冲没问题, 会返回正确写入(发送). 
	// 但发送的报文会导致对端发送RST报文, 因为对端的socket已经调用了close, 完全关闭, 
	// 既不发送, 也不接收数据. 所以, 第二次调用write方法(假设在收到RST之后), 
	// 会生成SIGPIPE信号, 导致进程退出
    
    // 底层socket已经关闭，但是上层未主动调用close，然后连续调用两次write/send，第二次就会宕机。比如server先sleep(60s),此时client调用close，然后
    // server两次write
	if (signal(SIGPIPE, SIG_IGN) == SIG_ERR)
		return 1;
#endif

	SOCKET client;
	SOCKET server;
	server = socket(PF_INET, SOCK_STREAM, 0);
	if (server == INVALID_SOCKET) {
		printf("socket error! \n");
		return -2;
	}

	SOCKADDR_IN serverAddr;
	SOCKADDR_IN clientAddr;
	memset(&serverAddr, 0, sizeof(serverAddr));
	serverAddr.sin_family = AF_INET;
	serverAddr.sin_addr.s_addr = htonl(INADDR_ANY);
	serverAddr.sin_port = htons(PORT);
	
	int optval = 1;
        setsockopt(server, SOL_SOCKET, SO_REUSEADDR, &optval, sizeof(optval));

	ret = bind(server, (SOCKADDR*)&serverAddr, sizeof(serverAddr));
	if (ret == SOCKET_ERROR) {
		printf("connect error! \n");
		return -3;
	}

	ret = listen(server, 5);
	if (ret == SOCKET_ERROR){
		printf("listen error! \n");
		return -4;
	}

	szClntAddr = sizeof(clientAddr);
	int connect_count = 0;
	for (;;) {
		client = accept(server, (SOCKADDR*)&clientAddr, (socklen_t*)&szClntAddr);
		if (client == INVALID_SOCKET) {
			printf("accept error!, msg : %s \n", strerror(errno));
			sleep(10);
			continue;
		}
		connect_count += 1;
		printf("当前链接数:%d \n", connect_count);

	}
#ifdef WIN32
	WSACleanup();
#endif
	return 0;
}
```



## 1.2 UDP







# 第二章 http

