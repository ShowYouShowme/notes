# 接口文档

[链接](https://www.showdoc.cc/baidang201?page_id=4165938892306231)





# 区块链API

[链接](https://dev.bitshares.works/en/master/api/blockchain_api.html)





# 入门手册

[链接](https://dev.bitshares.works/en/master/bts_guide/index_faq.html)





# 常用API





# 业务知识

1. block_num最小值是1







# 项目发布

1. 上传文件

   ```shell
   # 打包
   tar -zcvf dna-explorer-api.tar.gz --exclude=dna-explorer-api/.idea/ --exclude=dna-explorer-api/.git/ dna-explorer-api/
   
   # 上传文件
   scp -P 12008 ./dna-explorer-api.tar.gz root@dna3.viewdao.com:/tmp
   ```

2. 停止服务

   ```shell
   ps -ef | grep python
   
   # 停止进程 /root/dna-explorer-api/wrappers_env/bin/python ...
   ```



# 项目代码

1. github

   ```shell
   https://github.com/mvs-org
   ```

   



# dna-explorer-api 测试文档

***

[链接](https://shimo.im/folder/6QwKYVDhRyvqkGtX)