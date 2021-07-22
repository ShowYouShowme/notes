# 第一章 安装

***

1. 下载代码

   ```shell
   git clone https://github.com/ethereum/go-ethereum.git
   ```

2. 编译

   ```shell
   make all
   ```

   



# 第二章 常用命令

***

```c#
web3.eth.coinbase          // 节点挖矿的账户地址，默认为账户列表的第一个账户
personal.listAccounts[0]   // 查看账户列表的第一个账户
txpool.status              // 查看交易的状态
miner.setEtherbase(xxx)    // 设置挖矿的账户，xxx为账户地址
web3.fromWei()             // 将返回值换算成以太币
```



## 2.1 创建账户

***

```shell
personal.newAccount("xxx")
eth.accounts # 查看账户
eth.getBalance(eth.accounts[0]) # 查看账户余额，返回值的单位是wei，wei是以太币的最小单位，1个以太币=10^18wei。
```



## 2.2 挖矿

***

```shell
miner.start($thread_count) # 开始挖矿
miner.stop() # 停止挖矿
```



## 2.3 转账

***

```shell
#从账户A 转账 到账户B，必须先解锁账户A
personal.unlockAccount(eth.accounts[0])

eth.sendTransaction({from:eth.accounts[0],to:eth.accounts[1],value:web3.toWei(8,'ether')})
```



## 2.4 查看交易和区块

***

```shell
eth.blockNumber            # 查看交易的区块号
eth.getTransaction         # 查看交易区块信息,输入参数是交易哈希
eth.getBlock(xxx)          # 根据区块号查看区块信息，xxx为区块号
```

