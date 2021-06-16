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

unsigned short PORT = 5670;
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
	for (;;) {
		client = accept(server, (SOCKADDR*)&clientAddr, &szClntAddr);
		if (client == INVALID_SOCKET) {
			printf("accept error! \n");
			return -5;
		}

		char message[1024] = { 0 };
		
		//recv 成功返回收到的字节数 0表示对方关闭了socket <0 出错
		int strLen = recv(client, message, sizeof(message) - 1, 0);
		if (strLen < 0) {
			printf("recv error! \n");
			return -3;
		}
		// send 成功返回发送的字节数 失败返回-1
		//strLen = send(client, message, strlen(message), 0);
		//if (strLen < 0) {
		//	printf("send error! \n");
		//	return -3;
		//}
		// closesocket(client);

		/// 从关闭的socket 接受消息返回-1
		//strLen = recv(client, message, sizeof(message) - 1, 0);
		//if (strLen < 0) {
		//	DWORD dwError = WSAGetLastError();
		//	printf("recv error! \n");
		//	return -3;
		//}

		message[0] = 'H';
		message[1] = 'e';
		message[2] = '\0';
		/// TIPS: 向自己关闭的socket 写数据返回-1
		/// TIPS: socket 未关闭,但是对端已经关闭,第一次写入正常
		strLen = send(client, message, strlen(message), 0);
		if (strLen < 0) {
			printf("send error! \n");
			return -3;
		}

		/// 第二次向对端已经关闭的socket写数据, 触发SIGPIPE信号,写数据返回-1
		strLen = send(client, message, strlen(message), 0);
		if (strLen < 0) {
			printf("2---send error! \n");
			//return -3;
		}
	}
#ifdef WIN32
	WSACleanup();
#endif
	return 0;
}
```



## 1.2 UDP







# 第二章 http

