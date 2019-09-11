# 将源码文件生成VS项目

1. 利用vs的`从现有代码创建项目`的方式创建项目
2. 将`gen.py`、`gen_filters.py`、`gen_vcsproj.py`拷贝至源码路径，运行`python gen.py`即可
3. Python是3.x的版本，每次更新代码重新生成即可