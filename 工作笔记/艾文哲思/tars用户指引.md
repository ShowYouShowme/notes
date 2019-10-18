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

重点关注的服务

> 1. Node：定时发送心跳[可选，只有发布到框架的服务才需要此参数，把此参数去掉远程调试不会中断]
> 2. Log：远程日志[可选]
> 3. Config：配置中心，不配置的话无法从远程配置中心拉取配置文件
> 4. Notify：上报中心，统计上报数据[可选]

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

## 2-1 通信器[~~~]

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

+ 服务名在主控注册：通过服务名寻址，在生成通信器时指定registry（主控）的地址

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

   

4. 指定set方式调用[TODO]

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



# 4 染色[未阅读--重点]





# 5 tars 协议数据包大小[一般默认即可]

+ tars协议对数据包大小进行了限制

  > 1. 通信器（客户端）对发出去的包大小没有限制，对收到的回包有限制，默认是10000000字节（接近10M）
  > 2. 服务端对发送的包没有限制，对收到的包有大小限制，默认是100000000字节（接近100M）

+ 修改数据包大小限制

  > 1. 修改服务器接收数据包大小
  >
  >    ```c++
  >    addServantProtocol(ServerConfig::Application + "." + ServerConfig::ServerName + ".BObj",AppProtocol::parseLenLen<100000000>);
  >    ```
  >
  > 2. 修改客户端接收数据包大小
  >
  >    ```c++
  >    Communicator comm;
  >    
  >    HelloServantPrx prx;
  >    comm.stringToProxy("Test.HelloServer.HelloServantObj@tcp -h 10.10.10.168 -p 10016", prx);
  >    ProxyProtocol prot;
  >    prot.requestFunc = ProxyProtocol::tarsRequest;
  >    prot.responseFunc = ProxyProtocol::tarsResponseLen<1000000000>;
  >    prx->tars_set_protocol(prot);
  >    ```
  >
  >    





# 6 业务配置

## 6-1 添加配置

服务管理-->添加配置：将配置文件写入到表t_config_files





## 6-2 配置拉取到服务可执行文件目录

方法1：服务管理-->PUSH配置文件



方法2：在SayHeyServer::initialize() 添加 ----->建议使用此方式

```shell
addConfig("HelloServer.conf");
```





# 7 日志

## 7-1 滚动日志

+ API

  ```c++
  #define LOG             (TarsRollLogger::getInstance()->logger())
  
  #define LOGMSG(level,msg...) do{ if(LOG->IsNeedLog(level)) LOG->log(level)<<msg;}while(0)
  
  
  #define TLOGINFO(msg...)    LOGMSG(TarsRollLogger::INFO_LOG,msg) // 信息
  #define TLOGDEBUG(msg...)   LOGMSG(TarsRollLogger::DEBUG_LOG,msg) //调试
  #define TLOGWARN(msg...)    LOGMSG(TarsRollLogger::WARN_LOG,msg) // 警告
  #define TLOGERROR(msg...)   LOGMSG(TarsRollLogger::ERROR_LOG,msg) //错误
  ```

+ 用法

  ```c++
  // 设置日志级别
  TarsRollLogger::getInstance()->logger()->setLogLevel(TC_RollLogger::INFO_LOG);
  
  // 设置同步打印日志
  TarsRollLogger::getInstance()->sync(true);
  
  // 替换ostream
  ostream &print(ostream &os);
  
  print(LOG->debug());
  ```

+ 注意事项

  > 1. 可以在web管理设置服务LOG的当前级别
  > 2. 滚动日志大小在配置文件中用logsize配置
  > 3. 滚动日志文件名为：${app}.${server}.log
  > 4. TLOGXXX是全局的单件，任何地方可以使用
  > 5. 滚动日志不会发送到远程tarslog服务

## 7-2 按天日志

+ API

  ```shell
  # 日志文件名：${app}.${server}_${滚动方式}.log
  DLOG
  
  # 日志文件名:${app}.${server}_${fileName}_${滚动方式}.log
  FDLOG(${fileName})
  ```

+ 说明

  > 1. 保存日志的方式：
  >    11. 仅保存到本地
  >    12. 仅保存至tarslog
  >    13. 保存到本地和tarslog，这是默认的选项
  > 2. 可以修改滚动的时间，比如按分钟，小时等；默认按天滚动

+ 代码

  ```c++
  int main(int argc, char ** argv)
  {
  
  
      CommunicatorPtr c = new Communicator();
  
      string logObj = "tars.tarslog.LogObj@tcp -h 127.0.0.1 -p 20500";
  
      //初始化本地滚动日志
      TarsRollLogger::getInstance()->setLogInfo("Test", "TestServer", "./");
  
      //初始化时间日志
      TarsTimeLogger::getInstance()->setLogInfo(c, logObj, "Test", "TestServer", "./");
  
      //如果是Tars服务，不需要上面部分的代码，框架已经自动完成初始化，不用业务自己初始化
  
      //缺省的按天日志不用上传到服务器
      TarsTimeLogger::getInstance()->enableRemote("", false);
  
      //缺省的按天日志按分钟滚动
      TarsTimeLogger::getInstance()->initFormat("", "%Y%m%d%H%M");
  
      //abc2文件不用上传到服务器
      TarsTimeLogger::getInstance()->enableRemote("abc2", false);
  
      //abc2文件按小时滚动
      TarsTimeLogger::getInstance()->initFormat("abc2", "%Y%m%d%H");
  
      //abc3文件不记本地
      TarsTimeLogger::getInstance()->enableLocal("abc3", false);
  
      int i = 100000;
      while (i--)
      {
          //与上一个一样
          TLOGDEBUG(i << endl);
  
          //error级别
          TLOGERROR(i << endl);
  
          DLOG << "+++++++++++" << i  << "++++++++++" << endl;
  
          FDLOG("abc1") << i << endl;
          FDLOG("abc2") << i << endl;
          FDLOG("abc3") << i << endl;
  
          if (i % 1000 == 0)
          {
              cout << i << endl;
          }
          usleep(10);
      }
      getchar();
  
  
      return 0;
  }
  ```

  

