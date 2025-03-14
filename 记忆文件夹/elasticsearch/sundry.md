# 第一章 安装

本文档使用的是7.x版本，8.x版本需要配置ssl比较麻烦



## 1.1 安装gpg key

```shell
rpm --import https://artifacts.elastic.co/GPG-KEY-elasticsearch
```



## 1.2 创建yum仓库

```shell
vim /etc/yum.repos.d/elasticsearch.repo

[elasticsearch]
name=Elasticsearch repository for 7.x packages
baseurl=https://artifacts.elastic.co/packages/7.x/yum
gpgcheck=1
gpgkey=https://artifacts.elastic.co/GPG-KEY-elasticsearch
enabled=0
autorefresh=1
type=rpm-md
```



## 1.3 安装软件

```shell
yum install --enablerepo=elasticsearch elasticsearch kibana filebeat
```



## 1.4 安装Elasticsearch Heads

在chrome网上应用商店里，查找Elasticsearch Heads安装即可。



## 1.5 配置



### 1.5.1 Elasticsearch 

```shell
vim /etc/elasticsearch/elasticsearch.yml


network.host: 0.0.0.0
http.port: 9200
discovery.type: single-node
```



### 1.5.2 kibana

```shell
vim /etc/kibana/kibana.yml

server.port: 5601
server.host: "0.0.0.0"
elasticsearch.hosts: ["http://localhost:9200"]
i18n.locale: "zh-CN"
```



### 1.5.3 filebeat

```shell
vim /etc/filebeat/filebeat.yml

filebeat.inputs:

- type: log 
  enabled: true
  paths:
    - /var/log/nginx/*.log
 
 
# ======================= Elasticsearch template setting ======================= 
setup.ilm.enabled: false
setup.template.name: "nginx_log"
setup.template.pattern: "nginx_log-*"
setup.template.settings:
  index.number_of_shards: 1  
  
  
setup.kibana:
  host: "localhost:5601"  
  
# ---------------------------- Elasticsearch Output ----------------------------
output.elasticsearch:
  # Array of hosts to connect to.
  hosts: ["localhost:9200"]
  index: "nginx_log-%{+YYYY.MM.dd}" #索引名称  
```





# 第二章 常见操作

1. 列出全部索引

   ```shell
   GET /_cat/indices\?v
   
   # 例子
   192.168.0.79:9200/_cat/indices\?v
   ```

2. 列出索引的字段定义

   ```shell
   # 类似mysql表的定义
   GET /test_index/_mapping
   
   # 例子
   192.168.0.79:9200/tb_account_num/_mapping
   ```

3. 列出所有表和字段定义

   ```shell
   GET /_mapping
   ```

4. 查看_cat相关命令

   ```shell
   GET /_cat/
   
   # 例子
   curl -i -XGET http://192.168.11.119:9200/_cat/
   ```

5. 查看集群健康状况

   ```shell
   GET /_cat/health?v
   
   # 例子
   curl -XGET http://192.168.11.119:9200/_cat/health\?v
   ```

6. 创建索引

   ```shell
   PUT /test_index?pretty
   
   # 例子
   curl -i -XPUT http://192.168.11.119:9200/test_index\?pretty
   ```

7. 删除索引

   ```shell
   DELETE /test_index?pretty
   ```

8. 新建文档并建立索引

   ```shell
   PUT /index/type/id
   {
       "json数据"
   }
   
   # 例子
   curl --location --request PUT '192.168.0.79:9200/test_index/_doc/1' \
   --header 'Content-Type: application/json' \
   --data-raw '{
       "name": "小明",
       "email": "[email protected]",
       "tags": ["篮球","游泳"]
   }'
   ```

9. 根据id查询文档

   ```shell
   GET /索引/类型/字段值
   
   # 例子
   curl -i -XGET http://192.168.11.119:9200/test_index/user/1\?pretty
   ```

