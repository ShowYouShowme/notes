# dna私链多节点搭建

***

1. 安装依赖

   ```shell
   apt-get install ntp
   apt-get install libcurl4-openssl-dev
   apt-get install libcurl3
   ```

2. 编译项目

   ```shell
   git clone https://github.com/bitshares/bitshares-core.git
   cd bitshares-core
   git checkout master # may substitute "master" with current release tag
   git submodule update --init --recursive
   cmake -DCMAKE_BUILD_TYPE=RelWithDebInfo .
   make # 如果内存不够报错,可以限定使用一个cpu编译 make -j1
   ```

   

3. 生成私钥,公钥和钱包地址

   ```shell
   ./cli_wallet --suggest-brain-key
   ```

4. 修改配置文件

   1. 配置文件`./libraries/egenesis/genesis.json`

      ```shell
      cd ./libraries/egenesis/
      cp ./genesis-dev.json genesis.json
      ```

   2. 编辑配置文件

      + initial_accounts

        ```shell
        # 1- 修改init0到init10的owner_key和active_key,为方便起见,两个值设置为一样
        
        # 2- 修改nathan的owner_key和active_key
        
        # 3- 增加mvs账号
        ```

      + initial_balances

        ```shell
        设置mvs账号的余额，将owner改为mvs的钱包地址
        ```

      + initial_witness_candidates

        ```shell
        设置init0到init10的block_signing_key为公钥
        ```

      + **修改了该配置文件要重新编译项目**

        ```shell
        cd ../..
        make -j1
        ```

        

5. 预启动witness_node,生成配置文件

   ```shell
   cd ./programs/witness_node/
   
    ./witness_node --rpc-endpoint "127.0.0.1:8190" --p2p-endpoint  "0.0.0.0:8776" --seed-nodes "[]" --enable-stale-production -d test_net  
    
    # 打印区块链ID后按下ctrl+c停止节点运行
    Chain ID is 74d67bade02ac55b3cd5e43aca401538284c80a2e270ddca2f7e619515653640
   ```

6. 编辑配置文件`./test_net/config.ini`

   + 将`required-participation`的值改为0

   + 在`#witness-id = `后面添加以下内容

     ```shell
     witness-id = "1.6.1"
     witness-id = "1.6.2"
     witness-id = "1.6.3"
     witness-id = "1.6.4"
     witness-id = "1.6.5"
     witness-id = "1.6.6"
     witness-id = "1.6.7"
     witness-id = "1.6.8"
     witness-id = "1.6.9"
     witness-id = "1.6.10"
     witness-id = "1.6.11"
     ```

   + 添加见证人节点的公私钥对,如果init0-init10的公钥不一样,private-key设置多行

     ```shell
     # Tuple of [PublicKey, WIF private key] (may specify multiple times)
     private-key = ["BTS53HQrJqduECBXFcGjTx8s7VTa2m9NtMiWQUmcgZ6M42x2nnGCy","5HzUzjeVn8H3czCyHNJc4z3xmWfd8FbJiVH3sfEpm1rVn9YEmtP"]
     ```

   + 删除文件夹blockchain,重启winess_node节点

     ```shell
     rm -rf ./blockchain
     
     cd ../
     
      ./witness_node --rpc-endpoint "127.0.0.1:8190" --p2p-endpoint  "0.0.0.0:8776" --seed-nodes "[]" --enable-stale-production -d test_net  
     ```

7. 启动钱包客户端

   + 启动,如果存在wallet.json先删除

     ```shell
      ./cli_wallet --chain-id="20dbcef42a367d6577976b6bcb4cdbad5e64b544397f2a3ca96279dede32c929" -s ws://127.0.0.1:8190 -w wallet.json -r 127.0.0.1:8199   -H 127.0.0.1:8192 
     ```

   + 客户端命令

     1. 设置钱包密码

        ```shell
        set_password ${passwd}
        ```

     2. 解锁钱包

        ```shell
        unlock ${passwd}
        ```

     3. 导入私钥

        ```shell
        import_key ${account} ${private_key}
        
        import_key mvs 5Kkn3Scxy9uGHTmg8MWXns9nMKBzGgDnsdsegip5cbovQkcHb1Q
        ```

     4. 导入创世区块的余额

        ```shell
        import_balance ${account} ["${private_key}"] true
        
        import_balance mvs ["5Kkn3Scxy9uGHTmg8MWXns9nMKBzGgDnsdsegip5cbovQkcHb1Q"]  true
        ```

     5. 查询余额

        ```shell
        list_account_balances ${account}
        
        list_account_balances mvs
        ```

     6. 升级为会员，只有会员才有资格成为超级节点

        ```shell
        upgrade_account ${account} true
        
        upgrade_account mvs true
        ```

     7. 注册超级节点

        ```shell
        create_witness  ${account}  "${url}" true
        
        create_witness  mvs  "http://www.mvs.org" true
        ```

     8. 投票

        ```shell
        vote_for_witness dna mvs true true
        ```

     9. 查询节点信息

        ```shell
        get_witness mvs
        ```

     10. 输出所有节点公私钥对

         ```shell
         dump_private_keys
         ```

         