# 8 服务管理

+ 功能

  > 动态接收命令，来处理相关的业务逻辑，例如：动态更新配置等

+ 相关宏

  > - TARS_ADD_ADMIN_CMD_PREFIX：添加前置的命令处理方法，在所有Normal方法之前执行，多个前置方法之间顺序不确定
  > - TARS_ADD_ADMIN_CMD_NORMAL：添加Normal命令处理方法，在所有前置方法最后执行，多个Normal方法之间顺序不确定

+ 注册接口处理

  1. 全局接口处理：该接口处理与服务相关

     ```c++
     bool HelloServer::procDLOG(const string& command, const string& params, string& result)
     {
         TarsTimeLogger::getInstance()->enableLocal(params, false);
         return false;
     }
     
     void HelloServer::initialize()
     {
         addServant(...);
         addConfig(…);
     
     	//注册处理函数：
         TARS_ADD_ADMIN_CMD_NORMAL("DISABLEDLOG", HelloServer::procDLOG);
     }
     ```

     



# 9 发送管理命令

+ 发送方式

  > 将TARS服务发布到平台上，通过管理平台发送命令

+ 可用命令

  > - tars.help //查看所有管理命令
  > - tars.loadconfig //从配置中心, 拉取配置下来: tars.loadconfig filename
  > - tars.setloglevel //设置滚动日志的等级: tars.setloglevel [NONE, ERROR, WARN, DEBUG]
  > - tars.viewstatus //查看服务状态
  > - tars.connection //查看当前链接情况
  > - tars.loadproperty //使配置文件的property信息生效
  > - tars.setdyeing    //设置染色信息 tars.setdyeing key servant [interface]





# 10 统计上报

+ 定义

  > Tars框架内部，向tarsstat上报调用耗时等信息

+ 原理

  > 客户端调用上报接口后，实际先暂存在内存中，当到达某个时间点后才正式上报到tarsstat服务

+ 使用上报

  > 1. web管理系统上部署的服务会自动上报
  >
  > 2. 不在web上部署的服务按如下设置
  >
  >    ```c++
  >    //初始化通信器
  >    CommunicatorPtr pcomm = new Communicator();
  >    //初始化tarsregistry服务地址
  >    pcomm->setProperty("locator", "tars.tarsregistry.QueryObj@tcp -h xxx.xxx.xxx.xx -p xxxx"
  >    //初始化stat服务
  >    pcomm->setProperty("stat", "tars.tarsstat.StatObj");
  >    //设置上报间隔
  >    pcomm->setProperty("report-interval", "1000");
  >    //设置上报主调名称
  >    pcomm->setProperty("modulename", "Test.TestServer_Client");
  >    ```



# 异常上报

可以在程序中上报三种不同类型的异常

```c++
//上报普通信息
TARS_NOTIFY_NORMAL(info) 
//上报警告信息
TARS_NOTIFY_WARN(info) 
//上报错误信息
TARS_NOTIFY_ERROR(info)
```





# 属性统计

+ 统计类型

  > 1. 求和（sum）
  > 2. 平均（avg）
  > 3. 分布（distr）
  > 4. 最大值（max）
  > 5. 最小值（min）
  > 6. 计数（count）

+ 使用

  ```c++
  //初始化通信器
  Communicator _comm;
  //初始化property服务地址
  _comm.setProperty("property", "tars.tarsproperty.PropertyObj@ tcp -h xxx.xxx.xxx.xxx -p xxxx");
  
  //初始化分布数据范围
  vector<int> v;
  v.push_back(10);
  v.push_back(30);
  v.push_back(50);
  v.push_back(80);
  v.push_back(100);
  
  //创建test1属性，该属性用到了上诉所有的集中统计方式，注意distrv的初始化
  PropertyReportPtr srp = _comm.getStatReport()->createPropertyReport("test1", 
  PropertyReport::sum(), 
  PropertyReport::avg(), 
  PropertyReport::count(),
  PropertyReport::max(), 
  PropertyReport::min(),
  PropertyReport::distr(v));
  
  //上报数据，property只支持int类型的数据上报
  int iValue = 0;
  for ( int i = 0; i < 10000000; i++ )
  {
          sleep(1);
       srp->report(rand() % 100 );
  }
  ```

  说明：

  1. 调用createPropertyReport时，必须在服务启动以后创建并保存好创建的对象，后续拿这个对象report即可，不要每次使用的时候create
  2. createPropertyReport的参数可以是任何统计方式的集合





# tars调用链

功能：上报rpc调用路径至zipkin，以协助定位网络调用问题







# db_tars表介绍

1. t_adapter_conf：servant的配置
2. t_config_files 和 t_config_history_files：管理后台发布的配置文件
3. t_server_patchs ： 管理后台发布的包的记录
4. t_server_notifys：异常上报信息，调用接口TARS_NOTIFY_NORMAL、TARS_NOTIFY_WARN和TARS_NOTIFY_ERROR上报的信息会存放于此处
5. t_task 和 t_task_item：存放管理后台执行过的命令
6. t_profile_template：存放配置文件的模板
7. t_node_info：存放tarsnode 服务的信息
8. t_registry_info ： 存放tarsregistry的信息
9. t_server_conf ： 部署的各个服务的信息



# tars_property

按小时分表，记录上报数据，比如内存使用，用户自定义的上报信息



# tars_stat

按小时分表，记录接口调用耗时等信息



