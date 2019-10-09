# 1 C++ 服务端

实现回声服务器



## 1-1 定义接口

```c++
module TestApp
{

interface Hello
{
    int test();
    int testHello(string sReq, out string sRsp);
};

}; 
```

## 1-2 编译接口文件

```
/usr/local/tars/cpp/tools/tars2cpp hello.tars
```



## 1-3 实现接口





## 1-4 ServerConfig

服务框架中有全局的结构ServerConfig，它记录了服务的基本信息。

ServerConfig的成员变量都是静态的，在服务框架初始化时会自动从服务配置文件中初始化这些参数。

```C++
/**
 * 服务基本信息
 */
struct ServerConfig
{
    static std::string Application;         //应用名称
    static std::string ServerName;          //服务名称,一个服务名称含一个或多个服务标识
    static std::string BasePath;            //应用程序路径，用于保存远程系统配置的本地目录
    static std::string DataPath;            //应用程序数据路径用于保存普通数据文件
    static std::string LocalIp;             //本机IP
    static std::string LogPath;             //log路径
    static int         LogSize;             //log大小(字节)
    static int         LogNum;              //log个数()
    static std::string LogLevel;            //log日志级别
    static std::string Local;               //本地套接字
    static std::string Node;                //本机node地址
    static std::string Log;                 //日志中心地址
    static std::string Config;              //配置中心地址
    static std::string Notify;              //信息通知中心
    static std::string ConfigFile;          //框架配置文件路径
    static int         ReportFlow;          //是否服务端上报所有接口stat流量 0不上报 1上报(用于非tars协议服务流量统计)
    static int         IsCheckSet;          //是否对按照set规则调用进行合法性检查 0,不检查，1检查
    static bool        OpenCoroutine;        //是否启用协程处理方式
    static size_t      CoroutineMemSize;    //协程占用内存空间的最大大小
    static uint32_t    CoroutineStackSize;    //每个协程的栈大小(默认128k)
};
```



## 1-5 服务启动

```shell
# 就服务而言，可以单独运行，不需要发布到TARS系统框架上
HelloServer --config=config.conf
```



配置文件

```xml
<tars>
	<application>
		enableset=n
		setdivision=NULL
		<server>
			node=tars.tarsnode.ServerObj@tcp -h 10.10.10.168 -p 19386 -t 60000 <!-- [可选]NODE地址,定时给其发心跳,发布到框架才需要此参数 -->
            app=XGame   <!-- 应用名 -->
			server=FriendsServer   <!-- 服务名 -->
			localip=10.10.10.168   <!-- 本机非127.0.0.1的第一块网卡IP -->
			local=tcp -h 127.0.0.1 -p 10009 -t 3000 <!-- 管理端口,web后台通过此端口给服务发送名 -->
			basepath=/usr/local/app/tars/tarsnode/data/XGame.FriendsServer/bin/ <!-- 可执行文件路径 -->
			datapath=/usr/local/app/tars/tarsnode/data/XGame.FriendsServer/data/ <!-- 数据文件路径 -->
			logpath=/usr/local/app/tars/app_log/  <!-- 日志文件路径 -->
			logsize=10M  <!-- 滚动日志文件大小 -->
			config=tars.tarsconfig.ConfigObj   <!-- [可选]addConfig函数从远程拉取配置 -->
			notify=tars.tarsnotify.NotifyObj        <!-- [可选]信息上报中心地址 -->
			log=tars.tarslog.LogObj  <!-- [可选]记录远程日志 -->
			deactivating-timeout=3000
			logLevel=DEBUG   <!-- 滚动log日志级别 -->
            
            
            <!-- 在服务配置文件中增加adapter项，即可以完成TARS增加一个Servant处理对象 -->
			<XGame.FriendsServer.FriendsServantObjAdapter>
				allow
				endpoint=tcp -h 10.10.10.168 -p 10009 -t 60000   <!-- 监听IP地址 -->
				handlegroup=XGame.FriendsServer.FriendsServantObjAdapter <!-- 处理组 -->
				maxconns=200000  <!-- 最大连接数 -->
				protocol=tars     <!-- 协议 -->
				queuecap=10000   <!-- 队列大小 -->
				queuetimeout=6000000 <!-- 队列超时时间 毫秒 -->
				servant=XGame.FriendsServer.FriendsServantObj <!-- 处理对象 -->
				threads=1  <!-- 线程数 -->
			</XGame.FriendsServer.FriendsServantObjAdapter>
		</server>
		<client>
			locator=tars.tarsregistry.QueryObj@tcp -h 10.10.10.168 -p 17890 <!-- 主控地址 -->
			sync-invoke-timeout=3000 <!-- 同步超时时间 -->
			async-invoke-timeout=5000 <!-- 异步超时时间 -->
			refresh-endpoint-interval=60000  <!-- 刷新ip列表的时间间隔 -->
			stat=tars.tarsstat.StatObj
			property=tars.tarsproperty.PropertyObj
			report-interval=60000 <!-- 上报数据的时间间隔 -->
			sample-rate=100000  <!-- 采样率 -->
			max-sample-count=50 <!-- 最大采样数 -->
			asyncthread=3 <!-- 异步线程数 -->
			modulename=XGame.FriendsServer <!-- 模块名 -->
		</client>
	</application>
</tars>

```



