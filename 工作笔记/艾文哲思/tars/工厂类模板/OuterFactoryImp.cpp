#include <sstream>
#include "OuterFactoryImp.h"
#include "LogComm.h"
#include "GoldPigServer.h"

using namespace wbl;

OuterFactoryImp::OuterFactoryImp()
	: _pFileConf(NULL)
{
	createAllObject();
}

OuterFactoryImp::~OuterFactoryImp()
{
	deleteAllObject();
}

void OuterFactoryImp::deleteAllObject()
{
	if(NULL != _pFileConf)
	{
		delete _pFileConf;
		_pFileConf = NULL;
	}
}

void OuterFactoryImp::createAllObject()
{
	try
	{
		//
		deleteAllObject();

		//本地配置文件
		_pFileConf = new tars::TC_Config();
		if(NULL == _pFileConf)
		{
			ROLLLOG_ERROR << "create config parser fail, ptr null." << endl;

			terminate();
		}
		
		//tars代理Factory,访问其他tars接口时使用
		_pProxyFactory = new OuterProxyFactory();
		if((long int)NULL == _pProxyFactory)
		{
			ROLLLOG_ERROR << "create outer proxy factory fail, ptr null." << endl;

			terminate();
		}

		LOG_DEBUG << "init proxy factory succ." << endl;	

		//读取所有配置
		load();
	}
	catch (TC_Exception& ex)
	{
		LOG->error() << ex.what() << endl;
	}
	catch (exception& e)
	{
		LOG->error() << e.what() << endl;
	}
	catch (...)
	{
		LOG->error() << "unknown exception." << endl;
	}

	return;
}

//读取所有配置
void OuterFactoryImp::load()
{	
	__TRY__

	wbl::WriteLocker lock(m_rwlock);

	_pFileConf->parseFile(ServerConfig::BasePath + ServerConfig::ServerName + ".conf");
	LOG_DEBUG << "init config file succ:" << ServerConfig::BasePath + ServerConfig::ServerName + ".conf" << endl;
	
	//代理配置
	readPrxConfig();
	printPrxConfig();
	__CATCH__
}

//代理配置
void OuterFactoryImp::readPrxConfig()
{
	//配置服务
	_ConfigServantObj = (*_pFileConf).get("/Main/Interface/ConfigServer<ProxyObj>", "");
	_DataProxyServantObj = (*_pFileConf).get("/Main/Interface/DataProxyServer<ProxyObj>", "");
	_DBAgentServantObj = (*_pFileConf).get("/Main/Interface/DBAgentServer<ProxyObj>", "");
}

//打印代理配置
void OuterFactoryImp::printPrxConfig()
{
	FDLOG_CONFIG_INFO << "_ConfigServantObj ProxyObj:" << _ConfigServantObj << endl;
	FDLOG_CONFIG_INFO << "_DataProxyServantObj ProxyObj:" << _DataProxyServantObj << endl;
	FDLOG_CONFIG_INFO << "_DBAgentServantObj ProxyObj:" << _DBAgentServantObj << endl;
}

// 获取代理
//游戏配置服务代理
const ConfigServantPrx OuterFactoryImp::getConfigServantPrx()
{
	if (!_ConfigServerPrx)
	{
		_ConfigServerPrx = Application::getCommunicator()->stringToProxy<ConfigServantPrx>(_ConfigServantObj);
		ROLLLOG_DEBUG << "Init _ConfigServantObj succ, _ConfigServantObj:" << _ConfigServantObj << endl;
	}

	//
	return _ConfigServerPrx;
}


//数据存储代理服务代理
const DataProxyServantPrx OuterFactoryImp::getDataProxyServantPrx()
{
	if (!_DataProxyServerPrx)
	{
		_DataProxyServerPrx = Application::getCommunicator()->stringToProxy<dataproxy::DataProxyServantPrx>(_DataProxyServantObj);
		ROLLLOG_DEBUG << "Init _DataProxyServantObj succ, _DataProxyServantObj:" << _DataProxyServantObj << endl;
	}

	//
	return _DataProxyServerPrx;
}

//数据库代理服务代理
const DBAgentServantPrx OuterFactoryImp::getDBAgentServantPrx()
{
	if (!_DBAgentServerPrx)
	{
		_DBAgentServerPrx = Application::getCommunicator()->stringToProxy<dbagent::DBAgentServantPrx>(_DBAgentServantObj);
		ROLLLOG_DEBUG << "Init _DBAgentServantObj succ, _DBAgentServantObj:" << _DBAgentServantObj << endl;
	}

	//
	return _DBAgentServerPrx;
}

//格式化时间	
string OuterFactoryImp::GetTimeFormat()
{
	string sFormat("%Y-%m-%d %H:%M:%S");
	time_t t = time(NULL);
	struct tm* pTm = localtime(&t);
	if(pTm == NULL) 
	{ 
		return "";
	}

	///format
	char sTimeString[255] = "\0"; 
	strftime(sTimeString, sizeof(sTimeString), sFormat.c_str(), pTm);
	return string(sTimeString);
}

//拆分字符串成整形
int OuterFactoryImp::splitInt(string szSrc, vector<int>& vecInt)
{
	split_int(szSrc, "[ \t]*\\|[ \t]*", vecInt);
		
	return 0;
}

////////////////////////////////////////////////////////////////////////////////


