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





# 第三章  私有链部署

***



## 3.1 单节点部署

***

1. 定义创世状态配置文件genesis.json

   ```JSO
   {
     "config": {
       "chainId": <arbitrary positive integer>,
       "homesteadBlock": 0,
       "eip150Block": 0,
       "eip155Block": 0,
       "eip158Block": 0,
       "byzantiumBlock": 0,
       "constantinopleBlock": 0,
       "petersburgBlock": 0,
       "istanbulBlock": 0,
       "berlinBlock": 0
     },
     "alloc": {},
     "coinbase": "0x0000000000000000000000000000000000000000",
     "difficulty": "0x20000",
     "extraData": "",
     "gasLimit": "0x2fefd8",
     "nonce": "0x0000000000000042",
     "mixhash": "0x0000000000000000000000000000000000000000000000000000000000000000",
     "parentHash": "0x0000000000000000000000000000000000000000000000000000000000000000",
     "timestamp": "0x00"
   }
   
   ```

2. 初始化创世纪节点

   ```shell
   ./geth --datadir ./data init genesis.json
   ```

3. 启动节点

   ```shell
   ./geth --datadir ./data --networkid 15
   ```

4. 客户端连接节点

   ```shell
   ./geth attach ipc:./data/geth.ipc
   ```

5. 挖矿

   ```shell
   # 查看一下系统有的用户
   > eth.accounts
   []
   
   # 查看详细的用户信息
   > personal
   
   # 创建两个账号用于转账，或者使用 personal.newAccount() 也会提示输入密码
   > personal.newAccount('123456')
   > personal.newAccount('123456')
   
   > eth.accounts
   ["0x18a6581a285f40ac3faaa646e13d7c6dd87276f4", "0x2455572ef500cf8634a4090d6d6096c588013e2a"]
   # 此时可以看下 keystore 目录，多出了两个文件，也就是我们刚才创建的两个账户密钥（丢了它，你就等于丢了币）
   
   # 查看账号1下的余额
   > eth.getBalance(eth.accounts[0])
   
   # 查看coinbase账号
   > eth.coinbase
   0x18a6581a285f40ac3faaa646e13d7c6dd87276f4
   
   # 如果想要把挖到的矿存入其他账户，可以使用
   > miner.setEtherbase(eth.accounts[1])
   true
   
   开始挖矿，我们先把coinbase改成账号1
   > miner.setEtherbase(eth.accounts[0])
   true
   
   # 如果出现 miner.start() 直接返回 null 的情况，请先查看是否还未创建过账户。
   > miner.start(1)
   INFO [05-31|19:57:17] Updated mining threads                   threads=0
   INFO [05-31|19:57:17] Transaction pool price threshold updated price=18000000000
   INFO [05-31|19:57:17] Starting mining operation
   INFO [05-31|19:57:17] Commit new mining work                   number=12 txs=0 uncles=0 elapsed=194.667µs
   INFO [05-31|19:57:19] Successfully sealed new block            number=12 hash=82d29d…65290c
   INFO [05-31|19:57:19]  mined potential block                  number=12 hash=82d29d…65290c
   INFO [05-31|19:57:19] Commit new mining work                   number=13 txs=0 uncles=0 elapsed=159.066µs
   INFO [05-31|19:57:19] Successfully sealed new block            number=13 hash=e91844…e962a6
   INFO [05-31|19:57:19]  mined potential block                  number=13 hash=e91844…e962a6
   等到 percentage 达到100就能挖出来了，请耐心等待~，出现小锤头的时候意味着你挖到了！
   
   # 已经挖到了，我们先暂停挖矿，注意：输入的字符会被挖矿刷屏信息冲掉，没有关系，只要输入完整的miner.stop()之后回车，即可停止挖矿。正在执行的挖矿进程不会立即暂停，仍然会等到当前完整快写完后才会暂停
   > miner.stop()
   true
   
   然后查看账户余额
   > eth.getBalance(eth.accounts[0])
   112000000000000000000
   # 不要被这个零的个数吓到，这里默认显示的以 wei 为单位的，而 1 ether = 10^18 wei，所以我们转换一下单位立马就清晰了，
   
   > web3.fromWei(eth.getBalance(eth.accounts[0]), 'ether')
   112
   # 嗯，其实我们目前就挖了112个ether
   ```

6. 转账

   ```shell
   > personal.unlockAccount(eth.accounts[0])
   
   # 我们先转8个ether给账号2
   > eth.sendTransaction({from:eth.accounts[0],to:eth.accounts[1],value:web3.toWei(8,'ether')})
   
   #让矿工挖矿打包交易
   > miner.start(1)
   # 持续几秒
   > miner.stop()
   
   # 然后查看账号2的余额，已经有余额
   > eth.getBalance(eth.accounts[1])
   8000000000000000000
   ```




## 3.2 多节点部署

***

1. 每个节点使用同样配置文件初始化创世纪节点

2. 启动一个节点，每个节点的networkid 必须一致

   ```shell
   ./geth --datadir data2 --networkid 1024 --ipcdisable --port 3002 --rpcport 9000 console
   ```

3. 获取节点Enoded url

   ```shell
   #第一种方式
   admin.nodeInfo.enode #获取的数据要修改
   
   #第二种方式 节点启动时有以下信息
   INFO [07-22|17:22:46.014] Started P2P networking                   self=enode://c0a48e233e3f04309be23df05ce31fc4a1454e63468c231d90038447f9cccff361076ac487f759780c6b2ca077ef0fb6da543ee5ce7949337e472541bce2524b@127.0.0.1:3002
   ```

4. 启动第二个节点

   ```shell
   ./geth --datadir data3 --networkid 1024 --ipcdisable --port 3003 --rpcport 9001 console
   ```

5. 在第二个节点里添加第一个节点

   ```shell
   admin.addPeer($enodeUrl)
   ```

6. 查看对端信息

   ```shell
   admin.peers
   ```

7. 尝试挖矿，然后看第一个节点是否能同步数据