# 2 C++ 客户端

## 2-1 通信器

+ 初始化

  1. 用配置文件初始化

     ```c++
     TC_Config conf("config.conf");
     CommunicatorPtr c = new Communicator();
     c-> setProperty(conf);
     ```

  2. 用属性初始化

     ```c++
     CommunicatorPtr c = new Communicator();
     c->setProperty("property", "tars.tarsproperty.PropertyObj");
     c->setProperty("locator", "tars.tarsregistry.QueryObj@tcp -h ... -p ...");
     ```

     

+ 使用要点

  > 1. 用Tars框架做服务端使用，通信器创建方式如下
  >
  >    ```c++
  >    Application::getCommunicator()->stringToProxy<dataproxy::DataProxyServantPrx>(_DataProxyServantObj);
  >    ```
  >
  > 2. 纯客户端，通信器创建方式如下
  >
  >    ```c++
  >    Communicator comm;
  >    ```
  >
  > 3. 对于通信器创建出来的代理，初始化时建立好，后面直接使用就可以了
  >
  > 4. 获取代理对应ip列表
  >
  >    ```c++
  >    // 方法一
  >    Application::getCommunicator()->getEndpoint（”obj”）
  >    
  >    //方法二
  >    Application::getCommunicator()->stringToProxy(…) ->getEndpoint()
  >    ```

+ 属性介绍

  > - locator: registry服务的地址，必须是有ip port的，如果不需要registry来定位服务，则不需要配置；
  > - sync-invoke-timeout：调用最大超时时间（同步），毫秒，没有配置缺省为3000
  > - async-invoke-timeout：调用最大超时时间（异步），毫秒，没有配置缺省为5000
  > - refresh-endpoint-interval：定时去registry刷新配置的时间间隔，毫秒，没有配置缺省为1分钟
  > - stat：模块间调用服务的地址，如果没有配置，则上报的数据直接丢弃；
  > - property：属性上报地址，如果没有配置，则上报的数据直接丢弃；
  > - report-interval：上报给stat/property的时间间隔，默认为60000毫秒；
  > - asyncthread：异步调用时，回调线程的个数，默认为1；
  > - modulename：模块名称，默认为可执行程序名称；

+ 配置文件格式

  ```xml
  <tars>
    <application>
      #proxy需要的配置
      <client>
          #地址
          locator                     = tars.tarsregistry.QueryObj@tcp -h 127.0.0.1 -p 17890
          #同步最大超时时间(毫秒)
          sync-invoke-timeout         = 3000
          #异步最大超时时间(毫秒)
          async-invoke-timeout        = 5000
          #刷新端口时间间隔(毫秒)
          refresh-endpoint-interval   = 60000
          #模块间调用
          stat                        = tars.tarsstat.StatObj
          #属性上报地址
          property                    = tars.tarsproperty.PropertyObj
          #report time interval
          report-interval             = 60000
          #网络异步回调线程个数
          asyncthread                 = 3
          #模块名称
          modulename                  = Test.HelloServer
      </client>
    </application>
  </tars>
  ```

  

## 2-2 超时控制

+ 配置文件中设置，对所有proxy设置超时

  ```shell
  #同步最大超时时间(毫秒)
  sync-invoke-timeout          = 3000
  #异步最大超时时间(毫秒)
  async-invoke-timeout         = 5000
  ```

+ 对指定proxy设置超时

  ```c++
  ProxyPrx  pproxy;
  //设置该代理的同步的调用超时时间 单位毫秒
  pproxy->tars_timeout(3000);
  //设置该代理的异步的调用超时时间 单位毫秒
  pproxy->tars_async_timeout(4000);
  ```

+ 对指定接口设置超时

  ```c++
  //设置该代理的本次接口调用的超时时间.单位是毫秒，设置单次有效
  pproxy->tars_set_timeout(2000)->a(); 
  ```

  

## 2-3 调用

### 寻址方式

***

