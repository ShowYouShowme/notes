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

4. 修改配置文件`./libraries/egenesis/genesis.json`

   1. 复制配置文件

      ```shell
      cd ./libraries/egenesis/
      cp ./genesis-dev.json genesis.json
      ```

   2. 修改配置文件

      + initial_accounts

        ```shell
        # 1- 修改init0到init10的owner_key和active_key,为方便起见,两个值设置为一样
        
        # 2- 修改nathan的owner_key和active_key
        
        # 3- 增加mvs账号
        
        # 钱包的公钥和地址用'BTS'开头，线上的用'DNA'开头
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
     # 区块链的数据存在文件夹blockchain里面,把它删除就没有数据了
     
     rm -rf ./blockchain
     
     cd ../
     
      ./witness_node --rpc-endpoint "127.0.0.1:8190" --p2p-endpoint  "0.0.0.0:8776" --seed-nodes "[]" --enable-stale-production -d test_net  
     ```

7. 启动钱包客户端

   + 启动,如果存在`wallet.json`先删除

     ```shell
      # 8190 是witness_node提供的websocket端口
      # 8199 和 8192 是cli_wallet作为服务器监听的端口
      # id 是区块链的id,错了会在remote_chain_id里提示
      ./cli_wallet --chain-id="20dbcef42a367d6577976b6bcb4cdbad5e64b544397f2a3ca96279dede32c929" -s ws://127.0.0.1:8190 -w wallet.json -r 127.0.0.1:8199   -H 127.0.0.1:8192 
     ```

   + 客户端命令

     1. 设置钱包密码

        ```shell
        set_password ${passwd}
        
        # 返回值为null
        ```

     2. 解锁钱包

        ```shell
        unlock ${passwd}
        
        # 返回值为null
        ```

     3. 导入私钥

        ```shell
        import_key ${account} ${private_key}
        
        import_key mvs 5JMWPyYd5QqGyenXx6BURZdnrCoCmVRAwMQzc79ewr8qp78rn1P
        
        # 返回值
        2260132ms th_a       wallet.cpp:984                save_wallet_file     ] saving wallet to file wallet.json
        2260133ms th_a       wallet.cpp:1003               save_wallet_file     ] saved successfully wallet to tmp file wallet.json.tmp
        2260133ms th_a       wallet.cpp:1009               save_wallet_file     ] validated successfully tmp wallet file wallet.json.tmp
        2260133ms th_a       wallet.cpp:1013               save_wallet_file     ] renamed successfully tmp wallet file wallet.json.tmp
        2260133ms th_a       wallet.cpp:1020               save_wallet_file     ] successfully saved wallet to file wallet.json
        2260133ms th_a       wallet.cpp:565                copy_wallet_file     ] backing up wallet wallet.json to after-import-key-6a038e4e.wallet
        true
        ```

     4. 导入创世区块的余额

        ```shell
        import_balance ${account} ["${private_key}"] true
        
        import_balance mvs ["5JMWPyYd5QqGyenXx6BURZdnrCoCmVRAwMQzc79ewr8qp78rn1P"]  true
        
        # 返回值
        [{
            "ref_block_num": 15,
            "ref_block_prefix": 3259107138,
            "expiration": "2020-05-12T08:44:20",
            "operations": [[
                37,{
                  "fee": {
                    "amount": 0,
                    "asset_id": "1.3.0"
                  },
                  "deposit_to_account": "1.2.18",
                  "balance_to_claim": "1.15.0",
                  "balance_owner_key": "BTS584N5T65aVbXgZjDPWCtK8evXcg1LbBuVf9ynXRvHWVhN8YJTd",
                  "total_claimed": {
                    "amount": "1230000000000000",
                    "asset_id": "1.3.0"
                  }
                }
              ]
            ],
            "extensions": [],
            "signatures": [
              "1f481150c2298b0cd21f9f0d46aba5d3a17bc363d381959db475d0a0e4efe3715c38380600f7c2724d9be622bf928d8bc4416e644ae079cc905754cf2f9936f1cc"
            ]
          }
        ]
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
        
        # 返回值
        {
          "ref_block_num": 48,
          "ref_block_prefix": 4091519137,
          "expiration": "2020-05-12T08:47:05",
          "operations": [[
              8,{
                "fee": {
                  "amount": 1000000000,
                  "asset_id": "1.3.0"
                },
                "account_to_upgrade": "1.2.18",
                "upgrade_to_lifetime_member": true,
                "extensions": []
              }
            ]
          ],
          "extensions": [],
          "signatures": [
            "207cc84af87d80dc30ed1f6027e08b86c789dc5468342eba701a7f21c1ba89abf375f2b432a4956d9620190fc4db2998614205d1ef8e1e98803589f32ae7a9aecb"
          ]
        }
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

     11. 退出钱包客户端

         ```shell
         ctrl + c
         ```

         