10. 修改文档

    + 全部修改=> PUT

      ```shell
      curl -i -XPUT http://192.168.11.119:9200/test_index/user/1 -d '{
          "name": "小明",
          "email": "[email protected]",
          "tags": ["篮球","游泳","足球"]
      }'
      ```

      

    + 部分修改=> POST

      ```shell
      # 1 => 调用_update方法
      # 2 => 修改的fields放在doc属性里面
      curl -i -XPOST http://192.168.11.119:9200/test_index/user/1/_update -d '{
              "doc":{
                  "email": "[email protected]"
              }
      }'
      ```

11. 删除文档

    ```shell
    DELETE /test_index/user/1
    
    # 例子
    curl -i -XDELETE http://192.168.11.119:9200/test_index/user/2
    ```

12. 查询

    + 查出type里面全部文档

      ```shell
      GET /test_index/user/_search
      
      # 例子
      curl -i -XGET http://192.168.11.119:9200/test_index/user/_search\?pretty
      ```

      

    + 查出符合指定条件的文档

      ```shell
      GET /test_index/user/_search\?pretty\&q=$field:'$value'
      
      curl -i -XGET http://192.168.11.119:9200/test_index/user/_search\?&q=name:'bruce'&sort=email:desc
      ```

      

13. 查询DSL

    + 查询所有文档

      ```shell
      # 语法 7.0以后没有type了
      curl -i -XGET url/${index}/_search\?pretty -d ${json} 
      
      curl -i -XGET http://192.168.11.119:9200/test_index/user/_search\?pretty -d '
      {
        "query": {
                      "match_all": {
                      }
      }
      }
      ```
      
    + 查询包含输入字符串的文档
    
      ```shell
      curl -i -XGET http://192.168.11.119:9200/test_index/user/_search\?pretty -d '
          {
            "query": {
                   "match": {
                      "name" : "br"
                    }
            },
            "sort": [
                     {
                       "email" : "desc"
                     }
        			]
          }
      ```
    
    + 增加分页操作 from 从0开始 只获取email字段
    
      ```javascript
        curl -i -XGET http://192.168.11.119:9200/test_index/user/_search?pretty -d '
        {
          "query": {
           		"match_all": {
           		} 
          },
          "from" : 1,
          "size" : 2,
          "_source" : ["email"],
          "sort": [
          		{
          			"email" : "asc"
          		}
          ]
        }
      ```
    
    + 查询过滤器
    
      ```javascript
      	// 搜索商品名包含Rhinestone，售卖价格小于3大于等于1的商品，结果按售卖价升序
          curl -i -XGET http://192.168.11.119:9200/en_es_category_products/product/_search?pretty -d '
          {
            "query": {
             		"bool": {
             			"must" : {
             				"match" : {
             					"product_name" : "Rhinestone"
             				}
             			},
             			"filter" : {
             				"range" : {
             					"store_price" : {
             					   "gte" :  1
             						"lt" : 3
             					}
             				}
             			}
             		}
            },
            "_source" : [
            		"product_id",
            		"product_name",
            		"store_price",
            		"icon"
            ],
              "sort": [
            		{
            			"store_price" : "asc"
            		}
            ]
          }
      ```
    
    + range操作符
    
      + gt :: 大于
      + gte:: 大于等于
      + lt :: 小于
      + lte:: 小于等于

​      

# 第三章 查看日志



## 3.1 选择索引

Kibana --> Analytics --> Discover--> 选择一个索引



## 3.2 查找

1. 可用字段选择message

2. 搜索框里填入

   ```shell
   # 查找全部包含127.0.0.1的日志
   message : "127.0.0.1"
   
   # 查找包含null 和 pointer 的日志,不比按照指定次序
   message: null pointer
   
   # 查找包含null 和 pointer 的日志,按照指定次序
   message: "null pointer"
   ```




# 第四章 实时日志

kibana可以模拟tail -f 查看实时日志。
