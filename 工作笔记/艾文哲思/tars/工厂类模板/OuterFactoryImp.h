#ifndef _OUTER_FACTORY_IMP_H_
#define _OUTER_FACTORY_IMP_H_

#include <string>
#include <map>

#include "servant/Application.h"
#include "globe.h"
#include "OuterFactory.h"

//wbl
#include <wbl/regex_util.h>

//配置服务
#include "ConfigServant.h"
#include "DataProxyServant.h"
#include "DBAgentServant.h"

using namespace config;
using namespace dataproxy;
using namespace dbagent;

#define ONE_DAY_TIME (24*60*60)
#define ZONE_TIME_OFFSET (8*60*60)

class OuterFactoryImp;
typedef TC_AutoPtr<OuterFactoryImp> OuterFactoryImpPtr;

/**
 * 外部工具接口对象工厂
 */
class OuterFactoryImp : public OuterFactory
{
private:
	OuterFactoryImp();
	~OuterFactoryImp();

	///
	friend class GoldPigServantImp;
	friend class GoldPigServer;

public:
	//框架中用到的outer接口(不能修改):
	const OuterProxyFactoryPtr& getProxyFactory() const
	{
		 return _pProxyFactory;
	}

	tars::TC_Config& getConfig() const
	{
	 	return *_pFileConf;
	}

public:	
	//读取所有配置
	void load();

	//代理配置
	void readPrxConfig();
	//打印代理配置
	void printPrxConfig();


private:
	void createAllObject();
	void deleteAllObject();

public:
	// 获取代理
	//游戏配置服务代理
	const ConfigServantPrx getConfigServantPrx();

	//数据存储代理服务代理
	const DataProxyServantPrx getDataProxyServantPrx();

	//数据库代理服务代理
	const DBAgentServantPrx getDBAgentServantPrx();
	
public:
	//格式化时间
	string GetTimeFormat();

private:
	//拆分字符串成整形
	int splitInt(string szSrc, vector<int>& vecInt);

private:
	wbl::ReadWriteLocker m_rwlock;  //读写锁，防止脏读

private:
	//框架用到的共享对象(不能修改):
	tars::TC_Config* _pFileConf;

	OuterProxyFactoryPtr _pProxyFactory;

private:
	//业务自有的共享对象:
	//...
	//游戏配置服务
	std::string _ConfigServantObj;
	ConfigServantPrx _ConfigServerPrx;

	//数据存储代理服务
	std::string _DataProxyServantObj;
	DataProxyServantPrx _DataProxyServerPrx;

	//数据库代理服务
	std::string _DBAgentServantObj;
	DBAgentServantPrx _DBAgentServerPrx;
};

////////////////////////////////////////////////////////////////////////////////
#endif