+ 服务器在主控注册：通过服务名寻址，在生成通信器时指定registry（主控）的地址

  ```c++
  // 指定两个主控,用于容错
  CommunicatorPtr c = new Communicator();
  c->setProperty("locator", "tars.tarsregistry.QueryObj@tcp -h .. -p ..")
  ```

  

+ 服务名不在主控注册：在服务的obj后面指定要访问的ip地址，直接寻址

  ```c++
  HelloPrx pPrx = c->stringToProxy<HelloPrx>("Test.HelloServer.HelloObj@tcp -h 127.0.0.1 -p 9985:tcp -h 192.168.1.1 -p 9983");
  ```

### 调用方式

***

1. 单向调用：只发数据，不接受响应，也不管服务器是否收到数据

   ```c++
   int main(int argc,char ** argv)
   {
       Communicator comm;
   
       HelloServantPrx prx;
       comm.stringToProxy("Test.HelloServer.HelloServantObj@tcp -h 10.10.10.168 -p 10016" , prx);
   
       HelloServantPrxCallbackPtr cb = new HelloCallback();
       string sReq("hello world");
       string sRsp("");
       prx->async_testHello(NULL, sReq);  // 重点关注这行
   
       getchar();
   
       return 0;
   }
   ```

   

2. 同步调用

   ```c++
   int main(int argc, char ** argv)
   {
       Communicator comm;
   
   
       HelloServantPrx prx;
       comm.stringToProxy("Test.HelloServer.HelloServantObj@tcp -h 10.10.10.168 -p 10016", prx);
   
   
       HelloServantPrxCallbackPtr cb = new HelloCallback();
       string sReq("hello world");
       string sRsp("");
   
       int ret = prx->testHello(sReq, sRsp);
   
       std::cout << "ret : " << ret << ", resp : " << sRsp << endl;
       getchar();
   
   
       return 0;
   }
   ```

   错误码

   ```
   const int TARSSERVERSUCCESS       = 0;       //服务器端处理成功
   const int TARSSERVERDECODEERR     = -1;      //服务器端解码异常
   const int TARSSERVERENCODEERR     = -2;      //服务器端编码异常
   const int TARSSERVERNOFUNCERR     = -3;      //服务器端没有该函数
   const int TARSSERVERNOSERVANTERR  = -4;      //服务器端没有该Servant对象
   const int TARSSERVERRESETGRID     = -5;      //服务器端灰度状态不一致
   const int TARSSERVERQUEUETIMEOUT  = -6;      //服务器队列超过限制
   const int TARSASYNCCALLTIMEOUT    = -7;      //异步调用超时
   const int TARSINVOKETIMEOUT       = -7;      //调用超时
   const int TARSPROXYCONNECTERR     = -8;      //proxy链接异常
   const int TARSSERVEROVERLOAD      = -9;      //服务器端超负载,超过队列长度
   const int TARSADAPTERNULL         = -10;     //客户端选路为空，服务不存在或者所有服务down掉了
   const int TARSINVOKEBYINVALIDESET = -11;     //客户端按set规则调用非法
   const int TARSCLIENTDECODEERR     = -12;     //客户端解码异常
   const int TARSSERVERUNKNOWNERR    = -99;     //服务器端位置异常
   ```

   

3. 异步调用

   ```c++
   struct HelloCallback : public HelloServantPrxCallback
   {
       //回调函数
       virtual void callback_testHello(int ret, const string &r)
       {
           std::cout << "ret : " << r << endl;
       }
   
       virtual void callback_testHello_exception(tars::Int32 ret)
       {
           assert(ret == 0);
           cout << "callback exception:" << ret << endl;
       }
   };
   int main(int argc, char ** argv)
   {
       Communicator comm;
   
   
       HelloServantPrx prx;
       comm.stringToProxy("Test.HelloServer.HelloServantObj@tcp -h 10.10.10.168 -p 10016", prx);
   
   
       HelloServantPrxCallbackPtr cb = new HelloCallback();
       string sReq("hello world");
       string sRsp("");
   
       prx->async_testHello(cb, sReq);
   
       std::cout << "finished! " << endl;
       getchar();
   
   
       return 0;
   }
   ```

   

4. 指定set方式调用

5. Hash调用

   > 服务可以部署多台，请求也是随机分发到服务上，但是在某些场合下，希望请求总是在某一台服务器上
   >
   > ```c++
   > //如果该服务器当掉,请求会迁移到其它服务器
   > QQInfo qi = pPrx->tars_hash(uin)->query(uin);
   > ```
   >
   > ```c++
   > // 请求随机分发至一台服务器
   > QQInfo qi = pPrx->query(uin);
   > ```





# 3 异步嵌套



# 4 染色





# 5 tars 协议数据包大小







# 6 业务配置





# 7 日志





# 8 服务管理

