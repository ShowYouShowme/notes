# 第一章 安装

```shell
#git地址
url=https://github.com/swagger-api/swagger-ui
#ui编辑器
url=https://editor.swagger.io/

#安装
docker pull swaggerapi/swagger-ui

#启动

#指定配置文件启动,json可以写入yaml格式的数据
docker run -p 80:8080 -e SWAGGER_JSON=/foo/swagger.json -v /bar:/foo swaggerapi/swagger-ui

#推荐的命令
mkdir -p /home/roglic/doc/swaggerConfig
touch /home/roglic/doc/swaggerConfig/swagger.json
#写入配置
...
#启动服务
docker run -p 80:8080 -e SWAGGER_JSON=/foo/swagger.json -v /home/roglic/doc/swaggerConfig:/foo swaggerapi/swagger-ui
```





# 第二章 配置文件

```yaml
# 参考地址:https://editor.swagger.io/
openapi: 3.0.3
info:
  title: Swagger Petstore - OpenAPI 3.0
  description: |-
    This is a sample Pet Store Server based on the OpenAPI 3.0 specification.  You can find out more about
    Swagger at [https://swagger.io](https://swagger.io). In the third iteration of the pet store, we've switched to the design first approach!
    You can now help us improve the API whether it's by making changes to the definition itself or to the code.
    That way, with time, we can improve the API in general, and expose some of the new features in OAS3.

    _If you're looking for the Swagger 2.0/OAS 2.0 version of Petstore, then click [here](https://editor.swagger.io/?url=https://petstore.swagger.io/v2/swagger.yaml). Alternatively, you can load via the `Edit > Load Petstore OAS 2.0` menu option!_
    
    Some useful links:
    - [The Pet Store repository](https://github.com/swagger-api/swagger-petstore)
    - [The source API definition for the Pet Store](https://github.com/swagger-api/swagger-petstore/blob/master/src/main/resources/openapi.yaml)
  termsOfService: http://swagger.io/terms/
  contact:
    email: apiteam@swagger.io
  license:
    name: Apache 2.0
    url: http://www.apache.org/licenses/LICENSE-2.0.html
  version: 1.0.11



externalDocs:
  description: Find out more about Swagger
  url: http://swagger.io
  
  

# 配置服务地址
servers:
  - url: http://192.168.2.110:9002


# 一个tag对应一个模块,每个模块有多个接口
tags:
  - name: pet
    description: Everything about your Pets
    externalDocs:
      description: Find out more
      url: http://swagger.io
  - name: store
    description: Access to Petstore orders
    externalDocs:
      description: Find out more about our store
      url: http://swagger.io
  - name: user
    description: Operations about user

# 配置路由
paths:
  /server/login/checklogintoken:
    post:
      tags:
        - pet
      summary: Add a new pet to the store
      description: Add a new pet to the store
      operationId: addPet
      requestBody:
        description: Create a new pet in the store
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/PetReq'
        required: true
      responses:
        '200':
          description: Successful operation
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/PetResp'          
        '405':
          description: Invalid input

# 定义数据类型
components:
  schemas:
    PetReq:
      type: object
      properties:
        token:
          type: string
    PetResp:
      type: object
      properties:
        code:
          type: integer
          format: int32
        msg:
          type: string  
        data:
          $ref: '#/components/schemas/Data'
    Data:
      type: object
      properties:
        uid:
          type: integer
          format: int32
        avatar:
          type: string
        nickname:
          type: string      
```

